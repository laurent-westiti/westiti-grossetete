"""
Paiement par Stripe.

Le client paie sur une page de Stripe, dans sa langue. C'est Stripe qui
collecte le courriel, le téléphone et l'adresse de livraison, et non notre
formulaire : Stripe valide les adresses mieux que nous, et aucune
coordonnée bancaire ne traverse jamais notre service.

Une commande ne devient « payée » qu'à la réception du webhook signé par
Stripe, et jamais au retour du navigateur. Un client qui ferme son onglet
juste après avoir payé doit recevoir sa grosse tête quand même, et une
adresse de retour forgée à la main ne doit rien déclencher du tout.

Même méthode que Westiti Memories, sur un compte Stripe distinct.
"""

import json

import stripe

import commandes
import reglages
import traductions as tr


class ErreurPaiement(RuntimeError):
    """Stripe a refusé la demande, ou n'est pas configuré."""


def _client():
    if not reglages.STRIPE_CLE_SECRETE:
        raise ErreurPaiement("le paiement n'est pas encore configuré")
    stripe.api_key = reglages.STRIPE_CLE_SECRETE
    return stripe


def _texte(cle, langue, **valeurs):
    return tr.T[cle][langue].format(**valeurs)


def parametres_session(commande, base_url):
    """Les réglages de la page de paiement, séparés de l'appel pour être testés."""
    langue = commande["langue"]
    hauteur = reglages.TAILLES[commande["taille"]]["hauteur"]
    quantite = commande["quantite"]
    nom = _texte("stripe.produit", langue, h=hauteur)
    if quantite > 1:
        nom += f" × {quantite}"
    description = _texte("stripe.description", langue, n=quantite)
    return dict(
        mode="payment",
        # Un seul article au prix du lot : les prix de 2 et 3 exemplaires ne
        # sont pas des multiples du prix unitaire.
        line_items=[{
            "quantity": 1,
            "price_data": {
                "currency": reglages.DEVISE,
                "unit_amount": commande["montant"],
                "product_data": {"name": nom, "description": description},
            },
        }],
        locale=langue,
        shipping_address_collection={"allowed_countries": reglages.PAYS_LIVRAISON},
        phone_number_collection={"enabled": True},
        allow_promotion_codes=True,
        # Une vraie facture, numérotée et envoyée par Stripe avec le reçu.
        invoice_creation={
            "enabled": True,
            "invoice_data": {
                "description": f"{nom} — {description}",
                "metadata": {"commande": commande["id"]},
                "footer": _texte("stripe.pied_facture", langue),
                **({"account_tax_ids": [reglages.STRIPE_TVA]} if reglages.STRIPE_TVA else {}),
                "rendering_options": {"amount_tax_display": "include_inclusive_tax"},
            },
        },
        # L'identifiant de commande voyage dans les métadonnées : c'est lui
        # que le webhook retrouvera.
        metadata={"commande": commande["id"]},
        client_reference_id=commande["id"],
        success_url=f"{base_url}{tr.url('merci', langue)}?commande={commande['id']}",
        cancel_url=f"{base_url}{tr.url('creer', langue)}?taille={commande['taille']}",
    )


def ouvrir_paiement(commande, base_url):
    """Crée la page de paiement Stripe et renvoie son adresse."""
    client = _client()
    try:
        session = client.checkout.Session.create(**parametres_session(commande, base_url))
    except stripe.error.StripeError as erreur:
        raise ErreurPaiement(str(erreur))
    commandes.modifier(commande["id"], stripe_session=session.id)
    return session.url


def lire_evenement(charge, signature):
    """Vérifie la signature du webhook et renvoie l'événement.

    Sans cette vérification, n'importe qui pourrait nous annoncer un paiement
    et repartir avec une grosse tête imprimée.
    """
    if not reglages.STRIPE_SECRET_WEBHOOK:
        raise ErreurPaiement("le secret du webhook n'est pas configuré")
    try:
        return stripe.Webhook.construct_event(charge, signature, reglages.STRIPE_SECRET_WEBHOOK)
    except (ValueError, stripe.error.SignatureVerificationError) as erreur:
        raise ErreurPaiement(f"webhook refusé : {erreur}")


def _en_dictionnaire(objet):
    """Un objet Stripe en dictionnaire ordinaire (leçon apprise sur Memories :
    les objets Stripe refusent `.get()` selon les versions)."""
    if isinstance(objet, dict):
        return objet
    try:
        return json.loads(str(objet))
    except (TypeError, ValueError):
        return dict(objet)


def _adresse_lisible(livraison):
    """L'adresse Stripe en une seule chaîne, telle qu'on l'écrit sur un colis."""
    if not livraison:
        return ""
    a = livraison.get("address") or {}
    lignes = [
        livraison.get("name") or "",
        a.get("line1") or "",
        a.get("line2") or "",
        " ".join(x for x in [a.get("postal_code"), a.get("city")] if x),
        a.get("country") or "",
    ]
    return "\n".join(l for l in lignes if l.strip())


def traiter(evenement):
    """Traite un événement Stripe. Renvoie l'identifiant de commande concerné, ou None."""
    genre = evenement["type"]
    if genre not in ("checkout.session.completed", "checkout.session.expired"):
        return None

    session = _en_dictionnaire(evenement["data"]["object"])
    identifiant = (session.get("metadata") or {}).get("commande") or session.get("client_reference_id")
    commande = commandes.lire(identifiant) if identifiant else None
    if not commande:
        return None

    # La page de paiement a expiré sans paiement : la photo s'en va.
    if genre == "checkout.session.expired":
        commandes.abandonner(identifiant)
        return identifiant

    # Stripe peut répéter un webhook : une commande déjà payée ne change plus.
    if commande["statut"] != "attente_paiement":
        return identifiant
    # Un moyen de paiement différé (rare en carte) n'est pas encore encaissé.
    if session.get("payment_status") not in ("paid", "no_payment_required"):
        return identifiant

    details = session.get("customer_details") or {}
    livraison = (session.get("collected_information") or {}).get("shipping_details") \
        or session.get("shipping_details") or {}
    commandes.modifier(
        identifiant,
        statut="payee",
        courriel=details.get("email") or "",
        telephone=details.get("phone") or "",
        nom=livraison.get("name") or details.get("name") or "",
        adresse=_adresse_lisible(livraison),
        montant=session.get("amount_total") or commande["montant"],
    )
    # À brancher : l'envoi de la commande à Fulfiller, dès que l'accès à son
    # API sera ouvert.
    return identifiant

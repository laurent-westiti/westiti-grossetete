"""
Tests du parcours de paiement, sans réseau.

Stripe est remplacé par une doublure qui enregistre ce que le site lui
demande, et les webhooks sont signés exactement comme Stripe les signe.

    cd service && python3 test_paiement.py
"""

import hashlib
import hmac
import io
import json
import os
import sys
import tempfile
import time
import types

DOSSIER = tempfile.mkdtemp(prefix="grossetete-test-")
os.environ.update({
    "STRIPE_SECRET_KEY": "sk_test_doublure",
    "STRIPE_WEBHOOK_SECRET": "whsec_doublure",
    "WG_DONNEES": DOSSIER,
})

from PIL import Image                                          # noqa: E402
import stripe                                                  # noqa: E402
from fastapi.testclient import TestClient                      # noqa: E402

import app                                                     # noqa: E402
import commandes                                               # noqa: E402
import reglages                                                # noqa: E402

DEMANDES = []
ECHEC_STRIPE = {"actif": False}


def faux_create(**parametres):
    if ECHEC_STRIPE["actif"]:
        raise stripe.error.APIConnectionError("réseau coupé")
    DEMANDES.append(parametres)
    n = len(DEMANDES)
    return types.SimpleNamespace(id=f"cs_test_{n}", url=f"https://checkout.stripe.com/c/pay/cs_test_{n}")


stripe.checkout.Session.create = faux_create

client = TestClient(app.application)
client.__enter__()          # déclenche le démarrage (création de la base)


def photo_jpeg():
    tampon = io.BytesIO()
    Image.new("RGB", (900, 900), "#cba").save(tampon, "JPEG")
    return tampon.getvalue()


def commander(langue="fr", taille="80", quantite=3, accord="oui"):
    return client.post("/commander", follow_redirects=False,
                       data={"taille": taille, "quantite": quantite, "accord": accord,
                             "langue": langue, "zoom": 1.4, "decalage_x": 0.1, "decalage_y": -0.05},
                       files={"photo": ("visage.jpg", photo_jpeg(), "image/jpeg")})


def webhook(genre, identifiant, secret="whsec_doublure", paye=True):
    session = {
        "id": "cs_test_x", "object": "checkout.session",
        "metadata": {"commande": identifiant}, "client_reference_id": identifiant,
        "payment_status": "paid" if paye else "unpaid", "amount_total": 9900,
        "customer_details": {"email": "camille@exemple.fr", "phone": "+33600000000", "name": "Camille Martin"},
        "collected_information": {"shipping_details": {"name": "Camille Martin", "address": {
            "line1": "12 rue des Coureurs", "line2": None, "postal_code": "75011",
            "city": "Paris", "country": "FR"}}},
    }
    charge = json.dumps({"id": "evt_test", "object": "event", "type": genre,
                         "data": {"object": session}})
    t = int(time.time())
    v1 = hmac.new(secret.encode(), f"{t}.{charge}".encode(), hashlib.sha256).hexdigest()
    return client.post("/stripe/webhook", content=charge,
                       headers={"stripe-signature": f"t={t},v1={v1}", "content-type": "application/json"})


def dernier_id():
    return commandes.lister()[0]["id"]


def photo_existe(identifiant):
    c = commandes.lire(identifiant)
    return bool(c["photo"]) and os.path.exists(os.path.join(reglages.DOSSIER_PHOTOS, c["photo"]))


RESULTATS = []


def verifier(nom, condition):
    RESULTATS.append((nom, bool(condition)))
    print(("  ok    " if condition else "  ÉCHEC ") + nom)


# 1. Commande en français : redirection vers Stripe, commande et photo enregistrées.
r = commander("fr", "80", 3)
ident = dernier_id()
p = DEMANDES[-1]
verifier("la commande renvoie vers la page Stripe", r.status_code == 303 and r.headers["location"].startswith("https://checkout.stripe.com/"))
verifier("la commande est en attente de paiement", commandes.lire(ident)["statut"] == "attente_paiement")
verifier("la photo est conservée pendant le paiement", photo_existe(ident))
verifier("le montant envoyé à Stripe est 99 € (80 cm × 3)", p["line_items"][0]["price_data"]["unit_amount"] == 9900)
verifier("un seul article, au prix du lot", p["line_items"][0]["quantity"] == 1)
verifier("le nom du produit est en français", p["line_items"][0]["price_data"]["product_data"]["name"] == "Grosse tête 80 cm × 3")
verifier("la page Stripe s'affiche en français", p["locale"] == "fr")
verifier("la livraison est limitée à la France", p["shipping_address_collection"]["allowed_countries"] == ["FR"])
verifier("une facture est émise", p["invoice_creation"]["enabled"] is True)
verifier("le retour après paiement mène à /merci", f"/merci?commande={ident}" in p["success_url"])
verifier("l'abandon ramène à l'atelier avec la taille", p["cancel_url"].endswith("/creer?taille=80"))
verifier("le cadrage est enregistré", json.loads(commandes.lire(ident)["cadrage"])["zoom"] == 1.4)

# 2. Anglais et espagnol.
commander("en", "30", 1)
p = DEMANDES[-1]
verifier("anglais : page Stripe en anglais", p["locale"] == "en")
verifier("anglais : produit « Big Head 30 cm » à 49 €", p["line_items"][0]["price_data"]["product_data"]["name"] == "Big Head 30 cm"
         and p["line_items"][0]["price_data"]["unit_amount"] == 4900)
verifier("anglais : retour vers /en/thank-you", "/en/thank-you?commande=" in p["success_url"])
commander("es", "100", 2)
p = DEMANDES[-1]
verifier("espagnol : page Stripe en espagnol", p["locale"] == "es")
verifier("espagnol : 159 € pour 100 cm × 2", p["line_items"][0]["price_data"]["unit_amount"] == 15900)
verifier("espagnol : retour vers /es/crear en cas d'abandon", p["cancel_url"].endswith("/es/crear?taille=100"))

# 3. Webhook signé : la commande passe payée, l'adresse est enregistrée.
r = webhook("checkout.session.completed", ident)
c = commandes.lire(ident)
verifier("le webhook signé est accepté", r.status_code == 200)
verifier("la commande passe à « payée »", c["statut"] == "payee")
verifier("l'adresse de livraison est enregistrée", "12 rue des Coureurs" in c["adresse"] and "75011 Paris" in c["adresse"])
verifier("le courriel et le téléphone sont enregistrés", c["courriel"] == "camille@exemple.fr" and c["telephone"])
verifier("la photo est gardée pour la fabrication", photo_existe(ident))

# 4. Webhook répété : rien ne change.
avant = commandes.lire(ident)
webhook("checkout.session.completed", ident)
verifier("un webhook répété ne change rien", commandes.lire(ident)["statut"] == "payee" and commandes.lire(ident)["adresse"] == avant["adresse"])

# 5. Webhook falsifié : refusé.
commander("fr", "45", 1)
ident_faux = dernier_id()
r = webhook("checkout.session.completed", ident_faux, secret="whsec_pirate")
verifier("un webhook à la signature fausse est refusé", r.status_code == 400)
verifier("la commande visée reste impayée", commandes.lire(ident_faux)["statut"] == "attente_paiement")

# 6. Paiement pas encore encaissé : la commande attend.
webhook("checkout.session.completed", ident_faux, paye=False)
verifier("un paiement non encaissé ne valide pas la commande", commandes.lire(ident_faux)["statut"] == "attente_paiement")

# 7. Page de paiement expirée : photo effacée.
webhook("checkout.session.expired", ident_faux)
verifier("une page expirée abandonne la commande", commandes.lire(ident_faux)["statut"] == "abandonnee")
verifier("et efface la photo", not photo_existe(ident_faux))

# 8. Stripe injoignable : message d'erreur, rien de conservé.
ECHEC_STRIPE["actif"] = True
r = commander("es", "60", 1)
ident_echec = dernier_id()
ECHEC_STRIPE["actif"] = False
verifier("Stripe injoignable : l'atelier réaffiche un message en espagnol", r.status_code == 200 and "La página de pago no ha podido abrirse" in r.text)
verifier("Stripe injoignable : la photo n'est pas gardée", not photo_existe(ident_echec))

# 9. Balayage des paniers oubliés.
commander("fr", "60", 1)
ident_vieux = dernier_id()
commandes.modifier(ident_vieux, cree_a=int(time.time()) - 30 * 3600)
n = commandes.balayer_abandons()
verifier("le balayage efface les photos impayées de plus de 24 h", n >= 1 and not photo_existe(ident_vieux))
verifier("le balayage ne touche pas aux commandes payées", photo_existe(ident))

# 10. Refus avant paiement.
r = commander("en", "60", 1, accord="")
verifier("sans accord coché, pas de paiement (message en anglais)", r.status_code == 200 and "consent" in r.text)

# 11. Sans clé Stripe, la page « bientôt » s'affiche et rien n'est gardé.
cle = reglages.STRIPE_CLE_SECRETE
reglages.STRIPE_CLE_SECRETE = ""
nb = len(commandes.lister())
r = commander("fr", "60", 1)
reglages.STRIPE_CLE_SECRETE = cle
verifier("sans clé Stripe, la page « bientôt » s'affiche", "le paiement pas encore" in r.text)
verifier("sans clé Stripe, aucune commande n'est créée", len(commandes.lister()) == nb)

client.__exit__(None, None, None)
echecs = [n for n, ok in RESULTATS if not ok]
print(f"\n{len(RESULTATS) - len(echecs)}/{len(RESULTATS)} vérifications réussies")
sys.exit(1 if echecs else 0)

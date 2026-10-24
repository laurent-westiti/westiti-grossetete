"""
Réglages de Westiti Grosse Tête.

Tout ce qui peut changer sans toucher au code vit ici : les tailles, les
prix, les délais annoncés, et les clés lues dans l'environnement.

Les prix et les délais ci-dessous sont PROVISOIRES. Ils seront fixés une fois
connus les tarifs revendeur de Fulfiller et ses délais de fabrication.
"""

import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTION = os.environ.get("WG_PRODUCTION") == "1"

# --------------------------------------------------------------------------
# L'offre
# --------------------------------------------------------------------------

# Hauteur du panneau en centimètres, prix TTC en euros pour le premier
# exemplaire. La clé sert d'identifiant dans les formulaires.
TAILLES = {
    "45": {"hauteur": 45, "prix": 29.0, "nom": "Visible", "pour": "Facile à tenir à bout de bras, même sur un long parcours."},
    "60": {"hauteur": 60, "prix": 39.0, "nom": "Repérable", "pour": "Le bon compromis : elle se voit de loin et se transporte sans peine."},
    "80": {"hauteur": 80, "prix": 55.0, "nom": "Impossible à rater", "pour": "Pour les arrivées, les ravitos et les virages où toute la foule se masse."},
}
TAILLE_CONSEILLEE = "60"

# Remise appliquée à chaque exemplaire du même visage au-delà du premier.
REMISE_SUPPLEMENTAIRE = 0.20
QUANTITE_MAX = 10

LIVRAISON_OFFERTE = True
DELAI_EXPEDITION = "sous 4 jours ouvrés"


def prix_commande(taille: str, quantite: int) -> float:
    """Prix total TTC d'une commande, arrondi au centime."""
    base = TAILLES[taille]["prix"]
    quantite = max(1, min(int(quantite), QUANTITE_MAX))
    total = base + (quantite - 1) * base * (1 - REMISE_SUPPLEMENTAIRE)
    return round(total, 2)


def prix_plancher() -> float:
    return min(t["prix"] for t in TAILLES.values())


# --------------------------------------------------------------------------
# Les clés (posées dans les variables de Railway, jamais dans le code)
# --------------------------------------------------------------------------

STRIPE_CLE_SECRETE = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_SECRET_WEBHOOK = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
FULFILLER_CLE = os.environ.get("FULFILLER_API_KEY", "")
FULFILLER_BAC_A_SABLE = os.environ.get("FULFILLER_SANDBOX", "1") == "1"
ADRESSE_PUBLIQUE = os.environ.get("WG_ADRESSE", "https://grossetete.westiti.app")

# Poids maximal d'une photo envoyée, en mégaoctets.
PHOTO_MAX_MO = 15


def paiement_ouvert() -> bool:
    return bool(STRIPE_CLE_SECRETE)


def fabrication_branchee() -> bool:
    return bool(FULFILLER_CLE)

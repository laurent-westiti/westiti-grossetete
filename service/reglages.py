"""
Réglages de Westiti Grosse Tête.

Tout ce qui peut changer sans toucher au code vit ici : les tailles, les
prix, les délais annoncés, et les clés lues dans l'environnement.

Les prix ci-dessous sont ceux fixés par Laurent. Le délai d'expédition reste
provisoire, en attendant celui de Fulfiller.
"""

import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTION = os.environ.get("WG_PRODUCTION") == "1"

# --------------------------------------------------------------------------
# L'offre
# --------------------------------------------------------------------------

# Hauteur du panneau en centimètres, et prix TTC en euros de la commande
# selon le nombre d'exemplaires du même visage (1, 2 ou 3). Les deuxième et
# troisième exemplaires coûtent très peu : c'est l'argument des commandes
# familiales. La clé sert d'identifiant dans les formulaires.
TAILLES = {
    "30":  {"hauteur": 30,  "nom": "Compacte",           "pour": "Légère et facile à glisser dans un sac, idéale pour les enfants.",
            "prix": {1: 39.90, 2: 44.90, 3: 46.90}},
    "45":  {"hauteur": 45,  "nom": "Visible",            "pour": "Facile à tenir à bout de bras, même sur un long parcours.",
            "prix": {1: 44.90, 2: 49.90, 3: 55.90}},
    "60":  {"hauteur": 60,  "nom": "Repérable",          "pour": "Le bon compromis : elle se voit de loin et se transporte sans peine.",
            "prix": {1: 59.90, 2: 66.90, 3: 74.90}},
    "80":  {"hauteur": 80,  "nom": "Impossible à rater", "pour": "Pour les arrivées, les ravitos et les virages où toute la foule se masse.",
            "prix": {1: 64.90, 2: 69.90, 3: 76.90}},
    "100": {"hauteur": 100, "nom": "Géante",             "pour": "Un mètre de haut : elle dépasse toutes les têtes de la foule.",
            "prix": {1: 120.00, 2: 130.00, 3: 144.90}},
}
TAILLE_CONSEILLEE = "60"
QUANTITES = (1, 2, 3)
QUANTITE_MAX = max(QUANTITES)

LIVRAISON_OFFERTE = True
DELAI_EXPEDITION = "sous 4 jours ouvrés"


def prix_commande(taille: str, quantite: int) -> float:
    """Prix total TTC d'une commande."""
    quantite = max(1, min(int(quantite), QUANTITE_MAX))
    return TAILLES[taille]["prix"][quantite]


def prix_par_tete(taille: str, quantite: int) -> float:
    return round(prix_commande(taille, quantite) / quantite, 2)


def prix_plancher() -> float:
    return min(t["prix"][1] for t in TAILLES.values())


def economie_max() -> int:
    """La plus forte baisse du prix par tête à trois exemplaires, en %."""
    return max(round(100 * (1 - t["prix"][3] / 3 / t["prix"][1])) for t in TAILLES.values())


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

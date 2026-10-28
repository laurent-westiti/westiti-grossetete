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
# troisième exemplaires coûtent bien moins cher que le premier : c'est
# l'argument des commandes familiales. La clé sert d'identifiant dans les
# formulaires. Les noms des tailles sont dans traductions.py.
TAILLES = {
    "30":  {"hauteur": 30,  "prix": {1: 49, 2: 54, 3: 59}},
    "45":  {"hauteur": 45,  "prix": {1: 52, 2: 59, 3: 64}},
    "60":  {"hauteur": 60,  "prix": {1: 59, 2: 69, 3: 79}},
    "80":  {"hauteur": 80,  "prix": {1: 64, 2: 84, 3: 99}},
    "100": {"hauteur": 100, "prix": {1: 124, 2: 159, 3: 199}},
}
TAILLE_CONSEILLEE = "60"
QUANTITES = (1, 2, 3)
QUANTITE_MAX = max(QUANTITES)

LIVRAISON_OFFERTE = True
# Jours ouvrés entre la commande et l'expédition (phrase dans traductions.py).
DELAI_JOURS = 4


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

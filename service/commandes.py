"""
Registre des commandes, et photos des visages.

Le registre est durable : il porte ce dont l'entreprise a besoin pour honorer
une vente et tenir sa comptabilité (la taille, le nombre d'exemplaires, le
montant, le courriel et l'adresse de livraison, le statut).

La photo, elle, ne l'est pas. Elle est gardée le temps de payer, puis de
fabriquer. Si le paiement n'aboutit pas, elle est effacée au bout de
quelques heures : nous ne conservons pas le visage de quelqu'un qui n'a rien
acheté. Une fois la commande expédiée, elle sera effacée aussi.
"""

import json
import os
import secrets
import sqlite3
import time
from contextlib import contextmanager

import reglages

# Les statuts, dans l'ordre où ils se succèdent.
STATUTS = {
    "attente_paiement": "En attente de paiement",
    "payee": "Payée",
    "chez_fabricant": "Envoyée au fabricant",
    "expediee": "Expédiée",
    "livree": "Livrée",
    "abandonnee": "Abandonnée (non payée)",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS commandes (
    id             TEXT PRIMARY KEY,
    cree_a         INTEGER NOT NULL,
    modifie_a      INTEGER NOT NULL,
    statut         TEXT    NOT NULL,
    langue         TEXT    NOT NULL DEFAULT 'fr',
    -- Le produit.
    taille         TEXT    NOT NULL,
    quantite       INTEGER NOT NULL,
    montant        INTEGER NOT NULL,          -- en centimes, TTC
    -- Le cadrage choisi dans l'aperçu : zoom et décalage du visage.
    cadrage        TEXT    NOT NULL DEFAULT '{}',
    photo          TEXT,                      -- nom du fichier, vide une fois effacée
    -- Ce que Stripe nous renvoie une fois le paiement confirmé.
    stripe_session TEXT,
    courriel       TEXT    NOT NULL DEFAULT '',
    nom            TEXT    NOT NULL DEFAULT '',
    telephone      TEXT    NOT NULL DEFAULT '',
    adresse        TEXT    NOT NULL DEFAULT '',
    -- Le suivi du colis, renseigné à l'expédition.
    suivi          TEXT    NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS commandes_statut ON commandes (statut, cree_a);
"""

EXTENSIONS = {
    "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp",
    "image/heic": "heic", "image/heif": "heif",
}


def chemin_base():
    return os.path.join(reglages.DONNEES, "commandes.sqlite")


@contextmanager
def base():
    connexion = sqlite3.connect(chemin_base(), timeout=10)
    connexion.row_factory = sqlite3.Row
    try:
        yield connexion
        connexion.commit()
    finally:
        connexion.close()


def initialiser():
    os.makedirs(reglages.DOSSIER_PHOTOS, exist_ok=True)
    with base() as b:
        b.executescript(SCHEMA)


def creer(langue, taille, quantite, montant_centimes, cadrage, photo_octets, type_photo):
    """Enregistre une commande en attente de paiement, avec sa photo."""
    identifiant = "gt_" + secrets.token_urlsafe(12)
    extension = EXTENSIONS.get(type_photo, "jpg")
    fichier = f"{identifiant}.{extension}"
    with open(os.path.join(reglages.DOSSIER_PHOTOS, fichier), "wb") as f:
        f.write(photo_octets)
    maintenant = int(time.time())
    with base() as b:
        b.execute(
            "INSERT INTO commandes (id, cree_a, modifie_a, statut, langue, taille, quantite,"
            " montant, cadrage, photo) VALUES (?, ?, ?, 'attente_paiement', ?, ?, ?, ?, ?, ?)",
            (identifiant, maintenant, maintenant, langue, taille, quantite,
             montant_centimes, json.dumps(cadrage), fichier),
        )
    return identifiant


def lire(identifiant):
    with base() as b:
        ligne = b.execute("SELECT * FROM commandes WHERE id = ?", (identifiant,)).fetchone()
    return dict(ligne) if ligne else None


def modifier(identifiant, **champs):
    if not champs:
        return
    champs["modifie_a"] = int(time.time())
    colonnes = ", ".join(f"{c} = ?" for c in champs)
    with base() as b:
        b.execute(f"UPDATE commandes SET {colonnes} WHERE id = ?", (*champs.values(), identifiant))


def lister(statut=None, limite=200):
    with base() as b:
        if statut:
            lignes = b.execute("SELECT * FROM commandes WHERE statut = ? ORDER BY cree_a DESC, rowid DESC LIMIT ?",
                               (statut, limite)).fetchall()
        else:
            lignes = b.execute("SELECT * FROM commandes ORDER BY cree_a DESC, rowid DESC LIMIT ?", (limite,)).fetchall()
    return [dict(l) for l in lignes]


def effacer_photo(identifiant):
    commande = lire(identifiant)
    if not commande or not commande["photo"]:
        return
    try:
        os.remove(os.path.join(reglages.DOSSIER_PHOTOS, commande["photo"]))
    except FileNotFoundError:
        pass
    modifier(identifiant, photo=None)


def abandonner(identifiant):
    """Une commande non payée : sa photo est effacée tout de suite."""
    commande = lire(identifiant)
    if commande and commande["statut"] == "attente_paiement":
        effacer_photo(identifiant)
        modifier(identifiant, statut="abandonnee")


def balayer_abandons():
    """Efface les photos des commandes restées impayées trop longtemps.

    Stripe annonce lui-même la plupart des abandons (au bout de 24 heures,
    une page de paiement expire). Ce balayage rattrape les cas où cette
    annonce ne nous serait jamais parvenue.
    """
    limite = int(time.time()) - reglages.ABANDON_HEURES * 3600
    with base() as b:
        ids = [l["id"] for l in b.execute(
            "SELECT id FROM commandes WHERE statut = 'attente_paiement' AND cree_a < ?", (limite,))]
    for identifiant in ids:
        abandonner(identifiant)
    return len(ids)

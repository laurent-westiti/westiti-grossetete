# Westiti Grosse Tête

Site de commande de « grosses têtes » : des panneaux rigides imprimés à
l'effigie d'un coureur, découpés au contour de son visage, que ses proches
brandissent au bord du parcours. Même ossature et même charte que Westiti
Memories.

| Dossier | Rôle |
|---|---|
| `service/` | Le site (FastAPI) : pages, formulaire, futur paiement et fabrication |
| `service/gabarits/` | Les pages : `accueil.html`, `creer.html`, `merci.html`, `bientot.html`, `legal.html` |
| `service/statique/` | La feuille de style commune et l'aperçu en direct (`creer.js`) |
| `site/img/` | Les images. Les emplacements « Photo à venir » attendent de vraies photos |

## Langues

Le site existe en français (`/`), en anglais (`/en`), en espagnol (`/es`) et
en italien (`/it`). Quatre drapeaux dans l'en-tête permettent de passer d'une
langue à l'autre sur n'importe quelle page. Les adresses des pages sont
traduites (`/creer`, `/en/create`, `/es/crear`, `/it/crea`…), et tous les
textes vivent dans `service/traductions.py`, une phrase par clé dans les
quatre langues. Le
service refuse de démarrer si une traduction manque.

## Où changer quoi

| Pour changer… | Fichier |
|---|---|
| Un texte, dans n'importe quelle langue | `service/traductions.py` |
| Les tailles, les prix, le délai | `service/reglages.py` |
| La mise en page de l'accueil | `service/gabarits/accueil.html` |
| Les couleurs | `service/statique/westiti.css`, en tête de fichier |

Grille tarifaire (TTC, prix du lot de 1 à 5 exemplaires du même visage) :

| Taille | 1 | 2 | 3 | 4 | 5 | Panneau en plus |
|---|---|---|---|---|---|---|
| 30 cm | 49 € | 54 € | 59 € | 64 € | 69 € | +5 € |
| 45 cm | 54 € | 64 € | 74 € | 84 € | 94 € | +10 € |
| 60 cm | 59 € | 72 € | 85 € | 98 € | 111 € | +13 € |
| 80 cm | 69 € | 91 € | 113 € | 135 € | 157 € | +22 € |
| 100 cm | 132 € | 172 € | 212 € | 252 € | 292 € | +40 € |

Le délai d'expédition affiché reste provisoire, en attendant celui de
Fulfiller.

## État

| Brique | État |
|---|---|
| Page d'accueil, atelier de création, aperçu en direct | Fait |
| Paiement Stripe | Fait, sur un compte Stripe dédié (clés à poser dans Railway) |
| Détourage automatique du visage | À brancher |
| Envoi à Fulfiller et suivi par webhook | À brancher (accès API demandé) |
| Textes légaux | Trame à faire valider |

## Paiement

Le client paie sur une page de Stripe, dans sa langue. Stripe collecte le
courriel, le téléphone et l'adresse de livraison (France uniquement), et
envoie la facture. Une commande ne devient « payée » qu'à la réception du
webhook signé par Stripe (`/stripe/webhook`, événements
`checkout.session.completed` et `checkout.session.expired`).

La commande et la photo sont enregistrées dans `/data` (volume Railway). Une
photo dont la commande n'est pas payée est effacée à l'expiration de la page
de paiement, et au plus tard au bout de 24 heures.

Sans clé Stripe, une commande aboutit à une page « paiement bientôt ouvert »
et rien n'est conservé.

Tests du parcours de paiement, sans réseau :

```bash
cd service && python3 test_paiement.py
```

## Démarrage en développement

```bash
pip install -r service/requirements.txt
cd service && uvicorn app:application --reload
```

## Couleurs

| Usage | Code |
|---|---|
| Action (corail Westiti assombri, texte blanc lisible) | `#D9533F` |
| Corail de marque (décors) | `#ED766A` |
| Vert Westiti | `#2A736E` |
| Crème | `#FBF8F3` |
| Encre | `#0C1A18` |

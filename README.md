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

Le site existe en français (`/`), en anglais (`/en`) et en espagnol (`/es`).
Trois drapeaux dans l'en-tête permettent de passer d'une langue à l'autre
sur n'importe quelle page. Les adresses des pages sont traduites
(`/creer`, `/en/create`, `/es/crear`…), et tous les textes vivent dans
`service/traductions.py`, une phrase par clé dans les trois langues. Le
service refuse de démarrer si une traduction manque.

## Où changer quoi

| Pour changer… | Fichier |
|---|---|
| Un texte, dans n'importe quelle langue | `service/traductions.py` |
| Les tailles, les prix, le délai | `service/reglages.py` |
| La mise en page de l'accueil | `service/gabarits/accueil.html` |
| Les couleurs | `service/statique/westiti.css`, en tête de fichier |

Grille tarifaire (TTC, pour 1, 2 ou 3 exemplaires du même visage) :

| Hauteur | 1 tête | 2 têtes | 3 têtes |
|---|---|---|---|
| 30 cm | 49 € | 54 € | 59 € |
| 45 cm | 52 € | 59 € | 64 € |
| 60 cm | 59 € | 69 € | 79 € |
| 80 cm | 64 € | 84 € | 99 € |
| 100 cm | 124 € | 159 € | 199 € |

Le délai d'expédition affiché reste provisoire, en attendant celui de
Fulfiller.

## État

| Brique | État |
|---|---|
| Page d'accueil, atelier de création, aperçu en direct | Fait |
| Paiement Stripe | À brancher (clés à poser dans Railway) |
| Détourage automatique du visage | À brancher |
| Envoi à Fulfiller et suivi par webhook | À brancher (accès API demandé) |
| Textes légaux | Trame à faire valider |

Sans clé Stripe, une commande aboutit à une page « paiement bientôt ouvert »
et la photo n'est pas conservée.

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

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

## Où changer quoi

| Pour changer… | Fichier |
|---|---|
| Les tailles, les prix, la remise, le délai | `service/reglages.py` |
| Les textes de la page d'accueil | `service/gabarits/accueil.html` |
| Les couleurs | `service/statique/westiti.css`, en tête de fichier |

Les prix et délais actuels sont **provisoires**, en attendant les tarifs
revendeur de Fulfiller.

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

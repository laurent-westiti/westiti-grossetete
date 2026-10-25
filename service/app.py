"""
Service web de Westiti Grosse Tête.

Le parcours tient en quatre temps : le proche envoie une photo et choisit sa
taille, il voit l'aperçu, il paie sur Stripe, puis la grosse tête est
fabriquée et expédiée par Fulfiller.

État actuel : les pages et le formulaire sont en place. Le paiement Stripe,
le détourage automatique et l'envoi à Fulfiller se brancheront ici dès que
les clés seront disponibles ; d'ici là, une commande aboutit à une page qui
annonce l'ouverture prochaine, et la photo n'est pas conservée.

Démarrage en développement :

    cd service && uvicorn app:application --reload
"""

import json
import os

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import reglages

HERE = os.path.dirname(os.path.abspath(__file__))
GABARITS = Jinja2Templates(directory=os.path.join(HERE, "gabarits"))

application = FastAPI(title="Westiti Grosse Tête", docs_url=None, redoc_url=None)
application.mount("/statique", StaticFiles(directory=os.path.join(HERE, "statique")), name="statique")
application.mount("/img", StaticFiles(directory=os.path.join(reglages.RACINE, "site", "img")), name="img")

FORMATS_ACCEPTES = {"image/jpeg", "image/png", "image/heic", "image/heif", "image/webp"}


def _euros(montant: float) -> str:
    if abs(montant - round(montant)) < 0.005:
        return f"{montant:.0f} €"
    return f"{montant:.2f} €".replace(".", ",")


def _commun() -> dict:
    """Ce que toutes les pages savent de l'offre."""
    return {
        "tailles": reglages.TAILLES,
        "conseillee": reglages.TAILLE_CONSEILLEE,
        "plancher": reglages.prix_plancher(),
        "quantites": reglages.QUANTITES,
        "economie": reglages.economie_max(),
        "livraison_offerte": reglages.LIVRAISON_OFFERTE,
        "delai": reglages.DELAI_EXPEDITION,
    }


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

@application.get("/", response_class=HTMLResponse)
def accueil(request: Request):
    return GABARITS.TemplateResponse(request, "accueil.html", _commun())


@application.get("/creer", response_class=HTMLResponse)
def creer(request: Request, taille: str = "", erreur: str = ""):
    contexte = _commun()
    contexte.update({
        "choix_taille": taille if taille in reglages.TAILLES else reglages.TAILLE_CONSEILLEE,
        "tailles_json": json.dumps(reglages.TAILLES, ensure_ascii=False),
        "choix_quantite": 1,
        "photo_max": reglages.PHOTO_MAX_MO,
        "erreur": erreur,
    })
    return GABARITS.TemplateResponse(request, "creer.html", contexte)


@application.post("/commander", response_class=HTMLResponse)
async def commander(
    request: Request,
    photo: UploadFile = File(...),
    taille: str = Form(...),
    quantite: int = Form(1),
    accord: str = Form(""),
    zoom: float = Form(1.0),
    decalage_x: float = Form(0.0),
    decalage_y: float = Form(0.0),
):
    def refuser(message: str):
        return creer(request, taille=taille, erreur=message)

    if taille not in reglages.TAILLES:
        return refuser("Choisis une taille avant de commander.")
    if accord != "oui":
        return refuser("Confirme que tu as l'accord de la personne représentée.")
    if photo.content_type not in FORMATS_ACCEPTES:
        return refuser("Ce format de photo n'est pas accepté. Envoie un fichier JPEG ou PNG.")
    contenu = await photo.read()
    if len(contenu) > reglages.PHOTO_MAX_MO * 1024 * 1024:
        return refuser(f"La photo dépasse {reglages.PHOTO_MAX_MO} Mo.")

    if quantite not in reglages.QUANTITES:
        return refuser("Choisis 1, 2 ou 3 exemplaires.")
    total = reglages.prix_commande(taille, quantite)

    if not reglages.paiement_ouvert():
        # Rien n'est conservé tant que le paiement n'est pas branché.
        return GABARITS.TemplateResponse(request, "bientot.html", {
            "taille": reglages.TAILLES[taille]["hauteur"],
            "quantite": quantite,
            "total": _euros(total),
        })

    # À brancher : enregistrement de la commande, détourage, session Stripe
    # Checkout (adresse de livraison collectée par Stripe), puis redirection.
    return RedirectResponse("/creer?erreur=Le+paiement+arrive+bient%C3%B4t.", status_code=303)


@application.get("/sante")
def sante():
    return {
        "ok": True,
        "paiement": reglages.paiement_ouvert(),
        "fabrication": reglages.fabrication_branchee(),
    }


@application.get("/merci", response_class=HTMLResponse)
def merci(request: Request):
    return GABARITS.TemplateResponse(request, "merci.html", {})


# --------------------------------------------------------------------------
# Textes légaux (trame, à faire valider)
# --------------------------------------------------------------------------

LEGAL = {
    "cgv": ("Conditions générales de vente", [
        ("Objet", "Les présentes conditions encadrent la vente de panneaux imprimés personnalisés à l'effigie d'une personne, dits « grosses têtes », sur le site grossetete.westiti.app."),
        ("Commande", "La commande est ferme une fois le paiement confirmé par Stripe. Le client valide l'aperçu avant de payer."),
        ("Produit personnalisé", "Le produit étant confectionné selon les spécifications du client et nettement personnalisé, le droit de rétractation ne s'applique pas, conformément à l'article L221-28 3° du Code de la consommation."),
        ("Droit à l'image", "Le client garantit disposer de l'accord de la personne représentée sur la photo transmise."),
        ("Livraison", "Les délais et zones de livraison sont précisés sur le site au moment de la commande."),
    ]),
    "mentions-legales": ("Mentions légales", [
        ("Éditeur", "Westiti — raison sociale, siège, SIRET et directeur de la publication à compléter."),
        ("Hébergement", "Railway Corporation — adresse à compléter."),
    ]),
    "confidentialite": ("Politique de confidentialité", [
        ("Données collectées", "La photo transmise, l'adresse de courriel et l'adresse de livraison, uniquement pour fabriquer et livrer la commande."),
        ("Conservation", "La photo est effacée une fois la commande expédiée. Les données de facturation sont conservées pendant la durée légale."),
        ("Sous-traitants", "Stripe pour le paiement, Fulfiller pour la fabrication et l'expédition."),
    ]),
}


@application.get("/{page}", response_class=HTMLResponse)
def legal(request: Request, page: str):
    if page not in LEGAL:
        return HTMLResponse("Page introuvable", status_code=404)
    titre, sections = LEGAL[page]
    return GABARITS.TemplateResponse(request, "legal.html", {"titre_page": titre, "sections": sections})

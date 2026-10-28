"""
Service web de Westiti Grosse Tête.

Le parcours tient en quatre temps : le proche envoie une photo et choisit sa
taille, il voit l'aperçu, il paie sur Stripe, puis la grosse tête est
fabriquée et expédiée par Fulfiller.

Le site existe en trois langues. Le français vit à la racine (/, /creer…),
l'anglais sous /en (/en, /en/create…) et l'espagnol sous /es (/es,
/es/crear…). Les textes sont tous dans `traductions.py`.

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
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markupsafe import Markup

import reglages
import traductions as tr

HERE = os.path.dirname(os.path.abspath(__file__))
GABARITS = Jinja2Templates(directory=os.path.join(HERE, "gabarits"))

application = FastAPI(title="Westiti Grosse Tête", docs_url=None, redoc_url=None)
application.mount("/statique", StaticFiles(directory=os.path.join(HERE, "statique")), name="statique")
application.mount("/img", StaticFiles(directory=os.path.join(reglages.RACINE, "site", "img")), name="img")

FORMATS_ACCEPTES = {"image/jpeg", "image/png", "image/heic", "image/heif", "image/webp"}

tr.verifier()


# --------------------------------------------------------------------------
# Ce que toutes les pages reçoivent
# --------------------------------------------------------------------------

def _traducteur(langue: str):
    """Renvoie la fonction t("clé", ...) de la langue demandée."""
    defauts = {
        "delai": tr.T["delai"][langue].format(j=reglages.DELAI_JOURS),
        "economie": reglages.economie_max(),
    }

    def t(cle: str, **valeurs) -> Markup:
        texte = tr.T[cle].get(langue) or tr.T[cle][tr.LANGUE_DEFAUT]
        return Markup(texte.format(**{**defauts, **valeurs}))

    return t


def contexte(request: Request, langue: str, page: str, **plus) -> dict:
    t = _traducteur(langue)
    return {
        "request": request,
        "lang": langue,
        "page": page,
        "t": t,
        "prix": lambda montant: tr.prix(montant, langue),
        "url": lambda autre: tr.url(autre, langue),
        "urls_langues": {l: tr.url(page, l) for l in tr.LANGUES},
        "langues": tr.LANGUES,
        "noms_langues": tr.NOMS_LANGUES,
        "adresse": reglages.ADRESSE_PUBLIQUE,
        "tailles": reglages.TAILLES,
        "conseillee": reglages.TAILLE_CONSEILLEE,
        "plancher": reglages.prix_plancher(),
        "quantites": reglages.QUANTITES,
        "economie": reglages.economie_max(),
        "livraison_offerte": reglages.LIVRAISON_OFFERTE,
        "expediee": t("commun.expediee"),
        **plus,
    }


def _rendre(request: Request, langue: str, page: str, **plus):
    if page == "accueil":
        return GABARITS.TemplateResponse(request, "accueil.html", contexte(request, langue, page))
    if page == "creer":
        return _page_creer(request, langue, **plus)
    if page == "merci":
        return GABARITS.TemplateResponse(request, "merci.html", contexte(request, langue, page))
    if page in tr.LEGAL:
        titre, sections = tr.LEGAL[page][langue]
        return GABARITS.TemplateResponse(request, "legal.html", contexte(
            request, langue, page, titre_page=titre, sections=sections))
    return HTMLResponse("Page introuvable", status_code=404)


def _page_creer(request: Request, langue: str, taille: str = "", erreur: str = ""):
    # Les textes du script gardent leurs {accolades} : c'est lui qui les remplit.
    textes_js = {cle[3:]: (v.get(langue) or v[tr.LANGUE_DEFAUT]) for cle, v in tr.T.items() if cle.startswith("js.")}
    textes_js["gain2"] = tr.T["creer.gain2"][langue]
    textes_js["gain3"] = tr.T["creer.gain3"][langue]
    return GABARITS.TemplateResponse(request, "creer.html", contexte(
        request, langue, "creer",
        choix_taille=taille if taille in reglages.TAILLES else reglages.TAILLE_CONSEILLEE,
        choix_quantite=1,
        tailles_json=json.dumps(reglages.TAILLES),
        textes_json=json.dumps(textes_js, ensure_ascii=False),
        photo_max=reglages.PHOTO_MAX_MO,
        erreur=erreur,
    ))


# --------------------------------------------------------------------------
# Routes techniques (avant les routes de pages, qui attrapent tout)
# --------------------------------------------------------------------------

@application.get("/sante")
def sante():
    return {
        "ok": True,
        "paiement": reglages.paiement_ouvert(),
        "fabrication": reglages.fabrication_branchee(),
    }


@application.post("/commander", response_class=HTMLResponse)
async def commander(
    request: Request,
    photo: UploadFile = File(...),
    taille: str = Form(...),
    quantite: int = Form(1),
    accord: str = Form(""),
    langue: str = Form("fr"),
    zoom: float = Form(1.0),
    decalage_x: float = Form(0.0),
    decalage_y: float = Form(0.0),
):
    if langue not in tr.LANGUES:
        langue = tr.LANGUE_DEFAUT
    t = _traducteur(langue)

    def refuser(cle: str, **valeurs):
        return _page_creer(request, langue, taille=taille, erreur=t(cle, **valeurs))

    if taille not in reglages.TAILLES:
        return refuser("err.taille")
    if accord != "oui":
        return refuser("err.accord")
    if photo.content_type not in FORMATS_ACCEPTES:
        return refuser("err.format")
    contenu = await photo.read()
    if len(contenu) > reglages.PHOTO_MAX_MO * 1024 * 1024:
        return refuser("err.poids", mo=reglages.PHOTO_MAX_MO)
    if quantite not in reglages.QUANTITES:
        return refuser("err.quantite")
    total = reglages.prix_commande(taille, quantite)

    if not reglages.paiement_ouvert():
        # Rien n'est conservé tant que le paiement n'est pas branché.
        return GABARITS.TemplateResponse(request, "bientot.html", contexte(
            request, langue, "creer",
            taille=reglages.TAILLES[taille]["hauteur"],
            quantite=quantite,
            total=tr.prix(total, langue),
        ))

    # À brancher : enregistrement de la commande, détourage, session Stripe
    # Checkout (adresse de livraison collectée par Stripe, langue `langue`),
    # puis redirection.
    return refuser("err.paiement")


# --------------------------------------------------------------------------
# Pages, dans les trois langues
# --------------------------------------------------------------------------

@application.get("/", response_class=HTMLResponse)
def accueil(request: Request):
    return _rendre(request, "fr", "accueil")


@application.get("/{langue}", response_class=HTMLResponse)
def page_simple(request: Request, langue: str, taille: str = ""):
    # « /en » et « /es » sont les accueils ; « /creer », « /cgv »… sont des
    # pages françaises.
    if langue in tr.LANGUES and langue != tr.LANGUE_DEFAUT:
        return _rendre(request, langue, "accueil")
    page = tr.page_depuis_slug(langue, "fr")
    if not page:
        return HTMLResponse("Page introuvable", status_code=404)
    return _rendre(request, "fr", page, taille=taille) if page == "creer" else _rendre(request, "fr", page)


@application.get("/{langue}/{slug}", response_class=HTMLResponse)
def page_traduite(request: Request, langue: str, slug: str, taille: str = ""):
    if langue not in tr.LANGUES or langue == tr.LANGUE_DEFAUT:
        return HTMLResponse("Page introuvable", status_code=404)
    page = tr.page_depuis_slug(slug, langue)
    if not page or page == "accueil":
        return HTMLResponse("Page introuvable", status_code=404)
    return _rendre(request, langue, page, taille=taille) if page == "creer" else _rendre(request, langue, page)

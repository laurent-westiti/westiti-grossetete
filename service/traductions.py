"""
Les textes du site, en français, en anglais, en espagnol et en italien.

Chaque clé donne la même phrase dans les quatre langues. Les pages ne
contiennent aucun texte en dur : elles appellent `t("clé")`. Pour corriger
une phrase, il suffit donc de la changer ici, dans la bonne langue.

Les accolades {comme_ceci} sont remplacées au moment de l'affichage par un
prix, un délai ou une taille. Le HTML léger (<i>, <br>, <sup>) est permis.

Le français tutoie, l'espagnol aussi (tú) comme l'italien (tu), l'anglais dit « you ».
"""

LANGUES = ("fr", "en", "es", "it")
LANGUE_DEFAUT = "fr"

NOMS_LANGUES = {"fr": "Français", "en": "English", "es": "Español", "it": "Italiano"}

# Les adresses des pages dans chaque langue. Le français n'a pas de préfixe,
# l'anglais vit sous /en, l'espagnol sous /es et l'italien sous /it.
PAGES = {
    "accueil":          {"fr": "",                 "en": "",             "es": "",            "it": ""},
    "creer":            {"fr": "creer",            "en": "create",       "es": "crear",       "it": "crea"},
    "merci":            {"fr": "merci",            "en": "thank-you",    "es": "gracias",     "it": "grazie"},
    "cgv":              {"fr": "cgv",              "en": "terms",        "es": "condiciones", "it": "condizioni"},
    "mentions-legales": {"fr": "mentions-legales", "en": "legal-notice", "es": "aviso-legal", "it": "note-legali"},
    "confidentialite":  {"fr": "confidentialite",  "en": "privacy",      "es": "privacidad",  "it": "privacy"},
}


def url(page: str, langue: str) -> str:
    slug = PAGES[page][langue]
    prefixe = "" if langue == LANGUE_DEFAUT else f"/{langue}"
    if not slug:
        return prefixe or "/"
    return f"{prefixe}/{slug}"


def page_depuis_slug(slug: str, langue: str):
    for page, slugs in PAGES.items():
        if slugs[langue] == slug:
            return page
    return None


def prix(montant: float, langue: str) -> str:
    """49 € et 19,67 € en français, en espagnol et en italien, €49 et €19.67 en anglais."""
    m = round(float(montant), 2)
    entier = abs(m - round(m)) < 0.005
    if langue == "en":
        return f"€{m:.0f}" if entier else f"€{m:.2f}"
    return (f"{m:.0f}" if entier else f"{m:.2f}".replace(".", ",")) + " €"


T = {
    # ------------------------------------------------------------ général
    "meta.titre": {
        "fr": "Westiti Grosse Tête — sa tête en géant, pour l'encourager",
        "en": "Westiti Big Head — their face, giant-sized, to cheer them on",
        "es": "Westiti Cabeza Gigante — su cara en grande, para animarle",
        "it": "Westiti Testa Gigante — il suo volto in grande, per fare il tifo",
    },
    "meta.description": {
        "fr": "Sa tête en géant, découpée à la forme de son visage, pour l'encourager au bord du parcours. Une photo suffit, nous imprimons et livrons.",
        "en": "Their face, giant-sized and cut to shape, to cheer them on along the course. One photo is all it takes: we print it and ship it.",
        "es": "Su cara en grande, recortada con la forma de su rostro, para animarle a lo largo del recorrido. Basta una foto: la imprimimos y te la enviamos.",
        "it": "Il suo volto in grande, ritagliato sulla forma del viso, per fare il tifo lungo il percorso. Basta una foto: la stampiamo e te la spediamo.",
    },
    "meta.og": {
        "fr": "Une photo suffit. Nous détourons son visage, l'imprimons en grand sur un panneau rigide découpé à la forme, et te l'envoyons avant la course.",
        "en": "One photo is all it takes. We cut out their face, print it large on a rigid board cut to shape, and ship it to you before the race.",
        "es": "Basta una foto. Recortamos su cara, la imprimimos en grande sobre un panel rígido recortado a medida y te la enviamos antes de la carrera.",
        "it": "Basta una foto. Scontorniamo il suo viso, lo stampiamo in grande su un pannello rigido sagomato e te lo spediamo prima della gara.",
    },
    "nav.grosse_tete": {"fr": "La grosse tête", "en": "The Big Head", "es": "La cabeza gigante", "it": "La testa gigante"},
    "nav.tailles": {"fr": "Les tailles", "en": "Sizes", "es": "Tamaños", "it": "Le misure"},
    "nav.comment": {"fr": "Comment ça marche", "en": "How it works", "es": "Cómo funciona", "it": "Come funziona"},
    "nav.questions": {"fr": "Questions", "en": "FAQ", "es": "Preguntas", "it": "Domande"},
    "nav.cta": {"fr": "Créer une grosse tête", "en": "Create a Big Head", "es": "Crear una cabeza gigante", "it": "Crea una testa gigante"},
    "nav.cta_court": {"fr": "Créer", "en": "Create", "es": "Crear", "it": "Crea"},
    "nav.retour": {"fr": "Retour à l'accueil", "en": "Back to home", "es": "Volver al inicio", "it": "Torna alla home"},
    "nav.langue": {"fr": "Choisir la langue", "en": "Choose language", "es": "Elegir idioma", "it": "Scegli la lingua"},
    "nav.accueil_aria": {"fr": "Westiti Grosse Tête, accueil", "en": "Westiti Big Head, home", "es": "Westiti Cabeza Gigante, inicio", "it": "Westiti Testa Gigante, home"},
    "pied.creation": {
        "fr": "Westiti Grosse Tête — une création {lien}",
        "en": "Westiti Big Head — made by {lien}",
        "es": "Westiti Cabeza Gigante — una creación de {lien}",
        "it": "Westiti Testa Gigante — una creazione {lien}",
    },
    "pied.cgv": {"fr": "Conditions de vente", "en": "Terms of sale", "es": "Condiciones de venta", "it": "Condizioni di vendita"},
    "pied.mentions": {"fr": "Mentions légales", "en": "Legal notice", "es": "Aviso legal", "it": "Note legali"},
    "pied.confidentialite": {"fr": "Confidentialité", "en": "Privacy", "es": "Privacidad", "it": "Privacy"},
    "pied.contact": {"fr": "Contact", "en": "Contact", "es": "Contacto", "it": "Contatti"},

    "delai": {"fr": "sous {j} jours ouvrés", "en": "within {j} working days", "es": "en {j} días hábiles", "it": "entro {j} giorni lavorativi"},
    "commun.expediee": {"fr": "Expédiée {delai}", "en": "Ships {delai}", "es": "Se envía {delai}", "it": "Spedita {delai}"},
    "commun.livraison_offerte": {"fr": "Livraison offerte", "en": "Free delivery", "es": "Envío gratis", "it": "Spedizione gratuita"},
    "commun.photo_a_venir": {"fr": "Photo à venir", "en": "Photo coming soon", "es": "Foto próximamente", "it": "Foto in arrivo"},
    "commun.ou": {"fr": "ou", "en": "or", "es": "o", "it": "oppure"},

    # -------------------------------------------------------------- héros
    "heros.promesse": {
        "fr": "Marathon, semi, trail, ultra, triathlon",
        "en": "Marathon, half, trail, ultra, triathlon",
        "es": "Maratón, media, trail, ultra, triatlón",
        "it": "Maratona, mezza, trail, ultra, triathlon",
    },
    "heros.titre": {
        "fr": "Sa tête en géant,<br>pour l'encourager",
        "en": "Their face, giant-sized,<br>to cheer them on",
        "es": "Su cara en gigante,<br>para animarle",
        "it": "Il suo volto in grande,<br>per fare il tifo",
    },
    "heros.emotion": {
        "fr": "Voir son propre visage au milieu de la foule lui apportera <i>réconfort</i> et <i>émotion</i>.",
        "en": "Seeing their own face in the middle of the crowd will bring them <i>comfort</i> and <i>emotion</i>.",
        "es": "Ver su propia cara en medio del público le dará <i>ánimo</i> y <i>emoción</i>.",
        "it": "Vedere il proprio viso in mezzo alla folla gli darà <i>conforto</i> ed <i>emozione</i>.",
    },
    "heros.texte": {
        "fr": "Tu nous envoies une photo, nous détourons son visage et l'imprimons en grand sur un panneau rigide découpé à sa forme. Tu le reçois chez toi avant la course, prêt à être brandi là où le besoin sera le plus fort.",
        "en": "You send us a photo, we cut out their face and print it large on a rigid board cut to its shape. It arrives at your door before the race, ready to be held up wherever they will need it most.",
        "es": "Nos envías una foto, recortamos su cara y la imprimimos en grande sobre un panel rígido recortado a su forma. La recibes en casa antes de la carrera, lista para levantarla allí donde más falta haga.",
        "it": "Ci mandi una foto, noi scontorniamo il suo viso e lo stampiamo in grande su un pannello rigido ritagliato sulla sua forma. Lo ricevi a casa prima della gara, pronto da sollevare nel punto in cui ce ne sarà più bisogno.",
    },
    "heros.voir_tailles": {"fr": "Voir les tailles", "en": "See the sizes", "es": "Ver los tamaños", "it": "Vedi le misure"},
    "heros.des": {"fr": "Dès {prix}", "en": "From {prix}", "es": "Desde {prix}", "it": "Da {prix}"},
    "heros.alt": {
        "fr": "Au bord d'un semi-marathon, des supporters brandissent deux grosses têtes souriantes au passage des coureurs",
        "en": "Along a half marathon, fans hold up two smiling Big Heads as the runners go by",
        "es": "Junto al recorrido de una media maratón, unos aficionados levantan dos cabezas gigantes sonrientes al paso de los corredores",
        "it": "Al bordo di una mezza maratona, alcuni tifosi sollevano due teste giganti sorridenti al passaggio dei corridori",
    },

    # ---------------------------------------------------------- confiance
    "confiance.photo_b": {"fr": "1 photo", "en": "1 photo", "es": "1 foto", "it": "1 foto"},
    "confiance.photo": {"fr": "suffit, prise avec un simple téléphone", "en": "is enough, taken with any phone", "es": "basta, hecha con cualquier móvil", "it": "basta, scattata con un semplice telefono"},
    "confiance.haut_b": {"fr": "{min} à {max} cm", "en": "{min} to {max} cm", "es": "{min} a {max} cm", "it": "Da {min} a {max} cm"},
    "confiance.haut": {"fr": "de haut, pour se voir de loin", "en": "tall, to be seen from afar", "es": "de alto, para verse de lejos", "it": "di altezza, per farsi vedere da lontano"},
    "confiance.pvc_b": {"fr": "3 mm", "en": "3 mm", "es": "3 mm", "it": "3 mm"},
    "confiance.pvc": {"fr": "de PVC rigide, qui ne craint pas la pluie", "en": "of rigid PVC that doesn't mind the rain", "es": "de PVC rígido, resistente a la lluvia", "it": "di PVC rigido, che non teme la pioggia"},
    "confiance.decoupe_b": {"fr": "100 %", "en": "100%", "es": "100 %", "it": "100 %"},
    "confiance.decoupe": {"fr": "découpée au contour de son visage", "en": "cut around the outline of their face", "es": "recortada al contorno de su cara", "it": "ritagliata sul contorno del viso"},

    # ----------------------------------------------------------- problème
    "probleme.titre": {
        "fr": "Au bord d'une course,<br>tout le monde crie.",
        "en": "Along a race course,<br>everyone is shouting.",
        "es": "Al borde de una carrera,<br>todo el mundo grita.",
        "it": "Al bordo di una gara,<br>gridano tutti.",
    },
    "probleme.emotion": {
        "fr": "Une pancarte de plus se perd dans la foule.<br><i>Un visage géant, jamais.</i>",
        "en": "One more sign gets lost in the crowd.<br><i>A giant face never does.</i>",
        "es": "Un cartel más se pierde entre el público.<br><i>Una cara gigante, nunca.</i>",
        "it": "Un cartello in più si perde nella folla.<br><i>Un volto gigante, mai.</i>",
    },
    "probleme.p1": {
        "fr": "Tu connais ce moment. Tu attends depuis une heure, les coureurs passent par centaines, et la personne pour qui tu es là file devant toi sans te voir. Elle a la tête baissée, les jambes lourdes, et ton prénom crié au milieu de mille autres ne lui parvient pas.",
        "en": "You know the moment. You have been waiting for an hour, runners stream past by the hundred, and the person you came for rushes by without seeing you. Their head is down, their legs are heavy, and your voice calling their name among a thousand others never reaches them.",
        "es": "Conoces ese momento. Llevas una hora esperando, los corredores pasan por cientos y la persona por la que estás allí pasa delante de ti sin verte. Va con la cabeza baja, las piernas pesadas, y su nombre gritado entre otros mil no le llega.",
        "it": "Conosci quel momento. Aspetti da un'ora, i corridori passano a centinaia, e la persona per cui sei lì ti sfila davanti senza vederti. Ha la testa bassa, le gambe pesanti, e il suo nome gridato in mezzo a mille altri non le arriva.",
    },
    "probleme.p2": {
        "fr": "Une grosse tête change tout, parce que c'est la seule chose qu'un coureur repère à coup sûr dans une foule : son propre visage, en grand. Il lève les yeux, il rit, il te trouve. Pour quelques secondes, les jambes oublient les kilomètres.",
        "en": "A Big Head changes everything, because it is the one thing a runner is sure to spot in a crowd: their own face, in giant size. They look up, they laugh, they find you. For a few seconds, their legs forget the miles.",
        "es": "Una cabeza gigante lo cambia todo, porque es lo único que un corredor encuentra seguro entre el público: su propia cara, en grande. Levanta la vista, se ríe, te encuentra. Durante unos segundos, las piernas olvidan los kilómetros.",
        "it": "Una testa gigante cambia tutto, perché è l'unica cosa che un corridore nota di sicuro in mezzo alla folla: il proprio viso, in grande. Alza lo sguardo, ride, ti trova. Per qualche secondo, le gambe dimenticano i chilometri.",
    },

    # ------------------------------------------------------- ce que tu reçois
    "recois.titre": {"fr": "Ce que tu reçois", "en": "What you get", "es": "Lo que recibes", "it": "Cosa ricevi"},
    "recois.intro": {
        "fr": "Un panneau rigide à son effigie, découpé au plus près de son visage, qui se tient d'une main et se range ensuite sur une étagère.",
        "en": "A rigid board with their face on it, cut closely around their features, that you hold in one hand and keep on a shelf afterwards.",
        "es": "Un panel rígido con su cara, recortado al ras de su rostro, que se sujeta con una mano y luego se guarda en una estantería.",
        "it": "Un pannello rigido con il suo volto, ritagliato il più vicino possibile al viso, che si tiene con una mano e poi trova posto su uno scaffale.",
    },
    "recois.p1_photo": {
        "fr": "Une supportrice brandit une grosse tête à côté d'une pancarte « T'es le meilleur »",
        "en": "A supporter holds up a Big Head next to a sign saying “You're the best”",
        "es": 'Una aficionada levanta una cabeza gigante junto a un cartel que dice «Eres el mejor»',
        "it": "Una tifosa solleva una testa gigante accanto a un cartello «Sei il migliore»",
    },
    "recois.p1_titre": {"fr": "Découpée à la forme", "en": "Cut to shape", "es": "Recortada a medida", "it": "Ritagliata su misura"},
    "recois.p1": {
        "fr": "Nous suivons le contour de son visage et de ses cheveux, avec une fine marge blanche qui fait ressortir la silhouette.",
        "en": "We follow the outline of their face and hair, with a thin white border that makes the silhouette stand out.",
        "es": "Seguimos el contorno de su cara y de su pelo, con un fino margen blanco que hace resaltar la silueta.",
        "it": "Seguiamo il contorno del viso e dei capelli, con un sottile bordo bianco che fa risaltare la sagoma.",
    },
    "recois.p2_photo": {
        "fr": "Une supportrice brandit une grosse tête sous la pluie, au passage d'un coureur",
        "en": 'A supporter holds up a Big Head in the rain as a runner goes by',
        "es": 'Una aficionada levanta una cabeza gigante bajo la lluvia al paso de un corredor',
        "it": "Una tifosa solleva una testa gigante sotto la pioggia, al passaggio di un corridore",
    },
    "recois.p2_titre": {"fr": "Un PVC rigide de 3 mm", "en": "Rigid 3 mm PVC", "es": "PVC rígido de 3 mm", "it": "PVC rigido da 3 mm"},
    "recois.p2": {
        "fr": "Il ne se plie pas dans le vent et ne gondole pas sous la pluie. Il reste léger, si bien qu'il se porte à bout de bras toute une matinée.",
        "en": "It doesn't bend in the wind or warp in the rain. It stays light, so you can hold it at arm's length all morning.",
        "es": "No se dobla con el viento ni se deforma con la lluvia. Es ligero, así que se puede sostener con el brazo en alto toda la mañana.",
        "it": "Non si piega al vento e non si deforma sotto la pioggia. Resta leggero, tanto da poterlo tenere a braccio teso per tutta una mattina.",
    },
    "recois.p3_photo": {
        "fr": "Une famille brandit trois grosses têtes du même visage au bord d'un trail",
        "en": 'A family holds up three Big Heads of the same face beside a trail race',
        "es": 'Una familia levanta tres cabezas gigantes de la misma cara junto a un trail',
        "it": "Una famiglia solleva tre teste giganti dello stesso viso al bordo di un trail",
    },
    "recois.p3_titre": {"fr": "Pour toute la bande", "en": "For the whole crew", "es": "Para toda la pandilla", "it": "Per tutta la squadra"},
    "recois.p3": {
        "fr": "Jusqu'à cinq exemplaires du même visage. Chaque panneau en plus ne coûte qu'un supplément, si bien qu'à cinq chacun revient jusqu'à {economie} % moins cher. La famille, le club et les collègues peuvent chacun avoir le sien.",
        "en": 'Up to five copies of the same face. Each extra board only costs a small supplement, so with five each one costs up to {economie}% less. Family, club mates and colleagues can each have their own.',
        "es": 'Hasta cinco ejemplares de la misma cara. Cada panel adicional solo cuesta un suplemento, así que con cinco cada uno sale hasta un {economie} % más barato. La familia, el club y los compañeros pueden tener cada uno el suyo.',
        "it": 'Fino a cinque copie dello stesso viso. Ogni pannello in più costa solo un supplemento, tanto che con cinque copie ognuno costa fino al {economie} % in meno. La famiglia, la società sportiva e i colleghi possono averne uno ciascuno.',
    },
    "recois.p4_photo": {
        "fr": 'Une grosse tête fixée à une barrière, au bord du parcours, pendant que les coureurs passent',
        "en": 'A Big Head fixed to a barrier along the course as the runners go by',
        "es": 'Una cabeza gigante sujeta a una valla junto al recorrido, mientras pasan los corredores',
        "it": "Una testa gigante fissata a una transenna, al bordo del percorso, mentre passano i corridori",
    },
    "recois.p4_titre": {"fr": "Elle reste après la course", "en": "It stays after the race", "es": "Se queda después de la carrera", "it": "Resta anche dopo la gara"},
    "recois.p4": {
        "fr": "Elle finit souvent au mur, à côté de la médaille et du dossard. Le souvenir dure bien plus longtemps que la course.",
        "en": "It often ends up on the wall, next to the medal and the race bib. The memory lasts much longer than the race.",
        "es": "A menudo acaba en la pared, junto a la medalla y el dorsal. El recuerdo dura mucho más que la carrera.",
        "it": "Spesso finisce appesa al muro, accanto alla medaglia e al pettorale. Il ricordo dura molto più a lungo della gara.",
    },

    # ------------------------------------------------------------ tailles
    "tailles.titre": {"fr": "Cinq tailles, à l'échelle", "en": "Five sizes, to scale", "es": "Cinco tamaños, a escala", "it": "Cinque misure, in scala"},
    "tailles.intro1": {
        "fr": "Chaque taille est tenue ici par une silhouette d'un mètre soixante-quinze, pour que tu voies ce que donnera la tienne au bord du parcours.",
        "en": "Each size is held here by a 1.75 m (5'9\") figure, so you can see how yours will look along the course.",
        "es": "Cada tamaño aparece aquí sostenido por una silueta de un metro setenta y cinco, para que veas cómo quedará la tuya junto al recorrido.",
        "it": "Ogni misura è tenuta qui da una sagoma alta un metro e settantacinque, così vedi come apparirà la tua al bordo del percorso.",
    },
    "tailles.intro2": {
        "fr": "Chacune se commande de 1 à 5 exemplaires du même visage. Seul le premier panneau est au plein tarif : chaque panneau en plus ne coûte qu'un supplément, si bien qu'à cinq chaque panneau revient jusqu'à {economie} % moins cher qu'à l'unité.",
        "en": 'Each one comes in 1 to 5 copies of the same face. Only the first board is full price: each extra board only costs a supplement, so with five, each board costs up to {economie}% less than buying one.',
        "es": 'Cada uno se pide de 1 a 5 ejemplares de la misma cara. Solo el primer panel va a precio completo: cada panel adicional solo cuesta un suplemento, así que con cinco cada panel sale hasta un {economie} % más barato que por unidad.',
        "it": 'Ognuna si ordina da 1 a 5 copie dello stesso viso. Solo il primo pannello è a prezzo pieno: ogni pannello in più costa solo un supplemento, tanto che con cinque copie ogni pannello costa fino al {economie} % in meno rispetto a uno solo.',
    },
    "tailles.conseil": {"fr": "Notre conseil", "en": "Our pick", "es": "Nuestra recomendación", "it": "Il nostro consiglio"},
    "taille.30.nom": {"fr": "Compacte", "en": "Compact", "es": "Compacta", "it": "Compatta"},
    "taille.30.pour": {
        "fr": "Légère et facile à glisser dans un sac, idéale pour les enfants.",
        "en": "Light and easy to slip into a bag, ideal for children.",
        "es": "Ligera y fácil de meter en una mochila, ideal para los niños.",
        "it": "Leggera e facile da infilare in una borsa, ideale per i bambini.",
    },
    "taille.45.nom": {"fr": "Visible", "en": "Visible", "es": "Visible", "it": "Visibile"},
    "taille.45.pour": {
        "fr": "Facile à tenir à bout de bras, même sur un long parcours.",
        "en": "Easy to hold at arm's length, even along a long course.",
        "es": "Fácil de sostener con el brazo en alto, incluso en un recorrido largo.",
        "it": "Facile da tenere a braccio teso, anche su un percorso lungo.",
    },
    "taille.60.nom": {"fr": "Repérable", "en": "Easy to spot", "es": "Fácil de ver", "it": "Riconoscibile"},
    "taille.60.pour": {
        "fr": "Le bon compromis : elle se voit de loin et se transporte sans peine.",
        "en": "The sweet spot: seen from afar and easy to carry.",
        "es": "El término medio: se ve de lejos y se transporta sin esfuerzo.",
        "it": "Il giusto compromesso: si vede da lontano e si trasporta senza fatica.",
    },
    "taille.80.nom": {"fr": "Impossible à rater", "en": "Impossible to miss", "es": "Imposible no verla", "it": "Impossibile da non notare"},
    "taille.80.pour": {
        "fr": "Pour les arrivées, les ravitos et les virages où toute la foule se masse.",
        "en": "For finish lines, aid stations and corners where the whole crowd gathers.",
        "es": "Para las metas, los avituallamientos y las curvas donde se agolpa el público.",
        "it": "Per gli arrivi, i ristori e le curve dove si accalca tutta la folla.",
    },
    "taille.100.nom": {"fr": "Géante", "en": "Giant", "es": "Gigante", "it": "Gigante"},
    "taille.100.pour": {
        "fr": "Un mètre de haut : elle dépasse toutes les têtes de la foule.",
        "en": "One metre tall: it rises above every head in the crowd.",
        "es": "Un metro de alto: sobresale por encima de todas las cabezas.",
        "it": "Un metro di altezza: supera tutte le teste della folla.",
    },
    "grille.une": {"fr": "1 panneau", "en": "1 board", "es": "1 panel", "it": "1 pannello"},
    "grille.plusieurs": {"fr": "{n} panneaux", "en": "{n} boards", "es": "{n} paneles", "it": "{n} pannelli"},
    "grille.supplement": {"fr": "par panneau en plus", "en": "each extra board", "es": "por panel adicional", "it": "per pannello in più"},
    "grille.fourchette": {"fr": "+{a} à {b}", "en": "+{a} to {b}", "es": "+{a} a {b}", "it": "+{a} – {b}"},
    "grille.col_n": {"fr": "Qté", "en": "Qty", "es": "Cant.", "it": "Q.tà"},
    "grille.col_total": {"fr": "Total", "en": "Total", "es": "Total", "it": "Totale"},
    "grille.col_unite": {"fr": "Par panneau", "en": "Per board", "es": "Por panel", "it": "A pannello"},
    "echelle.aria": {
        "fr": "Une grosse tête de {h} cm tenue par une personne d'un mètre soixante-quinze",
        "en": "A {h} cm Big Head held by a person 1.75 m tall",
        "es": "Una cabeza gigante de {h} cm sostenida por una persona de 1,75 m",
        "it": "Una testa gigante da {h} cm tenuta da una persona alta un metro e settantacinque",
    },
    "echelle.personne": {"fr": "1,75 m", "en": "1.75 m", "es": "1,75 m", "it": "1,75 m"},

    # -------------------------------------------------- comment ça marche
    "comment.titre": {"fr": "Comment ça marche", "en": "How it works", "es": "Cómo funciona", "it": "Come funziona"},
    "comment.intro": {
        "fr": "Tu vois ta grosse tête telle qu'elle sera imprimée avant de payer quoi que ce soit.",
        "en": "You see your Big Head exactly as it will be printed before paying anything.",
        "es": "Ves tu cabeza gigante tal y como se imprimirá antes de pagar nada.",
        "it": "Vedi la tua testa gigante così come sarà stampata prima di pagare qualsiasi cosa.",
    },
    "comment.e1_t": {"fr": "Tu envoies une photo de son visage", "en": "You send a photo of their face", "es": "Envías una foto de su cara", "it": "Ci mandi una foto del suo viso"},
    "comment.e1": {
        "fr": "Une photo nette prise au téléphone suffit. Inutile de la détourer, nous nous en chargeons.",
        "en": "A sharp photo taken with a phone is enough. No need to cut it out, we take care of that.",
        "es": "Basta una foto nítida hecha con el móvil. No hace falta recortarla, nos encargamos nosotros.",
        "it": "Basta una foto nitida scattata con il telefono. Non serve scontornarla, ci pensiamo noi.",
    },
    "comment.e2_t": {"fr": "Nous détourons et te montrons l'aperçu", "en": "We cut it out and show you a preview", "es": "La recortamos y te mostramos la vista previa", "it": "Scontorniamo il viso e ti mostriamo l'anteprima"},
    "comment.e2": {
        "fr": "Son visage apparaît découpé, à la taille choisie, tenu par une silhouette qui donne l'échelle. Tu peux recadrer jusqu'à ce qu'il te plaise.",
        "en": "Their face appears cut out at the chosen size, held by a figure that shows the scale. You can reframe it until you're happy.",
        "es": "Su cara aparece recortada, al tamaño elegido, sostenida por una silueta que da la escala. Puedes reencuadrarla hasta que te guste.",
        "it": "Il suo viso appare ritagliato, nella misura scelta, tenuto da una sagoma che dà la scala. Puoi ritagliare l'inquadratura finché non ti piace.",
    },
    "comment.e3_t": {"fr": "Tu choisis la taille et le nombre d'exemplaires", "en": "You choose the size and number of copies", "es": "Eliges el tamaño y el número de ejemplares", "it": "Scegli la misura e il numero di copie"},
    "comment.e3": {
        "fr": "Le paiement se fait en trente secondes sur une page sécurisée de Stripe, et la facture arrive aussitôt par courriel.",
        "en": "Payment takes thirty seconds on a secure Stripe page, and the invoice arrives by email straight away.",
        "es": "El pago se hace en treinta segundos en una página segura de Stripe, y la factura llega al momento por correo.",
        "it": "Il pagamento richiede trenta secondi su una pagina sicura di Stripe, e la fattura arriva subito per email.",
    },
    "comment.e4_t": {"fr": "Nous imprimons et expédions", "en": "We print and ship", "es": "Imprimimos y enviamos", "it": "Stampiamo e spediamo"},
    "comment.e4": {
        "fr": "Ta grosse tête est fabriquée en France et expédiée {delai}. Pense à commander une dizaine de jours avant la course.",
        "en": "Your Big Head is made in France and ships {delai}. Remember to order about ten days before the race.",
        "es": "Tu cabeza gigante se fabrica en Francia y se envía {delai}. Acuérdate de pedirla unos diez días antes de la carrera.",
        "it": "La tua testa gigante è prodotta in Francia e spedita {delai}. Ricordati di ordinarla una decina di giorni prima della gara.",
    },

    # -------------------------------------------------------------- objet
    "objet.titre": {"fr": "L'objet", "en": "The product", "es": "El producto", "it": "L'oggetto"},
    "objet.h_b": {"fr": "De {min} à {max} cm", "en": "{min} to {max} cm", "es": "De {min} a {max} cm", "it": "Da {min} a {max} cm"},
    "objet.h": {
        "fr": "{liste} cm de haut, la largeur suit son visage",
        "en": "{liste} cm tall, the width follows their face",
        "es": "{liste} cm de alto, el ancho sigue su cara",
        "it": "{liste} cm di altezza, la larghezza segue il viso",
    },
    "objet.pvc_b": {"fr": "PVC expansé 3 mm", "en": "3 mm foam PVC", "es": "PVC espumado de 3 mm", "it": "PVC espanso 3 mm"},
    "objet.pvc": {"fr": "Rigide, léger, résistant à l'eau", "en": "Rigid, light, water-resistant", "es": "Rígido, ligero, resistente al agua", "it": "Rigido, leggero, resistente all'acqua"},
    "objet.dec_b": {"fr": "Découpe à la forme", "en": "Cut to shape", "es": "Recorte a medida", "it": "Ritaglio sagomato"},
    "objet.dec": {
        "fr": "Impression couleur haute définition, au contour du visage",
        "en": "High-definition colour print, cut around the face",
        "es": "Impresión en color de alta definición, al contorno de la cara",
        "it": "Stampa a colori ad alta definizione, sul contorno del viso",
    },
    "objet.ex_b": {"fr": "De 1 à 5 exemplaires", "en": "1 to 5 copies", "es": "De 1 a 5 ejemplares", "it": "Da 1 a 5 copie"},
    "objet.ex": {"fr": "Du même visage, dans le même colis", "en": "Of the same face, in the same parcel", "es": "De la misma cara, en el mismo paquete", "it": "Dello stesso viso, nello stesso pacco"},

    # --------------------------------------------------------------- prix
    "prix.titre": {"fr": "Une photo, un prix clair.", "en": "One photo, one clear price.", "es": "Una foto, un precio claro.", "it": "Una foto, un prezzo chiaro."},
    "prix.texte": {
        "fr": "Détourage, impression, découpe et expédition sont compris. Chaque panneau en plus ne coûte qu'un supplément. Tu ne paies qu'après avoir vu l'aperçu, et rien ne t'y oblige.",
        "en": 'Cut-out, printing, shaping and shipping are all included. Each extra board only costs a supplement. You only pay after seeing the preview, and nothing obliges you to.',
        "es": 'Recorte, impresión, troquelado y envío incluidos. Cada panel adicional solo cuesta un suplemento. Solo pagas después de ver la vista previa, y nada te obliga.',
        "it": "Scontorno, stampa, ritaglio e spedizione sono inclusi. Ogni pannello in più costa solo un supplemento. Paghi solo dopo aver visto l'anteprima, e nulla ti obbliga a farlo.",
    },
    "prix.a_partir": {"fr": "À partir de", "en": "From", "es": "Desde", "it": "A partire da"},

    # -------------------------------------------------------- bande verte
    "bande.etiquette": {"fr": "Famille, club, collègues", "en": "Family, club, colleagues", "es": "Familia, club, compañeros", "it": "Famiglia, società sportiva, colleghi"},
    "bande.titre": {
        "fr": "Toute la bande sera au bord du parcours&nbsp;?",
        "en": "Is the whole crew coming to cheer?",
        "es": "¿Toda la pandilla estará junto al recorrido?",
        "it": "Tutta la squadra sarà al bordo del percorso?",
    },
    "bande.texte": {
        "fr": "Commande jusqu'à cinq exemplaires du même visage en une seule fois. Chaque panneau en plus ne coûte qu'un supplément : à cinq, chaque panneau revient jusqu'à {economie} % moins cher qu'à l'unité. Tout arrive dans le même colis, et chacun pourra se poster à un endroit différent du parcours.",
        "en": 'Order up to five copies of the same face in one go. Each extra board only costs a supplement: with five, each board costs up to {economie}% less than a single one. Everything arrives in the same parcel, and everyone can stand at a different spot along the course.',
        "es": 'Pide hasta cinco ejemplares de la misma cara de una sola vez. Cada panel adicional solo cuesta un suplemento: con cinco, cada panel sale hasta un {economie} % más barato que por unidad. Todo llega en el mismo paquete, y cada uno podrá colocarse en un punto distinto del recorrido.',
        "it": 'Ordina fino a cinque copie dello stesso viso in una sola volta. Ogni pannello in più costa solo un supplemento: con cinque copie, ogni pannello costa fino al {economie} % in meno rispetto a uno solo. Arriva tutto nello stesso pacco, e ognuno potrà appostarsi in un punto diverso del percorso.',
    },
    "bande.cta": {"fr": "Commander pour la bande", "en": "Order for the crew", "es": "Pedir para la pandilla", "it": "Ordina per la squadra"},

    # ---------------------------------------------------------- fondateur
    "fondateur.alt": {"fr": "Portrait de Laurent Thillaye du Boullay", "en": "Portrait of Laurent Thillaye du Boullay", "es": "Retrato de Laurent Thillaye du Boullay", "it": "Ritratto di Laurent Thillaye du Boullay"},
    "fondateur.c1": {
        "fr": "« Chez Westiti, nos photographes voient passer des milliers de coureurs à chaque course. Sur les photos, les plus grands sourires apparaissent presque toujours au même endroit : là où un proche brandit une grosse tête.",
        "en": "“At Westiti, our photographers see thousands of runners go by at every race. In the photos, the biggest smiles almost always appear in the same place: wherever a loved one is holding up a Big Head.",
        "es": "«En Westiti, nuestros fotógrafos ven pasar a miles de corredores en cada carrera. En las fotos, las sonrisas más grandes aparecen casi siempre en el mismo sitio: donde un ser querido levanta una cabeza gigante.",
        "it": "«Da Westiti, i nostri fotografi vedono passare migliaia di corridori a ogni gara. Nelle foto, i sorrisi più grandi compaiono quasi sempre nello stesso punto: dove una persona cara solleva una testa gigante.",
    },
    "fondateur.c2": {
        "fr": "J'ai voulu que chacun puisse offrir ce moment, sans logiciel ni imprimeur à chercher. Une photo suffit, et nous nous occupons du reste. »",
        "en": "I wanted everyone to be able to give that moment, without software or a printer to track down. One photo is enough, and we take care of the rest.”",
        "es": "Quise que cualquiera pudiera regalar ese momento, sin programas ni imprentas que buscar. Basta una foto, y nosotros nos encargamos del resto.»",
        "it": "Volevo che tutti potessero regalare quel momento, senza dover cercare un programma o una tipografia. Basta una foto, al resto pensiamo noi.»",
    },
    "fondateur.role": {
        "fr": "CEO Westiti — plus de 380 photographes partenaires, partout en France",
        "en": "CEO of Westiti — more than 380 partner photographers across France",
        "es": "CEO de Westiti — más de 380 fotógrafos colaboradores en toda Francia",
        "it": "CEO Westiti — oltre 380 fotografi partner in tutta la Francia",
    },

    # ---------------------------------------------------------------- faq
    "faq.titre": {"fr": "Questions", "en": "Questions", "es": "Preguntas", "it": "Domande"},
    "faq.q1": {"fr": "Quelle photo dois-je envoyer&nbsp;?", "en": "Which photo should I send?", "es": "¿Qué foto debo enviar?", "it": "Che foto devo inviare?"},
    "faq.r1": {
        "fr": "Une photo nette, de face ou de trois quarts, où le visage est bien éclairé et occupe une bonne partie de l'image. Une photo prise au téléphone convient très bien. Évite les captures d'écran et les photos floues, et inutile de la détourer toi-même.",
        "en": "A sharp photo, facing the camera or at a slight angle, where the face is well lit and fills a good part of the picture. A phone photo works perfectly. Avoid screenshots and blurry photos, and there's no need to cut it out yourself.",
        "es": "Una foto nítida, de frente o de tres cuartos, con la cara bien iluminada y ocupando buena parte de la imagen. Una foto hecha con el móvil sirve perfectamente. Evita las capturas de pantalla y las fotos borrosas, y no hace falta que la recortes tú.",
        "it": "Una foto nitida, frontale o di tre quarti, in cui il viso sia ben illuminato e occupi buona parte dell'immagine. Una foto scattata con il telefono va benissimo. Evita gli screenshot e le foto sfocate, e non serve scontornarla tu.",
    },
    "faq.q2": {"fr": "Combien de temps avant la course dois-je commander&nbsp;?", "en": "How long before the race should I order?", "es": "¿Con cuánta antelación debo pedirla?", "it": "Quanto tempo prima della gara devo ordinare?"},
    "faq.r2": {
        "fr": "Ta grosse tête est expédiée {delai}, puis la livraison prend en général deux à trois jours. Nous te conseillons de commander une dizaine de jours avant la course pour être tranquille.",
        "en": "Your Big Head ships {delai}, then delivery usually takes two to three days. We recommend ordering about ten days before the race to be on the safe side.",
        "es": "Tu cabeza gigante se envía {delai} y la entrega suele tardar de dos a tres días. Te aconsejamos pedirla unos diez días antes de la carrera para ir tranquilo.",
        "it": "La tua testa gigante viene spedita {delai}, poi la consegna richiede di solito due o tre giorni. Ti consigliamo di ordinare una decina di giorni prima della gara per stare tranquillo.",
    },
    "faq.q3": {"fr": "Puis-je voir le résultat avant de payer&nbsp;?", "en": "Can I see the result before paying?", "es": "¿Puedo ver el resultado antes de pagar?", "it": "Posso vedere il risultato prima di pagare?"},
    "faq.r3": {
        "fr": "Oui. L'aperçu te montre son visage détouré, à la taille choisie, tel qu'il sera imprimé. Tu peux recadrer, changer de photo ou de taille autant de fois que tu veux avant de commander.",
        "en": "Yes. The preview shows their face cut out, at the chosen size, just as it will be printed. You can reframe, change the photo or the size as many times as you like before ordering.",
        "es": "Sí. La vista previa te muestra su cara recortada, al tamaño elegido, tal y como se imprimirá. Puedes reencuadrar, cambiar de foto o de tamaño tantas veces como quieras antes de pedir.",
        "it": "Sì. L'anteprima ti mostra il suo viso scontornato, nella misura scelta, così come sarà stampato. Puoi ritagliare, cambiare foto o misura tutte le volte che vuoi prima di ordinare.",
    },
    "faq.q4": {"fr": "Faut-il l'accord de la personne représentée&nbsp;?", "en": "Do I need the consent of the person pictured?", "es": "¿Hace falta el permiso de la persona de la foto?", "it": "Serve il consenso della persona ritratta?"},
    "faq.r4": {
        "fr": "Oui. Son visage lui appartient, et tu nous confirmes au moment de la commande que tu as son accord. Pour une surprise, l'accord d'un proche qui la connaît bien suffit en général, mais c'est à toi d'en juger.",
        "en": "Yes. Their face belongs to them, and you confirm when ordering that you have their consent. For a surprise, the agreement of someone close who knows them well is usually enough, but that's your call.",
        "es": "Sí. Su cara le pertenece, y al hacer el pedido nos confirmas que tienes su permiso. Para una sorpresa, suele bastar el visto bueno de alguien cercano que la conozca bien, pero eso lo decides tú.",
        "it": "Sì. Il suo volto le appartiene, e al momento dell'ordine ci confermi di avere il suo consenso. Per una sorpresa, di solito basta il consenso di una persona che la conosce bene, ma sta a te valutare.",
    },
    "faq.q5": {"fr": "Que faites-vous de la photo&nbsp;?", "en": "What do you do with the photo?", "es": "¿Qué hacéis con la foto?", "it": "Cosa fate della foto?"},
    "faq.r5": {
        "fr": "Elle sert uniquement à fabriquer ta grosse tête. Nous l'effaçons une fois la commande expédiée, et elle n'est jamais réutilisée ni montrée ailleurs.",
        "en": "It is used only to make your Big Head. We delete it once the order has shipped, and it is never reused or shown anywhere else.",
        "es": "Solo sirve para fabricar tu cabeza gigante. La borramos en cuanto se envía el pedido, y nunca se reutiliza ni se muestra en otro sitio.",
        "it": "Serve solo a produrre la tua testa gigante. La cancelliamo una volta spedito l'ordine, e non viene mai riutilizzata né mostrata altrove.",
    },
    "faq.q6": {"fr": "Est-ce que ça résiste à la pluie&nbsp;?", "en": "Does it hold up in the rain?", "es": "¿Aguanta la lluvia?", "it": "Resiste alla pioggia?"},
    "faq.r6": {
        "fr": "Oui. Le PVC ne craint pas l'eau et l'impression ne coule pas. Le panneau reste rigide même par grand vent, ce qui n'est pas le cas d'une pancarte en carton.",
        "en": "Yes. PVC doesn't mind water and the print won't run. The board stays rigid even in strong wind, unlike a cardboard sign.",
        "es": "Sí. El PVC no teme al agua y la impresión no se corre. El panel sigue rígido incluso con mucho viento, algo que no ocurre con un cartel de cartón.",
        "it": "Sì. Il PVC non teme l'acqua e la stampa non cola. Il pannello resta rigido anche con il vento forte, cosa che un cartello di cartone non fa.",
    },
    "faq.q7": {"fr": "Puis-je commander plusieurs têtes différentes&nbsp;?", "en": "Can I order several different heads?", "es": "¿Puedo pedir varias cabezas distintas?", "it": "Posso ordinare più teste diverse?"},
    "faq.r7": {
        "fr": "Oui. Crée la première, puis recommence avec une autre photo. Pour le même visage, tu peux commander jusqu'à cinq exemplaires, et chaque panneau revient alors jusqu'à {economie} % moins cher.",
        "en": 'Yes. Create the first one, then start again with another photo. For the same face, you can order up to five copies, and each board then costs up to {economie}% less.',
        "es": 'Sí. Crea la primera y vuelve a empezar con otra foto. Para la misma cara, puedes pedir hasta cinco ejemplares, y cada panel sale entonces hasta un {economie} % más barato.',
        "it": "Sì. Crea la prima, poi ricomincia con un'altra foto. Per lo stesso viso puoi ordinare fino a cinque copie, e ogni pannello costa allora fino al {economie} % in meno.",
    },
    "faq.q8": {"fr": "Vous livrez où&nbsp;?", "en": "Where do you deliver?", "es": "¿Dónde hacéis envíos?", "it": "Dove spedite?"},
    "faq.r8": {
        "fr": "Partout en France métropolitaine, à l'adresse de ton choix.",
        "en": "Anywhere in mainland France, to the address of your choice.",
        "es": "A cualquier punto de la Francia metropolitana, a la dirección que elijas.",
        "it": "In tutta la Francia metropolitana, all'indirizzo che preferisci.",
    },
    "faq.r8_offerte": {"fr": "La livraison est offerte.", "en": "Delivery is free.", "es": "El envío es gratis.", "it": "La spedizione è gratuita."},

    # ------------------------------------------------------ dernier appel
    "final.titre": {
        "fr": "Sa prochaine course mérite un supporter qu'on ne rate pas.",
        "en": "Their next race deserves a supporter nobody can miss.",
        "es": "Su próxima carrera merece un apoyo imposible de pasar por alto.",
        "it": "La sua prossima gara merita un tifoso impossibile da non notare.",
    },
    "final.texte": {
        "fr": "Une photo pour commencer. Rien à payer pour voir l'aperçu.",
        "en": "One photo to get started. Nothing to pay to see the preview.",
        "es": "Una foto para empezar. Nada que pagar para ver la vista previa.",
        "it": "Una foto per cominciare. Nulla da pagare per vedere l'anteprima.",
    },

    # ============================================================ création
    "creer.titre_page": {"fr": "Créer une grosse tête", "en": "Create a Big Head", "es": "Crear una cabeza gigante", "it": "Crea una testa gigante"},
    "creer.h1": {"fr": "Créer ma grosse tête", "en": "Create my Big Head", "es": "Crear mi cabeza gigante", "it": "Crea la mia testa gigante"},
    "creer.intro": {
        "fr": "Trois étapes, et l'aperçu se met à jour à chaque choix. Tu ne paies qu'à la fin.",
        "en": "Three steps, and the preview updates with every choice. You only pay at the end.",
        "es": "Tres pasos, y la vista previa se actualiza con cada elección. Solo pagas al final.",
        "it": "Tre passaggi, e l'anteprima si aggiorna a ogni scelta. Paghi solo alla fine.",
    },
    "creer.photo_t": {"fr": "Sa photo", "en": "Their photo", "es": "Su foto", "it": "La sua foto"},
    "creer.photo_aide": {
        "fr": "Une photo nette de son visage, prise au téléphone. Inutile de la détourer, nous nous en chargeons.",
        "en": "A sharp photo of their face, taken with a phone. No need to cut it out, we take care of that.",
        "es": "Una foto nítida de su cara, hecha con el móvil. No hace falta recortarla, nos encargamos nosotros.",
        "it": "Una foto nitida del suo viso, scattata con il telefono. Non serve scontornarla, ci pensiamo noi.",
    },
    "creer.choisir": {"fr": "Choisir une photo", "en": "Choose a photo", "es": "Elegir una foto", "it": "Scegli una foto"},
    "creer.glisser": {
        "fr": "ou la glisser ici — JPEG, PNG ou HEIC, {mo} Mo au plus",
        "en": "or drop it here — JPEG, PNG or HEIC, {mo} MB max",
        "es": "o arrástrala aquí — JPEG, PNG o HEIC, {mo} MB como máximo",
        "it": "oppure trascinala qui — JPEG, PNG o HEIC, al massimo {mo} MB",
    },
    "creer.c1_b": {"fr": "Nette et bien éclairée", "en": "Sharp and well lit", "es": "Nítida y bien iluminada", "it": "Nitida e ben illuminata"},
    "creer.c1": {"fr": "La lumière du jour donne le meilleur résultat.", "en": "Daylight gives the best result.", "es": "La luz del día da el mejor resultado.", "it": "La luce del giorno dà il risultato migliore."},
    "creer.c2_b": {"fr": "Le visage en grand", "en": "A big face", "es": "La cara en grande", "it": "Il viso in grande"},
    "creer.c2": {"fr": "Il doit occuper une bonne partie de la photo.", "en": "It should fill a good part of the photo.", "es": "Debe ocupar buena parte de la foto.", "it": "Deve occupare buona parte della foto."},
    "creer.c3_b": {"fr": "Sans lunettes de soleil", "en": "No sunglasses", "es": "Sin gafas de sol", "it": "Senza occhiali da sole"},
    "creer.c3": {"fr": "Les yeux font toute la ressemblance.", "en": "The eyes make the likeness.", "es": "Los ojos hacen todo el parecido.", "it": "Sono gli occhi a fare la somiglianza."},
    "creer.recadrer": {"fr": "Recadrer le visage", "en": "Reframe the face", "es": "Reencuadrar la cara", "it": "Inquadra il viso"},
    "creer.recadrer_aide": {
        "fr": "Fais glisser la photo dans l'aperçu pour la centrer, et ajuste le zoom ici.",
        "en": "Drag the photo in the preview to centre it, and adjust the zoom here.",
        "es": "Arrastra la foto en la vista previa para centrarla y ajusta el zoom aquí.",
        "it": "Trascina la foto nell'anteprima per centrarla, e regola lo zoom qui.",
    },
    "creer.taille_t": {"fr": "La taille", "en": "The size", "es": "El tamaño", "it": "La misura"},
    "creer.taille_aide": {
        "fr": "La hauteur du panneau, du haut des cheveux au menton. La largeur suit la forme du visage.",
        "en": "The height of the board, from the top of the hair to the chin. The width follows the shape of the face.",
        "es": "La altura del panel, desde lo alto del pelo hasta la barbilla. El ancho sigue la forma de la cara.",
        "it": "L'altezza del pannello, dalla cima dei capelli al mento. La larghezza segue la forma del viso.",
    },
    "creer.des": {"fr": "dès {prix}", "en": "from {prix}", "es": "desde {prix}", "it": "da {prix}"},
    "creer.quantite_t": {"fr": "Combien d'exemplaires&nbsp;?", "en": "How many copies?", "es": "¿Cuántos ejemplares?", "it": "Quante copie?"},
    "creer.quantite_aide": {
        "fr": 'Le même visage, de 1 à 5 exemplaires : pratique quand toute la famille se répartit le long du parcours.',
        "en": 'The same face, in 1 to 5 copies: handy when the whole family spreads out along the course.',
        "es": 'La misma cara, de 1 a 5 ejemplares: práctico cuando toda la familia se reparte a lo largo del recorrido.',
        "it": 'Lo stesso viso, da 1 a 5 copie: comodo quando tutta la famiglia si distribuisce lungo il percorso.',
    },
    "creer.meilleur": {"fr": "Meilleur prix", "en": "Best price", "es": "Mejor precio", "it": "Miglior prezzo"},
    "creer.unite": {"fr": "Prix à l'unité", "en": "Single price", "es": "Precio por unidad", "it": "Prezzo unitario"},
    "creer.regle": {
        "fr": '1<sup>er</sup> panneau {premier}, puis <b>{plus}</b> par panneau en plus.',
        "en": 'First board {premier}, then <b>{plus}</b> for each extra one.',
        "es": 'Primer panel {premier}, luego <b>{plus}</b> por cada panel adicional.',
        "it": 'Primo pannello {premier}, poi <b>{plus}</b> per ogni pannello in più.',
    },
    "creer.mot_1": {"fr": "panneau", "en": "board", "es": "panel", "it": "pannello"},
    "creer.mot_n": {"fr": "panneaux", "en": "boards", "es": "paneles", "it": "pannelli"},
    "creer.par_panneau": {"fr": "soit {unite} le panneau", "en": "{unite} per board", "es": "{unite} por panel", "it": "{unite} a pannello"},
    "creer.accord": {
        "fr": "Je confirme avoir l'accord de la personne représentée pour faire imprimer son visage.",
        "en": "I confirm I have the consent of the person pictured to have their face printed.",
        "es": "Confirmo que tengo el permiso de la persona de la foto para imprimir su cara.",
        "it": "Confermo di avere il consenso della persona ritratta per far stampare il suo viso.",
    },
    "creer.legende_vide": {"fr": "Ton aperçu apparaîtra ici", "en": "Your preview will appear here", "es": "Tu vista previa aparecerá aquí", "it": "La tua anteprima apparirà qui"},
    "creer.toile_aria": {"fr": "Aperçu de la grosse tête", "en": "Big Head preview", "es": "Vista previa de la cabeza gigante", "it": "Anteprima della testa gigante"},
    "creer.r_taille": {"fr": "Taille", "en": "Size", "es": "Tamaño", "it": "Misura"},
    "creer.r_ex": {"fr": "Exemplaires", "en": "Copies", "es": "Ejemplares", "it": "Copie"},
    "creer.r_livraison": {"fr": "Livraison", "en": "Delivery", "es": "Envío", "it": "Spedizione"},
    "creer.offerte": {"fr": "Offerte", "en": "Free", "es": "Gratis", "it": "Gratuita"},
    "creer.calculee": {"fr": "Calculée à l'étape suivante", "en": "Calculated at the next step", "es": "Se calcula en el paso siguiente", "it": "Calcolata al passaggio successivo"},
    "creer.total": {"fr": "Total", "en": "Total", "es": "Total", "it": "Totale"},
    "creer.paiement": {
        "fr": "Paiement sur une page sécurisée de Stripe. {expediee}.",
        "en": "Payment on a secure Stripe page. {expediee}.",
        "es": "Pago en una página segura de Stripe. {expediee}.",
        "it": "Pagamento su una pagina sicura di Stripe. {expediee}.",
    },
    "creer.note": {
        "fr": "L'aperçu montre le cadrage. Le détourage précis, au contour des cheveux, est réalisé avant l'impression.",
        "en": "The preview shows the framing. The precise cut-out around the hair is done before printing.",
        "es": "La vista previa muestra el encuadre. El recorte preciso, al contorno del pelo, se hace antes de imprimir.",
        "it": "L'anteprima mostra l'inquadratura. Lo scontorno preciso, lungo i capelli, viene realizzato prima della stampa.",
    },

    # Les textes que le script de l'aperçu affiche lui-même.
    "js.photo_ici": {"fr": "Sa photo ici", "en": "Their photo here", "es": "Su foto aquí", "it": "La sua foto qui"},
    "js.glisser": {"fr": "Fais glisser pour centrer le visage", "en": "Drag to centre the face", "es": "Arrastra para centrar la cara", "it": "Trascina per centrare il viso"},
    "js.changer": {"fr": "Changer de photo", "en": "Change photo", "es": "Cambiar de foto", "it": "Cambia foto"},
    "js.trop_lourde": {
        "fr": "Cette photo dépasse {mo} Mo. Choisis-en une plus légère.",
        "en": "This photo is larger than {mo} MB. Please choose a smaller one.",
        "es": "Esta foto supera los {mo} MB. Elige una más ligera.",
        "it": "Questa foto supera {mo} MB. Scegline una più leggera.",
    },
    "js.petite": {
        "fr": "Cette photo est un peu petite : le visage risque d'être flou une fois imprimé en grand. Une photo plus grande donnera un meilleur résultat.",
        "en": "This photo is a little small: the face may look blurry once printed large. A bigger photo will give a better result.",
        "es": "Esta foto es un poco pequeña: la cara puede verse borrosa una vez impresa en grande. Una foto más grande dará mejor resultado.",
        "it": "Questa foto è un po' piccola: il viso rischia di risultare sfocato una volta stampato in grande. Una foto più grande darà un risultato migliore.",
    },
    "js.illisible": {
        "fr": "Nous n'arrivons pas à lire cette photo. Essaie avec un fichier JPEG ou PNG.",
        "en": "We can't read this photo. Please try a JPEG or PNG file.",
        "es": "No conseguimos leer esta foto. Prueba con un archivo JPEG o PNG.",
        "it": "Non riusciamo a leggere questa foto. Prova con un file JPEG o PNG.",
    },
    "js.commander": {"fr": "Commander", "en": "Order", "es": "Pedir", "it": "Ordina"},
    "js.commander_total": {"fr": "Commander — {total}", "en": "Order — {total}", "es": "Pedir — {total}", "it": "Ordina — {total}"},
    "js.instant": {"fr": "Un instant…", "en": "One moment…", "es": "Un momento…", "it": "Un attimo…"},
    "js.m_photo": {"fr": "Ajoute une photo", "en": "Add a photo", "es": "Añade una foto", "it": "Aggiungi una foto"},
    "js.m_taille": {"fr": "Choisis une taille", "en": "Choose a size", "es": "Elige un tamaño", "it": "Scegli una misura"},
    "js.m_accord": {"fr": "Confirme l'accord", "en": "Confirm consent", "es": "Confirma el permiso", "it": "Conferma il consenso"},
    "js.manque_photo": {"fr": "Ajoute une photo pour continuer.", "en": "Add a photo to continue.", "es": "Añade una foto para continuar.", "it": "Aggiungi una foto per continuare."},
    "js.manque_taille": {"fr": "Choisis une taille pour continuer.", "en": "Choose a size to continue.", "es": "Elige un tamaño para continuar.", "it": "Scegli una misura per continuare."},
    "js.manque_accord": {
        "fr": "Confirme l'accord de la personne pour continuer.",
        "en": "Confirm the person's consent to continue.",
        "es": "Confirma el permiso de la persona para continuar.",
        "it": "Conferma il consenso della persona per continuare.",
    },
    "js.pret": {"fr": "Tout est prêt.", "en": "All set.", "es": "Todo listo.", "it": "È tutto pronto."},

    # Les erreurs renvoyées par le serveur.
    "err.taille": {"fr": "Choisis une taille avant de commander.", "en": "Please choose a size before ordering.", "es": "Elige un tamaño antes de pedir.", "it": "Scegli una misura prima di ordinare."},
    "err.accord": {
        "fr": "Confirme que tu as l'accord de la personne représentée.",
        "en": "Please confirm you have the consent of the person pictured.",
        "es": "Confirma que tienes el permiso de la persona de la foto.",
        "it": "Conferma di avere il consenso della persona ritratta.",
    },
    "err.format": {
        "fr": "Ce format de photo n'est pas accepté. Envoie un fichier JPEG ou PNG.",
        "en": "This photo format isn't accepted. Please send a JPEG or PNG file.",
        "es": "Este formato de foto no se acepta. Envía un archivo JPEG o PNG.",
        "it": "Questo formato di foto non è accettato. Invia un file JPEG o PNG.",
    },
    "err.poids": {"fr": "La photo dépasse {mo} Mo.", "en": "The photo is larger than {mo} MB.", "es": "La foto supera los {mo} MB.", "it": "La foto supera {mo} MB."},
    "err.quantite": {"fr": "Choisis de 1 à 5 exemplaires.", "en": "Please choose 1 to 5 copies.", "es": "Elige de 1 a 5 ejemplares.", "it": "Scegli da 1 a 5 copie."},
    "err.paiement": {"fr": "Le paiement arrive bientôt.", "en": "Payment is coming soon.", "es": "El pago llegará pronto.", "it": "Il pagamento sarà disponibile a breve."},
    "err.paiement_echec": {
        "fr": "La page de paiement n'a pas pu s'ouvrir. Réessaie dans un instant en choisissant de nouveau ta photo.",
        "en": "The payment page couldn't open. Please try again in a moment; just choose your photo again.",
        "es": "La página de pago no ha podido abrirse. Vuelve a intentarlo en un momento; solo tienes que elegir tu foto de nuevo.",
        "it": "Non è stato possibile aprire la pagina di pagamento. Riprova tra un attimo scegliendo di nuovo la tua foto.",
    },

    # Ce que Stripe affiche sur sa page de paiement et sur la facture.
    "stripe.produit": {"fr": "Grosse tête {h} cm", "en": "Big Head {h} cm", "es": "Cabeza gigante {h} cm", "it": "Testa gigante {h} cm"},
    "stripe.description": {
        "fr": "{n} exemplaire(s) du même visage, PVC rigide 3 mm découpé à la forme, imprimé et expédié",
        "en": "{n} copy/copies of the same face, rigid 3 mm PVC cut to shape, printed and shipped",
        "es": "{n} ejemplar(es) de la misma cara, PVC rígido de 3 mm recortado a medida, impreso y enviado",
        "it": "{n} copia/e dello stesso viso, PVC rigido 3 mm sagomato, stampato e spedito",
    },
    "stripe.pied_facture": {
        "fr": "Merci pour ta commande. Pour toute question sur cette facture, réponds simplement au courriel de confirmation.",
        "en": "Thank you for your order. For any question about this invoice, simply reply to the confirmation email.",
        "es": "Gracias por tu pedido. Para cualquier pregunta sobre esta factura, responde al correo de confirmación.",
        "it": "Grazie per il tuo ordine. Per qualsiasi domanda su questa fattura, rispondi semplicemente all'email di conferma.",
    },

    # ================================================= bientôt, merci
    "bientot.titre_page": {"fr": "Presque prêt", "en": "Almost ready", "es": "Casi listo", "it": "Quasi pronto"},
    "bientot.h1": {
        "fr": "Ta grosse tête est prête, le paiement pas encore.",
        "en": "Your Big Head is ready, payment isn't yet.",
        "es": "Tu cabeza gigante está lista, el pago todavía no.",
        "it": "La tua testa gigante è pronta, il pagamento non ancora.",
    },
    "bientot.texte": {
        "fr": "Nous ouvrons les commandes dans quelques jours. Ta photo n'a pas été conservée : il te suffira de revenir et de recommencer, cela prend une minute.",
        "en": "We are opening orders in a few days. Your photo has not been kept: just come back and start again, it only takes a minute.",
        "es": "Abrimos los pedidos dentro de unos días. Tu foto no se ha guardado: solo tendrás que volver y empezar de nuevo, es cuestión de un minuto.",
        "it": "Apriamo gli ordini tra qualche giorno. La tua foto non è stata conservata: ti basterà tornare e ricominciare, ci vuole un minuto.",
    },
    "bientot.recap": {
        "fr": "Ton choix : {taille} cm × {quantite}, soit {total} au total.",
        "en": "Your choice: {taille} cm × {quantite}, {total} in total.",
        "es": "Tu elección: {taille} cm × {quantite}, {total} en total.",
        "it": "La tua scelta: {taille} cm × {quantite}, cioè {total} in totale.",
    },
    "bientot.retour": {"fr": "Revenir à l'atelier", "en": "Back to the workshop", "es": "Volver al taller", "it": "Torna al laboratorio"},
    "merci.titre_page": {"fr": "Merci", "en": "Thank you", "es": "Gracias", "it": "Grazie"},
    "merci.emotion": {"fr": "Commande reçue.", "en": "Order received.", "es": "Pedido recibido.", "it": "Ordine ricevuto."},
    "merci.h1": {
        "fr": "Sa grosse tête part en fabrication.",
        "en": "Their Big Head is going into production.",
        "es": "Su cabeza gigante entra en fabricación.",
        "it": "La sua testa gigante entra in produzione.",
    },
    "merci.p1": {
        "fr": "Tu viens de recevoir la confirmation et la facture par courriel. Nous t'écrirons de nouveau au moment de l'expédition, avec le numéro de suivi du colis.",
        "en": "You have just received the confirmation and invoice by email. We will write again when it ships, with the parcel's tracking number.",
        "es": "Acabas de recibir la confirmación y la factura por correo. Te volveremos a escribir en el momento del envío, con el número de seguimiento del paquete.",
        "it": "Hai appena ricevuto la conferma e la fattura per email. Ti scriveremo di nuovo al momento della spedizione, con il numero di tracciamento del pacco.",
    },
    "merci.p2": {
        "fr": "Il ne te reste plus qu'à repérer le meilleur endroit du parcours.",
        "en": "All that's left is to find the best spot on the course.",
        "es": "Solo te queda encontrar el mejor sitio del recorrido.",
        "it": "Non ti resta che trovare il punto migliore del percorso.",
    },
    "merci.retour": {"fr": "Retour à l'accueil", "en": "Back to home", "es": "Volver al inicio", "it": "Torna alla home"},

    "legal.en_cours": {
        "fr": "Ce texte est en cours de rédaction et sera validé par notre conseil avant l'ouverture des commandes.",
        "en": "This text is being drafted and will be reviewed by our legal adviser before orders open.",
        "es": "Este texto está en redacción y lo validará nuestro asesor legal antes de abrir los pedidos.",
        "it": "Questo testo è in fase di redazione e sarà convalidato dal nostro consulente legale prima dell'apertura degli ordini.",
    },
}


# Les pages légales : un titre et des sections, dans chaque langue.
LEGAL = {
    "cgv": {
        "fr": ("Conditions générales de vente", [
            ("Objet", "Les présentes conditions encadrent la vente de panneaux imprimés personnalisés à l'effigie d'une personne, dits « grosses têtes », sur le site grossetete.westiti.app."),
            ("Commande", "La commande est ferme une fois le paiement confirmé par Stripe. Le client valide l'aperçu avant de payer."),
            ("Produit personnalisé", "Le produit étant confectionné selon les spécifications du client et nettement personnalisé, le droit de rétractation ne s'applique pas, conformément à l'article L221-28 3° du Code de la consommation."),
            ("Droit à l'image", "Le client garantit disposer de l'accord de la personne représentée sur la photo transmise."),
            ("Livraison", "Les délais et zones de livraison sont précisés sur le site au moment de la commande."),
        ]),
        "en": ("Terms of sale", [
            ("Purpose", "These terms govern the sale of personalised printed boards bearing a person's likeness, known as “Big Heads”, on the website grossetete.westiti.app."),
            ("Orders", "An order is final once payment has been confirmed by Stripe. The customer approves the preview before paying."),
            ("Personalised product", "As the product is made to the customer's specifications and clearly personalised, the right of withdrawal does not apply, in accordance with article L221-28 3° of the French Consumer Code."),
            ("Image rights", "The customer guarantees that they have the consent of the person shown in the photo provided."),
            ("Delivery", "Delivery times and areas are stated on the website at the time of ordering."),
        ]),
        "es": ("Condiciones generales de venta", [
            ("Objeto", "Las presentes condiciones regulan la venta de paneles impresos personalizados con la imagen de una persona, llamados «cabezas gigantes», en el sitio grossetete.westiti.app."),
            ("Pedido", "El pedido es firme una vez que Stripe confirma el pago. El cliente valida la vista previa antes de pagar."),
            ("Producto personalizado", "Al confeccionarse según las especificaciones del cliente y estar claramente personalizado, el producto no admite derecho de desistimiento, conforme al artículo L221-28 3° del Código de consumo francés."),
            ("Derecho de imagen", "El cliente garantiza que cuenta con el permiso de la persona que aparece en la foto enviada."),
            ("Envío", "Los plazos y zonas de envío se indican en el sitio en el momento del pedido."),
        ]),
        "it": ("Condizioni generali di vendita", [
            ("Oggetto", "Le presenti condizioni regolano la vendita di pannelli stampati personalizzati con l'immagine di una persona, detti «teste giganti», sul sito grossetete.westiti.app."),
            ("Ordine", "L'ordine è definitivo una volta che Stripe ha confermato il pagamento. Il cliente approva l'anteprima prima di pagare."),
            ("Prodotto personalizzato", "Poiché il prodotto è realizzato secondo le specifiche del cliente e chiaramente personalizzato, il diritto di recesso non si applica, ai sensi dell'articolo L221-28 3° del Codice del consumo francese."),
            ("Diritto all'immagine", "Il cliente garantisce di avere il consenso della persona ritratta nella foto inviata."),
            ("Spedizione", "I tempi e le zone di consegna sono indicati sul sito al momento dell'ordine."),
        ]),
    },
    "mentions-legales": {
        "fr": ("Mentions légales", [
            ("Éditeur", "Westiti — raison sociale, siège, SIRET et directeur de la publication à compléter."),
            ("Hébergement", "Railway Corporation — adresse à compléter."),
        ]),
        "en": ("Legal notice", [
            ("Publisher", "Westiti — company name, registered office, SIRET number and publication director to be completed."),
            ("Hosting", "Railway Corporation — address to be completed."),
        ]),
        "es": ("Aviso legal", [
            ("Editor", "Westiti — razón social, domicilio, número SIRET y director de la publicación por completar."),
            ("Alojamiento", "Railway Corporation — dirección por completar."),
        ]),
        "it": ("Note legali", [
            ("Editore", "Westiti — ragione sociale, sede, numero SIRET e direttore della pubblicazione da completare."),
            ("Hosting", "Railway Corporation — indirizzo da completare."),
        ]),
    },
    "confidentialite": {
        "fr": ("Politique de confidentialité", [
            ("Données collectées", "La photo transmise, l'adresse de courriel et l'adresse de livraison, uniquement pour fabriquer et livrer la commande."),
            ("Conservation", "La photo est effacée une fois la commande expédiée. Les données de facturation sont conservées pendant la durée légale."),
            ("Sous-traitants", "Stripe pour le paiement, Fulfiller pour la fabrication et l'expédition."),
        ]),
        "en": ("Privacy policy", [
            ("Data collected", "The photo provided, the email address and the delivery address, solely to make and deliver the order."),
            ("Retention", "The photo is deleted once the order has shipped. Billing data is kept for the legally required period."),
            ("Processors", "Stripe for payment, Fulfiller for production and shipping."),
        ]),
        "es": ("Política de privacidad", [
            ("Datos recogidos", "La foto enviada, la dirección de correo y la dirección de entrega, únicamente para fabricar y entregar el pedido."),
            ("Conservación", "La foto se borra una vez enviado el pedido. Los datos de facturación se conservan durante el plazo legal."),
            ("Encargados del tratamiento", "Stripe para el pago, Fulfiller para la fabricación y el envío."),
        ]),
        "it": ("Informativa sulla privacy", [
            ("Dati raccolti", "La foto inviata, l'indirizzo email e l'indirizzo di consegna, esclusivamente per produrre e consegnare l'ordine."),
            ("Conservazione", "La foto viene cancellata una volta spedito l'ordine. I dati di fatturazione sono conservati per il periodo previsto dalla legge."),
            ("Responsabili del trattamento", "Stripe per il pagamento, Fulfiller per la produzione e la spedizione."),
        ]),
    },
}


def verifier():
    """Chaque clé doit exister dans les quatre langues."""
    manques = [(cle, l) for cle, v in T.items() for l in LANGUES if l not in v]
    manques += [(p, l) for p, v in LEGAL.items() for l in LANGUES if l not in v]
    if manques:
        raise ValueError(f"Traductions manquantes : {manques}")

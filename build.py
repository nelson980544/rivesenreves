#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du site statique RivesEnRêves
=========================================

Usage :   python3 build.py

Ce script (Python 3.8+, aucune dépendance à installer) :
  1. lit config.json (nom de domaine, e-mail du formulaire, téléphone...) ;
  2. assemble chaque page de src/pages/ avec le gabarit src/templates/base.html
     (en-tête, menus, fil d'Ariane, pied de page, balises SEO, JSON-LD) ;
  3. copie les fichiers de src/static/ (CSS, JS, polices, images, robots.txt,
     llms.txt, .htaccess) en remplaçant les marqueurs de configuration ;
  4. génère sitemap.xml, les images provisoires « PHOTO À REMPLACER »
     et la liste docs/photos-a-fournir.md.

Le résultat est écrit dans public/ : c'est CE dossier qu'on dépose chez l'hébergeur.

Format d'une page (src/pages/<chemin>/index.html) :
    <!--
    { ...métadonnées JSON : title, description, label, univers, faq... }
    -->
    <contenu HTML de la page, avec des jetons {{...}} décrits plus bas>

Jetons utilisables dans le contenu :
    {{root}}                    préfixe relatif vers la racine du site (ex. ../../)
    {{img name="x" alt="..." hint="..." w="1200" h="800" [eager] [class="..."]}}
    {{faq}}                     section FAQ (à partir de la métadonnée "faq")
    {{autres-univers}}          encart « Vous n'êtes pas au bon endroit ? »
    {{articles univers="..."}}  cartes des articles de blog (univers optionnel)
    {{article-meta}}            auteur + dates de publication / mise à jour
    {{fait:cle}}                affirmation vérifiable identique sur tout le site
    {{definition}}              phrase de définition de l'entreprise
    {{zone}}                    territoire d'intervention (bassin de la Seine + Canal de Bourgogne)
    {{email}} {{telephone}} {{telephone_international}}
"""

import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
STATIC = SRC / "static"
TEMPLATES = SRC / "templates"
# Dossier de sortie (public/ par défaut). Variables d'environnement pour la version
# d'aperçu publiée sur GitHub Pages (voir README, « Aperçu sur GitHub Pages ») :
#   RER_SORTIE=dossier   RER_APERCU=1 (bandeau + non indexé)   RER_BASE=/rivesenreves/
OUT = Path(os.environ.get("RER_SORTIE") or (ROOT / "public"))
APERCU = os.environ.get("RER_APERCU") == "1"
BASE_404 = os.environ.get("RER_BASE", "/")
PHOTOS_DIR = STATIC / "assets" / "img" / "photos"

# ---------------------------------------------------------------------------
# Contenus de référence (GEO) : une seule formulation, réutilisée partout.
# Modifiez-les ici pour qu'ils changent sur l'ensemble du site.
# ---------------------------------------------------------------------------
DEFINITION = (
    "RivesEnRêves est une entreprise fluviale fondée par Joël Le Mercier, qui propose "
    "des balades en bateau, des services aux plaisanciers, des études de report modal "
    "vers le fluvial financées par VNF et des services aux professionnels, et du conseil "
    "en développement du tourisme fluvial aux administrations."
)

# Territoire d'intervention : formulation unique, reprise partout (jeton {{zone}}).
ZONE = "le bassin de la Seine (Seine amont, Seine aval, canaux parisiens, Marne) et le Canal de Bourgogne"
ZONE_COURTE = "Bassin de la Seine et Canal de Bourgogne"
ZONE_LIEUX = ["Bassin de la Seine", "Seine amont", "Seine aval", "Canaux parisiens", "Marne",
              "Canal de Bourgogne"]

FAITS = {
    "haltes": "4 haltes fluviales exploitées sur la Marne de 2019 à 2025 en collaboration avec Coulommiers Pays de Brie Tourisme, dont 2 à La Ferté-sous-Jouarre",
    "haltes-rien": "4 haltes fluviales exploitées sur la Marne de 2019 à 2025 en collaboration avec Coulommiers Pays de Brie Tourisme, dont 2 à La Ferté-sous-Jouarre, créées sur des sites où il n'y avait rien à l'origine",
    "pouilly": "accompagnement de la Communauté de communes de Pouilly-Bligny dans l'achat d'un bateau pour naviguer sur le Canal de Bourgogne et développer l'activité touristique du territoire",
    "billebaude": "La Billebaude, bateau à passagers trouvé aux Pays-Bas par RivesEnRêves et acheminé jusqu'à Pouilly-en-Auxois pour la Communauté de communes de Pouilly-Bligny, qui l'exploite pour des balades fluviales sur le Canal de Bourgogne",
    "vnf-conseil": "mission de conseil en logistique fluviale pour VNF",
    "vnf-etudes": "études de report modal vers le fluvial financées par VNF",
    "fublaines": "site de Fublaines (Seine-et-Marne), en bord de Marne, occupé dans le cadre d'une sous-occupation de la convention de Valfrance",
    "renflouement": "renflouement d'un bateau à l'aide de ballons de flottaison",
    "decoupe": "découpe de bateaux : déconstruction de bateaux en fin de vie, évacuation de coques et d'épaves",
}

UNIVERS = {
    "balades": {
        "nom": "Balades",
        "url": "balades-bateau/",
        "profil": "particulier",
        "porte": "Je veux faire une balade",
        "accroche": "Balades en bateau sur la Marne et nuits insolites en gîte nautique.",
        "icone": "sun",
    },
    "plaisanciers": {
        "nom": "Plaisanciers",
        "url": "plaisanciers/",
        "profil": "plaisancier",
        "porte": "J'ai un bateau",
        "accroche": "Convoyage vers les chantiers avec les démarches administratives, renflouement, découpe.",
        "icone": "boat",
    },
    "professionnels": {
        "nom": "Professionnels",
        "url": "professionnels/",
        "profil": "professionnel",
        "porte": "Je suis un professionnel",
        "accroche": "Études de report modal financées par VNF, logistique fluviale, pousseur ERNA, interventions sur l'eau.",
        "icone": "crate",
    },
    "administrations": {
        "nom": "Administrations",
        "url": "administrations/",
        "profil": "administration",
        "porte": "Je représente une administration",
        "accroche": "Conseil en développement du tourisme fluvial, de l'idée à la mise en œuvre.",
        "icone": "columns",
    },
}

ICONES = {
    "sun": '<path d="M12 3v2M12 19v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M3 12h2M19 12h2M4.6 19.4L6 18M18 6l1.4-1.4"/><circle cx="12" cy="12" r="4"/>',
    "boat": '<path d="M3 15l2 4h14l2-4H3z"/><path d="M12 3v12M12 4l6 9h-6"/><path d="M2 21c2 0 2-1 4-1s2 1 4 1 2-1 4-1 2 1 4 1 2-1 4-1"/>',
    "crate": '<path d="M3 7l9-4 9 4v10l-9 4-9-4V7z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
    "columns": '<path d="M3 21h18M4 10h16M12 3l9 5H3l9-5z"/><path d="M6 10v8M10 10v8M14 10v8M18 10v8"/>',
}


def icone(nom, cls="ico"):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (cls, ICONES[nom]))


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
def charger_config():
    with open(ROOT / "config.json", encoding="utf-8") as f:
        cfg = json.load(f)
    domaine = cfg.get("nom_de_domaine", "[NOM_DE_DOMAINE]").strip().rstrip("/")
    domaine = re.sub(r"^https?://", "", domaine)
    cfg["nom_de_domaine"] = domaine
    cfg["base_url"] = "https://%s/" % domaine
    return cfg


def est_marqueur(v):
    return not v or (isinstance(v, str) and v.strip().startswith("["))


def remplacer_marqueurs(texte, cfg):
    """Remplace les marqueurs de config.json dans un texte (HTML, JS, txt...)."""
    pairs = {
        "[NOM_DE_DOMAINE]": cfg["nom_de_domaine"],
        "[ADRESSE_EMAIL_DE_RECEPTION]": cfg.get("email_reception_formulaire", ""),
        "[EMAIL_CONTACT]": cfg.get("email_contact", ""),
        "[TELEPHONE]": cfg.get("telephone", ""),
        "[TELEPHONE_INTERNATIONAL]": cfg.get("telephone_international", ""),
        "[WEB3FORMS_ACCESS_KEY]": cfg.get("web3forms_access_key", ""),
        "[DATE_MISE_A_JOUR]": cfg.get("date_mise_a_jour_site", ""),
    }
    for k, v in pairs.items():
        # Une valeur restée « marqueur » ne remplace rien (le marqueur reste visible).
        if v and v != k:
            texte = texte.replace(k, v)
    return texte


# ---------------------------------------------------------------------------
# Lecture des pages
# ---------------------------------------------------------------------------
FRONT = re.compile(r"^\s*<!--\s*(\{.*?\})\s*-->\s*", re.S)


def lire_pages():
    pages = []
    for f in sorted(PAGES.rglob("*.html")):
        rel = f.relative_to(PAGES).as_posix()
        brut = f.read_text(encoding="utf-8")
        m = FRONT.match(brut)
        if not m:
            sys.exit("Métadonnées JSON manquantes en tête de %s" % rel)
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            sys.exit("JSON invalide dans %s : %s" % (rel, e))
        corps = brut[m.end():]
        if rel == "index.html":
            url = ""
        elif rel.endswith("/index.html"):
            url = rel[: -len("index.html")]
        else:
            url = rel  # ex. 404.html
        profondeur = url.count("/")
        pages.append({
            "fichier": rel,
            "url": url,
            # La page 404 est servie à n'importe quelle adresse : chemins absolus.
            "root": BASE_404 if url == "404.html" else ("../" * profondeur if profondeur else "./"),
            "meta": meta,
            "corps": corps,
        })
    return pages


# ---------------------------------------------------------------------------
# Images : photo réelle si elle existe, sinon image provisoire générée
# ---------------------------------------------------------------------------
PHOTOS_MANQUANTES = {}
EXT_PHOTOS = ["avif", "webp", "jpg", "jpeg", "png"]


def svg_provisoire(nom, hint, w, h):
    lignes, ligne = [], ""
    for mot in hint.split():
        if len(ligne) + len(mot) > 46:
            lignes.append(ligne)
            ligne = mot
        else:
            ligne = (ligne + " " + mot).strip()
    if ligne:
        lignes.append(ligne)
    fs = max(18, int(min(w, h) / 22))
    y0 = h / 2 - (len(lignes) * fs * 1.3) / 2 + fs * 0.4
    texte = "".join(
        '<text x="50%%" y="%d" text-anchor="middle" font-size="%d">%s</text>'
        % (y0 + i * fs * 1.3, fs, html.escape(l)) for i, l in enumerate(lignes))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#cfe0e6"/><stop offset=".55" stop-color="#7fa9bb"/>'
        '<stop offset="1" stop-color="#2f6378"/></linearGradient></defs>'
        '<rect width="100%" height="100%" fill="url(#g)"/>'
        '<path d="M0 {a} Q {q1} {b} {hw} {a} T {w} {a} V {h} H 0 Z" fill="#1d4b5e" opacity=".45"/>'
        '<g font-family="Georgia, serif" fill="#ffffff">'
        '<text x="50%" y="{ty}" text-anchor="middle" font-size="{fs2}" letter-spacing="3" opacity=".9">PHOTO À REMPLACER</text>'
        '{texte}'
        '<text x="50%" y="{fy}" text-anchor="middle" font-size="{fs3}" font-family="monospace" opacity=".85">Fichier attendu : photos/{nom}.webp</text>'
        '</g></svg>'
    ).format(w=w, h=h, a=int(h * .78), b=int(h * .70), q1=int(w * .25), hw=int(w / 2),
             ty=int(h * .2), fs2=max(14, int(fs * .7)), texte=texte, fy=int(h * .9),
             fs3=max(12, int(fs * .55)), nom=nom)


def rendre_img(attrs, page):
    nom = attrs["name"]
    alt = attrs.get("alt", "")
    w, h = int(attrs.get("w", 1200)), int(attrs.get("h", 800))
    cls = attrs.get("class", "")
    eager = "eager" in attrs
    root = page["root"]
    src = None
    for ext in EXT_PHOTOS:
        if (PHOTOS_DIR / ("%s.%s" % (nom, ext))).exists():
            src = "%sassets/img/photos/%s.%s" % (root, nom, ext)
            break
    if src is None:
        hint = attrs.get("hint", alt)
        PHOTOS_MANQUANTES.setdefault(nom, {"hint": hint, "w": w, "h": h, "pages": set()})
        PHOTOS_MANQUANTES[nom]["pages"].add("/" + page["url"])
        src = "%sassets/img/a-remplacer/%s.svg" % (root, nom)
        cls = (cls + " is-placeholder").strip()
    charge = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return ('<img src="%s" alt="%s" width="%d" height="%d" %s decoding="async"%s>'
            % (src, html.escape(alt, quote=True), w, h, charge,
               (' class="%s"' % cls) if cls else ""))


ATTR = re.compile(r'(\w[\w-]*)(?:="([^"]*)")?')


def parse_attrs(s):
    return {k: v for k, v in ATTR.findall(s)}


# ---------------------------------------------------------------------------
# Blocs réutilisables
# ---------------------------------------------------------------------------
def bloc_faq(meta):
    faq = meta.get("faq") or []
    if not faq:
        return ""
    items = "".join(
        '<details class="faq-item"><summary><h3>%s</h3></summary><div class="faq-answer"><p>%s</p></div></details>'
        % (html.escape(q["q"]), q["a"]) for q in faq)
    titre = meta.get("faq_titre", "Questions fréquentes")
    return ('<section class="section faq" aria-labelledby="faq-titre"><div class="container narrow">'
            '<h2 id="faq-titre">%s</h2><div class="faq-list">%s</div></div></section>' % (titre, items))


def bloc_autres_univers(page):
    courant = page["meta"].get("univers")
    cartes = ""
    for cle, u in UNIVERS.items():
        if cle == courant:
            continue
        cartes += ('<a class="switch-card u-%s" href="%s%s">%s<span><strong>%s</strong>'
                   '<small>%s</small></span></a>'
                   % (cle, page["root"], u["url"], icone(u["icone"]), u["porte"], u["nom"]))
    return ('<aside class="switcher" aria-labelledby="switch-titre"><div class="container">'
            '<h2 id="switch-titre" class="switcher-title">Vous n\'êtes pas au bon endroit ?</h2>'
            '<div class="switch-grid">%s</div></div></aside>' % cartes)


def bloc_articles(pages, page, univers=None):
    arts = [p for p in pages if p["meta"].get("type") == "article"
            and (univers is None or p["meta"].get("univers") == univers)]
    arts.sort(key=lambda p: p["meta"]["article"]["datePublished"], reverse=True)
    if not arts:
        return ""
    cartes = ""
    for a in arts:
        m = a["meta"]
        u = UNIVERS[m["univers"]]
        cartes += (
            '<article class="post-card u-%s" data-univers="%s"><a href="%s%s">'
            '<span class="tag">%s</span><h3>%s</h3><p>%s</p>'
            '<span class="post-date">Mis à jour le <time datetime="%s">%s</time></span>'
            '<span class="link-arrow">Lire l\'article</span></a></article>'
            % (m["univers"], m["univers"], page["root"], a["url"], u["nom"], html.escape(m["h1"]),
               html.escape(m["description"]), m["article"]["dateModified"],
               date_fr(m["article"]["dateModified"])))
    return '<div class="post-grid">%s</div>' % cartes


MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def date_fr(iso):
    a, m, j = iso.split("-")
    return "%d %s %s" % (int(j), MOIS[int(m) - 1], a)


def bloc_article_meta(page):
    art = page["meta"]["article"]
    return ('<p class="article-meta">Par <a href="%sa-propos/#joel-le-mercier">Joël Le Mercier</a>, '
            'fondateur de RivesEnRêves · Publié le <time datetime="%s">%s</time> · '
            'Mis à jour le <time datetime="%s">%s</time></p>'
            % (page["root"], art["datePublished"], date_fr(art["datePublished"]),
               art["dateModified"], date_fr(art["dateModified"])))


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
MENU = [
    ("balades", "Balades", "balades-bateau/"),
    ("plaisanciers", "Plaisanciers", "plaisanciers/"),
    ("professionnels", "Professionnels", "professionnels/"),
    ("administrations", "Administrations", "administrations/"),
    ("a-propos", "À propos", "a-propos/"),
    ("contact", "Contact", "contact/"),
]


def section_courante(page):
    u = page["meta"].get("univers")
    if u and page["meta"].get("type") != "article":
        return u
    for cle, _, url in MENU[4:]:
        if page["url"].startswith(url):
            return cle
    return None


def rendre_menu(page):
    cur = section_courante(page)
    items = ""
    for cle, label, url in MENU:
        actif = ' aria-current="page"' if page["url"] == url else ""
        cls = ' class="is-active"' if cle == cur else ""
        items += '<li%s><a href="%s%s"%s>%s</a></li>' % (
            cls, page["root"], url, actif, label)
    return items


def rendre_barre_univers(page):
    """Accès direct aux 4 univers sur mobile (un seul geste)."""
    cur = page["meta"].get("univers") if page["meta"].get("type") != "article" else None
    items = ""
    for cle, u in UNIVERS.items():
        items += '<a class="u-%s%s" href="%s%s">%s<span>%s</span></a>' % (
            cle, " is-active" if cle == cur else "", page["root"], u["url"],
            icone(u["icone"]), u["nom"])
    return items


def rendre_sous_nav(page, pages):
    u = page["meta"].get("univers")
    if not u or page["meta"].get("type") == "article":
        return ""
    base = UNIVERS[u]["url"]
    enfants = [p for p in pages if p["url"].startswith(base) and p["url"] != base]
    enfants.sort(key=lambda p: p["meta"].get("ordre", 50))
    liens = '<a href="%s%s"%s>Vue d\'ensemble</a>' % (
        page["root"], base, ' aria-current="page"' if page["url"] == base else "")
    for e in enfants:
        liens += '<a href="%s%s"%s>%s</a>' % (
            page["root"], e["url"], ' aria-current="page"' if page["url"] == e["url"] else "",
            e["meta"]["label"])
    return ('<nav class="subnav u-%s" aria-label="Pages de l\'univers %s"><div class="container">'
            '<span class="subnav-title">%s</span><div class="subnav-links">%s</div></div></nav>'
            % (u, UNIVERS[u]["nom"], UNIVERS[u]["nom"], liens))


def ancetres(page, index):
    """Liste des pages parentes (pour le fil d'Ariane)."""
    chaine = []
    parts = [p for p in page["url"].split("/") if p]
    for i in range(1, len(parts)):
        url = "/".join(parts[:i]) + "/"
        if url in index:
            chaine.append(index[url])
    return chaine


def rendre_ariane(page, index):
    if page["url"] in ("", "404.html"):
        return "", None
    chaine = ancetres(page, index) + [page]
    items = '<li><a href="%s">Accueil</a></li>' % page["root"]
    for p in chaine[:-1]:
        items += '<li><a href="%s%s">%s</a></li>' % (page["root"], p["url"], p["meta"]["label"])
    items += '<li aria-current="page">%s</li>' % page["meta"]["label"]
    html_ = ('<nav class="breadcrumb" aria-label="Fil d\'Ariane"><div class="container"><ol>%s</ol></div></nav>'
             % items)
    return html_, [("Accueil", "")] + [(p["meta"]["label"], p["url"]) for p in chaine]


# ---------------------------------------------------------------------------
# Données structurées JSON-LD
# ---------------------------------------------------------------------------
def jsonld(page, cfg, ariane):
    base = cfg["base_url"]
    meta = page["meta"]
    org_id = base + "#organisation"
    person_id = base + "a-propos/#joel-le-mercier"
    url = base + page["url"]
    graph = []

    org = {
        "@type": ["Organization", "LocalBusiness"],
        "@id": org_id,
        "name": "RivesEnRêves",
        "url": base,
        "logo": base + ("assets/img/logo-officiel.webp" if (IMG_DIR / "logo-officiel.webp").exists()
                        else "assets/img/logo-rivesenreves.svg"),
        "image": base + "assets/img/og-rivesenreves.jpg",
        "description": DEFINITION,
        "founder": {"@id": person_id},
        "legalName": "RivesEnRêves",
        "alternateName": "Rives en Rêves",
        "foundingDate": "2022-01-21",
        "vatID": "FR71909449548",
        "identifier": [{"@type": "PropertyValue", "propertyID": "SIREN", "value": "909449548"},
                       {"@type": "PropertyValue", "propertyID": "SIRET", "value": "90944954800025"}],
        "areaServed": [{"@type": "Place", "name": n} for n in ZONE_LIEUX] + [
            {"@type": "AdministrativeArea", "name": "Île-de-France"},
            {"@type": "AdministrativeArea", "name": "Seine-et-Marne"},
            {"@type": "AdministrativeArea", "name": "Bourgogne-Franche-Comté"},
        ],
        "knowsAbout": [
            "tourisme fluvial", "haltes fluviales", "balade en bateau", "gîte nautique",
            "convoyage de bateau", "renflouement de bateau", "découpe de bateau",
            "report modal fluvial", "transport fluvial de marchandises", "logistique fluviale",
            "Seine", "Marne", "canaux parisiens", "Canal de Bourgogne", "VNF",
        ],
    }
    if not est_marqueur(cfg.get("email_contact")):
        org["email"] = cfg["email_contact"]
    if not est_marqueur(cfg.get("telephone_international")):
        org["telephone"] = cfg["telephone_international"]
    adr = cfg.get("adresse") or {}
    if adr.get("ville"):
        champs = {"streetAddress": adr.get("rue"), "postalCode": adr.get("code_postal"),
                  "addressLocality": adr.get("ville"), "addressRegion": adr.get("region"),
                  "addressCountry": adr.get("pays", "FR")}
        org["address"] = dict({"@type": "PostalAddress"}, **{k: v for k, v in champs.items() if v})
    if cfg.get("liens_officiels"):
        org["sameAs"] = cfg["liens_officiels"]

    personne = {
        "@type": "Person",
        "@id": person_id,
        "name": "Joël Le Mercier",
        "jobTitle": "Président et fondateur de RivesEnRêves ; gestionnaire, maître de port et commandant de bord",
        "worksFor": {"@id": org_id},
        "url": base + "a-propos/#joel-le-mercier",
        "image": base + "assets/img/photos/portrait-joel-le-mercier.webp",
        "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": n} for n in (
            "Permis fluvial", "Permis mer côtier", "Extension grande plaisance",
            "Certificat restreint de radiotéléphoniste (CRR) maritime et fluvial",
            "Attestation spéciale passagers", "PSC1")],
        "knowsAbout": ["tourisme fluvial", "haltes fluviales", "navigation fluviale", "convoyage de bateaux", "règlements de police de la navigation",
                       "logistique fluviale", "report modal", "travaux sur bateaux"],
        "description": "Fondateur de RivesEnRêves, créateur et exploitant de 4 haltes fluviales sur la Marne de 2019 à 2025 en collaboration avec Coulommiers Pays de Brie Tourisme, conseiller en logistique fluviale et en développement du tourisme fluvial.",
    }
    if cfg.get("linkedin_joel"):
        personne["sameAs"] = [cfg["linkedin_joel"]]

    if page["url"] == "" or page["url"].startswith("a-propos"):
        graph += [org, personne]
        if page["url"] == "":
            graph.append({"@type": "WebSite", "@id": base + "#site", "url": base,
                          "name": "RivesEnRêves", "inLanguage": "fr-FR",
                          "publisher": {"@id": org_id}})
    else:
        graph.append({"@type": "Organization", "@id": org_id, "name": "RivesEnRêves", "url": base})

    if meta.get("type") == "article":
        art = meta["article"]
        graph.append({
            "@type": "Article", "@id": url + "#article",
            "headline": meta["h1"], "description": meta["description"],
            "datePublished": art["datePublished"], "dateModified": art["dateModified"],
            "author": {"@type": "Person", "@id": person_id, "name": "Joël Le Mercier"},
            "publisher": {"@id": org_id},
            "mainEntityOfPage": url, "inLanguage": "fr-FR",
            "image": base + "assets/img/og-rivesenreves.jpg",
            "about": art.get("about", []),
        })
    else:
        graph.append({"@type": meta.get("schema_page", "WebPage"), "@id": url + "#page",
                      "url": url, "name": meta["title"], "description": meta["description"],
                      "inLanguage": "fr-FR", "isPartOf": {"@id": base + "#site"},
                      "about": {"@id": org_id},
                      "dateModified": cfg.get("date_mise_a_jour_site")})

    for s in meta.get("services", []):
        node = {
            "@type": "Service",
            "name": s["name"],
            "serviceType": s.get("type", s["name"]),
            "description": s["description"],
            "provider": {"@id": org_id},
            "audience": {"@type": "Audience", "audienceType": s["audience"]},
            "areaServed": [{"@type": "Place", "name": n} for n in (
                [s["zone"]] if s.get("zone") else ZONE_LIEUX)],
            "url": url,
        }
        graph.append(node)

    if meta.get("faq"):
        graph.append({
            "@type": "FAQPage", "@id": url + "#faq",
            "mainEntity": [{
                "@type": "Question", "name": q["q"],
                "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", q["a"])},
            } for q in meta["faq"]],
        })

    if ariane:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                 "item": base + u} for i, (n, u) in enumerate(ariane)],
        })

    data = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")


# ---------------------------------------------------------------------------
# Assemblage d'une page
# ---------------------------------------------------------------------------
TOKEN_IMG = re.compile(r"\{\{img\s+(.*?)\}\}", re.S)
TOKEN_ART = re.compile(r"\{\{articles(?:\s+univers=\"(\w+)\")?\}\}")
TOKEN_FAIT = re.compile(r"\{\{fait:([\w-]+)\}\}")


def rendre_corps(page, pages, cfg):
    c = page["corps"]
    c = TOKEN_IMG.sub(lambda m: rendre_img(parse_attrs(m.group(1)), page), c)
    c = TOKEN_ART.sub(lambda m: bloc_articles(pages, page, m.group(1)), c)
    c = TOKEN_FAIT.sub(lambda m: FAITS[m.group(1)], c)
    c = c.replace("{{faq}}", bloc_faq(page["meta"]))
    c = c.replace("{{autres-univers}}", bloc_autres_univers(page))
    c = c.replace("{{definition}}", DEFINITION)
    c = c.replace("{{zone}}", ZONE)
    if page["meta"].get("type") == "article":
        c = c.replace("{{article-meta}}", bloc_article_meta(page))
    c = c.replace("{{root}}", page["root"])
    return c


IMG_DIR = STATIC / "assets" / "img"


def rendre_logo(page):
    """Logo officiel s'il a été déposé (assets/img/logo-officiel.svg/.png/.webp),
    sinon emblème provisoire + nom « Rives en Rêves » aux couleurs du logo."""
    for ext in ("svg", "webp", "png"):
        if (IMG_DIR / ("logo-officiel." + ext)).exists():
            return ('<img class="brand-logo-full" src="%sassets/img/logo-officiel.%s" '
                    'alt="RivesEnRêves" width="747" height="243">' % (page["root"], ext))
    return ('<img src="%sassets/img/logo-rivesenreves.svg" alt="" width="40" height="40">'
            '<span class="brand-name"><span class="b1">Rives</span><span class="b2">en</span>'
            '<span class="b3">Rêves</span></span>' % page["root"])


def construire():
    cfg = charger_config()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    gabarit = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    pages = lire_pages()
    index = {p["url"]: p for p in pages}

    for page in pages:
        meta = page["meta"]
        corps = rendre_corps(page, pages, cfg)
        ariane_html, ariane = rendre_ariane(page, index)
        canon = cfg["base_url"] + page["url"]
        univers = meta.get("univers") or "none"
        robots = "noindex, follow" if meta.get("noindex") else \
            "index, follow, max-image-preview:large, max-snippet:-1"
        if APERCU:
            robots = "noindex, nofollow"
        valeurs = {
            "title": html.escape(meta["title"]),
            "description": html.escape(meta["description"], quote=True),
            "canonical": canon,
            "robots": robots,
            "og_type": "article" if meta.get("type") == "article" else "website",
            "og_image": cfg["base_url"] + "assets/img/og-rivesenreves.jpg",
            "jsonld": jsonld(page, cfg, ariane),
            "body_class": "u-%s page-%s" % (univers, (page["url"].strip("/").replace("/", "-") or "accueil")),
            "menu": rendre_menu(page),
            "barre_univers": rendre_barre_univers(page),
            "sous_nav": rendre_sous_nav(page, pages),
            "ariane": ariane_html,
            "contenu": corps,
            "root": page["root"],
            "annee": cfg.get("date_mise_a_jour_site", "2026")[:4],
            "logo": rendre_logo(page),
            "bandeau": ('<div class="apercu-bandeau" role="note">Aperçu de démonstration du futur site '
                        '<strong>rivesenreves.com</strong> · contenus et photos en cours de finalisation</div>'
                        if APERCU else ""),
        }
        sortie = gabarit
        for k, v in valeurs.items():
            sortie = sortie.replace("{{%s}}" % k, v)
        sortie = sortie.replace("{{root}}", page["root"])
        sortie = sortie.replace("{{zone}}", ZONE)
        sortie = remplacer_marqueurs(sortie, cfg)
        if "{{" in sortie:
            restant = re.findall(r"\{\{[^}]*\}\}", sortie)[:3]
            sys.exit("Jeton non remplacé dans %s : %s" % (page["fichier"], restant))
        dest = OUT / page["fichier"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(sortie, encoding="utf-8")

    # Fichiers statiques (CSS, JS, polices, images, robots.txt, llms.txt, .htaccess)
    TEXTE = {".css", ".js", ".txt", ".xml", ".svg", ".htaccess", ".json", ".webmanifest", ".md"}
    for f in STATIC.rglob("*"):
        if f.is_dir():
            continue
        rel = f.relative_to(STATIC)
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if f.suffix in TEXTE or f.name == ".htaccess":
            t = remplacer_marqueurs(f.read_text(encoding="utf-8"), cfg)
            if f.name == ".htaccess":
                t = htaccess(t, cfg)
            dest.write_text(t, encoding="utf-8")
        else:
            shutil.copy2(f, dest)

    if APERCU:
        # Version de démonstration : jamais indexée par les moteurs
        (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
        (OUT / ".nojekyll").write_text("", encoding="utf-8")
        (OUT / ".htaccess").unlink(missing_ok=True)

    # Images provisoires
    ph = OUT / "assets" / "img" / "a-remplacer"
    ph.mkdir(parents=True, exist_ok=True)
    for nom, d in PHOTOS_MANQUANTES.items():
        (ph / ("%s.svg" % nom)).write_text(svg_provisoire(nom, d["hint"], d["w"], d["h"]), encoding="utf-8")

    # sitemap.xml
    lignes = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        if p["meta"].get("noindex") or p["url"] == "404.html":
            continue
        lastmod = p["meta"].get("article", {}).get("dateModified") or cfg.get("date_mise_a_jour_site")
        lignes.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>"
                      % (cfg["base_url"], p["url"], lastmod))
    lignes.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(lignes) + "\n", encoding="utf-8")

    # Liste des photos à fournir
    doc = ["# Photos à fournir", "",
           "Liste générée automatiquement par `build.py` : chaque emplacement ci-dessous affiche",
           "encore une image provisoire « PHOTO À REMPLACER ». Déposez la photo dans",
           "`src/static/assets/img/photos/` sous le nom indiqué (format `.webp` conseillé,",
           "`.avif`, `.jpg` ou `.png` acceptés), puis relancez `python3 build.py`.", "",
           "| Fichier attendu | Format conseillé (px) | Contenu suggéré | Pages |",
           "|---|---|---|---|"]
    for nom, d in sorted(PHOTOS_MANQUANTES.items()):
        doc.append("| `%s.webp` | %d × %d | %s | %s |" % (
            nom, d["w"], d["h"], d["hint"], ", ".join(sorted(d["pages"]))))
    if not PHOTOS_MANQUANTES:
        doc.append("| – | – | Toutes les photos sont en place. | – |")
    (ROOT / "docs" / "photos-a-fournir.md").write_text("\n".join(doc) + "\n", encoding="utf-8")

    print("Site généré dans public/ : %d pages, %d photos encore à fournir."
          % (len(pages), len(PHOTOS_MANQUANTES)))
    if est_marqueur(cfg["nom_de_domaine"]):
        print("Rappel : renseignez \"nom_de_domaine\" dans config.json avant la mise en ligne définitive.")


def htaccess(t, cfg):
    """Active les redirections HTTPS / domaine canonique selon config.json."""
    dom = cfg["nom_de_domaine"]
    regex = re.escape(dom)
    t = t.replace("[NOM_DE_DOMAINE_REGEX]", regex)
    if cfg.get("forcer_https") and not est_marqueur(dom):
        t = t.replace("# [HTTPS] ", "")
    if cfg.get("forcer_domaine_canonique") and not est_marqueur(dom):
        t = t.replace("# [CANONIQUE] ", "")
    return t


if __name__ == "__main__":
    os.chdir(ROOT)
    construire()

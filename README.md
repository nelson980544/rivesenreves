# Site internet RivesEnRêves

Site vitrine de **RivesEnRêves**, entreprise fluviale fondée par Joël Le Mercier.
Site statique léger (HTML, CSS, JavaScript, sans framework ni base de données) : il fonctionne sur n'importe quel hébergement web classique, dont **VICEM**.

Le site est découpé en **quatre univers**, un par public :

| Univers | Adresse | Public | Couleur |
|---|---|---|---|
| Balades | `/balades-bateau/` | Particuliers | vert (logo) |
| Plaisanciers | `/plaisanciers/` | Propriétaires de bateaux | bleu (logo) |
| Professionnels | `/professionnels/` | Entreprises, ports, chantiers | bleu profond |
| Administrations | `/administrations/` | Collectivités, établissements publics | anthracite |

---

## Sommaire

1. [Organisation des fichiers](#1-organisation-des-fichiers)
2. [Modifier le site (textes, images, coordonnées)](#2-modifier-le-site)
3. [Formulaire de contact (gratuit, réception par e-mail)](#3-formulaire-de-contact)
4. [Mise en ligne pas à pas : GitHub → VICEM → nom de domaine → HTTPS](#4-mise-en-ligne-pas-à-pas)
5. [Référencement après la mise en ligne](#5-référencement-après-la-mise-en-ligne)
6. [Documents annexes](#6-documents-annexes)

---

## 1. Organisation des fichiers

```
rivesenreves/
├── config.json            ← LE fichier de configuration (domaine, e-mail, téléphone…)
├── build.py               ← génère le site (python3 build.py)
├── src/
│   ├── templates/base.html    ← en-tête, menus, pied de page, balises SEO communes
│   ├── pages/                 ← UNE page = UN fichier index.html (textes du site)
│   │   ├── index.html                     (accueil)
│   │   ├── balades-bateau/…               (univers 1)
│   │   ├── plaisanciers/…                 (univers 2)
│   │   ├── professionnels/…               (univers 3)
│   │   ├── administrations/…              (univers 4)
│   │   ├── a-propos/, references/, blog/, contact/…
│   │   └── 404.html
│   └── static/                ← copié tel quel dans le site
│       ├── .htaccess, robots.txt, llms.txt
│       └── assets/ (css, js, polices, images, photos/)
├── public/                ← LE SITE GÉNÉRÉ, prêt à déposer chez VICEM (ne pas modifier à la main)
├── docs/                  ← checklists et listes d'éléments à fournir
└── .github/workflows/deploy.yml   ← déploiement automatique (facultatif)
```

**Principe :** on modifie `config.json` et les fichiers de `src/`, puis on lance `python3 build.py`, qui reconstruit `public/`. C'est le contenu de `public/` qui est mis en ligne.

Pourquoi un générateur ? Pour que l'en-tête, les menus, le pied de page, le sitemap, les données structurées et toutes les adresses absolues (domaine) soient produits **automatiquement et sans erreur** sur les 27 pages. Python 3 est déjà installé sur macOS et Linux ; sous Windows, installez-le depuis [python.org](https://www.python.org/downloads/) (aucun module supplémentaire n'est nécessaire).

## 2. Modifier le site

### 2.1 Coordonnées, domaine, e-mail : `config.json`

Ouvrez `config.json` avec un éditeur de texte et remplacez les valeurs entre crochets :

| Clé | Exemple | Effet |
|---|---|---|
| `nom_de_domaine` | `www.rivesenreves.fr` | URL canoniques, sitemap, robots.txt, llms.txt, Open Graph, JSON-LD |
| `email_reception_formulaire` | `contact@rivesenreves.fr` | adresse qui reçoit les messages du formulaire |
| `email_contact` | `contact@rivesenreves.fr` | adresse affichée sur le site |
| `telephone` / `telephone_international` | `06 12 34 56 78` / `+33612345678` | téléphone affiché / liens « appeler » |
| `adresse` | rue, code postal, ville | données structurées (SEO local) |
| `liens_officiels` | `["https://www.linkedin.com/company/…"]` | liens `sameAs` (LinkedIn, Google Business Profile…) |
| `forcer_https`, `forcer_domaine_canonique` | `true` / `false` | redirections dans `.htaccess` (voir § 4.4) |
| `date_mise_a_jour_site` | `2026-10-08` | date affichée dans le sitemap et les pages légales |

Puis : `python3 build.py`.

> Le marqueur `[NOM_DE_DOMAINE]` n'est écrit **qu'à un seul endroit** : `config.json`. Tant qu'il n'est pas renseigné, le site fonctionne (tous les liens internes sont relatifs), seules les adresses absolues du référencement contiennent le marqueur.

### 2.2 Les textes

Chaque page est un fichier `src/pages/…/index.html`. Il commence par un bloc de métadonnées (entre `<!--` et `-->`) :

```json
{
  "title": "Titre affiché dans Google (≈ 60 caractères)",
  "description": "Description affichée dans Google (≈ 155 caractères)",
  "label": "Nom court (fil d'Ariane, sous-menu)",
  "univers": "plaisanciers",
  "faq": [ {"q": "Question ?", "a": "Réponse."} ]
}
```

- Le **contenu** se modifie directement en HTML sous ce bloc.
- La **FAQ** se modifie dans `"faq"` : elle est affichée sur la page **et** balisée automatiquement en données structurées `FAQPage`.
- `"services"` alimente les données structurées `Service`.
- Les **marqueurs `[À COMPLÉTER : …]`** (surlignés en jaune sur le site) signalent les informations à fournir : cherchez « À COMPLÉTER » dans `src/` pour tous les retrouver.

Jetons utiles dans les textes : `{{root}}` (lien vers la racine du site), `{{fait:haltes}}` et les autres affirmations clés, `{{definition}}` (phrase de définition de l'entreprise). Ces affirmations sont définies **une seule fois**, en haut de `build.py` (`DEFINITION` et `FAITS`), pour rester identiques sur tout le site (important pour les moteurs d'IA).

### 2.3 Les photos

Chaque emplacement de photo affiche pour l'instant une image provisoire « PHOTO À REMPLACER » qui indique le **nom de fichier attendu**. La liste complète (51 emplacements, avec dimensions conseillées et pages concernées) est générée dans [`docs/photos-a-fournir.md`](docs/photos-a-fournir.md).

Pour remplacer une photo :

1. Préparez l'image aux dimensions conseillées, au format **WebP** (qualité 75-80, poids < 250 Ko ; outils gratuits : [Squoosh](https://squoosh.app)). AVIF, JPG et PNG sont aussi acceptés.
2. Nommez-la exactement comme indiqué, ex. `erna-hero.webp`.
3. Déposez-la dans `src/static/assets/img/photos/`.
4. Lancez `python3 build.py` : la page utilise automatiquement la vraie photo.

Le texte alternatif (attribut `alt`, important pour l'accessibilité et le SEO) se modifie dans la page, dans le jeton `{{img name="…" alt="…"}}`.

### 2.4 Logo et couleurs

Les couleurs reprennent celles du logo : vert anis `#90c03c`, bleu `#0093d3`, bleu soutenu `#1878a8` et anthracite. Elles sont définies en tête de `src/static/assets/css/style.css` (`--logo-green`, `--logo-sky`, `--logo-blue`, `--logo-grey`), avec une teinte par univers : vert pour Balades, bleu pour Plaisanciers, bleu profond pour Professionnels, anthracite pour Administrations.

Le logo affiché est `src/static/assets/img/logo-officiel.webp` (en-tête, pied de page, données structurées). Pour le remplacer par une version haute définition, déposez `logo-officiel.svg` au même endroit (prioritaire sur le .webp), puis lancez `python3 build.py`. Remplacez aussi `favicon.svg` et `apple-touch-icon.png` par l'emblème seul.

### 2.5 Ajouter un article de blog

Copiez un dossier de `src/pages/blog/` (ex. `etude-report-modal-financee-vnf/`), renommez-le (adresse courte, sans accents), puis adaptez les métadonnées (`h1`, `univers`, `article.datePublished`, `article.dateModified`, `faq`) et le contenu. L'article apparaît automatiquement sur la page Blog, dans l'univers correspondant et dans le sitemap. **Mettez à jour `dateModified`** à chaque modification : la date est affichée sur l'article.

Ajoutez aussi l'article dans `src/static/llms.txt`.

### 2.6 Voir le site sur son ordinateur

```bash
python3 build.py
cd public && python3 -m http.server 8000
```

Puis ouvrez <http://localhost:8000>.

## 3. Formulaire de contact

Le formulaire (`/contact/`) envoie les messages **directement par e-mail**, gratuitement, sans serveur à gérer.

- **Service par défaut : [FormSubmit](https://formsubmit.co)** (gratuit, sans compte). Il suffit de renseigner `email_reception_formulaire` dans `config.json`.
- **Alternative : [Web3Forms](https://web3forms.com)** (gratuit, 250 messages/mois). Créez une clé d'accès sur leur site avec votre adresse e-mail, puis collez-la dans `web3forms_access_key` de `config.json`. Si cette clé est renseignée, elle est utilisée à la place de FormSubmit.

La configuration est reprise en haut de `src/static/assets/js/contact.js` (variable `CONTACT_CONFIG`, marqueur `[ADRESSE_EMAIL_DE_RECEPTION]`).

Fonctionnement :

- **Champ « Vous êtes… »** à quatre choix (particulier, plaisancier, professionnel, administration), **présélectionné** selon la page d'origine grâce au paramètre d'URL `?profil=plaisancier` (et `&objet=etude-vnf`, `convoyage`, `renflouement`, `decoupe`, `logistique`, `erna`, `intervention`).
- **Objet de l'e-mail reçu** : `[Plaisancier] Nouvelle demande de contact`, `[Professionnel] …`, `[Administration] …`, `[Balade] …`.
- **Champs complémentaires** selon le profil : offre et date (particulier), type de bateau et trajet (plaisancier), marchandises transportées et trajets actuels (professionnel), collectivité et fonction (administration).
- **Anti-spam** : champ piège invisible (honeypot `_honey`). FormSubmit propose en plus un captcha : remplacez `value="false"` par `value="true"` dans le champ `_captcha` de `src/pages/contact/index.html` si le spam devient gênant.
- Message de confirmation, gestion des erreurs, mention RGPD. Sans JavaScript, le formulaire fonctionne aussi (envoi classique puis page `/contact/merci/`).

**Activation (FormSubmit) :** le tout premier message envoyé déclenche un e-mail de confirmation de FormSubmit à l'adresse de réception : cliquez sur le lien d'activation. FormSubmit vous propose ensuite un **identifiant aléatoire** à utiliser à la place de l'adresse e-mail (recommandé pour éviter que l'adresse soit visible dans le code) : collez-le dans `email_reception_formulaire` puis relancez `python3 build.py`.

**À tester sur le domaine définitif** une fois en ligne (voir § 4.6).

## 4. Mise en ligne pas à pas

### 4.1 Créer le dépôt GitHub

1. Créez un compte sur [github.com](https://github.com) (si besoin), puis **New repository** : nom `rivesenreves`, visibilité **Private** conseillée, sans README (il existe déjà).
2. Sur votre ordinateur, dans le dossier du site :
   ```bash
   git init -b main
   git add .
   git commit -m "Première version du site RivesEnRêves"
   git remote add origin https://github.com/VOTRE-COMPTE/rivesenreves.git
   git push -u origin main
   ```
3. Ensuite, à chaque modification : `python3 build.py`, puis `git add .`, `git commit -m "…"`, `git push`.

Le dépôt GitHub est la **source unique** du site et en garde tout l'historique.

### 4.2 Premier déploiement chez VICEM (dépôt manuel)

1. Dans l'espace client VICEM, ouvrez l'hébergement web et notez les **accès FTP/SFTP** (serveur, identifiant, mot de passe) et le **dossier web** (souvent `www/` ou `public_html/`).
2. Lancez `python3 build.py`.
3. Avec un logiciel FTP gratuit ([FileZilla](https://filezilla-project.org)) ou le gestionnaire de fichiers du panneau VICEM, **envoyez tout le contenu du dossier `public/`** (pas le dossier lui-même) dans le dossier web. Vérifiez que le fichier caché `.htaccess` est bien envoyé (FileZilla : menu *Serveur > Forcer l'affichage des fichiers cachés*).
4. Ouvrez l'adresse provisoire fournie par VICEM : le site doit s'afficher à l'identique.

### 4.3 Déploiement automatique depuis GitHub (facultatif)

Le fichier `.github/workflows/deploy.yml` régénère le site et l'envoie chez VICEM à chaque `git push` sur `main`.

1. Sur GitHub : **Settings > Secrets and variables > Actions > New repository secret**, créez :
   | Secret | Valeur |
   |---|---|
   | `FTP_HOST` | serveur FTP/SFTP fourni par VICEM |
   | `FTP_USER` | identifiant |
   | `FTP_PASSWORD` | mot de passe |
   | `FTP_PROTOCOL` | `sftp` si VICEM le propose, sinon `ftp` |
   | `FTP_REMOTE_DIR` | dossier web, ex. `/www` |
2. Faites un `git push` : suivez le déploiement dans l'onglet **Actions**.

Les identifiants restent dans les secrets GitHub, **jamais dans le code**. Sans secrets, le workflow s'arrête proprement sans rien envoyer. Par prudence, il n'efface pas les fichiers distants : supprimez à la main un fichier retiré du site.

### 4.4 Rattacher le nom de domaine

Le nom de domaine est déjà détenu chez VICEM.

1. Dans l'espace client VICEM, associez le domaine (et sa variante `www`) à l'hébergement web (zone DNS : enregistrements `A`/`AAAA` ou `CNAME` vers l'hébergement, selon la procédure VICEM).
2. Choisissez **une seule version** de l'adresse, avec ou sans `www` (ex. `www.rivesenreves.fr`).
3. Dans `config.json`, renseignez `"nom_de_domaine": "www.rivesenreves.fr"`, puis `python3 build.py` et redéployez.

### 4.5 Activer le HTTPS

1. Dans le panneau VICEM, activez le **certificat SSL** (souvent Let's Encrypt, gratuit) pour le domaine **et** sa variante avec/sans `www`.
2. Vérifiez que `https://votre-domaine` s'affiche avec le cadenas.
3. Seulement alors, dans `config.json`, passez `"forcer_https": true` et `"forcer_domaine_canonique": true`, puis `python3 build.py` et redéployez. Le fichier `.htaccess` redirige alors :
   - `http://` → `https://` (et active l'en-tête HSTS) ;
   - toute autre adresse (sans `www`, adresse provisoire) → l'adresse unique choisie.

> ⚠️ N'activez pas ces deux options avant que le certificat soit actif : le site deviendrait inaccessible.

Le `.htaccess` gère aussi la **page 404 personnalisée**, la **compression** et le **cache navigateur**. Si l'hébergement VICEM n'utilise pas Apache (Nginx seul), transmettez ces règles au support VICEM.

### 4.6 Tester le formulaire sur le domaine final

1. Ouvrez `https://votre-domaine/contact/`, envoyez un message test pour chaque profil.
2. FormSubmit : activez le formulaire via l'e-mail reçu (premier envoi). Web3Forms : si vous avez restreint les domaines autorisés dans votre tableau de bord, ajoutez le domaine définitif.
3. Vérifiez la réception, l'objet (`[Plaisancier] …`) et les champs.

### 4.7 Soumettre le site aux moteurs de recherche

1. **Google Search Console** ([search.google.com/search-console](https://search.google.com/search-console)) : ajoutez une propriété *Domaine*, validez-la par l'enregistrement DNS TXT proposé (dans la zone DNS VICEM), puis menu **Sitemaps** : soumettez `sitemap.xml`.
2. **Bing Webmaster Tools** ([bing.com/webmasters](https://www.bing.com/webmasters)) : importez directement le site depuis Search Console, puis soumettez `sitemap.xml`. Bing alimente aussi Copilot et une partie des réponses de ChatGPT.
3. Contrôlez les données structurées avec le [test des résultats enrichis](https://search.google.com/test/rich-results) et le [validateur Schema.org](https://validator.schema.org).

## 5. Référencement après la mise en ligne

Ce qui est déjà intégré au site :

- une page = une intention de recherche, un seul H1, titres hiérarchisés, URL courtes ;
- `title`, `meta description`, canonique, Open Graph et Twitter Card uniques par page ;
- données structurées JSON-LD : `Organization` + `LocalBusiness`, `Person` (Joël Le Mercier, `founder`), `Service` (avec public visé), `FAQPage`, `BreadcrumbList`, `Article`, `WebSite` ;
- réponse directe en tête de chaque page, FAQ sur chaque page d'univers et de service, affirmations chiffrées identiques partout (GEO) ;
- `sitemap.xml`, `robots.txt` (robots d'IA explicitement autorisés : GPTBot, ClaudeBot, PerplexityBot, Google-Extended…), `llms.txt` ;
- HTML lisible sans JavaScript, polices hébergées localement, images à chargement différé avec dimensions fixes (pas de décalage de mise en page).

À faire hors du site : voir [`docs/checklist-seo-geo-hors-site.md`](docs/checklist-seo-geo-hors-site.md).

## 6. Documents annexes

- [`docs/checklist-seo-geo-hors-site.md`](docs/checklist-seo-geo-hors-site.md) : actions SEO et GEO à mener après la mise en ligne.
- [`docs/elements-a-fournir.md`](docs/elements-a-fournir.md) : ce que RivesEnRêves doit fournir (photos, textes à valider, coordonnées, informations légales).
- [`docs/photos-a-fournir.md`](docs/photos-a-fournir.md) : liste détaillée des photos (générée automatiquement).

Crédits : polices [Fraunces](https://github.com/undercasetype/Fraunces) et [Source Sans 3](https://github.com/adobe-fonts/source-sans), licence SIL Open Font License (fichiers de licence dans `assets/fonts/`). Carte : © contributeurs OpenStreetMap.

# Éléments à fournir par RivesEnRêves

Tant que ces éléments ne sont pas fournis, le site affiche des marqueurs surlignés en jaune `[À COMPLÉTER : …]` ou des images « PHOTO À REMPLACER ». Pour retrouver tous les marqueurs : rechercher « À COMPLÉTER » et « À VALIDER » dans le dossier `src/`.

## 1. Configuration technique (`config.json`)

- [ ] Nom de domaine définitif, avec ou sans `www` → `nom_de_domaine`
- [ ] Adresse e-mail de réception des messages du formulaire → `email_reception_formulaire`
- [ ] Adresse e-mail affichée sur le site → `email_contact`
- [ ] Téléphone (format affiché et format international) → `telephone`, `telephone_international`
- [ ] Adresse postale publique (identique à Google Business Profile) → `adresse`
- [ ] URL des profils officiels : LinkedIn entreprise, LinkedIn de Joël Le Mercier, Google Business Profile, Facebook, Instagram → `liens_officiels`, `linkedin_joel`
- [ ] Accès FTP/SFTP VICEM (à saisir uniquement dans les secrets GitHub, jamais dans un fichier)

## 2. Informations légales (pages Mentions légales et Confidentialité)

- [ ] Raison sociale, forme juridique, capital
- [ ] Adresse du siège social
- [ ] SIRET, RCS, n° de TVA intracommunautaire
- [ ] Coordonnées complètes de l'hébergeur VICEM (raison sociale, adresse, téléphone)
- [ ] Service de formulaire retenu (FormSubmit ou Web3Forms)
- [ ] Durée de conservation des demandes de contact (ex. 3 ans)

## 3. Textes à compléter ou à valider

### À propos et Joël Le Mercier
- [ ] Année de création de RivesEnRêves
- [ ] Parcours antérieur, formation, qualifications et titres de navigation de Joël Le Mercier
- [ ] Citation personnelle de Joël Le Mercier
- [ ] Anecdotes marquantes (création d'une halte, une intervention mémorable…)
- [ ] Noms et localisation des 2 haltes situées hors de La Ferté-sous-Jouarre
- [ ] Relecture et validation de la biographie rédigée

### Balades et gîte nautique
- [ ] Lieu(x) d'embarquement, durée, capacité, saison, horaires, tarifs, accessibilité (PMR, poussettes)
- [ ] Description du parcours type et des commentaires à bord
- [ ] Politique animaux, âge minimum, gilets enfants, conditions d'annulation et de report météo
- [ ] Gîte nautique : lieu d'amarrage, couchages, équipements (chauffage, cuisine, sanitaires, linge), horaires d'arrivée/départ, période d'ouverture, tarifs, bons cadeaux
- [ ] Avis clients réels (3 minimum, avec accord)

### Plaisanciers
- [ ] Renflouement : lieu et date de l'opération de référence, photos avant/après
- [ ] Découpe : exemples d'opérations réalisées (type de bateau, lieu) et photos
- [ ] Validation du déroulé du convoyage et de la liste des démarches prises en charge

### Professionnels
- [ ] Validation de la formulation « études de report modal financées par VNF » (sans conditions chiffrées, comme prévu)
- [ ] Mission de conseil en logistique pour VNF : objet et période, si leur diffusion est autorisée
- [ ] ERNA : photos (aucune caractéristique chiffrée ne sera publiée)
- [ ] Délai d'intervention habituel pour les interventions techniques
- [ ] Validation de la mention de la convention HAROPA (site de Fublaines)

### Administrations
- [ ] Nom officiel exact de la « Communauté de communes de Pouilly-Bligny » à utiliser partout
- [ ] Étude de cas : année, périmètre exact de la mission (marqué « À VALIDER »), usage du bateau, fréquentation ou retombées
- [ ] Accord de la collectivité pour être citée, et si possible un témoignage d'élu ou de technicien

## 4. Photos

51 emplacements, listés avec dimensions et pages dans [`photos-a-fournir.md`](photos-a-fournir.md). Prioritaires :

1. `accueil-hero` : grande photo d'ambiance de la Marne
2. `porte-balades`, `porte-plaisanciers`, `porte-professionnels`, `porte-administrations` : les 4 portes de l'accueil
3. `portrait-joel-le-mercier` : portrait du fondateur
4. `erna-hero` : le pousseur ERNA
5. `renflouement-avant` / `renflouement-apres` : référence technique
6. `site-fublaines`, `halte-ferte-sous-jouarre`, `pouilly-bligny-bateau`

Conseils : photos horizontales (sauf portrait), lumière naturelle, personnes ayant donné leur accord, droits d'utilisation détenus par RivesEnRêves. Format WebP, < 250 Ko.

## 5. Logo

Les couleurs du site sont déjà alignées sur le logo (vert anis `#8cc63f`, bleu ciel `#29a3da`, bleu `#1d71b8`, anthracite `#3c3c3b`). En attendant le fichier original, l'en-tête affiche un emblème redessiné d'après le logo, suivi du nom « Rives en Rêves » en trois couleurs.

- [ ] **Fichier original du logo complet** (SVG idéalement, sinon PNG fond transparent, au moins 600 px de large) : le déposer sous le nom `src/static/assets/img/logo-officiel.svg` (ou `.png` / `.webp`), puis `python3 build.py`. Il remplace automatiquement l'emblème et le nom dans l'en-tête et le pied de page.
- [ ] **Emblème seul** (cercle maison / arbres / vagues), carré : remplacera `logo-rivesenreves.svg`, `favicon.svg` et `apple-touch-icon.png` (180 × 180 px).
- [ ] Codes couleur exacts de la charte, s'ils existent, pour ajuster les teintes.

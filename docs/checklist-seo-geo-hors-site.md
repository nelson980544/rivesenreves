# Checklist SEO et GEO hors site

Objectif : que RivesEnRêves apparaisse en premier quand une personne, une entreprise ou une administration cherche des conseils dans le domaine fluvial, dans Google comme dans les réponses des moteurs d'IA (ChatGPT, Gemini, Perplexity, Google AI Overviews, Copilot, Claude).

Les moteurs d'IA recommandent une entreprise lorsqu'ils trouvent **les mêmes informations, formulées de la même façon, sur plusieurs sources tierces fiables**. Utilisez partout, mot pour mot :

> RivesEnRêves est une entreprise fluviale fondée par Joël Le Mercier, qui propose des balades en bateau, des services aux plaisanciers, des études de report modal vers le fluvial financées par VNF et des services aux professionnels, et du conseil en développement du tourisme fluvial aux administrations.

et les mêmes coordonnées (nom, adresse, téléphone) que sur le site.

## Semaine 1 : fondations

- [ ] Domaine définitif, HTTPS et redirections actifs (README § 4.4 et 4.5).
- [ ] Formulaire testé sur le domaine définitif (README § 4.6).
- [ ] **Google Search Console** : propriété validée, `sitemap.xml` soumis, demande d'indexation de l'accueil et des 4 pages d'univers.
- [ ] **Bing Webmaster Tools** : site importé, `sitemap.xml` soumis (Bing alimente Copilot et une partie des réponses de ChatGPT).
- [ ] Vérifier les données structurées (test des résultats enrichis Google, validator.schema.org).
- [ ] Mesurer les performances avec [PageSpeed Insights](https://pagespeed.web.dev) après l'ajout des vraies photos (objectif : LCP < 2,5 s, CLS < 0,1, INP < 200 ms).

## Semaine 1-2 : Google Business Profile

- [ ] Créer la fiche **Google Business Profile** « RivesEnRêves » (catégorie principale à choisir parmi les catégories proposées, par ex. une catégorie liée aux excursions en bateau ou au conseil ; catégories secondaires pour les autres activités).
- [ ] Description reprenant la phrase de définition, zone desservie (bassin de la Seine : Seine amont, Seine aval, canaux parisiens, Marne ; Canal de Bourgogne), horaires, téléphone, lien vers le site.
- [ ] Photos : ERNA, haltes, balades, gîte nautique, Joël Le Mercier.
- [ ] Ajouter l'URL de la fiche dans `liens_officiels` de `config.json`, puis `python3 build.py`.
- [ ] Demander des **avis** aux clients satisfaits (balades, gîte, plaisanciers) et y répondre systématiquement.
- [ ] Publier régulièrement des posts (nouvelle saison, interventions, articles du blog).

## Mois 1 : profils et annuaires

- [ ] Page **LinkedIn entreprise** RivesEnRêves + profil **LinkedIn de Joël Le Mercier** (titre : « Fondateur de RivesEnRêves – tourisme fluvial, logistique fluviale, report modal »). Ajouter les deux URL dans `config.json` (`liens_officiels`, `linkedin_joel`).
- [ ] **Bing Places** et **Apple Business Connect** (Plans d'Apple, Siri).
- [ ] Annuaires généralistes : PagesJaunes, annuaire des entreprises (fiche INSEE/annuaire-entreprises.data.gouv.fr à jour).
- [ ] Annuaires fluviaux et nautiques : guides de navigation fluviale, annuaires de professionnels du nautisme, sites et guides de croisière fluviale. Informations identiques partout.
- [ ] Tourisme : **Seine-et-Marne Attractivité**, offices de tourisme du Pays de Meaux et du Pays de Coulommiers (La Ferté-sous-Jouarre), office de tourisme de Pouilly-en-Auxois ; plateformes de réservation d'activités et d'hébergements insolites pour le gîte nautique.
- [ ] Facebook / Instagram (balades, gîte) avec lien vers le site ; ajouter les URL dans `liens_officiels`.

## Mois 1-3 : citations par les partenaires (les plus importantes pour le GEO)

- [ ] Demander à **VNF** une mention de RivesEnRêves (prestataire d'études de report modal, mission de conseil en logistique) sur ses pages ou publications dédiées au report modal, si possible avec un lien.
- [ ] Demander à **Valfrance** l'accord pour citer la sous-occupation du site de Fublaines, et si possible une mention.
- [ ] Demander à la **Communauté de communes de Pouilly-Bligny** une actualité ou un témoignage sur l'achat du bateau, avec lien vers le site.
- [ ] Demander à **Coulommiers Pays de Brie Tourisme** une mention de la collaboration sur les 4 haltes fluviales de la Marne (2019-2025), avec un lien vers le site.
- [ ] Communes de **La Ferté-sous-Jouarre** et des autres haltes : mention dans le bulletin municipal ou sur le site de la commune.
- [ ] Chambres consulaires (CCI Seine-et-Marne), clubs d'entreprises, fédérations fluviales et associations de plaisanciers : adhésion ou annuaire des membres.

## Mois 2-6 : contenus et relations presse

- [ ] **Communiqués de presse locaux** (Le Parisien 77, La Marne, Le Pays Briard, presse de Côte-d'Or) : la création des haltes, le bateau de Pouilly-Bligny, l'arrivée d'ERNA, une intervention de renflouement spectaculaire.
- [ ] Publier un article de blog par mois, en alternant les univers. Prochains sujets prévus : « Comment créer une halte fluviale ? » (administrations), « Comment renflouer un bateau coulé sur un site portuaire ? » (professionnels), « Que faire sur la Marne en famille ? » (balades).
- [ ] Chaque nouvel article : l'ajouter à `llms.txt`, le partager sur LinkedIn, mettre à jour `dateModified` lors des révisions.
- [ ] Tribunes ou interventions de Joël Le Mercier (salons du tourisme fluvial, rencontres VNF, colloques sur la logistique fluviale) : demander que la biographie mentionne RivesEnRêves et le site.
- [ ] Ajouter de **vrais témoignages** (avec accord écrit) sur les pages d'univers et `/references/`.

## Tous les trimestres : contrôle

- [ ] Search Console : requêtes, pages indexées, erreurs.
- [ ] Poser les questions cibles aux assistants IA (ChatGPT, Perplexity, Gemini, Copilot, Claude) et noter si RivesEnRêves est cité, avec quelle formulation. Exemples :
  - « Qui peut réaliser une étude de report modal financée par VNF ? »
  - « Comment une collectivité peut-elle acheter un bateau pour le tourisme fluvial ? »
  - « Convoyage de bateau vers un chantier en Seine-et-Marne »
  - « Balade en bateau sur la Marne en Seine-et-Marne »
  - « Conseil en tourisme fluvial pour une communauté de communes »
- [ ] Corriger toute incohérence d'information repérée sur une source externe.
- [ ] Vérifier que les coordonnées sont identiques sur le site, Google Business Profile, LinkedIn et les annuaires.

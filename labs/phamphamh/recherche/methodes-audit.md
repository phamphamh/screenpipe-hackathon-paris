# Les méthodes d'audit des grands cabinets, et nos 5 « méthodes » produit

Recherche du 17/10/2026, pour l'étape « le client choisit une méthodologie d'audit ».
Suite de `audits-ia.md` (même dossier), qui couvre déjà les chiffres d'adoption de l'IA et le task mining. Ici : **comment chaque cabinet raisonne, ce qu'il livre et à quoi ressemblent ses visuels**.

Le résultat machine est dans `methodes.json` (5 méthodes, schéma fixé).

**Statuts** (mêmes règles que `audits-ia.md`) :
- **[vérifié]** : lu sur la source primaire (site ou PDF du cabinet, de l'éditeur, de l'article).
- **[relayé]** : trouvé seulement dans des résumés, blogs ou extraits de recherche. À revérifier avant de le mettre sur une slide.
- **[vendeur]** : la source vend la prestation ou l'outil. Le contenu est réel, la méthode n'est pas auditée.
- **[déduit]** : mon raisonnement, pas une source.

**Règle de nommage** : aucune marque de cabinet ni nom déposé dans le nom de nos méthodes. Plusieurs noms sont des marques déposées (Results Delivery®, Founder's Mentality®, RAPID®, Net Promoter® chez Bain ; EY.ai Confidence Index chez EY). On les cite seulement dans la ligne « inspirée de ». [vérifié pour le ® sur les pages Bain ; le reste est une précaution]

---

## 0. En bref

1. Les cabinets vendent **une façon de raisonner** autant qu'un contenu. Chacun a un « geste » reconnaissable : McKinsey commence par la réponse et découpe en arbre ; BCG range dans une matrice 2×2 ; Bain met un chiffre, un responsable et une date ; les Big Four dressent une carte des risques et la liste des contrôles ; le Lean dessine le flux et chasse le gaspillage.
2. Ces gestes se transposent bien à nos données, car ils reposent tous sur **du temps, des étapes et des fréquences**. C'est ce que screenpipe mesure. [déduit]
3. Ce qu'aucun cabinet ne mesure, c'est **le travail réel à l'écran**. Ils partent d'entretiens, d'ateliers et de sondages (voir `audits-ia.md` § 1 et § 4). Le process mining et le task mining sont les seules méthodes qui partent des traces, et ce sont aussi les plus proches de nous.
4. Nos 5 méthodes : **Sommet** (McKinsey), **Frontière** (BCG et Accenture), **Résultat net** (Bain), **Garde-fou** (Big Four), **Gemba** (Toyota, Lean, Six Sigma, process mining).
5. Il manque **une dizaine de calculs** pour tout remplir (§ 9). Les plus utiles : heures par tâche et par semaine, coût par tâche, exposition IA de chaque tâche, part du temps à valeur ajoutée (PCE).

---

## 1. McKinsey

### La méthode réelle
- **Principe pyramidal (Barbara Minto)**. Le site officiel le résume ainsi : les idées sont faciles à saisir quand elles sont organisées en pyramide sous un point unique. L'introduction suit le schéma **Situation, Complication, Question** pour trouver la question que se pose le lecteur. Le livre est présenté comme un manuel utilisé par tous les grands cabinets. [vérifié] [barbaraminto.com](https://www.barbaraminto.com/)
  - La version **SCQA** ajoute la Réponse, souvent placée en premier (« la réponse d'abord »). [relayé] [ModelThinkers](https://modelthinkers.com/mental-model/minto-pyramid-scqa), [Management Consulted](https://managementconsulted.com/scqa-framework/)
  - Minto, ancienne de McKinsey, est aussi créditée du principe **MECE** (mutuellement exclusif, collectivement exhaustif : pas de doublon, pas de trou). La date (années 1960) varie selon les sources. [relayé] [MBA Crystal Ball](https://www.mbacrystalball.com/blog/strategy/mece-framework/), [Wikipedia, Issue tree](https://en.wikipedia.org/wiki/Issue_tree)
- **Résolution de problème en 7 étapes** (Charles Conn et Robert McLean, *Bulletproof Problem Solving*, 2018). Dans le podcast McKinsey : étape 1 « définir le problème », étape 2 « découper le problème avec des arbres logiques » (exemple type : l'arbre de profit, prix × quantité moins coûts), étape 3 « prioriser » (quelle branche pèse le plus, et sur laquelle on peut agir). Les dernières étapes servent à **synthétiser en une histoire** qui répond à « que dois-je faire ? ». [vérifié] [transcription PDF du podcast McKinsey, 2019](https://cdn.ksrinc.com/mckinseysurvey/How-to-master-the-seven-step-problem-solving-process.pdf), [page McKinsey](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/how-to-master-the-seven-step-problem-solving-process)
  - La liste complète (définir, découper, prioriser, plan de travail, analyses, synthèse, communication) vient de résumés du livre. [relayé]
- **Approche par hypothèses** : on pose tôt une réponse probable, puis on la teste avec des données. Une bonne hypothèse est testable, discutable et utile pour décider. [relayé] [Crafting Cases](https://www.craftingcases.com/issue-tree-guide/), [Slideworks](https://slideworks.io/resources/mckinsey-problem-solving-process)
- **80/20** : ce n'est pas une invention McKinsey. Joseph Juran a formulé « le petit nombre vital et le grand nombre trivial » et l'a appelé principe de Pareto. Les cabinets s'en servent pour prioriser (étape 3). [relayé] [iSixSigma](https://www.isixsigma.com/dictionary/trivial-many/), [Juran](https://www.juran.com/about-us/dr-jurans-history)
- **Rewired** (Lamarre, Smaje, Zemmel ; Wiley, juin 2023 ; 2e édition avec d'autres auteurs). **Six capacités** : une feuille de route qui vise une vraie valeur, un vivier de talents, un modèle opérationnel qui permet d'aller vite, une technologie distribuée et flexible, des données présentes partout, l'adoption et le passage à l'échelle. [vérifié] [Wiley, 2e édition](https://www.wiley.com/en-us/Rewired:+McKinsey's+Playbook+on+How+Leading+Companies+Win+with+Technology+and+AI,+2nd+Edition-p-9781394381913)
  - L'idée centrale est de refaire **un domaine entier** de bout en bout plutôt que d'empiler des pilotes. McKinsey dit s'appuyer sur plus de 200 grandes entreprises. [relayé] (extraits de la [page McKinsey](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/rewired-to-outcompete), qui ne s'est pas chargée)
- **Trois horizons** (Baghai, Coley, White, *The Alchemy of Growth*, 1999). Horizon 1 : défendre et étendre le cœur de métier. Horizon 2 : construire les activités émergentes. Horizon 3 : créer des options pour l'avenir. Les trois sont menés **en même temps**. [relayé] [page McKinsey « Enduring Ideas », 2009](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/enduring-ideas-the-three-horizons-of-growth) (la page ne s'est pas chargée, contenu vu en extrait)

### Le livrable type [déduit des sources ci-dessus]
1. Une page de synthèse : la réponse en une phrase, puis 3 arguments.
2. Chaque page porte un **titre-phrase** qui dit la conclusion (pas « Temps par catégorie » mais « Les réunions mangent un tiers de la semaine »).
3. Le corps : l'arbre du problème, les analyses, la priorisation.
4. La fin : le plan par horizons.

### Visuels signature
- **Arbre MECE** (arbre logique, arbre de profit).
- **Cascade (waterfall)**. Selon l'hommage de McKinsey à Gene Zelazny, son directeur de la communication visuelle et auteur de *Say It With Charts* (1985), certains graphiques comme la cascade « ont été inventés par McKinsey ». [relayé] [McKinsey Alumni](https://www.mckinsey.com/alumni/news-and-events/global-news/alumni-news/2023-05-remembering-gene-zelazny) (page en délai dépassé, vue en extrait)
- **Barres de Pareto** avec la courbe du cumul.
- **Frise des 3 horizons**.

### Ce qu'un dirigeant en retient [déduit]
« Je sais quoi faire en lisant une seule page, et je peux vérifier que rien n'a été oublié. »

---

## 2. BCG

### La méthode réelle
- **Matrice croissance / part de marché** (Bruce Henderson, essai *The Product Portfolio*, 1970). Axes : part de marché relative et croissance du marché. Les quatre cases : les « vaches à lait » financent le reste, les « étoiles » ont un fort potentiel, les « dilemmes » sont à financer ou abandonner, les « poids morts » (que BCG appelle *pets*) sont à vendre ou repositionner. À son pic, environ la moitié du Fortune 500 l'utilisait. BCG reconnaît aujourd'hui que la part de marché ne prédit plus la performance durable et qu'il faut un nouvel axe horizontal. [vérifié] [BCG, Classics Revisited, 2014](https://www.bcg.com/en-gb/publications/2014/growth-share-matrix-bcg-classics-revisited)
- **Règle 10/20/70 pour l'IA** : « 10 % des efforts sur les algorithmes, 20 % sur la technologie et les données, 70 % sur les personnes et les processus ». [vérifié] [BCG, Leader's Guide to Transforming with AI](https://www.bcg.com/featured-insights/the-leaders-guide-to-transforming-with-ai)
  - Un article BCG de 2026 inverse les deux premiers postes (10 % techno, 20 % données et algorithmes). Le 70 % ne change pas. [relayé] [BCG 2026](https://www.bcg.com/publications/2026/how-cios-can-prove-the-value-of-tech-in-the-age-of-ai)
- **Deploy, Reshape, Invent** : « déployer » la technologie pour des gains de productivité immédiats, « refondre » les fonctions critiques, « inventer » de nouveaux revenus. BCG dit que la refonte peut augmenter l'efficacité « jusqu'à 50 % ». [vérifié] [BCG, Leader's Guide](https://www.bcg.com/featured-insights/the-leaders-guide-to-transforming-with-ai)
  - Le chiffre de 10 à 15 % de productivité pour « déployer » vient d'une autre page BCG vue en extrait. [relayé] [BCG AI](https://www.bcg.com/capabilities/artificial-intelligence)
- **« Jagged frontier »** (HBS, BCG, Wharton, MIT, 2023, document de travail HBS 24-013). Expérience pré-enregistrée sur **758 consultants**, environ 7 % des consultants de BCG à ce niveau. Sur 18 tâches **dans** la frontière de l'IA : +12,2 % de tâches finies, 25,1 % plus rapide, qualité supérieure de plus de 40 %. Les moins bons gagnent 43 %, les meilleurs 17 %. Sur une tâche **hors** frontière : 19 points de moins de bonnes réponses. Deux façons de bien travailler avec l'IA : les « **centaures** » partagent les sous-tâches entre eux et l'IA, les « **cyborgs** » mêlent leur travail à l'IA en continu. [vérifié] [PDF du working paper, copie MIT Sloan](https://mitsloan.mit.edu/sites/default/files/2023-10/SSRN-id4573321.pdf)

### Le livrable type [déduit]
Un portefeuille d'initiatives rangé dans une matrice, puis une répartition de l'effort et un classement par niveau d'ambition (déployer, refondre, inventer).

### Visuels signature
- **Matrice 2×2** (le plus reconnaissable).
- **Barres 10/20/70**.
- **Frontière en dents de scie** : la même difficulté apparente, mais l'IA réussit d'un côté et échoue de l'autre.

### Ce qu'un dirigeant en retient [déduit]
« Je sais où investir et où ne pas mettre l'IA. Et l'essentiel de l'effort porte sur les gens, pas sur l'outil. »

---

## 3. Bain

### La méthode réelle
- **Results Delivery®** (conduite du changement) [vérifié] [Bain, « busting 3 myths »](https://www.bain.com/insights/results-delivery-busting-3-common-change-management-myths) :
  - Étude sur 184 entreprises : seulement 12 % des grands programmes de changement atteignent pleinement leurs objectifs ; 20 % échouent complètement ; 68 % se contentent de moins que l'ambition annoncée.
  - Bain a identifié **plus de 40 risques** de changement. L'évaluation doit faire ressortir les 4 ou 5 plus dangereux, leur ordre d'apparition et l'outil pour les contenir.
  - **Carte de chaleur** : une matrice 2×2 qui place chaque groupe selon son **importance pour le changement** et le **niveau de bouleversement** qu'il va subir.
  - **Chaîne de sponsors** de la base jusqu'au comité de direction ; chaque niveau anime une séance avec ses équipes.
  - Les conséquences (retour en temps réel, renforcement) seraient 4 fois plus efficaces que la formation ou les fiches de poste.
  - Le slogan « **le rouge est une bonne nouvelle** » (mieux vaut un indicateur rouge honnête qu'un vert de façade) apparaît seulement comme titre d'un article lié sur la même page Bain. [relayé] Résumé tiers de la méthode : [Umbrex](https://umbrex.com/resources/frameworks/project-management-frameworks/bain-results-delivery/)
- **RAPID®** (décisions) : Recommander, Être d'accord (veto limité), Exécuter, Contribuer, Décider. **Une seule personne** « a le D ». Rendu célèbre par l'article HBR « Who Has the D? » (Rogers et Blenko, 2006). Livrable : une carte des rôles par décision (« des rôles, pas des noms ») et un journal des décisions. [relayé] [Umbrex](https://umbrex.com/resources/frameworks/organization-frameworks/bain-rapid-decision-framework/), [Forbes / Bain Insights](https://www.forbes.com/sites/baininsights/2011/05/04/decisions-who-does-what/) (page bloquée)
- **Founder's Mentality®** (Chris Zook, James Allen, 2016) : une **mission d'insurgé**, l'**obsession du terrain**, un **état d'esprit de propriétaire**. Une entreprise sur neuf seulement tient une croissance rentable sur 10 ans. Le « tueur silencieux » de la croissance, c'est **la complexité** interne. [vérifié] [Bain, vidéo Chris Zook](https://www.bain.com/insights/chris-zook-overview-of-founders-mentality-video)
- **Net Promoter®** (Fred Reichheld, HBR 2003) : une question de 0 à 10 (« recommanderiez-vous… »). Promoteurs (9-10), passifs (7-8), détracteurs (0-6). Score = % promoteurs − % détracteurs. [relayé] [Bain, Introducing the Net Promoter System](https://www.bain.com/insights/introducing-the-net-promoter-system-loyalty-insights/)
  - Une étude de 2007 conteste que le score prédise mieux la croissance que la simple satisfaction. [relayé, blog]

### Le livrable type [déduit]
Un montant à atteindre, découpé en initiatives. Chaque initiative a un responsable, une échéance et un indicateur. Un tableau de bord rouge, orange, vert, revu chaque semaine. Une carte des rôles de décision.

### Visuels signature
- **Cascade de valeur** (d'où viennent les euros).
- **Carte de chaleur du changement** (importance × bouleversement).
- **Tableau de bord rouge, orange, vert**.
- **Grille RAPID** (décisions × rôles).
- **Anneau NPS** (promoteurs, passifs, détracteurs).

### Ce qu'un dirigeant en retient [déduit]
« Combien, qui, pour quand. Et je verrai tout de suite si ça dérape. »

---

## 4. Big Four (EY, Deloitte, PwC, KPMG)

Le point commun : la **confiance**, la **gouvernance** et le **risque**. Leur métier d'origine est l'audit, et leurs méthodes IA ressemblent à un audit de contrôle interne : inventaire, risques, contrôles, niveau de confiance.

### EY : indice de confiance IA [vérifié] [vendeur]
Sources : [document de discussion EY, mai 2024 (PDF)](https://www.ey.com/content/dam/ey-unified-site/ey-com/en-ca/services/ai/documents/ey-ai-confidence-index-discussion-paper.pdf), [page EY](https://www.ey.com/en_us/services/ai/platform/confidence-index).
- Les valeurs du cadre : **conception réfléchie, supervision vigilante, gouvernance agile**.
- Les principes notés : responsabilité, biais et équité, explicabilité, confidentialité, fiabilité, sécurité, durabilité, transparence, conformité.
- L'indice éprouve tout le cycle de vie des modèles. Il mêle des mesures chiffrées (performance) et qualitatives (transparence pour l'utilisateur), et donne des « niveaux de confiance mesurables ».
- **Visuels du document** : une **rosace par principe** (la couleur de chaque part = le niveau de confiance ; sa taille = le poids pour l'activité). Et une **matrice d'appétence au risque** (pertinence pour l'activité × niveau de confiance) qui donne un **feu vert ou rouge par solution**.
- La grille de notation exacte n'est pas publique.

### Deloitte : Trustworthy AI [vérifié]
Source : [communiqué Deloitte, 26/08/2020](https://www.prnewswire.com/news-releases/deloitte-introduces-trustworthy-ai-framework-to-guide-organizations-in-ethical-application-of-technology-in-the-age-of-with-301118495.html).
- Six dimensions : équitable et impartial, transparent et explicable, responsable et redevable, sûr et sécurisé, fiable, respectueux de la vie privée.
- Les pages récentes en comptent sept. [relayé] [Deloitte](https://www.deloitte.com/us/en/what-we-do/capabilities/applied-artificial-intelligence/articles/trustworthy-ethical-ai-thought-leadership.html)
- **AI readiness** : le rapport *State of AI in the Enterprise* 2026 met en avant l'écart entre la stratégie, jugée prête, et l'infrastructure, les données, le risque et les talents. Je n'ai trouvé **aucune grille de notation publique**. Des chiffres par dimension circulent, mais je n'ai pas pu les retrouver chez Deloitte, donc **je ne les cite pas**. [relayé] [Deloitte, State of AI 2026](https://www.deloitte.com/us/en/what-we-do/capabilities/applied-artificial-intelligence/content/state-of-ai-in-the-enterprise.html)

### PwC : Responsible AI [relayé] (pages PwC bloquées, erreur 403)
- 2019 : cinq dimensions (gouvernance ; éthique et réglementation ; interprétabilité et explicabilité ; robustesse et sécurité ; biais et équité), avec un questionnaire de diagnostic. [communiqué](https://www.prnewswire.com/in/news-releases/leaders-need-to-take-responsibility-for-and-action-on-responsible-ai-practices-pwc-820694938.html)
- Six catégories de risques IA : performance, sécurité, contrôle, économique, sociétal, entreprise. [PwC Indonésie](https://www.pwc.com/id/en/services/risk-assurance-services/data-analytics/responsible-ai.html)

### KPMG : Trusted AI [vérifié] [vendeur]
Source : [KPMG, *Deploying trustworthy AI: an illustrative risk and controls guide*, 2025 (PDF)](https://kpmg.com/kpmg-us/content/dam/kpmg/pdf/2025/trusted-ai-controls-matrix-tool-us.pdf), [cadre KPMG](https://kpmg.com/xx/en/what-we-do/services/ai/trusted-ai-framework.html).
- Trois principes : guidé par les valeurs, centré sur l'humain, digne de confiance.
- **Dix piliers** (lus dans le PDF) : équité, transparence, explicabilité, responsabilité, intégrité des données, fiabilité, sécurité (*security*), sûreté (*safety*), vie privée, durabilité.
- Le guide est un **inventaire de risques**, chacun avec des **contrôles conseillés**, rangés par pilier et par étape du cycle de vie. Il est aligné sur ISO 42001, le NIST AI RMF et l'AI Act européen.
- Exemple de risque qui nous concerne directement : « **contourner la gestion des risques IA** » (développer ou utiliser des outils IA sans supervision). C'est l'IA « fantôme ».

### Le livrable type des Big Four [déduit]
1. Inventaire des usages et systèmes IA.
2. Classement par niveau de risque.
3. **Carte de chaleur** (probabilité × impact, ou cas d'usage × pilier).
4. **Matrice risques / contrôles** : risque → contrôle → responsable → statut.
5. Note de confiance par pilier.
6. Plan de remédiation.

### Visuels signature
- **Carte de chaleur des risques**.
- **Matrice risques / contrôles** (tableau).
- **Rosace de confiance** (EY).
- **Matrice valeur × confiance**, avec feu vert ou rouge.

### Ce qu'un dirigeant en retient [déduit]
« Je sais ce qui tourne déjà chez moi, ce qui peut mal tourner, et ce qu'il faut verrouiller avant d'accélérer. »

---

## 5. Accenture

- ***The Art of AI Maturity*** (2022) : 1 176 entreprises qui utilisent l'IA et 1 615 dirigeants. Un indice de maturité de 0 à 100 combine des capacités **de base** (données, IA, cloud, stratégie, IA responsable, soutien de la direction, talents et culture) et des capacités **de différenciation**. Quatre profils [vérifié] [communiqué Accenture](https://newsroom.accenture.com/news/2022/more-than-60-percent-of-companies-are-only-experimenting-with-ai-creating-significant-opportunities-for-value-on-their-journey-to-ai-maturity-accenture-research-finds) :
  - **Achievers** : 12 % des entreprises, note 64.
  - **Innovators** (fortes en différenciation) : 13 %, note 50.
  - **Builders** (fortes sur la base) : 12 %, note 44.
  - **Experimenters** : 63 %, note 29.
  - Médiane : 36.
  - Les Achievers ont une croissance du chiffre d'affaires **50 % plus forte**. C'est une **corrélation**.
- **Réinvention** : 9 % des dirigeants interrogés ont déjà « la capacité de se réinventer en continu » (les « Reinventors »). Ils sont 1,8 fois plus nombreux à juger leur socle numérique solide. [vérifié] [Accenture, Reinvention by the numbers](https://www.accenture.com/us-en/insights/strategy/reinvention-by-numbers)
- **Visuel signature** : une **matrice 2×2 des profils** (capacités de base × capacités de différenciation). [déduit de la définition des profils]
- **Ce qu'un dirigeant retient** [déduit] : « Je sais dans quelle case je suis, et ce qui me sépare de la case du dessus. »
- Note : dans `audits-ia.md`, je n'avais pas trouvé de grille Accenture vérifiable. Le communiqué de 2022 est vérifié, mais la grille de notation détaillée reste non publique.

---

## 6. Lean, Toyota, Six Sigma

- **Muda (gaspillage)** : « toute activité qui consomme des ressources sans créer de valeur pour le client ». [vérifié] [Lean Enterprise Institute](https://www.lean.org/lexicon-terms/muda/)
- **Les 8 gaspillages** : transport, stocks, mouvements, attente, surproduction, surtraitement, défauts (les 7 de Taiichi Ohno, Toyota), plus les **compétences inutilisées**, ajoutées plus tard. Moyens mnémotechniques : TIMWOODS ou DOWNTIME. [relayé] [Learn Lean Sigma](https://www.learnleansigma.com/guides/8-wastes/), [The Lean Suite](https://www.theleansuite.com/blogs/8-wastes-lean-manufacturing-downtime)
- **Cartographie de la chaîne de valeur (VSM)** : « dessiner chaque étape des flux de matière et d'information » de la commande à la livraison. On fait la carte de l'**état actuel**, puis une carte de l'**état cible**. Chaque étape a sa boîte de données : temps de cycle, délai, « % complet et exact »… [vérifié] [LEI, Value-Stream Mapping](https://www.lean.org/lexicon-terms/value-stream-mapping/)
  - Méthode écrite pour la première fois par Rother et Shook (*Learning to See*, 1998-1999). [relayé] [LEI](https://www.lean.org/store/book/learning-to-see/)
  - Il existe une version **bureau** (*The Complete Lean Enterprise: VSM for Administrative and Office Processes*, Keyte et Locher, 2004). La VSM ne se limite donc pas à l'usine. [relayé] [Skillsoft](https://skillsoft.com/book/the-complete-lean-enterprise-value-stream-mapping-for-administrative-and-office-processes-50e5e5b0-efe2-11e6-9877-0242c0a80506)
- **PCE (efficacité du cycle)** = temps à valeur ajoutée ÷ délai total. Repères attribués à Michael George (*Lean Six Sigma*, McGraw-Hill, 2002) [relayé] [Quality America](https://qualityamerica.com/LSS-Knowledge-Center/leansixsigma/process_cycle_efficiency.php) :
  - Processus **administratif (transactionnel)** : 10 % typique, 50 % au meilleur niveau.
  - Travail **créatif** : 5 % typique, 25 % au meilleur niveau.
  - Après une démarche Lean, la PCE dépasse en général 25 %.
  - D'autres sources donnent d'autres repères, car les définitions varient. **Toujours citer la définition avec le chiffre.**
- **DMAIC** (Six Sigma) : Définir, Mesurer, Analyser, Améliorer, Contrôler. Les étapes se suivent toujours dans cet ordre. On mesure une base de départ, on cherche les causes racines (5 pourquoi, Ishikawa), puis on verrouille le gain. [relayé] [ASQ](https://asq.org/quality-resources/dmaic) (page bloquée, erreur 403), [Wikipedia](https://en.wikipedia.org/wiki/DMAIC)
- **Le geste Lean de base** [déduit] : le **gemba**, aller voir le travail là où il se fait plutôt que d'en parler en salle. screenpipe est littéralement un gemba numérique.

### Visuels signature
- **VSM** (boîtes d'étapes, triangles d'attente, ligne du temps en bas avec le temps à valeur ajoutée et le délai total).
- **Barres des 8 gaspillages**.
- **Jauge de PCE**.
- **Avant / après** (DMAIC, phase « Contrôler »).

### Ce qu'un dirigeant en retient [déduit]
« Je vois le chemin réel du travail et je sais combien de minutes partent à la poubelle, étape par étape. »

---

## 7. Process mining et task mining

- **Process mining** (Wil van der Aalst) : trois usages. La **découverte** (reconstruire le processus à partir des traces), la **conformité** (comparer le réel au processus prévu) et l'**amélioration**. [relayé] [manifeste, vdaalst.com](https://vdaalst.com/publications/p685.pdf), [Springer](https://link.springer.com/chapter/10.1007/978-3-642-28108-2_19)
- **Celonis** [vérifié] [vendeur] [Celonis, How does process mining work](https://www.celonis.com/insights/topics/how-does-process-mining-work) :
  - Le journal d'événements a trois champs : identifiant du dossier, activité, horodatage.
  - Le résultat est une **carte de processus interactive**. « Chaque chemin unique est appelé une variante. »
  - La conformité permet de « définir le chemin voulu et voir où les processus s'en écartent ».
  - Questions types : « Où sont les goulots ? Quelles activités sont souvent sautées ? »
  - Le **délai** d'un dossier = temps entre son premier et son dernier événement. [relayé] [Celonis PQL](https://www.researchgate.net/publication/360196445_Celonis_PQL_A_Query_Language_for_Process_Mining)
- **UiPath Task Mining** [relayé] [vendeur] [doc UiPath](https://docs.uipath.com/task-mining/automation-cloud/latest/user-guide/introduction-as), [glossaire](https://docs.uipath.com/task-mining/automation-suite/2023.4/user-guide/glossary) :
  - Un enregistreur sur le poste capture captures d'écran, frappes et clics, avec masquage des données personnelles.
  - Un modèle cherche les **suites d'étapes répétées** et les regroupe en tâches. La doc conseille au moins 10 000 actions, 50 000 en base.
  - **Le potentiel d'automatisation reste jugé à la main** par un analyste. L'IA propose des candidats, et il faut séparer les vraies tâches du bruit.
- Les KPI de Microsoft Process Advisor, Soroco et Skan (variantes, paires d'apps, copier-coller) sont détaillés dans `audits-ia.md` § 3.

### Visuels signature
- **Carte de processus** (réseau d'activités, épaisseur = fréquence).
- **Variantes classées**.
- **Délai par étape**.

### Ce qu'un dirigeant en retient [déduit]
« Ce n'est pas ce qu'on m'a raconté, c'est ce qui s'est passé. »

### Pour nous [déduit]
screenpipe fournit l'équivalent d'un journal d'événements : app, titre de fenêtre, horodatage, clics. Notre « tâche répétée » joue le rôle du dossier et nos « étapes » celui des activités. Il nous manque la notion de **variante** (§ 9).

---

## 8. Des visuels signature à notre vocabulaire de viz

| Visuel du cabinet | Notre `viz` | Utilisé dans |
|---|---|---|
| Page de synthèse, gros chiffre | `chiffre-cle` | toutes |
| Arbre MECE, arbre de profit | `arbre` | Sommet |
| Cascade (waterfall) | `cascade` | Sommet, Résultat net |
| Pareto | `liste-classee` (barres triées + cumul) | Sommet |
| Trois horizons, plan à 90 jours | `frise` | Sommet, Résultat net |
| Matrice 2×2 (portefeuille, profils, valeur × confiance, changement) | `matrice-2x2` | Frontière, Résultat net, Garde-fou |
| Barres 10/20/70, Deploy/Reshape/Invent, 8 gaspillages | `barres-empilees` | Frontière, Gemba |
| Carte de chaleur (risques, frontière, tableau de bord RAG) | `carte-chaleur` | Frontière, Résultat net, Garde-fou, Gemba |
| Rosace de confiance, anneau NPS, délégation / conversation | `anneau` | Frontière, Résultat net, Garde-fou, Gemba |
| VSM | `vsm` | Gemba |
| Carte de processus, outils communs | `reseau` | Frontière, Gemba |
| Avant / après | `course` | Gemba |

---

## 9. Les 5 méthodes produit (détail dans `methodes.json`)

| id | Nom | Inspirée de | Promesse |
|---|---|---|---|
| `pyramide` | **Sommet** | McKinsey (pyramide de Minto, arbres MECE, 7 étapes, Rewired, 3 horizons) | La réponse d'abord, puis seulement les preuves qui la portent |
| `frontiere` | **Frontière** | BCG (jagged frontier, Deploy-Reshape-Invent, 10/20/70, matrice croissance/part) et Accenture (profils de maturité IA) | Où l'IA aide vos équipes, où elle les piège, et où investir |
| `resultat` | **Résultat net** | Bain (Results Delivery, RAPID, Founder's Mentality, Net Promoter) | Chaque recommandation a un montant, un responsable et une date |
| `gardefou` | **Garde-fou** | EY, Deloitte, PwC, KPMG (confiance, gouvernance, risques et contrôles) | Quelle IA tourne déjà chez vous, ce qu'elle touche, quoi verrouiller |
| `gemba` | **Gemba** | Toyota et Lean (VSM, 8 gaspillages), Six Sigma (DMAIC, PCE), process mining (Celonis, UiPath) | Suivre le travail tel qu'il se fait et chiffrer chaque gaspillage |

Pourquoi ces 5 [déduit] : elles couvrent les **cinq questions** qu'un dirigeant peut poser. Que faire ? (Sommet). Où mettre l'IA ? (Frontière). Combien et qui ? (Résultat net). Est-ce risqué ? (Garde-fou). Où ça coince ? (Gemba). Elles ont aussi **cinq tons** différents, ce qui rend le choix visible pour le client.

### Les noms
- **Sommet** : le haut de la pyramide, là où on met la réponse.
- **Frontière** : la « jagged frontier ». Un mot courant, pas une marque.
- **Résultat net** : un jeu de mots sur le résultat chiffré et le résultat comptable.
- **Garde-fou** : le vocabulaire du contrôle, compréhensible sans jargon.
- **Gemba** : le mot japonais du Lean pour « le lieu réel du travail ». Un terme générique, pas une marque. Si l'équipe le trouve trop obscur, l'alternative est **Flux**.

### Les métriques
Dans `methodes.json`, une métrique **sans préfixe** existe déjà dans `labs/phamphamh/audit/construire.py` ou dans les résumés validés :
- par poste : `actif_min`, `par_categorie_min`, `ia_agent_min`, `ia_chat_min`, `part_ia`, `bascules`, `bascules_par_heure`, `ecran_median_s`, `plongee`, `paires`, `segments` ;
- entre postes : `ensemble_min`, `meme_sujet_min`, `outils` ;
- par tâche : `taches.frequence_par_semaine`, `taches.duree_moyenne_min`, `taches.etapes`, `taches.goulots` ;
- à l'onboarding : `cout_horaire`.

Une métrique **préfixée `calc:`** demande un calcul en plus :

| Métrique nouvelle | Calcul | Difficulté [déduit] | Méthodes |
|---|---|---|---|
| `calc:heures_semaine_tache` | fréquence/sem × durée moyenne | Triviale | toutes |
| `calc:cout_tache` | heures/sem × `cout_horaire` (pour un chiffre annuel : × semaines travaillées, un paramètre demandé à l'onboarding et affiché) | Triviale | Sommet, Résultat net |
| `calc:part_cumulee` | cumul trié des heures par tâche (Pareto) | Triviale | Sommet |
| `calc:exposition_ia` | un LLM note chaque tâche E0, E1 ou E2 avec la rubrique d'Eloundou (voir `audits-ia.md` § 2) | Moyenne (un appel LLM par tâche) | Sommet, Frontière, Garde-fou, Gemba |
| `calc:ia_dans_tache` | part des étapes d'une tâche faites dans une app IA (croiser `taches.etapes[].app` avec la liste IA de `construire.py`) | Facile | Frontière, Garde-fou |
| `calc:jours_actifs_ia` | nombre de jours avec au moins un segment IA, par poste | Facile | Frontière |
| `calc:gaspillages` | goulots → gaspillages : `waiting` → attente, `switching` → mouvements, `rework` → défauts, `handoff` → transport ; étapes `input` qui recopient → surtraitement ; `meme_sujet_min` → surproduction possible | Facile, mais le mapping est **notre choix** | Gemba |
| `calc:pce` | minutes des étapes `action` et `output` ÷ durée totale de la tâche. **Il faut une durée par étape**, absente aujourd'hui | Moyenne (horodater les étapes) | Gemba |
| `calc:duree_etape` | durée de chaque étape d'une tâche | Moyenne | Gemba |
| `calc:variantes_tache` | regrouper les exécutions d'une même tâche par suite d'apps ou d'étapes ; compter les chemins distincts et l'écart de durée | Difficile (il faut plusieurs exécutions détectées) | Gemba |
| `calc:ia_non_fournie` | outils IA observés absents de la liste fournie par le client à l'onboarding | Facile (nouvelle question d'onboarding) | Garde-fou |
| `calc:donnees_sensibles_vers_ia` | un LLM local signale qu'un texte de l'écran contient des données personnelles ou clients **pendant** qu'une app IA est au premier plan ; seul le compteur sort | Difficile, et sensible pour la vie privée | Garde-fou |
| `calc:niveau_confiance` | note de 1 à 5 par pilier et par tâche (règles + LLM), avec la règle « la note la plus basse bloque » | Moyenne, c'est **notre grille** | Garde-fou |
| `calc:decisions_par_tache` | nombre d'étapes `decision` et de goulots `handoff` par tâche | Triviale | Résultat net |
| `calc:part_coeur_metier` | `projet` ÷ (`projet` + `reunion` + `comm` + `admin`) | Triviale, mais la frontière « cœur de métier » est **notre choix** | Résultat net |
| `calc:tendance_semaine` | les mêmes mesures sur deux périodes (avant / après) | Moyenne (il faut une deuxième semaine) | Résultat net, Gemba |
| `calc:nps_salaries` | une question de 0 à 10 dans la page de relecture (« recommanderiez-vous cet agent à un collègue ? ») | Facile (nouvelle question) | Résultat net |
| `calc:recommandations_par_type` | classer nos recommandations en algorithme / techno et données / personnes et processus | Facile (étiquette posée par le LLM qui rédige) | Frontière |
| `calc:heures_recuperables` | somme sur les tâches E1/E2 de `heures_semaine_tache` × un taux de gain **affiché comme hypothèse** | Facile, mais le taux est une hypothèse à montrer | Sommet, Frontière |
| `calc:fragmentation_horaire` | bascules par heure, par tranche horaire et par jour | Facile | Gemba |

**Garde-fous d'affichage** (repris de `audits-ia.md` § 6.1) : au moins 3 postes par chiffre, 5 pour tout ce qui ressemble à de la performance, et jamais de classement de personnes. La carte du changement (Résultat net) et les variantes (Gemba) passent **par tâche**, pas par personne, quand il y a moins de 5 postes.

---

## 10. Repères chiffrés sourcés, utilisables sur une slide

À afficher **toujours avec la source** et la mention « repère publié, pas une mesure chez vous ».

| Repère | Valeur | Statut |
|---|---|---|
| Effort IA selon BCG | 10 % algorithmes, 20 % techno et données, 70 % personnes et processus | [vérifié] |
| Gain de la refonte selon BCG | efficacité « jusqu'à 50 % » | [vérifié] [vendeur] |
| Jagged frontier, dans la frontière | +12,2 % de tâches, 25,1 % plus rapide, qualité +40 % et plus | [vérifié] |
| Jagged frontier, hors frontière | −19 points de bonnes réponses | [vérifié] |
| Changements réussis (Bain) | 12 % atteignent pleinement leurs objectifs | [vérifié] [vendeur] |
| Croissance rentable durable (Bain) | 1 entreprise sur 9 sur 10 ans | [vérifié] [vendeur] |
| Maturité IA (Accenture 2022) | 12 % d'Achievers, 63 % d'Experimenters | [vérifié] [vendeur] |
| PCE d'un processus administratif (George 2002) | 10 % typique, 50 % au meilleur niveau | [relayé] |
| PCE d'un travail créatif (George 2002) | 5 % typique, 25 % au meilleur niveau | [relayé] |
| Attention sur un écran (Gloria Mark) | 47 s | [vérifié], voir `audits-ia.md` |

---

## 11. Ce qui n'est pas vérifié

- **McKinsey** : les pages Rewired, Trois horizons et Zelazny ont dépassé le délai (même problème que dans `audits-ia.md`). Leur contenu vient d'extraits de recherche. Les six capacités de Rewired sont vérifiées sur la page de l'éditeur (Wiley, 2e édition), pas sur le livre de 2023.
- **Liste complète des 7 étapes** : seules les étapes 1 à 3 et la synthèse sont lues dans la transcription.
- **MECE inventé par Minto** : seulement relayé par des blogs. Son site n'en parle pas.
- **« La cascade a été inventée par McKinsey »** : c'est McKinsey qui le dit, vu en extrait seulement.
- **RAPID** et **NPS** : la page Forbes de Bain est bloquée (403) et je n'ai pas ouvert la page NPS de Bain. Leurs définitions sont stables dans toutes les sources, mais [relayé].
- **« Red is good »** chez Bain : seulement le titre d'un article lié. Je n'ai pas lu son contenu.
- **Carte de chaleur de Bain** (importance × bouleversement) : lue dans un résumé automatique de la page Bain, pas en citation exacte.
- **PwC** : toutes les pages sont bloquées (403). Tout est [relayé].
- **Deloitte AI readiness** : pas de grille publique. Des pourcentages par dimension circulent sans que je puisse les retrouver chez Deloitte, donc je ne les cite pas.
- **EY** : la notation exacte de l'indice n'est pas publique. Les visuels (rosace, matrice d'appétence) viennent du document de discussion de 2024.
- **DMAIC** : la page ASQ est bloquée. Je me suis appuyé sur Wikipedia et des guides.
- **Repères de PCE** : une seule source secondaire (Quality America, qui cite George 2002). D'autres sources donnent d'autres chiffres.
- **Ce que contiennent nos vraies données aujourd'hui** (mesuré sur `donnees/audit/audit.json`, 17/10) : 5 tâches répétées, 16 étapes au total (7 `action`, 5 `check`, 2 `input`, 2 `output`), **aucune étape `decision`**, et des goulots `switching` (3), `unclear` (2) et `waiting` (1). Aucun `rework` ni `handoff`. Conséquences : le chapitre « Qui décide » (Résultat net) et les gaspillages « défauts » et « transport » (Gemba) seront **vides** tant que la détection des étapes ne s'enrichit pas. Le goulot `unclear` n'est pas prévu dans le brief et n'a pas d'équivalent Lean : je le classe « non attribué ».
- **Toutes les règles de calcul du § 9** sont mes propositions. Je ne les ai **pas testées** sur `donnees/audit/audit.json`. En particulier : les étapes ont-elles assez de détail pour une PCE ? Les tâches répétées ont-elles assez d'exécutions pour compter des variantes ? Ce sont les deux points les plus fragiles.
- **Correspondances « centaure / cyborg » ↔ « agent / conversation »** et **goulots ↔ 8 gaspillages** : ce sont des analogies de ma part, pas des définitions des auteurs. Il faut les présenter comme « inspirées de ».

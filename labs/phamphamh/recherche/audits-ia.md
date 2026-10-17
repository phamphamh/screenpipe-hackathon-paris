# Ce que mesurent les audits IA, et ce qu'on peut en reprendre

Recherche du 17/10/2026. Pour chaque chiffre : la source (URL) et un statut.

- **[vérifié]** : j'ai lu le chiffre sur la source primaire (page ou PDF de l'éditeur, de l'institut ou de l'article).
- **[relayé]** : je l'ai trouvé seulement dans des résumés ou des résultats de recherche, pas sur la source primaire. À revérifier avant de le mettre sur une slide.
- **[vendeur]** : la source vend un outil ou une prestation. Le chiffre est réel sur la page, mais rien ne garantit la méthode.
- **[déduction]** : c'est mon raisonnement, pas une source.

---

## 0. En bref

1. Les grands cadres (BCG, McKinsey, MIT, Gartner, Microsoft) mesurent **l'entreprise** (stratégie, données, gouvernance, adoption, résultat financier), et presque toujours **par sondage déclaratif**. Aucun ne regarde l'écran.
2. Les outils de *task mining* (Microsoft, UiPath, Celonis, Soroco, Skan) mesurent **le travail réel** : temps par tâche, variantes, changements d'app, copier-coller. C'est exactement ce que screenpipe sait faire, sans installer de mouchard d'entreprise.
3. Les grilles « tâche par tâche » (Eloundou E0/E1/E2, Anthropic Economic Index, Stanford WORKBank) donnent une **méthode publique** pour dire si une tâche est exposée à l'IA. Elles sont faites pour être appliquées par un LLM.
4. Les audits de PME livrent toujours la même chose : **état des lieux, une dizaine de cas d'usage classés valeur × faisabilité, feuille de route**. Ils facturent de 800 à 1 100 € HT par jour.
5. Notre avantage [déduction] : on peut remplir ce livrable avec **des mesures** au lieu d'entretiens, et ajouter ce que personne ne mesure en PME : l'usage réel de l'IA, y compris celui qui n'est pas déclaré.

---

## 1. Les cadres de maturité et de valeur

| Cadre | Ce qu'il regarde | Chiffres utiles | Statut |
|---|---|---|---|
| **BCG 10/20/70** | Où mettre l'effort : 10 % algorithmes, 20 % technologie et données, 70 % personnes et processus | — | [vérifié] [BCG, Leader's guide](https://www.bcg.com/featured-insights/the-leaders-guide-to-transforming-with-ai) |
| **BCG, *Where's the value in AI?* (oct. 2024)** | Capacités IA, passage du pilote à l'échelle | 22 % des entreprises ont dépassé la preuve de concept et 4 % créent une valeur substantielle. Le communiqué titre « 74 % peinent à obtenir de la valeur » | [vérifié] pour 22 % et 4 % ([BCG](https://www.bcg.com/featured-insights/the-leaders-guide-to-transforming-with-ai)). [relayé] pour 74 % ([communiqué BCG](https://www.bcg.com/press/24october2024-ai-adoption-in-2024-74-of-companies-struggle-to-achieve-and-scale-value)) |
| **BCG, *AI at Work* (juin 2025)** | Usage par les salariés, formation, IA non autorisée | 10 600 salariés dans 11 pays. 72 % utilisent l'IA régulièrement, contre 51 % chez les salariés de terrain. 36 % se disent bien formés. **54 % utiliseraient des outils IA même non autorisés.** 25 % des salariés de terrain disent recevoir assez de consignes | [vérifié] [communiqué BCG](https://www.bcg.com/press/26june2025-beyond-ai-adoption-full-potential) |
| | Effet de la formation | Avec plus de 5 h de formation, 79 % sont utilisateurs réguliers, contre 67 % en dessous | [relayé] ([BigDATAwire](https://www.bigdatawire.com/this-just-in/bcg-report-companies-must-go-beyond-ai-adoption-to-realize-its-full-potential), [Unleash](https://www.unleash.ai/artificial-intelligence/bcgs-ai-at-work-2025-report-four-takeaways-for-hr-leaders/)) |
| **BCG × Harvard, « jagged frontier » (2023)** | Effet de GPT-4 tâche par tâche, en expérience contrôlée | 758 consultants. Sur 18 tâches **dans** la frontière : +12,2 % de tâches finies, 25,1 % plus rapide, qualité supérieure de plus de 40 %. Les moins bons gagnent +43 %, les meilleurs +17 %. Sur une tâche **hors** frontière : 19 points de moins de bonnes réponses | [vérifié] résumé du PDF du [working paper HBS 24-013](https://www.hbs.edu/ris/Publication%20Files/24-013_d9b45b68-9e74-42d6-a1c6-c72fb70c7282.pdf) (copie lue sur [MIT Sloan](https://mitsloan.mit.edu/sites/default/files/2023-10/SSRN-id4573321.pdf)) |
| **McKinsey, *State of AI* (2025)** | Adoption par fonction, passage à l'échelle, impact sur l'EBIT, pratiques de gestion | 88 % utilisent l'IA dans au moins une fonction. Environ un tiers a commencé à passer à l'échelle. 62 % expérimentent des agents. 39 % voient un impact sur l'EBIT de l'entreprise | [relayé] : extraits de la [page McKinsey](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-state-of-ai-2025) dans les résultats de recherche. La page ne s'est pas chargée (délai dépassé) |
| | Les « high performers » | Environ 6 % (plus de 5 % de l'EBIT attribué à l'IA). Ils sont environ 3 fois plus nombreux à avoir **refait leurs processus** autour de l'IA | [relayé] seulement par des résumés ([CX Today](https://www.cxtoday.com/ai-automation-in-cx/mckinseys-state-of-ai-the-scaling-gap-is-now-cxs-problem/)). Les chiffres diffèrent selon les résumés (55 % ou « 3 fois ») |
| **MIT CISR, Enterprise AI Maturity Model (déc. 2024)** | 4 étapes : 1. Expérimenter et préparer, 2. Pilotes et capacités, 3. Façons de travailler IA, 4. Prêt pour l'avenir. Axes : processus, technologie, culture | 28 % / 34 % / 31 % / 7 % des entreprises. Étapes 1-2 : performance financière **sous** la moyenne du secteur. Étapes 3-4 : **bien au-dessus**. Enquête de 2022 sur 721 entreprises, surtout l'IA « classique » | [vérifié] [MIT Sloan](https://mitsloan.mit.edu/press/new-mit-cisr-research-finds-companies-advanced-enterprise-ai-outpace-industry-peers-financial-performance) |
| **Gartner AI Maturity Model** | 5 niveaux, un questionnaire de 7 questions | Organisations matures : 45 % gardent leurs projets IA en production 3 ans ou plus, contre 20 % chez les peu matures. Les métiers font confiance aux nouvelles solutions dans 57 % des cas, contre 14 % | [vérifié] [communiqué Gartner, 30/06/2025](https://www.gartner.com/en/newsroom/press-releases/2025-06-30-gartner-survey-finds-forty-five-percent-of-organizations-with-high-artificial-intelligence-maturity-keep-artificial-intelligence-projects-operational-for-at-least-three-years) |
| | Les 7 piliers (stratégie, produit, gouvernance, ingénierie, données, modèle opérationnel, culture) | — | [relayé] seulement par des blogs. Le modèle complet est payant |
| **Microsoft Work Trend Index 2025, « Frontier Firm »** | Entreprises « frontière » : IA déployée partout, maturité avancée, agents utilisés et prévus | 844 dirigeants « frontière » sur 9 037. 71 % disent que leur entreprise prospère, contre 39 % en moyenne. 55 % peuvent prendre plus de travail, contre 25 %. 53 % des dirigeants veulent plus de productivité, mais 80 % des salariés manquent de temps ou d'énergie | [vérifié] [Microsoft WorkLab](https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born) (source vendeur : Microsoft vend Copilot) |
| **Microsoft, « infinite workday » (2025, télémétrie M365)** | Interruptions, mails, réunions | Une interruption toutes les **2 minutes** entre 9 h et 17 h. 117 mails et 153 messages Teams par jour. 57 % des réunions sont improvisées, sans invitation | [vérifié] [Microsoft WorkLab](https://www.microsoft.com/en-us/worklab/work-trend-index/breaking-down-infinite-workday) [vendeur] |
| **Microsoft WTI 2024** | Usage de l'IA par les salariés | 75 % des travailleurs du savoir utilisent l'IA. **78 % de ces utilisateurs apportent leurs propres outils** (« BYOAI ») | [relayé] (extrait du [communiqué Microsoft](https://news.microsoft.com/source/?p=19728)) [vendeur] |
| **Deloitte, *State of GenAI in the Enterprise* (T4 2024)** | ROI, passage du pilote à la production | 74 % disent que leur projet le plus avancé atteint ou dépasse le ROI attendu, 20 % au-delà de 30 %. Plus des deux tiers pensent passer à l'échelle 30 % ou moins de leurs expériences dans les 3 à 6 mois | [relayé] (extraits de la [page Deloitte](https://www.deloitte.com/global/en/issues/ai/state-of-generative-ai-in-enterprise.html)) |
| **Accenture** | — | Je n'ai pas trouvé de grille de maturité IA d'Accenture vérifiable en accès libre. **Je ne la cite pas.** | — |

**Ce que ces cadres ont en commun** [déduction] :
- Ils mesurent par **sondage auprès des dirigeants**. McKinsey précise que l'impact sur l'EBIT est déclaré.
- Ils séparent tous **l'adoption**, qui est facile, de **la valeur**, qui est rare. Le facteur qui revient partout, c'est **refaire les processus** (BCG 70 %, McKinsey, MIT étape 3).
- Aucun ne dit **quelles tâches** chez **quels salariés**. C'est le trou que comblent le *task mining* et, pour nous, screenpipe.

---

## 2. Les grilles tâche par tâche

### Eloundou et al., « GPTs are GPTs » (OpenAI / UPenn, 2023)
- **Rubrique** [vérifié, [arXiv 2303.10130](https://arxiv.org/abs/2303.10130)] : une tâche est « exposée » si l'IA peut réduire son temps **d'au moins 50 %** à qualité égale.
  - **E0** : pas exposée.
  - **E1** : un LLM seul, type ChatGPT, suffit.
  - **E2** : il faut un logiciel construit sur un LLM (connecteur, outil, agent).
- **Chiffres** [vérifié, résumé de l'article] : 80 % des salariés américains ont au moins 10 % de tâches exposées, et 19 % en ont au moins 50 %. 15 % des tâches vont nettement plus vite avec un LLM seul, et **47 à 56 % avec des logiciels construits dessus**.
- Les auteurs ont fait étiqueter les tâches **par GPT-4 avec la même rubrique** que des humains [relayé, [ar5iv](https://ar5iv.labs.arxiv.org/html/2303.10130)]. C'est donc une méthode prévue pour un LLM.
- **Pour nous** [déduction] : l'écart entre E1 (« ChatGPT suffit ») et E2 (« il faut un outil ») est exactement l'écart entre **une formation** et **un workflow prêt à l'emploi**. Ce sont nos deux types de recommandation.

### Anthropic Economic Index
- **5 modes d'usage** [vérifié, [Anthropic, fév. 2025](https://www.anthropic.com/news/the-anthropic-economic-index)] :
  - **Automatisation** : *Directive* (l'IA fait la tâche déléguée) et *Feedback loop* (l'IA fait, guidée par les retours de l'environnement).
  - **Augmentation** : *Itération* (on affine à deux), *Apprentissage* (comprendre) et *Validation* (vérifier son propre travail).
  - Premier relevé : 57 % d'augmentation et 43 % d'automatisation. 36 % des métiers utilisent l'IA sur au moins un quart de leurs tâches, 4 % sur au moins trois quarts.
- **Entreprises, via l'API** [vérifié, [rapport sept. 2025](https://www.anthropic.com/research/anthropic-economic-index-september-2025-report)] : **77 % d'automatisation**, contre environ la moitié sur Claude.ai. Le rapport conclut que les déploiements complexes sont freinés **plus par l'accès à l'information (le contexte) que par le modèle**.
- **« Primitives économiques »** [vérifié, [rapport janv. 2026](https://www.anthropic.com/research/anthropic-economic-index-january-2026-report)] : complexité de la tâche (temps humain avec et sans IA), compétences, usage pro ou perso, autonomie de l'IA (échelle de 1 à 5) et réussite.
  - Temps moyen sans IA : 3,1 h sur Claude.ai. Avec IA : 15 min.
  - Le taux de réussite **baisse quand la tâche s'allonge**. Sur l'API, il passe d'environ 60 % pour les tâches de moins d'une heure à environ 45 % au-delà de 5 h.
  - Le rapport prévient lui-même : « aucune mesure n'est exacte ».
- **Gains de temps** [vérifié, [Anthropic, nov. 2025](https://www.anthropic.com/research/estimating-productivity-gains)] : sur 100 000 conversations, une tâche prend environ 90 min sans IA et l'IA réduit ce temps d'environ 80 %. Limite reconnue : le temps passé hors conversation (vérifier, corriger) n'est pas compté.
- **Pour nous** [déduction] : screenpipe voit justement ce temps « hors conversation ». On peut mesurer ce qu'Anthropic ne voit pas : le temps passé à recopier, vérifier et recoller la réponse de l'IA.

### Stanford, « Future of Work with AI Agents » (WORKBank, 2025)
- [vérifié, [arXiv 2506.06576](https://arxiv.org/html/2506.06576v2)] On croise le **désir des salariés** d'automatiser une tâche avec la **capacité technique**. On obtient 4 zones :
  - **Feu vert** : désir fort et capacité forte.
  - **Feu rouge** : capacité forte mais désir faible.
  - **R&D** : désir fort mais capacité faible.
  - **Faible priorité** : ni désir ni capacité.
- **Échelle d'implication humaine H1 à H5** : de H1 (l'IA fait tout) à H5 (humain indispensable en continu). H3, le partenariat égal, est le niveau préféré dans 45,2 % des métiers.
- Les salariés veulent automatiser 46,1 % des tâches. Leur raison n° 1 : **libérer du temps pour du travail à plus forte valeur** (69 % des réponses), puis le côté répétitif et la qualité (46,6 % chacun).
- **41 % des cas d'usage des start-ups YC** tombent en zone feu rouge ou faible priorité. Autrement dit, on construit souvent ce que les gens ne veulent pas.
- **Pour nous** [déduction] : la page de relecture du salarié peut poser **une seule question par tâche** (« Voulez-vous que l'IA fasse ça ? 1 à 5 »). Avec la capacité estimée par un LLM, on obtient la matrice de Stanford pour la PME.

### Effet mesuré par tâche (rappels utiles)
- **Support client** [relayé, [NBER w31161](https://nber.org/papers/w31161)] : un assistant IA augmente de 14 % les tickets résolus par heure, et de 34 % chez les débutants.
- **Perception ou mesure** [vérifié, [METR, juil. 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)] : 16 développeurs expérimentés, 246 tâches. Ils pensaient gagner 24 %. Ils ont été **19 % plus lents**, et croyaient pourtant après coup avoir gagné 20 %.
  - **Attention** : METR dit lui-même que ce résultat est dépassé. La suite de 2026 n'est pas concluante ([relayé](https://www.i-programmer.info/news/99-professional/18910-perceived-value-of-ai-tools.html)).
  - La leçon qui reste : **le ressenti ne remplace pas la mesure**.

---

## 3. Ce que mesurent les outils de task mining et de process mining

| Outil | KPI exacts | Statut |
|---|---|---|
| **Microsoft Power Automate, Process Advisor (task mining)** | Nombre d'enregistrements ; **nombre de variantes** (chaque chemin différent d'au moins une étape) ; temps moyen ; variantes par fréquence et par durée ; durée moyenne par activité. **Analyse des apps** : apps utilisées, nombre de retours sur chaque app, temps par app, actions par app. **Paires d'apps utilisées ensemble**, que Microsoft présente comme un signal de « transfert de données ou de saisie manuelle » | [vérifié] [Microsoft Learn](https://learn.microsoft.com/en-us/power-automate/process-advisor-visualize) [vendeur] |
| **UiPath Task Mining** | Par tâche : utilisateurs, *traces* (nombre d'occurrences), temps total, nombre médian d'étapes et d'actions, temps d'exécution médian, apps utilisées. Classement par **potentiel d'automatisation = répétabilité × complexité**. UiPath conseille de reclasser selon ses propres critères | [relayé] (extraits de la [doc UiPath](https://docs.uipath.com/task-mining/automation-suite/2023.4/user-guide/viewing-a-project) ; la page « latest » renvoie une erreur 404) [vendeur]. Un résultat signale que le mode « unassisted » aurait été retiré fin 2025 : non vérifié |
| **Celonis Task Mining** | Capture les clics, **copier-coller**, défilements et le temps par application, avec horodatage et captures d'écran. Relie ces actions aux dossiers métier pour mesurer le temps réel par dossier et le temps passé en activités « sans valeur ajoutée » | [vérifié] [Celonis](https://www.celonis.com/insights/topics/what-is-task-mining) [vendeur] |
| **Soroco Scout** | Changements d'app, **événements de presse-papier**, navigation dans les vieux logiciels, **nombre d'allers-retours, de copier-coller et de minutes dans des tableurs non documentés**. Leur exemple : « 14 bascules Excel, 23 copier-coller, 18 min dans un tableur de suivi ». Indicateurs : effort manuel, variance, réduction du temps de cycle, heures récupérées par an | [vérifié] [Soroco](https://soroco.com/scout-of-agentification/) [vendeur]. Cas client avec 25 % d'écart d'effort entre sites : [relayé](https://soroco.com/customer-stories/insurance/scout-discovered-variations-in-claims-processing-for-a-brokerage-giant/) |
| **Skan.ai** | Temps d'attente, délais de traitement, **taux de bascule entre apps**, effort par app, délai total de traitement, coût des changements de contexte | [relayé] ([Skan](https://www.skan.ai/use-cases/operational-excellence)) [vendeur] |
| **KYP.ai** | Usage des apps, transitions entre tâches, **fréquence des changements d'app**, heures de concentration maximale, taux d'utilisation. Les formules ne sont pas publiées | [relayé] ([KYP.ai](https://kyp.ai/time-tracking-software)) [vendeur] |
| **ActivTrak** | Part du temps passé dans chaque outil IA, adoption par niveau, avant et après adoption de l'IA | [vérifié] [ActivTrak](https://www.activtrak.com/blog/443-million-hours-data-ai-adoption-impact/) [vendeur], voir § 5 |
| **Worklytics** | Jours actifs IA par semaine, usages par jour actif, outils distincts par semaine, part des utilisateurs mono-outil | [vérifié] [Worklytics](https://www.worklytics.co/blog/how-to-measure-ai-skills-across-your-workforce) [vendeur], voir § 5 |

**Références sur la fragmentation** :
- [vérifié, [UC Newsroom](https://www.universityofcalifornia.edu/news/how-sharpen-your-attention-and-meet-your-goals-2024)] Gloria Mark (UC Irvine) mesure **47 secondes** d'attention moyenne sur un écran avant de changer (études 2016-2020), contre 2 min 30 en 2004. Se remettre d'une interruption peut prendre près d'une demi-heure.

**Ce qui revient chez tous** [déduction] : temps par tâche, nombre de répétitions, nombre de personnes concernées, nombre de variantes, changements d'app, copier-coller entre apps et attente. **screenpipe capte déjà les déclencheurs « changement de fenêtre », « clic », « frappe » et « copier-coller »** (voir `.context/hackathon-brief.md`). On a donc la matière première des KPI de task mining.

---

## 4. Les livrables des audits IA de PME

| Cabinet | Ce qu'il livre | Prix et durée | Statut |
|---|---|---|---|
| **Lonestone** (FR) | Rapport d'observations classées selon les objectifs du client, recommandations concrètes, réunion de restitution. Pas de matrice décrite publiquement | Audit IA à 1 100 € HT par jour, de 1 à 5 jours | [relayé] (résultat de recherche sur [lonestone.io](https://lonestone.io/offres/audit)) [vendeur] |
| **Hyperstack** (FR) | « Cartographie de la maturité data et IA », analyse de la qualité des données, **10 cas d'usage IA ou plus, priorisés par ROI**, **feuille de route sur 12 mois**, conformité à l'AI Act | « Quelques jours à 2 semaines ». Prix non affiché sur la page | [vérifié] [Hyperstack](https://www.hyperstack.studio/transition-ia) [vendeur] |
| | Côté audit : carte des processus, périmètre V1 chiffré en jours, architecture cible, plan V1/V2/V3 | 800 € HT par jour. « Audit Flash » de 1 à 2 jours (800 à 2 400 €) | [relayé] ([blog Hyperstack](https://www.hyperstack.studio/blog/audit-ia-entreprise)) [vendeur] |
| **Guides FR** (flowt, koino, juwa) | Quatre livrables : état des lieux, **matrice des cas d'usage impact × effort**, feuille de route (gains rapides, prérequis data, pilotes, gros chantiers), recommandations de formation. Notation de 1 à 5 sur cinq critères : impact, faisabilité data, complexité du SI, risque et conformité, délai | 2 à 8 semaines | [relayé] ([flowt](https://flowt.fr/blog/diagnostic-data-ia-etapes-opportunites-flowt/), [koino](https://www.koino.fr/articles/audit-ia-entreprise-methode-5-etapes), [juwa](https://juwa.co/blog/guides-methodes-ia/audit-ia-livrables-a-exiger/)) [vendeur] |
| **Équivalents anglo-saxons** | Grille 2×2 **effort × ROI** (gains rapides, paris stratégiques, petits gains). Note de préparation sur 6 axes (données, infra, cloud, intégration, compétences, gouvernance) de 1 à 5, où l'on regarde **la note la plus basse** plutôt que la moyenne. Paquet type : synthèse dirigeant, rapport de préparation, matrice d'opportunités, feuille de route à 90 jours, présentation | — | [relayé] ([SoluLab](https://www.solulab.com/ai-readiness-assessment-for-smbs/), [AUC1](https://blog.auc1consulting.com/ai-readiness-assessment-5-steps-to-know-if-your-business-is-actually-ready-for-ai/), [GoWest](https://www.gowest.ai/services/ai-readiness-assessment/)) [vendeur] |
| **Aide publique (FR)** | Le « Diag Data IA » de Bpifrance finance une partie du diagnostic | Le taux varie selon les sources | [relayé], à vérifier auprès de Bpifrance |

**Ce que tous ces livrables ont en commun** [déduction] : ils partent d'**entretiens** et d'**ateliers**. Les cas d'usage viennent de ce que les gens **disent** faire. Notre produit remplace cette étape par **une semaine de mesure** et garde le format de sortie que le dirigeant connaît déjà : matrice, ROI, feuille de route.

---

## 5. Comment les entreprises mesurent l'usage de l'IA

### Microsoft Copilot Dashboard (Viva Insights) [vérifié] [vendeur]
Sources : [doc du tableau de bord](https://learn.microsoft.com/en-us/viva/insights/org-team-insights/copilot-dashboard) et [rapport d'impact](https://learn.microsoft.com/en-us/viva/insights/advanced/analyst/templates/microsoft-365-copilot-impact).

- **4 familles d'indicateurs** : préparation, adoption, impact, ressenti.
- **Utilisateur actif** : au moins un jour avec une action Copilot. Le seuil est réglable (1 jour sur la période, 1 jour toutes les 4 semaines ou 1 jour par semaine).
- **Niveaux d'usage** sur 12 semaines :
  - *Power users* : 15 actions ou plus par semaine, et actifs au moins 9 semaines sur 12.
  - *Habituels* : de 1 à 14 actions par semaine, et actifs au moins 9 semaines sur 12.
  - *Novices* : au moins 1 action, mais pas régulièrement.
- **Utilisateurs qui reviennent** : actifs sur deux périodes de suite.
- **Heures assistées** : estimées par Microsoft à partir des actions et de coefficients issus de ses études. **Valeur** = heures × taux horaire, **72 $ par défaut**. Microsoft prévient que c'est une estimation et que la méthode évoluera.
- **Taux de satisfaction** : pouces levés divisés par le total des réactions.
- **Avant / après** : on compare les 4 semaines avant l'adoption et les 4 semaines après, avec la mise en garde que Copilot n'est pas seul en cause.
- **Confidentialité** : rien n'est affiché sous la « taille minimale de groupe » fixée par l'entreprise. L'exemple de la doc est un groupe de 10 personnes.

### Shopify, mémo de Tobi Lütke (avril 2025) [relayé]
Sources : [copie Readwise du mémo](https://readwise.io/reader/shared/01jr9218k2nf651ygvwygxrk0w/), [BetaKit](https://betakit.com/shopify-ceo-tobi-lutke-tells-employees-to-prove-ai-cant-do-the-job-before-asking-for-resources/). Je n'ai pas pu lire le post original sur X.

- Un usage **réflexe** de l'IA est le minimum attendu, dirigeants compris.
- L'IA doit être utilisée dès la phase de prototype.
- **Des questions sur l'usage de l'IA entrent dans les évaluations de performance et entre collègues.** Les questions exactes ne sont pas publiques.
- **Avant de demander un recrutement, une équipe doit montrer pourquoi l'IA ne peut pas faire le travail.** Le mémo pose la question : « à quoi ressemblerait ce domaine si des agents autonomes faisaient déjà partie de l'équipe ? »

### ActivTrak [vérifié] [vendeur]
Source : [ActivTrak, 443 millions d'heures](https://www.activtrak.com/blog/443-million-hours-data-ai-adoption-impact/). Mesuré sur le comportement réel, pas par sondage : 163 638 salariés dans 1 111 entreprises.

- Part des salariés qui utilisent des outils IA : 52 % en 2023, **80 % en 2025**. En moyenne, 7 outils IA par entreprise en 2025, contre 2 en 2023.
- **57 % des utilisateurs d'IA y passent moins de 1 % de leur temps de travail.** Les utilisateurs « les plus productifs » y passent 7 à 10 % de leur journée, mais ils ne sont que 3 %.
- Sur 10 584 salariés, 180 jours après l'adoption de l'IA : mails +104 %, messagerie +145 %.
- 50 % des dirigeants interrogés ne mesurent pas encore l'impact de l'IA. Cette enquête est séparée et sa taille n'est pas donnée.

### Worklytics [vérifié sur la page, méthode non décrite] [vendeur]
Source : [Worklytics](https://www.worklytics.co/blog/how-to-measure-ai-skills-across-your-workforce).

- Indicateurs : jours actifs IA par semaine, usages par jour actif, outils distincts par semaine, part des utilisateurs mono-outil.
- L'utilisateur actif médian utilise 1,8 outil par semaine et fait 3,4 interactions par jour actif. 54 % des actifs n'utilisent qu'un seul outil, ce que Worklytics lit comme le signe d'un usage superficiel.
- **Taille de l'échantillon et définition d'« actif » non publiées.**

### Contexte France
- **INSEE** [vérifié, [Insee Première n° 2120, juil. 2026](https://www.insee.fr/fr/statistiques/9025878)] : 18 % des entreprises de 10 salariés ou plus utilisent au moins une technologie d'IA en 2025.
  - Par taille : 15 % de 10 à 49 salariés, 31 % de 50 à 249, 58 % au-delà de 250.
  - Freins : chez les non-utilisatrices, l'IA « n'est pas jugée utile » (71 %) et elles manquent d'expertise (54 %).
- **Bpifrance Le Lab** [relayé, [Le Journal des entreprises](https://www.lejournaldesentreprises.com/article/seuls-32-des-pme-et-eti-utilisent-reellement-lintelligence-artificielle-selon-bpifrance-2120954)] : 32 % des PME et ETI utilisent réellement l'IA, 26 % l'IA générative (juin 2025, environ 1 200 dirigeants). Un autre baromètre (janv. 2026, TPE-PME) donne 55 % des **dirigeants** utilisateurs d'IA générative. Les deux ne sont pas comparables.
- [déduction] **L'écart est énorme entre ce que déclare l'entreprise (18 %) et ce que font les salariés** (BCG 72 %, ActivTrak 80 %). Personne ne mesure cet écart en PME française. Nous, si.

---

## 6. Synthèse pour nous

### 6.1 Les 15 métriques

Légende de la colonne « screenpipe » :
- **Direct** : se calcule avec l'app, l'URL, le titre de fenêtre et les événements, sans LLM.
- **LLM** : il faut qu'un LLM lise le texte de l'écran ou de l'audio **en local** pour étiqueter. Seule l'étiquette sort.
- **Non** : screenpipe ne peut pas la mesurer.

Toutes les colonnes « screenpipe » et « affichage » sont des **[déductions]**. Seules les colonnes « qui la regarde » renvoient à des sources.

| # | Métrique | Qui la regarde (source § ci-dessus) | screenpipe | Au dirigeant ? Comment l'afficher (agrégats ≥ 3 personnes) |
|---|---|---|---|---|
| 1 | **Adoption IA hebdomadaire** : nombre de volontaires actifs au moins un jour sur un outil IA | Copilot Dashboard, Worklytics, BCG, McKinsey | **Direct** (domaines chatgpt.com, claude.ai, gemini, copilot, mistral… et apps de bureau) | **Oui.** « 6 personnes sur 9 ont utilisé l'IA cette semaine ». Une seule ligne d'équipe, jamais de liste de noms |
| 2 | **Profondeur d'usage** : part du temps de travail dans les outils IA et jours actifs sur 5 | ActivTrak (repère 7 à 10 %), Copilot (niveaux d'usage) | **Direct** | **Oui**, en distribution : « 1 % ou moins / 1 à 7 % / plus de 7 % ». Une tranche de moins de 3 personnes est fusionnée avec la voisine |
| 3 | **Outils IA utilisés et IA « perso »** : outils fournis par l'entreprise ou non, nombre d'outils par personne | Microsoft BYOAI (78 %), BCG (54 % sans autorisation), Worklytics (mono-outil) | **Direct** pour l'outil. **LLM** pour reconnaître un compte perso ou pro (ce n'est pas toujours lisible) | **Oui, avec précaution** : liste des outils avec le nombre d'utilisateurs (≥ 3). Le présenter comme « une demande non servie », jamais comme une faute |
| 4 | **Mode d'usage de l'IA** : déléguer, itérer, apprendre, vérifier | Anthropic Economic Index (5 modes) | **LLM** (lit l'échange à l'écran, ne garde que la catégorie) | **Oui** : un camembert d'équipe « automatisation vs augmentation » |
| 5 | **À quoi sert l'IA** : rédaction, recherche, code, analyse, traduction… | Anthropic (tâches O*NET), Worklytics (catégories) | **LLM** | **Oui**, top 5 des usages pour l'équipe |
| 6 | **Temps par catégorie de tâche et par app** (h/semaine) | Process Advisor, UiPath, Celonis, ActivTrak | **Direct** pour les apps. **LLM** pour les catégories | **Oui**, c'est la slide « où part le temps », en heures cumulées de l'équipe |
| 7 | **Fragmentation** : changements d'app par heure, durée médiane avant de changer, nombre de blocs de concentration de 25 min ou plus | Microsoft (interruption toutes les 2 min), Gloria Mark (47 s), KYP, Skan | **Direct** | **Oui**, en médiane d'équipe : « vos équipes restent X s sur un écran ; la moyenne publiée est de 47 s » |
| 8 | **Ressaisie entre apps** : paires d'apps les plus fréquentes, avec le nombre de copier-coller et les minutes associées | Process Advisor (paires = saisie manuelle), Soroco (bascules et copier-coller), Celonis | **Direct** (déclencheur copier-coller et changement de fenêtre) | **Oui, c'est la slide la plus actionnable** : « Excel → CRM : 23 copier-coller par jour, environ N h par semaine, chez 4 personnes » |
| 9 | **Tâches répétitives** : occurrences × durée médiane × nombre de personnes | UiPath (traces, utilisateurs, temps médian), Process Advisor | **Direct** pour les séquences. **LLM** pour nommer la tâche | **Oui**, seulement les tâches faites par 3 personnes ou plus. Sinon, on la regroupe dans une catégorie |
| 10 | **Variantes** : nombre de façons de faire une même tâche et écart de durée | Process Advisor (variantes), Soroco (variance) | **Direct + LLM** (regrouper les séquences proches) | **Oui** : « 4 façons de faire, de 12 à 40 min ». **Jamais qui est le plus lent** |
| 11 | **Exposition IA des tâches observées** : part des heures en E0, E1 ou E2 | Eloundou et al. | **LLM** avec la rubrique publique | **Oui** : « X % des heures observées portent sur des tâches qu'un LLM seul accélère de 50 % ou plus ; Y % avec un outil » |
| 12 | **Coût et économie possible par tâche** : fréquence × durée × personnes × coût horaire | Copilot (heures × 72 $), Hyperstack (ROI), matrices des guides | **Direct + onboarding** (coût horaire donné par le dirigeant) | **Oui**, **en fourchette** (bas et haut) et en heures plutôt qu'en euros si le coût est incertain |
| 13 | **Attente et blocages** : écrans d'attente, relances, allers-retours avec validation | Skan (attente), Celonis, process mining | **Partiel, LLM**. On voit l'attente à l'écran, pas l'attente entre deux personnes | Oui si le signal est net, sinon en annexe |
| 14 | **Temps en réunion et suites de réunion** : heures de réunion, part des réunions improvisées, actions à faire | Microsoft « infinite workday » | **Direct** pour la détection. **LLM** pour les actions | **Oui**, en heures d'équipe. Le contenu des réunions ne sort jamais |
| 15 | **Envie d'automatiser** et niveau d'implication souhaité (H1 à H5) | Stanford WORKBank | **Non**. C'est une question posée au salarié dans la page de relecture | **Oui** : matrice feu vert / feu rouge. C'est aussi la meilleure protection contre « on va remplacer les gens » |

**Ce qu'on ne mesure pas** :
- L'EBIT et la vraie valeur (McKinsey, BCG).
- La qualité du résultat (jagged frontier).
- La qualité des données et la gouvernance (Gartner, guides FR).
- Le travail hors écran.

Il faut le dire au dirigeant : notre diagnostic couvre « travail et usage ». Pour « stratégie et données », on ajoute un court questionnaire. [déduction]

**Règle d'affichage** [déduction] : Microsoft masque tout groupe sous une taille minimale, et l'exemple de sa doc est de 10 personnes. **Notre seuil de 3 est plus faible.** Dans une équipe de 5, on peut deviner les individus. Je recommande :
- 3 personnes minimum par chiffre, et **5 pour tout ce qui ressemble à de la performance** (variantes, fragmentation) ;
- jamais de classement, jamais de « personne la plus / la moins » ;
- arrondir les petites valeurs (« moins de 1 h ») ;
- garder la règle « rien ne sort sans le clic du salarié », déjà dans `produit/decoupage.md`.

### 6.2 Les insights qui font « wow »

Les chiffres de la PME seront les nôtres. Les références ci-dessous servent de **point de comparaison sourcé** sur la slide.

1. **« Vos équipes recopient N heures par semaine d'une app à l'autre. »**
   - Top 3 des paires d'apps × copier-coller × personnes. C'est concret et chiffré, et ça se transforme directement en workflow (E2).
   - Sources : Microsoft et Soroco traitent ces paires comme des signaux de saisie manuelle.
2. **« L'IA est déjà chez vous, mais en surface, et en partie hors de votre contrôle. »**
   - X personnes sur Y l'utilisent, mais la plupart y passent moins de 1 % de leur temps.
   - Repères : 57 % des utilisateurs chez ActivTrak sont sous 1 %, et les plus avancés sont à 7-10 %.
   - Les outils sont en partie personnels : 78 % de BYOAI selon Microsoft, et 54 % des salariés utiliseraient l'IA sans autorisation selon BCG.
   - C'est un risque pour les données, et la preuve que la demande existe.
3. **« Une même tâche, quatre façons de la faire. »**
   - Les variantes et l'écart de durée entre personnes, sans noms.
   - Message de cabinet : **standardiser avant d'automatiser**. C'est la logique du 70 % de BCG et du « refaire les processus » de McKinsey.
4. **« X % de vos heures observées sont sur des tâches où l'IA fait gagner au moins 50 % du temps. »**
   - Rubrique E1/E2 d'Eloundou appliquée à la PME, filtrée par l'envie des salariés (feu vert de Stanford).
   - On ne promet pas les 50 %. Le jagged frontier montre −19 points de bonnes réponses hors frontière, donc on signale aussi **les tâches où l'IA est risquée**.
5. **« Vos équipes restent en moyenne X secondes sur un écran. »**
   - Fragmentation mesurée, comparée aux 47 s de Gloria Mark et à « une interruption toutes les 2 min » chez Microsoft.
   - Option : comparer avec **ce que les gens pensaient** (question d'onboarding). METR montre que le ressenti peut se tromper de 40 points.

### 6.3 Les méthodes de cabinet à reprendre telles quelles

1. **Rubrique E0/E1/E2 d'Eloundou** : la passer à un LLM, tâche par tâche, avec la définition exacte (au moins 50 % de temps en moins à qualité égale). E1 donne une recommandation de **formation ou de prompt**. E2 donne un **workflow ou un outil**.
2. **Les 5 modes d'Anthropic** (directive, feedback loop, itération, apprentissage, validation) pour classer chaque usage d'IA observé. Le Wrapped peut afficher le mix « automatisation vs augmentation ».
3. **Matrice de Stanford, désir × capacité** : une question de 1 à 5 par tâche dans la page de relecture, plus la capacité estimée par le LLM. Le résultat, ce sont **4 zones**, et on recommande seulement le feu vert.
4. **Matrice valeur × faisabilité des audits PME**, avec 5 critères notés de 1 à 5 (impact, faisabilité data, complexité SI, risque, délai) et la règle **« la note la plus basse bloque »**. La valeur vient de notre mesure (métrique 12), pas d'un atelier.
5. **KPI de Process Advisor et d'UiPath** tels quels : occurrences, personnes, temps médian, nombre de variantes, paires d'apps. Ce sont des termes que les DSI connaissent déjà.
6. **Niveaux d'usage Copilot** (power, habituel, novice), adaptés à 5 jours. Par exemple : actif 4 ou 5 jours = habituel, 1 à 3 jours = novice. [déduction : les seuils de Microsoft sont sur 12 semaines et ne se transposent pas tels quels]
7. **Calculateur heures × taux horaire** à la manière de Copilot : un taux par défaut que le dirigeant peut modifier, et la mention « estimation » à côté.
8. **Livrable final au format des cabinets FR** : 10 cas d'usage priorisés ou plus, feuille de route sur 12 mois découpée en « gains rapides / pilotes / gros chantiers », recommandations de formation. Repère de prix du marché : 800 à 1 100 € HT par jour, soit environ 1 000 à 5 500 € pour 1 à 5 jours.
9. **Grille 10/20/70 de BCG** pour équilibrer les recommandations : la majorité doit porter sur **les personnes et les processus** (formation, nouvelle façon de faire), pas sur l'outil.
10. **Étapes du MIT CISR** pour situer la PME en une phrase. Par exemple, « étape 1, expérimenter », si l'usage est individuel et sans outil commun. [déduction : le MIT ne donne pas de règle de classement automatique]
11. **Question de Shopify** à proposer au dirigeant : « avant de recruter, montrer pourquoi l'IA ne peut pas faire ce travail ». Elle se branche directement sur notre liste de tâches.

---

## 7. Ce qui n'est pas vérifié

- **McKinsey 2025** : la page primaire ne se charge pas (délai dépassé à trois essais). Les 88 % et 39 % viennent d'extraits de la page dans les résultats de recherche. Les 6 % de « high performers » et l'écart sur la refonte des processus viennent seulement de résumés, qui ne donnent pas les mêmes chiffres.
- **Gartner** : le communiqué est vérifié. Les 7 piliers et les noms des 5 niveaux viennent de blogs, car le modèle complet est payant.
- **UiPath** : la doc « latest » renvoie une erreur 404. Les définitions viennent de versions 2021 à 2023. Le retrait du mode « unassisted » n'est pas vérifié.
- **Shopify** : je n'ai pas pu lire le post original sur X (erreur 402). J'ai lu une copie Readwise et la presse.
- **Accenture** : rien trouvé d'utilisable et de vérifiable.
- **Lonestone** : le prix vient d'un résultat de recherche. Je n'ai pas ouvert la page moi-même.
- **BCG, effet de la formation (79 % contre 67 %)** : relayé par la presse, absent du communiqué BCG que j'ai lu.
- **Toutes les colonnes « screenpipe » et « affichage »** du § 6.1 sont mes déductions. Il faut les tester sur nos vraies données avant de les annoncer. Je n'ai par exemple **pas vérifié** combien d'événements copier-coller screenpipe capte sur une vraie journée : l'échantillon du brief n'en compte que 4.
- **Sources vendeurs** : Microsoft (WTI, Copilot, Process Advisor), UiPath, Celonis, Soroco, Skan, KYP.ai, ActivTrak, Worklytics, Hyperstack, Lonestone et les guides FR et anglo-saxons. Leurs chiffres sont réels sur leurs pages, mais leurs méthodes ne sont pas auditées.

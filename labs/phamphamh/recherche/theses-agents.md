# Les thèses de déploiement d'agents IA — ce qu'en disent les meilleurs

Recherche du 17/10/2026 pour le hackathon screenpipe × 42 Paris.
But : donner au client, après l'audit, **un choix entre 7 « thèses »** (des façons de déployer des agents), chacune fondée sur ce qu'écrivent les équipes qui en font tourner en production.

## Comment lire ce document

- **[vérifié]** = j'ai lu la source à l'URL indiquée et l'affirmation y figure. Les phrases entre guillemets « … » sont des citations relues sur la source (en anglais d'origine, traduites ou non).
- **[secondaire]** = je n'ai pas pu lire la source d'origine (paywall, PDF qui ne charge pas, post X) ; l'info vient d'un article qui la rapporte.
- **[déduit]** = c'est notre traduction pour le produit (screenpipe, skills Claude Code, pipes). Ce n'est écrit par aucun auteur cité.
- Échelle d'autonomie utilisée partout : **1 = suggère**, **2 = prépare et l'humain valide**, **3 = agit et notifie**, **4 = autonome**.

---

## 0. Ce sur quoi tout le monde est d'accord (le socle commun)

Avant les désaccords, six points qui reviennent chez presque tous les auteurs. Ils valent pour **toutes** les thèses.

1. **Commencer simple, ajouter de la complexité seulement si elle prouve qu'elle sert.** Anthropic : « find the simplest solution possible, and only increasing complexity when needed » [vérifié — https://www.anthropic.com/research/building-effective-agents]. OpenAI : « customers typically achieve greater success with an incremental approach » [vérifié — https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf].
2. **Les erreurs s'additionnent à chaque étape.** Chip Huyen : « If the model's accuracy is 95% per step, over 10 steps, the accuracy will drop to 60% » [vérifié — https://huyenchip.com/2025/01/07/agents.html]. Anthropic : « Agents are stateful and errors compound » [vérifié — https://www.anthropic.com/engineering/multi-agent-research-system].
3. **Le contexte donné au modèle est le levier n°1.** Harrison Chase : « The hard part of building reliable agentic systems is making sure the LLM has the appropriate context at each step » [vérifié — https://www.langchain.com/blog/how-to-think-about-agent-frameworks]. Philipp Schmid : la plupart des échecs d'agents « are not model failures anyemore, they are context failures » (sic) [vérifié — https://www.philschmid.de/context-engineering].
4. **Réussir une fois ne veut pas dire être fiable.** Sierra a créé la mesure *pass^k* (réussir la même tâche k fois de suite) ; le meilleur agent testé tombait à environ 25 % en pass^8 sur le commerce de détail [vérifié — https://sierra.ai/blog/benchmarking-ai-agents].
5. **Les tâches longues restent fragiles.** METR : la durée des tâches qu'un agent réussit à 50 % double environ tous les 7 mois, mais le succès est presque total sous 4 minutes de travail humain et tombe sous 10 % au-delà d'environ 4 heures [vérifié — https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/].
6. **Les actions risquées passent par un humain, au moins au début.** OpenAI : les actions « sensitive, irreversible, or have high stakes should trigger human oversight until confidence in the agent's reliability grows » [vérifié — guide OpenAI ci-dessus].

**Retours terrain qui montrent le prix de l'excès d'autonomie :**
- Klarna, mai 2025 : après avoir misé sur l'IA pour le service client, le PDG dit à Bloomberg que la qualité était plus basse et réembauche des humains ; « there will always be a human if you want » [secondaire — https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396].
- Karpathy, octobre 2025 : les agents « They're cognitively lacking and it's just not working. It will take about a decade to work through all of those issues » ; il conseille de les voir « almost like an employee or an intern » [vérifié via Fortune — https://fortune.com/2025/10/20/workers-fear-ai-job-cuts-open-ai-co-founder-says-ai-agents-will-take-a-decade-before-they-even-work-they-dont-have-enough-intelligence-unemployment-automation-2035].
- MIT NANDA (rapport préliminaire, juillet 2025) : environ 95 % des pilotes d'IA générative en entreprise ne passent pas à l'échelle ; l'auteur parle d'un « learning gap » : les outils génériques ne s'adaptent pas aux processus de l'entreprise [secondaire — https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/ ; nuance sur l'échantillon : https://letsdatascience.com/news/mit-report-documents-genai-pilot-roi-gap-e0924d7d].
- McKinsey (sept. 2025, revue de plus de 50 projets agentiques) : la valeur vient de la refonte du processus métier, pas de l'agent lui-même ; les agents ne sont pas toujours la bonne réponse [secondaire — PDF : https://www.mckinsey.com/~/media/mckinsey/business%20functions/quantumblack/our%20insights/one%20year%20of%20agentic%20ai%20six%20lessons%20from%20the%20people%20doing%20the%20work/one-year-of-agentic-ai-six-lessons-from-the-people-doing-the-work_final.pdf — le PDF n'a pas chargé chez moi, résumé lu sur https://richturrin.substack.com/p/top-six-agentic-ai-deployment-lessons].

**Ce que ça veut dire pour nous [déduit]** : screenpipe nous donne ce qui manque à la plupart des projets : **les vraies traces du travail** (ce qui a été vu, tapé, cliqué). C'est exactement la matière que les auteurs « évals d'abord » réclament, et c'est ce qui permet de mesurer le temps gagné après coup. Le « learning gap » du MIT est notre angle : on part du processus réel observé, pas d'un outil générique.

---

## 1. Les Rails d'abord

> **Accroche** : du code fixe pour le chemin, l'IA seulement aux carrefours où il faut comprendre du texte.

**Auteurs principaux**
- Anthropic, *Building effective agents* (19/12/2024) — https://www.anthropic.com/research/building-effective-agents
- Dex Horthy / HumanLayer, *12-Factor Agents* — https://github.com/humanlayer/12-factor-agents
- OpenAI, *A practical guide to building agents* (2025) — https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- Decagon, *Agent Operating Procedures* — https://decagon.ai/blog/from-sops-to-agent-operating-procedures
- Sierra, *Agent development life cycle* (03/06/2024) — https://sierra.ai/blog/agent-development-life-cycle

**L'idée en une phrase** : la plupart des « agents » qui marchent en production sont surtout du logiciel classique, avec quelques appels au modèle placés aux bons endroits.

**Ce que disent les sources [vérifié]**
- Anthropic sépare les **workflows** (« systems where LLMs and tools are orchestrated through predefined code paths ») des **agents** (le modèle décide lui-même de ses étapes). Les workflows conviennent aux tâches bien définies qui demandent de la prévisibilité. Cinq patrons de workflow : enchaînement de prompts avec contrôles entre les étapes, aiguillage (routing), parallélisation, orchestrateur-exécutants, évaluateur-optimiseur. — URL Anthropic ci-dessus.
- HumanLayer : beaucoup de produits vendus comme agents sont « mostly deterministic code, with LLM steps sprinkled in at just the right points » ; et « 80% isn't good enough for most customer-facing features ». Facteur 8 : « Own your control flow » ; on doit pouvoir arrêter la boucle avant une action à fort enjeu et attendre l'accord d'un humain. — https://github.com/humanlayer/12-factor-agents et https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md
- OpenAI : on ne construit un agent que si la tâche demande du jugement nuancé, des règles devenues ingérables, ou beaucoup de données non structurées ; sinon « a deterministic solution may suffice ». — guide OpenAI.
- Decagon : les procédures sont écrites en langage courant puis « compile into structured logic » ; « The code-based logic ensures that critical actions are executed correctly every time » (remboursements, vérification d'identité). Attention : contenu commercial du vendeur. — URL Decagon ci-dessus.
- Sierra : « deterministic guardrails that the agent cannot cross » et des versions figées d'agent qu'on peut annuler instantanément. — URL Sierra ci-dessus.

**Principes concrets**
1. Dessiner le processus comme une suite d'étapes fixes ; ne mettre le modèle que là où il faut lire, classer ou rédiger.
2. Mettre un contrôle automatique (une « porte ») entre chaque étape : format, champs obligatoires, montants.
3. Les actions critiques (paiement, envoi, suppression) sont du code, jamais une décision libre du modèle.
4. Chaque version du workflow est figée et peut être annulée en un geste.
5. Garder la main sur la boucle : on peut mettre en pause, reprendre, et demander un accord avant l'action.

**Quand la choisir** : processus répétitifs et stables (saisie, relances, rapprochements, reporting), entreprise peu tolérante au risque, PME sans équipe technique, secteurs régulés. C'est la thèse par défaut pour un premier déploiement.

**Risques** : rigide quand le processus change ; ne gère pas bien les cas imprévus ; peut finir en usine à gaz de règles (c'est justement le cas où OpenAI conseille un agent).

**Garde-fous** : contrôles entre étapes ; liste blanche des actions ; tout cas qui sort du rail part à un humain ; versions figées et retour arrière.

**Traduction dans un workflow déployé [déduit]**
- **Autonomie : 3** sur le rail (agit et notifie), avec bascule vers un humain dès qu'une porte échoue.
- **Où est l'humain** : il valide le dessin du rail au départ et traite les exceptions.
- **Tests avant déploiement** : rejouer 20 à 50 cas réels tirés des captures screenpipe (la même tâche faite à la main) et vérifier que chaque étape produit la même sortie ; tester chaque porte avec des entrées volontairement fausses.
- **Suivi après** : temps passé sur la tâche avant/après mesuré par screenpipe ; taux de cas sortis du rail ; taux de correction humaine ; nombre de retours arrière.

**Mini-schéma**
1. Déclencheur (fichier reçu, heure, événement vu par screenpipe)
2. Étape fixe : on récupère les données
3. Appel au modèle : lire / classer / rédiger
4. Porte de contrôle automatique → si échec, file d'attente humaine
5. Action en code + notification

---

## 2. Un Seul Cerveau

> **Accroche** : un seul agent, qui voit tout le dossier, plutôt qu'une équipe d'agents qui se comprennent mal.

**Auteurs principaux**
- Walden Yan / Cognition, *Don't Build Multi-Agents* (12/06/2025) — https://cognition.com/blog/dont-build-multi-agents
- Anthropic, *Effective context engineering for AI agents* (29/09/2025) — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, *Agent Skills* (16/10/2025) — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- OpenAI, guide pratique (2025) — URL ci-dessus
- Drew Breunig, *How Contexts Fail* (22/06/2025) et *How to Fix Your Context* (26/06/2025) — https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html, https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html
- Harrison Chase, *How to think about agent frameworks* (20/04/2025) — URL ci-dessus

**L'idée en une phrase** : la fiabilité vient d'un seul agent qui garde tout le fil de la tâche, avec un contexte soigné (ni trop, ni trop peu), plutôt que de plusieurs agents qui prennent des décisions contradictoires.

**Ce que disent les sources [vérifié]**
- Cognition, deux principes : « Share context, and share full agent traces, not just individual messages » et « Actions carry implicit decisions, and conflicting decisions carry bad results ». Exemple : deux sous-agents chargés d'un clone de Flappy Bird produisent un décor style Mario et un oiseau qui ne va pas avec. Conclusion : « running multiple agents in collaboration only results in fragile systems » (en 2025). Le « context engineering » est « effectively the #1 job of engineers building AI agents ». — URL Cognition.
- OpenAI : « Our general recommendation is to maximize a single agent's capabilities first » ; souvent « a single agent with tools is sufficient ». — guide OpenAI.
- Anthropic : viser « the smallest possible set of high-signal tokens » ; la précision baisse quand le contexte grossit (« context rot ») ; charger l'information au moment où on en a besoin, résumer (compaction), prendre des notes hors du contexte. — URL context engineering.
- Anthropic, Skills : des dossiers d'instructions, scripts et ressources que l'agent charge seulement quand c'est utile (« progressive disclosure ») ; les scripts donnent des résultats déterministes. — URL Skills.
- Breunig : quatre façons dont le contexte casse : empoisonnement (une erreur reste et est réutilisée), distraction (trop long), confusion (contenu inutile, trop d'outils), conflit (infos contradictoires). « It turns out there can be such a thing as too many tools. » Remèdes : ne charger que les outils utiles, isoler, élaguer, résumer, décharger dans des notes ; « Is everything in this context earning its keep? » — URLs Breunig.

**Principes concrets**
1. Un agent par tâche métier, qui garde tout l'historique de ce qu'il a fait.
2. Peu d'outils, bien nommés et bien décrits (Anthropic : « More tools don't always lead to better outcomes » — https://www.anthropic.com/engineering/writing-tools-for-agents).
3. Le savoir-faire de l'entreprise est rangé en skills chargées à la demande, pas tout dans le prompt.
4. Pour les tâches longues : notes écrites hors contexte et résumés réguliers.
5. Une vérification exécutable à la fin (test, script, comparaison) pour que l'agent sache s'il a fini (doc Claude Code : « If you can't verify it, don't ship it » — https://code.claude.com/docs/en/best-practices).

**Quand la choisir** : tâches de connaissance où tout se tient (préparer un dossier client, rédiger une proposition, faire une analyse, coder) ; équipes à l'aise avec un outil comme Claude Code ; tolérance au risque moyenne.

**Risques** : la fenêtre de contexte finit par saturer sur les très longues tâches (Cognition le reconnaît) ; un seul point de défaillance ; plus le contexte grossit, plus la qualité baisse.

**Garde-fous** : contexte minimal et propre ; recommencer à neuf plutôt que corriger trois fois ; vérification automatique de fin ; permissions limitées sur les outils.

**Traduction dans un workflow déployé [déduit]**
- **Autonomie : 3** (agit et notifie avec la preuve de son travail).
- **Où est l'humain** : il donne la tâche et relit le résultat final avec les preuves (sortie de test, capture, sources).
- **Tests avant déploiement** : rejouer les cas observés par screenpipe avec la skill ; mesurer si l'agent déclenche la bonne skill ; vérifier le résultat final, pas le chemin.
- **Suivi après** : temps gagné par tâche (screenpipe) ; taux de reprise par l'humain ; longueur moyenne de contexte avant échec ; nombre de relances nécessaires.

**Mini-schéma**
1. L'humain lance la tâche (ou un pipe la lance)
2. L'agent charge seulement les skills et données utiles
3. Il travaille en boucle, prend des notes, résume si besoin
4. Il lance la vérification de fin
5. Il rend le résultat + les preuves

---

## 3. L'Armure, pas le Robot

> **Accroche** : l'IA prépare, l'humain vérifie vite — et c'est lui qui règle le curseur d'autonomie.

**Auteurs principaux**
- Andrej Karpathy, *Software Is Changing (Again)*, keynote AI Startup School (juin 2025) — vidéo https://www.youtube.com/watch?v=LCEmiRjPEtQ, transcription https://prepublish.ai/youtube-transcript/LCEmiRjPEtQ
- Karpathy au Dwarkesh Podcast (oct. 2025), rapporté par Fortune — URL ci-dessus
- Chip Huyen, *Agents* (07/01/2025) — https://huyenchip.com/2025/01/07/agents.html
- Feng, McDonald, Zhang, *Levels of Autonomy for AI Agents* (juin 2025) — https://arxiv.org/abs/2506.12469
- Anthropic, *Measuring AI agent autonomy in practice* (18/02/2026) — https://www.anthropic.com/research/measuring-agent-autonomy

**L'idée en une phrase** : construire des outils qui augmentent l'humain (comme l'armure d'Iron Man) avec un curseur d'autonomie, plutôt que des robots qui remplacent l'humain.

**Ce que disent les sources [vérifié]**
- Karpathy (transcription automatique YouTube) : il parle de « partial autonomy apps » ; « you are in charge of the autonomy slider » ; « there should be an autonomy slider in your product » ; dans la boucle, l'IA génère et « we as humans are doing the verification », et il faut rendre cette boucle aussi rapide que possible ; « we have to keep the AI on the leash » ; « it's less Iron Man robots and more Iron Man suits that you want to build » ; « this is the decade of agents ». Il rappelle un trajet Waymo sans intervention en 2013, alors que l'autonomie complète a pris bien plus longtemps. — URL transcription.
- Chip Huyen : séparer le plan de l'exécution (« planning should be decoupled from execution ») ; faire valider le plan ; demander l'accord explicite pour les actions risquées ; définir clairement le niveau d'automatisation de chaque action. — URL Huyen.
- Feng et al. : le niveau d'autonomie « can be treated as a deliberate design decision », séparé de ce que l'agent sait faire ; cinq niveaux selon le rôle de l'humain : opérateur, collaborateur, consultant, approbateur, observateur. — URL arXiv.
- Anthropic (données réelles de Claude Code) : les nouveaux utilisateurs approuvent chaque action ; les utilisateurs expérimentés laissent tourner en auto-approbation dans plus de 40 % des sessions mais interrompent plus souvent (environ 9 % des tours contre 5 %) ; la confiance se construit avec l'usage. Les auteurs parlent de « deployment overhang » : les modèles pourraient faire plus que ce qu'on leur confie. — URL Anthropic.

**Principes concrets**
1. L'IA propose, l'humain dispose : brouillon, pas envoi.
2. Rendre la vérification rapide : une interface qui montre ce qui change (diff, avant/après), pas un pavé de texte.
3. Petits morceaux vérifiables plutôt qu'un gros résultat d'un coup.
4. Un curseur d'autonomie réglable par tâche, qu'on monte quand la confiance est prouvée.
5. Le plan est validé avant l'exécution.

**Quand la choisir** : métiers où l'erreur coûte cher ou engage la responsabilité (juridique, finance, santé, relation client sensible) ; salariés méfiants envers l'IA ; premier contact avec les agents ; tâches où le jugement humain fait la valeur.

**Risques** : gain de temps plafonné par la vitesse de relecture ; fatigue de validation (on clique « OK » sans lire — la doc Claude Code le note : après la dixième approbation, on clique sans relire) ; l'IA peut rester sous-utilisée.

**Garde-fous** : interface de relecture conçue pour aller vite ; mesurer le taux de modification des brouillons ; monter le curseur seulement sur preuve chiffrée.

**Traduction dans un workflow déployé [déduit]**
- **Autonomie : 2** (prépare, l'humain valide), avec certaines sous-tâches à 1 (suggère).
- **Où est l'humain** : à chaque sortie ; il valide, corrige ou rejette.
- **Tests avant déploiement** : sur les cas observés par screenpipe, comparer le brouillon de l'IA à ce que le salarié a réellement produit ; mesurer combien de modifications il aurait fallu.
- **Suivi après** : taux d'acceptation sans modification ; ampleur moyenne des corrections ; temps de relecture vs temps de la tâche à la main (screenpipe) ; règle [déduit] : quand l'acceptation sans modification dépasse un seuil fixé avec le client sur plusieurs semaines, on propose de monter d'un cran.

**Mini-schéma**
1. screenpipe repère le moment où la tâche commence
2. L'IA prépare un brouillon (ou un plan)
3. L'humain voit l'avant/après et valide, corrige ou rejette
4. L'action part seulement après validation
5. On compte les corrections pour régler le curseur

---

## 4. Le Banc d'Essai

> **Accroche** : pas de déploiement sans examen : on mesure les erreurs sur de vrais cas avant et après.

**Auteurs principaux**
- Hamel Husain, *Your AI Product Needs Evals* (29/03/2024) — https://hamel.dev/blog/posts/evals/
- Hamel Husain, *A Field Guide to Rapidly Improving AI Products* (24/03/2025) — https://hamel.dev/blog/posts/field-guide/
- Hamel Husain & Shreya Shankar, *AI Evals FAQ* — https://hamel.dev/blog/posts/evals-faq/
- Shreya Shankar et al., *Who Validates the Validators?* (UIST 2024) — https://arxiv.org/abs/2404.12272
- Eugene Yan, *An LLM-as-Judge Won't Save The Product* (2025) — https://eugeneyan.com/writing/eval-process/
- Anthropic, *Demystifying evals for AI agents* (09/01/2026) — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Sierra, τ-bench et pass^k (20/06/2024) — https://sierra.ai/blog/benchmarking-ai-agents ; simulations (19/08/2025) — https://sierra.ai/blog/simulations-the-secret-behind-every-great-agent
- Decagon, *The future of AI agents is test driven* (23/07/2025) — https://decagon.ai/blog/the-future-of-ai-agents-is-test-driven

**L'idée en une phrase** : les produits IA échouent faute de système d'évaluation ; on regarde les vraies erreurs, on les compte, et l'agent n'est déployé (puis promu) que s'il passe ses tests.

**Ce que disent les sources [vérifié]**
- Hamel : les produits ratés partagent presque toujours la même cause, « a failure to create robust evaluation systems » ; trois niveaux : tests unitaires, évaluation humaine et par modèle, tests A/B ; « You must remove all friction from the process of looking at data ». — URL evals.
- Hamel : l'analyse d'erreurs est « the single most valuable activity in AI development » ; préférer un jugement binaire réussi/raté à une note sur 5 ; donner aux experts métier les moyens d'écrire les prompts. — URL field guide.
- Hamel & Shreya : relire au moins 100 traces ; continuer jusqu'à ce que les nouvelles traces ne révèlent plus de nouveau type d'erreur ; pour un agent, juger d'abord le résultat global (« Treat the agent as a black box and decide whether it met the user's goal »), puis descendre étape par étape ; un tableau « dernier état réussi × première étape ratée » pour trouver où ça casse. — URL FAQ.
- Shankar : « criteria drift » : on a besoin de critères pour juger, mais c'est en jugeant qu'on découvre ses critères. Donc les critères ne peuvent pas être fixés entièrement à l'avance. — URL arXiv.
- Eugene Yan : « First, write some evals; then, build systems that pass those evals » ; un juge automatique ne remplace pas la relecture humaine. — URL Yan.
- Anthropic : « 20-50 simple tasks drawn from real failures is a great start » ; « grade what the agent produced, not the path it took » ; « pass^k for agents where consistency is essential » ; « Read the transcripts! ». — URL Anthropic.
- Sierra : tests générés depuis les procédures internes et les anciennes conversations, un agent juge note chaque simulation, et les agents « should pass them before changes to any journey are published ». — URL simulations.

**Principes concrets**
1. Construire le jeu de tests à partir de vraies tâches et de vraies erreurs, pas de cas imaginés.
2. Juger en réussi/raté, avec une phrase d'explication.
3. Mesurer la constance (pass^k : la même tâche réussie k fois de suite), pas un succès isolé.
4. Chaque changement (prompt, modèle, skill) relance tous les tests ; pas de mise en production si ça régresse.
5. Continuer à relire des traces en production ; les critères évoluent.

**Quand la choisir** : clients qui veulent des preuves chiffrées avant de faire confiance ; processus à volume (beaucoup de répétitions = beaucoup de cas de test) ; déploiements appelés à grandir. C'est aussi la colonne vertébrale de toutes les autres thèses.

**Risques** : coûte du temps au départ (Hamel & Shreya disent y passer 60 à 80 % de leur temps de développement — URL FAQ) ; tests qui ne ressemblent pas à la réalité ; juge automatique mal calibré ; « réussir le test » sans réussir la tâche.

**Garde-fous** : juge automatique recalibré sur des jugements humains ; tests tirés des vraies traces ; relecture régulière d'échantillons ; un responsable des tests côté client.

**Traduction dans un workflow déployé [déduit]**
- **Autonomie : 2 au départ**, puis 3 quand le seuil de tests est atteint (l'autonomie est gagnée par les chiffres).
- **Où est l'humain** : il étiquette les cas (réussi/raté), fixe le seuil d'acceptation, relit un échantillon chaque semaine.
- **Tests avant déploiement** : 20 à 50 cas rejoués à partir des captures screenpipe ; pass^k (par exemple 5 essais par cas) ; un jeu de cas « ne doit pas agir » ; aucun déploiement sous le seuil convenu.
- **Suivi après** : taux de réussite sur un échantillon relu ; taux de correction humaine ; nouvelles erreurs ajoutées au jeu de tests chaque semaine ; temps gagné mesuré par screenpipe.

**Mini-schéma**
1. screenpipe fournit les vraies traces de la tâche
2. On en tire 20 à 50 cas de test étiquetés
3. On fait passer le workflow plusieurs fois par cas (pass^k)
4. Si le seuil est atteint → déploiement ; sinon on corrige
5. En production, chaque erreur relevée devient un nouveau test

---

## 5. Le Majordome Ambiant

> **Accroche** : l'agent travaille en fond sur ce qui se passe, et ne dérange l'humain que pour notifier, demander ou faire valider.

**Auteurs principaux**
- Harrison Chase / LangChain, *Introducing ambient agents* (14/01/2025) — https://www.langchain.com/blog/introducing-ambient-agents
- HumanLayer, *12-Factor Agents*, facteur 7 « Contact humans with tool calls » — https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-07-contact-humans-with-tools.md
- OpenAI, guide pratique, section « Plan for human intervention » — URL ci-dessus
- swyx / Latent Space, *Agent Engineering* (24/03/2025) — https://www.latent.space/p/agent

**L'idée en une phrase** : au lieu d'attendre qu'on lui parle, l'agent écoute un flux d'événements, avance seul sur ce qui est sûr, et passe par une « boîte de réception » quand il a besoin d'un humain.

**Ce que disent les sources [vérifié]**
- Chase : « Ambient agents listen to an event stream and act on it accordingly » ; ils ne sont pas forcément autonomes ; trois façons d'impliquer l'humain : *notify* (« let the user know some event is important, but not take any actions »), *question* (« ask the user a question to help unblock the agent »), *review* (« review an action the agent wants to take »). Une « agent inbox » plutôt que Slack, où les notifications se perdent. Les retours humains servent aussi de mémoire pour que l'agent apprenne. — URL LangChain.
- HumanLayer facteur 7 : l'agent contacte l'humain par un appel d'outil structuré (question, urgence, format oui/non ou choix), l'état est sauvegardé, la boucle s'arrête et reprend quand la réponse arrive ; agents « outer loop » lancés par un cron ou un événement. — URL facteur 7.
- OpenAI : deux déclencheurs d'intervention humaine : dépasser un seuil d'échecs (trop de tentatives) et les actions à haut risque. — guide OpenAI.
- swyx : la confiance (« Delegated Authority ») est « the most overlooked element » ; et des agents qui demandent confirmation avant chaque action externe « get old fast ». — URL Latent Space.

**Principes concrets**
1. Le déclencheur est un événement (un écran, un mail, un fichier, une heure), pas une conversation.
2. Classer chaque action : sans risque (l'agent agit), à valider (l'agent prépare), à signaler (l'agent notifie seulement).
3. Une seule boîte de réception où l'humain voit tout ce qui l'attend.
4. L'agent peut se mettre en pause et reprendre plus tard sans tout recommencer.
5. Chaque réponse humaine est gardée et réutilisée.

**Quand la choisir** : travail interrompu par plein de petites tâches (relances, suivi de dossiers, comptes rendus de réunion, mises à jour CRM) ; managers et indépendants débordés ; tolérance au risque moyenne. C'est la thèse la plus naturelle avec screenpipe, qui est lui-même un flux d'événements.

**Risques** : trop de notifications (l'humain décroche) ; actions faites dans son dos qui surprennent ; demandes de validation à chaque pas qui lassent (swyx).

**Garde-fous** : liste écrite des actions autorisées sans validation ; plafond de notifications par jour ; journal consultable de tout ce que l'agent a fait ; passage à l'humain après N échecs.

**Traduction dans un workflow déployé [déduit]**
- **Autonomie : 3** pour les actions sans risque (agit et notifie), 2 pour le reste (prépare, l'humain valide dans la boîte de réception).
- **Où est l'humain** : dans la boîte de réception ; il répond aux questions et valide les actions sensibles.
- **Tests avant déploiement** : rejouer une journée de captures screenpipe et vérifier que l'agent se déclenche aux bons moments (et pas aux mauvais) ; compter les notifications qu'il aurait envoyées.
- **Suivi après** : notifications par jour et taux d'ouverture ; délai de réponse humaine ; taux d'actions annulées après coup ; temps gagné sur les petites tâches (screenpipe).

**Mini-schéma**
1. screenpipe voit un événement (un écran, une réunion, un mail)
2. Un pipe planifié ou déclenché réveille l'agent
3. L'agent classe : agir / préparer / signaler
4. Ce qui demande un humain arrive dans la boîte de réception
5. La réponse humaine est enregistrée et l'agent reprend

---

## 6. La Brigade

> **Accroche** : une équipe de petits agents spécialisés, chacun sur un poste, un chef qui coordonne — et un seul qui écrit.

**Auteurs principaux**
- Anthropic, *How we built our multi-agent research system* (13/06/2025) — https://www.anthropic.com/engineering/multi-agent-research-system
- HumanLayer, facteur 10 « Small, Focused Agents » — https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-10-small-focused-agents.md
- Harrison Chase, *How and when to build multi-agent systems* (16/06/2025) — https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems
- NVIDIA (Belcak et al.), *Small Language Models are the Future of Agentic AI* (juin 2025) — https://arxiv.org/abs/2506.02153
- Anthropic, patron « routing » et « orchestrator-workers » — https://www.anthropic.com/research/building-effective-agents

**L'idée en une phrase** : découper le travail en petits agents qui font chacun une chose bien, coordonnés par un chef, surtout quand il s'agit de chercher et lire beaucoup en parallèle.

**Ce que disent les sources [vérifié]**
- HumanLayer : « build small, focused agents that do one thing well » ; « 3-10, maybe 20 steps max » par agent pour garder un contexte gérable. — URL facteur 10.
- Anthropic : un agent chef lance des sous-agents qui cherchent en parallèle, chacun dans son propre contexte ; le système multi-agents a fait 90,2 % mieux qu'un seul agent sur leur évaluation interne de recherche ; mais il consomme environ 15 fois plus de tokens qu'une conversation, et ne convient pas aux tâches où tous les agents doivent partager le même contexte ni à la plupart des tâches de code. — URL Anthropic.
- Chase réconcilie Cognition et Anthropic : « read actions are inherently more parallelizable than write actions » ; on parallélise la lecture, un seul agent écrit le résultat final. — URL LangChain.
- NVIDIA : les petits modèles sont « sufficiently powerful, inherently more suitable, and necessarily more economical » pour beaucoup de tâches d'agents ; systèmes mélangeant plusieurs modèles. — URL arXiv.
- Désaccord direct : Cognition (thèse 2) juge les systèmes multi-agents fragiles en 2025. Les deux camps s'accordent sur un point : ça marche pour lire, pas pour écrire à plusieurs.

**Principes concrets**
1. Un agent = un poste précis (extraire, classer, chercher, vérifier), 3 à 10 étapes maximum.
2. Un chef qui découpe et répartit ; des consignes très claires pour chaque sous-agent (sinon ils font le même travail en double, constat d'Anthropic).
3. Paralléliser la lecture ; un seul agent assemble et écrit.
4. Petits modèles pas chers pour les postes simples, gros modèle pour le chef.
5. Chaque poste a ses propres tests.

**Quand la choisir** : tâches larges de recherche ou de veille (étude de marché, revue de documents, analyse d'appels d'offres, audit de nombreux dossiers) ; volume élevé ; tâche à forte valeur qui justifie le coût en tokens.

**Risques** : coût (environ 15 fois plus de tokens selon Anthropic) ; décisions contradictoires entre agents (Cognition) ; débogage plus dur ; pannes en cascade.

**Garde-fous** : un seul rédacteur final ; consignes de mission précises pour chaque sous-agent ; budget de tokens plafonné ; traçage de chaque sous-agent ; reprise sur erreur sans tout relancer (Anthropic).

**Traduction dans un workflow déployé [déduit]**
- **Autonomie : 3** (la brigade produit le rapport et notifie ; aucune action externe sans validation).
- **Où est l'humain** : il valide la question de départ et lit la synthèse finale.
- **Tests avant déploiement** : tester chaque poste séparément sur des cas observés ; tester la synthèse finale avec un juge automatique calibré sur l'avis humain ; vérifier les sources citées.
- **Suivi après** : coût par rapport rendu ; taux de sources fausses ou inventées ; temps gagné vs recherche à la main (screenpipe) ; taux de rapports repris par l'humain.

**Mini-schéma**
1. L'humain pose la question
2. Le chef découpe en sous-missions
3. Des petits agents lisent et cherchent en parallèle
4. Le chef assemble, un vérificateur contrôle les sources
5. Un seul rapport final arrive chez l'humain

---

## 7. La Forteresse

> **Accroche** : on peut laisser l'agent seul, à condition qu'il ne puisse jamais à la fois lire vos secrets, lire du contenu étranger et parler à l'extérieur.

**Auteurs principaux**
- Simon Willison, *The lethal trifecta* (16/06/2025) — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Simon Willison, *Designing agentic loops* (30/09/2025) — https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
- Simon Willison, *The Dual LLM pattern* (25/04/2023) — https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- Beurer-Kellner et al., *Design Patterns for Securing LLM Agents against Prompt Injections* (2025), résumé par Willison — https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
- Anthropic, section sécurité des Agent Skills — URL ci-dessus
- Documentation screenpipe, permissions des pipes — https://docs.screenpipe.com/pipes

**L'idée en une phrase** : la sécurité se règle par l'architecture (ce que l'agent peut voir et faire), pas par des filtres ; une fois l'agent enfermé, on peut lui donner beaucoup d'autonomie.

**Ce que disent les sources [vérifié]**
- Willison, la « lethal trifecta » : « Access to your private data », « Exposure to untrusted content », « The ability to externally communicate ». Réunir les trois permet à un texte piégé de faire fuiter des données. Les filtres qui bloquent « 95% of attacks » ne suffisent pas : en sécurité web, 95 % est « very much a failing grade ». Seule solution sûre : ne jamais réunir les trois. — URL trifecta.
- Article des 14 auteurs : « once an LLM agent has ingested untrusted input, it must be constrained » ; six patrons, dont *Plan-Then-Execute* (le plan est fixé avant de lire le contenu douteux), *Dual LLM*, *Code-Then-Execute*, *Context-Minimization*. — URL patterns.
- Willison, *Dual LLM* : un modèle « privilégié » qui a les outils mais ne voit jamais le contenu douteux, un modèle « en quarantaine » qui lit le contenu douteux mais n'a aucun outil, et du code ordinaire entre les deux. L'auteur reconnaît que la solution est lourde (« This solution is pretty bad! »). — URL dual LLM.
- Willison, *agentic loops* : en mode sans validation, trois risques : commandes destructrices, fuite de fichiers ou secrets, machine utilisée pour attaquer ailleurs ; réponse : bac à sable, identifiants limités à un environnement de test, budget plafonné (« If a credential can spend money, set a tight budget limit »). — URL agentic loops.
- Anthropic, Skills : des skills malveillantes peuvent pousser l'agent à faire fuiter des données ; n'installer que des skills de confiance et les auditer. — URL Skills.
- screenpipe : sans champ `permissions`, un pipe a accès à toute l'API ; le préréglage `reader` limite aux lectures ; règles `allow`/`deny` par application, fenêtre, type de contenu ; « Deny always wins » ; mais ce n'est « not a filesystem or network sandbox ». — URL docs screenpipe.

**Pourquoi c'est central pour nous [déduit]** : screenpipe réunit par nature deux des trois éléments : des données privées (tout l'écran) et du contenu non fiable (les mails, pages web, messages affichés à l'écran peuvent contenir des instructions piégées). Un pipe qui peut en plus envoyer un mail, poster sur Slack ou appeler une API externe réunit la trifecta complète. Chaque workflow du pack doit donc dire lequel des trois il n'a pas.

**Principes concrets**
1. Pour chaque workflow, écrire noir sur blanc lequel des trois éléments est absent.
2. Moindre privilège : pipes en lecture seule par défaut, liste `deny` sur les applis sensibles (banque, santé, messageries privées).
3. Bac à sable et identifiants limités ; budget plafonné pour tout ce qui coûte de l'argent.
4. Le plan est fixé avant de lire le contenu non fiable ; le contenu lu ne peut pas déclencher d'action nouvelle.
5. Traitement local quand c'est possible ; aucune sortie vers l'extérieur sans validation.

**Quand la choisir** : secteurs régulés ou très sensibles (avocats, santé, finance, RH), données clients confidentielles, entreprises qui veulent que rien ne sorte des machines. Aussi : obligatoire en complément de toute thèse qui touche à l'écran et à l'extérieur.

**Risques** : workflows moins puissants (pas d'envoi automatique) ; contraintes qui agacent ; faux sentiment de sécurité si les permissions screenpipe sont prises pour un vrai bac à sable (la doc dit que ce n'en est pas un).

**Garde-fous** : revue de sécurité de chaque skill et pipe avant installation ; tests d'injection (on met un texte piégé à l'écran et on vérifie que l'agent n'agit pas) ; journal de tout accès aux données ; secrets dans `.env`, jamais dans le prompt.

**Traduction dans un workflow déployé [déduit]**
- **Autonomie : 4 à l'intérieur de la forteresse** (l'agent peut tourner seul tant qu'il n'a aucune sortie externe), et retombe à 2 dès qu'une action sort vers l'extérieur.
- **Où est l'humain** : au portillon de sortie : rien ne quitte la machine sans son accord.
- **Tests avant déploiement** : tests d'injection rejoués (pages et mails piégés affichés à l'écran) ; vérifier que les règles `deny` bloquent bien les applis sensibles ; vérifier qu'aucun appel réseau non prévu n'a lieu.
- **Suivi après** : nombre de tentatives d'action bloquées ; accès refusés par les règles `deny` ; appels réseau sortants ; incidents de sécurité (objectif : zéro).

**Mini-schéma**
1. On liste les données, les sources non fiables et les sorties du workflow
2. On coupe au moins une des trois
3. Le pipe tourne en lecture seule, dans un périmètre limité
4. Les résultats restent en local
5. Toute sortie vers l'extérieur passe par la validation humaine

---

## Comment ces thèses s'opposent et se combinent

| Désaccord | D'un côté | De l'autre | Point d'accord |
|---|---|---|---|
| Un agent ou plusieurs ? | **Un Seul Cerveau** (Cognition, OpenAI) | **La Brigade** (Anthropic recherche, HumanLayer facteur 10) | Plusieurs pour lire en parallèle, un seul pour écrire (Chase) |
| Code fixe ou liberté du modèle ? | **Les Rails d'abord** (Anthropic workflows, HumanLayer) | **Un Seul Cerveau** (agent qui choisit ses étapes) | Chase : on se demande « à quel point » c'est agentique, pas « si » |
| Où est l'humain ? | **L'Armure** : à chaque sortie, il pilote | **Le Majordome** : seulement quand l'agent l'appelle | Le curseur se règle par action (Huyen, Feng et al.) |
| Qu'est-ce qui rend fiable ? | **Le Banc d'Essai** : les tests | **La Forteresse** : l'architecture de sécurité | Les deux sont complémentaires, pas rivaux |

**[déduit] Recommandation pour le produit** : le client choisit une thèse « principale » parmi Rails, Seul Cerveau, Armure, Majordome, Brigade. **Le Banc d'Essai et la Forteresse s'appliquent à toutes** : on peut les présenter comme thèses pour les clients qui veulent mettre l'accent dessus, mais aucun workflow du pack ne part sans tests rejoués et sans vérification de la trifecta.

**[déduit] Grille de choix rapide**
- Processus stable et répétitif, faible tolérance au risque → **Les Rails d'abord**
- Travail de dossier où tout se tient, équipe à l'aise avec l'IA → **Un Seul Cerveau**
- Métier à responsabilité, équipe méfiante → **L'Armure, pas le Robot**
- Volume élevé, besoin de preuves chiffrées → **Le Banc d'Essai**
- Journées hachées de petites tâches → **Le Majordome Ambiant**
- Beaucoup de lecture et de recherche → **La Brigade**
- Données ultra-sensibles, secteur régulé → **La Forteresse**

---

## Ce qui n'est pas vérifié

- **Mémo de Tobi Lütke (Shopify, avril 2025)** : je n'ai pas pu lire le post original sur X (accès refusé). Les articles rapportent que les équipes doivent montrer pourquoi l'IA ne peut pas faire le travail avant de demander des embauches, et que l'usage de l'IA entre dans les évaluations [secondaire — https://www.tomsguide.com/ai/no-new-hires-if-ai-can-do-the-job-says-shopify-ceo-in-leaked-memo, https://thelogic.co/briefing/shopify-staff-must-use-ai-lutke-says/]. Pas utilisé comme thèse.
- **McKinsey, six leçons** : PDF non chargé ; seul le titre et le résumé secondaire sont utilisés.
- **MIT NANDA 95 %** : chiffre d'un rapport préliminaire, tailles d'échantillon rapportées différemment selon les articles.
- **Karpathy** : les citations du keynote viennent d'une transcription automatique YouTube (erreurs de transcription possibles sur les mots, pas sur le sens) ; celles du podcast Dwarkesh viennent de Fortune, pas de la transcription complète.
- **Decagon et Sierra** : contenus de vendeurs qui vendent leur plateforme ; les chiffres (taux de déflexion, nombre de tests par jour) ne sont pas vérifiés de façon indépendante.
- **Chiffres d'Anthropic** (90,2 %, 15× tokens, données Claude Code) : mesures internes d'Anthropic, non reproduites indépendamment.
- **Toutes les traductions en workflows (autonomie, tests, métriques)** sont de notre fait [déduit] et n'ont pas encore été testées sur un vrai client.

## Toutes les sources consultées

1. Anthropic — Building effective agents — https://www.anthropic.com/research/building-effective-agents
2. Anthropic — How we built our multi-agent research system — https://www.anthropic.com/engineering/multi-agent-research-system
3. Anthropic — Effective context engineering for AI agents — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
4. Anthropic — Equipping agents for the real world with Agent Skills — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
5. Anthropic — Writing effective tools for agents — https://www.anthropic.com/engineering/writing-tools-for-agents
6. Anthropic — Demystifying evals for AI agents — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
7. Anthropic — Measuring AI agent autonomy in practice — https://www.anthropic.com/research/measuring-agent-autonomy
8. Claude Code — Best practices — https://code.claude.com/docs/en/best-practices
9. Cognition (Walden Yan) — Don't Build Multi-Agents — https://cognition.com/blog/dont-build-multi-agents
10. HumanLayer (Dex Horthy) — 12-Factor Agents — https://github.com/humanlayer/12-factor-agents
11. 12-Factor Agents, facteur 7 — https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-07-contact-humans-with-tools.md
12. 12-Factor Agents, facteur 8 — https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md
13. 12-Factor Agents, facteur 10 — https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-10-small-focused-agents.md
14. Karpathy — Software Is Changing (Again), transcription — https://prepublish.ai/youtube-transcript/LCEmiRjPEtQ (vidéo : https://www.youtube.com/watch?v=LCEmiRjPEtQ)
15. Fortune — Karpathy au Dwarkesh Podcast — https://fortune.com/2025/10/20/workers-fear-ai-job-cuts-open-ai-co-founder-says-ai-agents-will-take-a-decade-before-they-even-work-they-dont-have-enough-intelligence-unemployment-automation-2035
16. Hamel Husain — Your AI Product Needs Evals — https://hamel.dev/blog/posts/evals/
17. Hamel Husain — A Field Guide to Rapidly Improving AI Products — https://hamel.dev/blog/posts/field-guide/
18. Hamel Husain & Shreya Shankar — AI Evals FAQ — https://hamel.dev/blog/posts/evals-faq/
19. Shreya Shankar et al. — Who Validates the Validators? — https://arxiv.org/abs/2404.12272
20. Eugene Yan — An LLM-as-Judge Won't Save The Product — https://eugeneyan.com/writing/eval-process/
21. Eugene Yan — Patterns for Building LLM-based Systems — https://eugeneyan.com/writing/llm-patterns/
22. Simon Willison — The lethal trifecta — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
23. Simon Willison — sa définition d'un agent : « An LLM agent runs tools in a loop to achieve a goal » — https://simonwillison.net/2025/Sep/18/agents/
24. Simon Willison — Designing agentic loops — https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
25. Simon Willison — The Dual LLM pattern — https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
26. Simon Willison — Design Patterns for Securing LLM Agents against Prompt Injections — https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
27. Chip Huyen — Agents — https://huyenchip.com/2025/01/07/agents.html
28. Lilian Weng — LLM Powered Autonomous Agents — https://lilianweng.github.io/posts/2023-06-23-agent/
29. Harrison Chase — Introducing ambient agents — https://www.langchain.com/blog/introducing-ambient-agents
30. Harrison Chase — How to think about agent frameworks — https://www.langchain.com/blog/how-to-think-about-agent-frameworks
31. Harrison Chase — How and when to build multi-agent systems — https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems
32. LangChain — Context engineering for agents — https://www.langchain.com/blog/context-engineering-for-agents
33. OpenAI — A practical guide to building agents — https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
34. Drew Breunig — How Contexts Fail — https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html
35. Drew Breunig — How to Fix Your Context — https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html
36. Philipp Schmid — Context Engineering — https://www.philschmid.de/context-engineering
37. swyx / Latent Space — Agent Engineering — https://www.latent.space/p/agent
38. Sierra — τ-bench — https://sierra.ai/blog/benchmarking-ai-agents
39. Sierra — Agent development life cycle — https://sierra.ai/blog/agent-development-life-cycle
40. Sierra — Simulations — https://sierra.ai/blog/simulations-the-secret-behind-every-great-agent
41. Decagon — From SOPs to Agent Operating Procedures — https://decagon.ai/blog/from-sops-to-agent-operating-procedures
42. Decagon — The future of AI agents is test driven — https://decagon.ai/blog/the-future-of-ai-agents-is-test-driven
43. METR — Measuring AI ability to complete long tasks — https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
44. Feng, McDonald, Zhang — Levels of Autonomy for AI Agents — https://arxiv.org/abs/2506.12469
45. NVIDIA (Belcak et al.) — Small Language Models are the Future of Agentic AI — https://arxiv.org/abs/2506.02153
46. screenpipe — Pipes (scheduled tasks) — https://docs.screenpipe.com/pipes
47. [secondaire] Klarna — https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396
48. [secondaire] MIT NANDA — https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/
49. [secondaire] McKinsey — https://richturrin.substack.com/p/top-six-agentic-ai-deployment-lessons
50. [secondaire] Shopify / Lütke — https://www.tomsguide.com/ai/no-new-hires-if-ai-can-do-the-job-says-shopify-ceo-in-leaked-memo

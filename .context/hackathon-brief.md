# Hackathon screenpipe × 42 Paris — fiche de préparation

Recherche faite le 16/10/2026 (jour J). Sources en bas.

## 1. L'événement

- **Nom** : « Build Agents That Remember » — hackathon @42 Paris
- **Quand** : 16 → 18 octobre 2026, 48 h non-stop
- **Où** : 42 Paris, 96 bd Bessières, 75017
- **Organisé par** : 42 Entrepreneurs + screenpipe (YC S26)
- **Hôtes listés** : Louis Beaumont (fondateur de screenpipe), Nassim Adam Bariol, Ethan Lopin,
  Hamza Konte, Ouafae Moudni, + un compte X @Nyrok10
- **Participants** : 149 inscrits, complet (liste d'attente)
- **Équipes** : 3 à 5, solo accepté, Discord pour trouver une équipe. Pas besoin d'idée en arrivant.
- **Ce qu'on gagne** :
  - 3 000 $ de prix
  - un **contrat payé** avec screenpipe
  - le projet gagnant est **intégré au produit** avec l'équipe screenpipe + repas avec les fondateurs
  - screenpipe recrute **1 à 2 stagiaires/alternants (4 à 6 mois)** parmi les participants
- **Pas sur la page** : noms du jury, critères de notation, horaires précis. → à demander à l'ouverture.

### Les 3 tracks (texte officiel, reformulé)

1. **Trouver quoi automatiser** — utiliser l'historique screenpipe pour repérer les tâches
   répétitives, et une interface qui aide à comprendre les étapes et à décider quoi automatiser.
2. **Apprendre son workflow à un agent** — transformer du travail enregistré en automatisation
   (skills d'agent, outils, ou entraînement de modèle) et la montrer **faire une vraie tâche de bout en bout**.
3. **Le faire marcher pour une équipe** — transformer un workflow perso en automatisation utilisable
   par d'autres : installation, **validations (approvals)**, outils partagés.

## 2. screenpipe, c'est quoi

**En une phrase** : une app qui tourne en fond sur ton ordi, enregistre ce que tu vois et entends
(écran + audio), le garde **en local**, et le rend interrogeable par n'importe quelle IA.

- **Pitch YC** : « Turn your company's computer work into AI agents. »
- **Tagline du site** : « Your computer history. Open to any AI. »
- **Mission** : « Turn what people know into what computers can scale. »
- **Le problème qu'ils vendent** : les agents IA démarrent sans contexte. Ils ne savent pas ce que tu
  as fait, vu, décidé. screenpipe leur donne une mémoire de ce qui s'est **réellement** passé.

### Comment ça marche (technique)

- Capture **sur événement** (changement d'app, clic, pause de frappe, scroll), pas une vidéo continue.
  Capture d'écran + **arbre d'accessibilité** de l'OS ; OCR seulement en secours.
- Audio : transcription locale (Whisper / Parakeet) ou Deepgram, avec identification des voix.
- Stockage : SQLite local (recherche plein texte) + fichiers MP4, dans `~/.screenpipe/`.
- **API REST locale sur `localhost:3030`** (protégée par token) : `/search`, frames, éléments d'UI,
  réunions, speakers, memories, activity summary, **SQL brut**, etc.
- **MCP** : `claude mcp add screenpipe -- npx -y screenpipe-mcp@latest`
- **Pipes / scheduled tasks** : un fichier `pipe.md` (prompt + planning) dans `~/.screenpipe/pipes/`.
  Les permissions sont dans l'en-tête YAML (apps, fenêtres, plage horaire, type de contenu) et
  appliquées par le code, pas par le prompt.
- SDK JS : `@screenpipe/js`. App desktop en Tauri (Rust + TS). macOS, Windows, Linux (expérimental).
- Repo : github.com/screenpipe/screenpipe — ~22k étoiles, licence commerciale (gratuit perso/recherche,
  payant en entreprise ; anciennes versions MIT).

### Le business

| Offre | Prix | Pour qui |
|---|---|---|
| Free | 0 € | 1 appareil, recherche récente |
| Basic | 21 $/mois | historique complet, MCP, workflows illimités |
| Business | 42 $/siège/mois | multi-appareils, workflows récurrents — **pas de contexte partagé entre collègues** |
| Enterprise | sur devis | SSO, MDM, rétention, « transformer le travail de l'entreprise en skills et agents » |

- Annoncé : 500+ clients, logos Google/Microsoft/NVIDIA/Shopify… (non vérifiés), 250-300k utilisateurs
  selon le GitHub du fondateur.
- Entreprise derrière : Negentropy Labs, Inc. (anciennement Mediar, 2,8 M$ levés en 2025), YC S26,
  2 personnes, San Francisco. Partner YC : Gustaf Alströmer.
- Ils recrutent : Founding Engineer, Forward Deployed Engineer (enterprise), Senior PM.

### Le fondateur — Louis Beaumont (très probablement au jury)

- Français, ex-renseignement français, ex-OVHcloud (observabilité cloud), bots de jeux vidéo à 14 ans.
- Construit un « second cerveau » IA depuis 2020. X : @louis030195.
- Ce qu'il valorise (d'après son VISION.md) : **stabilité > features**, pas de feature creep,
  local-first, perf (< 20 % CPU, < 3 Go RAM), « ship daily », « truth over comfort ».
- Sa conviction : « Sending prompts is obsolete, AI should just watch and work. »

## 3. Où ils vont (roadmap)

**Officiel (VISION.md)** :
1. **Maintenant : la mémoire** — Record, Rewind, Ask.
2. **Ensuite : la couche de contexte pour les agents** — n'importe quel agent interroge ton historique,
   agit, et se déclenche **sans prompt**.
3. **Plus tard : tout** — tout enregistrer 24/7, chiffré en local, connecté à l'IA.

**Ce que montre le changelog (août → oct. 2026)** — c'est là qu'est leur vraie priorité :
- **Workflows & SOP** : SOP vidéo narrées, SOP éditables, étapes modifiables (sorties du 28/09 au 06/10).
- **Entreprise** : ingestion d'activité, historique des appareils, installeurs, contrôles admin.
- **Agents partout** : plugins MCP pour Claude et OpenAI, cartes de résumé dans Claude/Cursor/Codex,
  pipes déclenchés par Linear et d'autres apps.
- **Réunions** : rappels, replay, résumés.

**Le parcours entreprise qu'ils vendent** : Map → Install → Test → Improve → Deploy (agents qui tournent
dans une VM, exécution via screenpipe Cloud, Zapier, n8n, Claude Code ou Codex). Leur page entreprise
admet elle-même que les SOP générées « ne sont pas des automatisations testées » et que les gains sont
des « estimations à valider ».

→ **Les 3 tracks = exactement les 3 trous de leur produit actuel** :
- Track 1 = leur « workflow discovery » (encore démo sur données fictives sur le site)
- Track 2 = passer de la SOP à l'agent **qui marche vraiment** (leur point faible avoué)
- Track 3 = le partage en équipe (« pas inclus actuellement » dans l'offre Business)

## 4. Les critiques qu'on leur fait (à retourner en force dans ton projet)

D'après le Launch HN :
- Un agent trop permissif peut lire **tout** l'historique → montrer des permissions fines.
- Vie perso / pro mélangées, employeurs qui interdisent les enregistreurs → filtres, mode « accessibilité seule ».
- Conso CPU (MacBook M1 qui chauffe).
- Mémoires périmées ou fausses → provenance, date, niveau de confiance.
- RGPD / surveillance des salariés en Europe → **gros sujet à Paris** ; un projet qui le traite bien marque des points.
- Concurrents cités : Claude Cowork, Daydream, Rewind/Limitless, Microsoft Recall, Granola.

## 5. Comment gagner (mon analyse)

Le prix n'est pas « le meilleur projet » mais « le projet que Louis veut **intégrer dans son produit** ».
Donc :

1. **Construire avec leurs briques, pas à côté.** Un `pipe.md`, un serveur MCP, l'API 3030, ou une PR
   sur le repo. Plus c'est facile à intégrer, plus c'est crédible.
2. **Démo sur de vraies données.** Installer screenpipe **dès maintenant** sur 1-2 machines et bosser
   normalement : il faut des heures d'historique réel avant la démo. Une démo sur données fictives,
   c'est ce qu'ils ont déjà sur leur site.
3. **Bout en bout, en live.** Track 2 le dit : « une vraie tâche de bout en bout ». Repérer → générer →
   exécuter → vérifier contre l'enregistrement d'origine.
4. **Mesurer.** Temps gagné calculé depuis l'historique (fréquence × durée), pas une estimation au doigt mouillé.
5. **Humain dans la boucle + confidentialité visibles.** Validation avant toute action, redaction,
   permissions. Ça répond aux critiques HN et au contexte européen.
6. **Respecter leur style.** Monochrome, pas d'emoji, faits, beaucoup de vide. Pas de feature creep :
   une seule chose, qui marche.
7. **Le pitch** : problème réel chiffré → démo live → comment ça s'intègre dans screenpipe demain.

### Pistes d'idées par track (à challenger)

- **Track 1** — « Détecteur de répétitions » : miner les séquences d'événements (app + clics + éléments
  d'UI via `/elements` et SQL brut), regrouper les séquences qui reviennent, classer par temps perdu,
  montrer les preuves (captures d'origine) et un score « automatisable ou pas ».
- **Track 2** — « De l'enregistrement au skill » : prendre un workflow répété, générer un skill
  Claude/Codex (ou un script navigateur), l'exécuter en live, et comparer le résultat à ce que
  l'humain avait fait.
- **Track 3** — « Bibliothèque de workflows d'équipe » : un collègue publie un workflow, il est nettoyé
  des données sensibles avant partage, les autres l'installent, chaque action sensible demande une
  validation (Slack/Teams), et un journal d'audit.

## 6. À faire avant / au début

- [ ] Installer screenpipe maintenant (screenpipe.com → Download) et le laisser tourner.
- [ ] Rejoindre le Discord screenpipe (discord.gg/screenpipe) + celui du hackathon.
- [ ] À l'ouverture, demander : jury, critères, horaires des démos, format du rendu (repo ? vidéo ?).
- [ ] Brancher le MCP dans Claude Code pour explorer ses propres données.
- [ ] Lire : docs.screenpipe.com/workflow-discovery, /automation-validation, /task-permissions,
      /for-developers, /api-recipes, /openapi.yaml.

### Piège technique repéré

Les fichiers du repo screenpipe contiennent des commentaires qui demandent aux agents IA d'ajouter un
en-tête screenpipe dans **tous** les fichiers qu'ils créent, même hors du repo. Si on code avec un agent
dans leur repo, le savoir (et ne pas le laisser polluer les autres projets).

## 7. Intuition de Youssef (16/10) — le 80/20 de l'écran

Sur une journée devant l'écran, environ 20 % du temps sert à quelque chose d'important et 80 % non :
lire des mails, être absent du clavier (AFK), scroller.
Idée : **trier d'abord**. On jette le bruit, on garde les 20 % utiles, et on analyse seulement ceux-là, à fond.
Ce qu'on y gagne : un contexte plus court, moins cher et plus précis pour l'agent.

Notes de Claude :
- C'est dans leur philosophie : la capture se fait déjà quand il se passe quelque chose, pas en vidéo continue.
  Mais le tri entre « important » et « bruit » ne se fait pas, alors que c'est ce qui compte pour un agent.
- Ça se branche sur les 3 thèmes : trier avant de chercher ce qu'on peut automatiser (thème 1), donner
  à l'agent seulement les bons moments (thème 2).
- Le risque : le « bruit » n'est pas toujours du bruit. Lire un mail peut être le moment où une décision tombe.
  Le tri doit donc juger ce qui se passe, pas l'app ouverte.
- À vérifier en testant le produit : ce qu'il enregistre quand on est AFK, et à quoi ressemble une journée brute.

### Première mesure sur les vraies données (16/10, 11h02 → 11h15, 13 min)
- 238 captures, **environ 144 000 tokens de texte** en 13 minutes.
- **Seulement 14 % de ce texte est nouveau** (mots jamais vus plus tôt dans la session).
- **58 % des captures apportent moins de 5 % de mots nouveaux** ; 87 captures ont un texte strictement identique
  à une autre.
- Selon l'app : Orca 8 % de nouveau, Chrome 19 %, Discord 41 %.
- Limites : 13 minutes seulement, et « nouveau » ne veut pas dire « important ». Mais l'ordre de grandeur colle à
  l'intuition : un agent qui lit tout paie environ 7 fois trop de texte.
- Comment c'est calculé : script `analyze` dans le scratchpad, basé sur `/search?content_type=all`. Le SQL brut
  ne donne pas le texte des captures archivées.

## 7b. Idée « pause / cooldown » (16/10) — DÉJÀ DANS LE PRODUIT
- Menu de la barre du haut > « Pause for… » : 5 min, 15 min, 30 min ou 1 h, avec reprise automatique et
  notification (`apps/screenpipe-app-tauri/src-tauri/src/tray.rs`, lignes 1707 à 1715).
- Le code garde exprès la pause accessible même quand l'entreprise masque l'icône (`tray.rs`, vers la ligne 492).
- Il existe aussi des horaires d'enregistrement (heures de travail). Un ticket ouvert (#7496) signale que
  l'enregistrement reste en pause après avoir désactivé ces horaires.
- Ce qui pourrait manquer (à vérifier) : que le salarié voie ce que son manager voit, et une pause « déclarée »
  que les analyses ne prennent pas pour un trou ou une absence (cf. #7377, une journée incomplète).

## 7c. Comment ça tourne vraiment (mesuré le 16/10)
- **Capture** : pas une capture par minute. Une capture à chaque événement (clic, changement d'app, pause de
  frappe, scroll). Sur le Mac : 238 captures en 13 min, soit **une toutes les 3 secondes environ**.
- **IA** : rien n'est envoyé à chaque capture. Ce sont des tâches programmées qui lisent l'historique :
  Digital Clone toutes les heures, Improve my skills toutes les 6 h, Daily Email Summary à 18 h ; le reste est
  à la demande. La chaîne de détection de workflows est désactivée.
- **Où appliquer le 80/20** :
  1. Au stockage : ne pas garder une capture identique à la précédente (87 doublons exacts sur 238).
  2. Entre la capture et l'IA : fusionner les captures presque identiques en un seul « moment » (début, fin,
     durée), et marquer les moments forts (on écrit, on envoie, on ouvre un nouveau document) et les faibles
     (scroll, lecture passive, absence du clavier). Les agents lisent les moments, pas les captures.
  3. Dans les tâches IA : ne lancer Digital Clone que s'il s'est passé quelque chose de nouveau depuis le
     dernier passage.
- Problème vu sur les données : **environ 30 % du texte capturé n'a pas de nom d'app** (170 000 caractères sur
  577 000). Ça rejoint le ticket #7580 (mauvaise attribution des apps sur Mac).

### Précisions (16/10, 287 captures, 11h02 → 11h24, Mac avec 2 écrans)
- Règles dans le code (`crates/screenpipe-engine/src/event_driven_capture.rs`) :
  - capture à chaque événement, avec au minimum 200 ms entre deux captures ;
  - s'il ne se passe rien, une capture « idle » toutes les 30 s (toutes les 5 s pendant une réunion).
- Ce qui a déclenché les captures :

  | Déclencheur | Captures |
  |---|---|
  | fin de scroll | 109 |
  | frappe clavier | 52 |
  | changement de fenêtre | 38 |
  | changement visuel | 32 |
  | rien ne se passe (idle) | 32 |
  | clic | 18 |
  | copier-coller | 4 |

- Rythme : un écart médian de 1,4 s, et 124 captures à moins d'1 s de la précédente. Ça varie de 1 à 50 captures
  par minute selon l'activité.
- **L'écran qu'on ne regarde pas est capturé aussi.** Le code (`focus_aware_controller.rs`) garde l'autre écran
  actif 2 s après qu'on l'a quitté, puis en veille légère jusqu'à 60 s. Résultat : 130 captures sur 287 viennent de
  l'écran non regardé.
- **Ces 130 captures sont exactement celles sans nom d'app.** Elles sont lues uniquement par OCR (l'arbre
  d'accessibilité ne lit que la fenêtre active). Corrélation à 100 % sur l'échantillon. La cause précise dans le
  code reste à confirmer.
- **70 des 87 doublons exacts viennent de l'écran non regardé**, souvent déclenchés par un scroll ou une frappe faits
  sur l'AUTRE écran. Écart médian avec l'original : 16 s.
- « Nouveau » = des mots jamais vus plus tôt dans la session. Une conversation qui avance compte comme nouvelle
  pour ses nouveaux messages ; le reste de l'écran (menus, barre latérale) compte comme répété.

### Tickets précisés
- **#7364 (batterie)** : la page d'accueil redemandait le résumé d'activité de TOUT l'historique toutes les 4 s, et
  chaque calcul prenait de 20 à 60 s. Le reporter confirme que c'est corrigé en 2.7.84 (Ezra) ; le ticket est
  encore ouvert. Une piste suggérée en commentaire : enregistrer le nom de l'app au moment de la capture, plutôt
  que de le recalculer à chaque lecture.
- **#7554 (chat spammé)** : chaque exécution d'une tâche automatique crée un fil de discussion. Les vraies
  conversations sont noyées sous les « Build a concise activity timeline… ». Ezra répond qu'on peut filtrer et que
  ce n'est pas sa priorité.

## 7d. Angle pitch de Youssef (16/10)
« Pas un hackathon normal : on améliore un produit. » Le déroulé :
1. l'état du marché ;
2. les besoins des agents en contexte ;
3. screenpipe répond à ça ;
4. état A → état B ;
5. les problèmes ciblés ;
6. les solutions déjà faites, avec les pull requests ouvertes.

Cohérent avec le prix (« intégrer le hack au produit »). Condition : les PR doivent être réelles et tester sur
leurs données avant de les annoncer. Dans LEUR repo, respecter leurs conventions (l'en-tête screenpipe dans
les fichiers fait partie de leurs règles de contribution).

## 7e. Deux gaspillages repérés par Youssef en regardant sa timeline (16/10)
1. **Double écran** : chaque clic sur l'autre écran déclenche une capture, et un clic sur l'un recapture l'autre.
   Les captures d'aller-retour sont rarement utiles. Mesuré : 130 captures sur 287 viennent de l'écran non regardé,
   et 70 des 87 doublons exacts.
2. **Chat IA qui « mouline »** : pendant que l'IA écrit, l'écran change en continu, donc il y a des captures en
   rafale. Or screenpipe lit déjà les historiques de Claude Code, Codex et Hermes (pipe Digital Clone), donc ces
   captures sont redondantes. **À mesurer** (pas encore vérifié) : la part de captures « changement visuel » ou
   « fin de scroll » prises pendant la génération d'une réponse.

## 7f. Jeux de données « vraie activité »
- **Données screenpipe d'autres utilisateurs** : rien de public (c'est privé par nature).
- **Le plus réaliste** : enregistrer l'équipe pendant les 48 h, avec l'accord de chacun. C'est la seule façon
  d'avoir de vraies journées, avec absences, mails, aller-retours et chats IA. Indispensable pour tester le 80/20.
- **Données publiques** (des démonstrations de tâches, pas des journées entières) :
  - AgentNet / OpenCUA (xlangai/AgentNet sur Hugging Face) : 22 625 trajectoires humaines sur Windows, Mac et
    Linux, avec vidéo, souris, clavier et arbre d'accessibilité.
  - CUA-Suite / VideoCUA (2026) : environ 55 h de vidéo d'experts en continu, 87 logiciels pros, 6 M d'images.
    C'est le plus proche d'un « écran qui tourne ».
  - ScreenLeak (de screenpipe) : un benchmark sur le masquage des données perso, en grande partie synthétique.
  - Le kit du hackathon : données fictives.

## 7g. Recherche récente utile — « la vidéo a déjà résolu une partie du problème »
Idée de Youssef : la vidéo et le montage IA ont beaucoup progressé sur le traitement de flux de milliers d'images.
On peut appliquer ces méthodes à l'écran pour « build agents that remember ».
- **Compression de vidéo en streaming (2026)** :
  - STC (CVPR 2026) réutilise le calcul des images visuellement similaires et élague ce qui part au modèle.
  - NovaCov (arXiv 2608.01169) choisit ce qu'il garde **par rapport à l'historique**, pas image par image.
    C'est exactement la mesure « nouveau vs déjà vu » faite sur le Mac.
  - Mémoires hiérarchiques : FluxMem (CVPR 2026), StreamingVLM (ICLR 2026), ProtoKV.
- **Loi du budget mémoire** (arXiv 2606.20726) : la précision monte avec le log du nombre d'images gardées, et le gain
  baisse pour les événements anciens. Donc : du détail sur le récent, des résumés pour l'ancien. Ça justifie les
  « moments » plus une mémoire en étages.
- **Induction de modèles de tâches à partir de traces d'ordinateur** (arXiv 2608.20319, août 2026) :
  - sépare les tâches entremêlées dans une trace brute (accord de 0,974), puis construit objectifs et procédure ;
  - les skills qui en sortent font +30 % sur des tâches nouvelles.
  - C'est directement les thèmes 1 et 2. Limite : testé sur des traces contrôlées, pas sur de vraies journées.
- **Mémoire d'agent** :
  - AgeMem (ACL 2026) : l'agent décide lui-même quoi retenir ou oublier, au lieu de règles fixes.
  - Survey sécurité (arXiv 2604.16548) : de faux souvenirs peuvent être plantés par du contenu web. Pour screenpipe,
    tout ce qui passe à l'écran est une entrée non fiable.
- **Montage IA** (OpusClip, Descript, AutoPod…) : détection de changement de scène, de pics audio, coupe des
  silences, l'humain valide. Métaphore de pitch : **« faire le dérush de ta journée »**, couper les temps morts et
  garder les moments forts.
- **Concurrence** :
  - OpenAI Chronicle (avril 2026, pour Codex) : envoie les captures à ses serveurs, réservé à Pro, **pas disponible
    en UE**. Argument fort à Paris pour screenpipe, qui reste en local.
  - OpenChronicle (Einsia, MIT) : la réponse open source, basée sur l'accessibilité.

## 7h. Est-ce que screenpipe (l'entreprise) voit mes données ?
- **Enregistrement, recherche, timeline, MCP, chat avec Ollama** : tout reste sur la machine (doc « privacy data flow »).
- **Quand on utilise l'IA « screenpipe cloud »** (le réglage par défaut, et celui des tâches Digital Clone et
  Improve my skills sur le Mac de Youssef) : la demande passe par **leur passerelle** (`packages/ai-gateway`,
  un Worker Cloudflare), puis part chez le fournisseur du modèle.
  - Techniquement, leur infrastructure voit donc passer le contenu envoyé.
  - Le code exige des fournisseurs « zéro rétention » et « pas d'entraînement » (tests ZDR et
    `require_no_training`). Je n'ai pas trouvé de code qui stocke le contenu des demandes. Il existe un réglage
    `capture_prompt_content`, désactivé par défaut dans les tests, à creuser.
  - Non vérifié : ce qui tourne réellement sur leurs serveurs au-delà du code public.
- **Avec sa propre clé API ou Ollama** : ça ne passe pas par eux.
- **Télémétrie** (PostHog, Sentry) : selon leur doc, pas de contenu d'écran, d'audio ni de fichiers. Se coupe avec
  `--disable-telemetry`.
- **Masquage des données perso en mode « enclave »** : le texte part dans un environnement confidentiel (Tinfoil),
  « conçu pour ne rien garder ».
- **Partage en équipe** : chiffré côté client, le serveur n'a pas la clé.
- Leur doc liste elle-même ses trous : télémétrie, rapports de crash, passerelle, rôle de Tinfoil, rétention chez
  les fournisseurs.

## 7i. Ce que les fondateurs suivent (étoiles GitHub)
**Louis** (étoiles récentes) :
- `marcelsamyn/screenpipe-distiller` (étoilé le 07/10) : **condense une journée screenpipe SANS IA** avant un seul appel
  au modèle. Regroupement par app, fenêtre ou URL, suppression des doublons, plafonds (25 extraits pour les
  conversations, 10 pour le reste). « Des milliers de captures → quelques Ko ». **C'est déjà une version communautaire
  de l'idée 80/20**, une seule fois par jour. Louis l'a remarquée. Notre version doit aller plus loin : dans le cœur
  du produit, en continu, et mesurée.
- `yujiachen-y/screenpipe-dashboard`, `awesome-screenpipe` : l'écosystème.
- `mnemoverse/awesome-agent-memory` : il fait de la veille sur la mémoire d'agent.
- Concurrents et clones étoilés : `snackbit/daydream`, `Screenata/open-chronicle`, `jaypopat/rewindos`,
  `janwilmake/efficient-recorder`, `JGalego/HiddenSteps`.
  - HiddenSteps : repère le travail répété sans jamais agir. Chaque chiffre est relié à de vrais événements. Pas de
    vue manager, « jamais ». Un aperçu en direct de ce qui est capturé, une pause en un clic.
- `apple-aiml-research/ml-ui-jepa` : comprendre l'intention de l'utilisateur à partir d'enregistrements d'interface.
  Deux jeux de données vidéo étiquetés, téléchargeables (IIT : 914 vidéos ; IIW : 1 600 vidéos de 25 s environ).
- Outils d'agent : `vercel-labs/agent-browser`, `openinterpreter`, `xai-org/grok-build`, `benchflow-ai/skillsbench`
  (évaluer des skills), `anthropics/sandbox-runtime`, `containers/bubblewrap` (isolation).
- Modèles en local : `ml-explore/mlx`, `mlx-swift-lm`, `vllm-mlx`, `baidu/Unlimited-OCR`, `qwen3-asr.cpp`, `VibeVoice`.
- Confidentialité : `tinfoilsh/*` (calcul confidentiel), `stronghold.rs` (gestion de secrets).
- `blader/humanizer`, `heygen-com/hyperframes` (vidéo en HTML pour agents), `motion-canvas` : le contenu et le marketing.

**Ezra** :
- `facebookresearch/vjepa2` (apprendre à partir de vidéo), `Blaizzy/mlx-vlm` (modèles vision en local),
  `cactus-compute/needle` (petit modèle d'automatisation de 8 à 29 Mo pour appareils légers),
  `MemoriLabs/Memori` (mémoire d'agent).
- `humanitas-labs/quill`, `CapSoftware/Cap` (enregistrement d'écran), `mediar-ai/terminator` (pilotage de Windows),
  `lightpanda`, `ego-lite` (navigateurs pour agents), `obra/superpowers` (skills d'agent), `comet-ml/opik` (évaluation
  de LLM).

**Ce que ça dit** : vision et vidéo en local (JEPA, MLX), mémoire d'agent, agents qui pilotent l'ordi, confidentialité
(enclaves, isolation), et beaucoup de veille sur les clones de Chronicle. Les « forks » de Louis sont surtout des listes
« awesome » où il ajoute screenpipe : de la distribution, pas de l'inspiration technique.

## 8. Hypothèse de Youssef (16/10) — brancher screenpipe sur Hermes

Constat : **le branchement existe déjà**, dans les deux sens.
- screenpipe → Hermes : connexion « Hermes » dans l'app (`crates/screenpipe-connect/src/connections/hermes.rs`).
  screenpipe peut envoyer des messages et programmer des tâches à un agent Hermes qui tourne
  (API sur `127.0.0.1:8642`, à lancer avec `hermes gateway`).
- Hermes → screenpipe : page de doc dédiée (docs.screenpipe.com/hermes) + skill screenpipe pour Hermes.
- La tâche « Digital Clone » lit déjà l'historique des chats Hermes (`~/.hermes/state.db`), en plus de Claude Code et Codex.
→ L'intérêt ne serait pas de faire le branchement, mais **ce qu'on fait avec**. Par exemple : Hermes exécute
  le workflow que screenpipe a repéré. Hermes n'est pas installé sur le Mac de Youssef.

## 9. Repo, équipe, communauté (vu le 16/10)

### Qui code
- **Louis Beaumont** : environ 9 500 commits, de très loin le premier. **Ezra Ellette** (screenpipe, SF) : environ 900,
  sans doute le 2e de l'équipe. **Matthew Diakonov** (m13v) : environ 400, il fait aussi des outils marketing.
- Les « forks » de Louis sont surtout des listes « awesome » où il ajoute screenpipe (de la croissance, pas de la tech).
- Ses 2 projets perso les plus récents en disent long sur où il va :
  - **hyperconsciousness** (15/10) : « iCloud pour agents ». Une mémoire chiffrée, synchronisée entre appareils,
    où **tu donnes à chaque agent un accès limité et qui expire**. Aligné avec le thème 3 et la confidentialité.
  - **bigbrother** (16/10) : un agent qui pilote l'ordi en lisant l'interface (accessibilité) :
    observer, cliquer sur un élément vu, observer à nouveau. C'est l'exécution du thème 2.
- « Claude même » : je n'ai trouvé aucun « claude-mem » dans le repo. Leur agent interne est **pi**
  (pi-coding-agent, installé dans `~/.screenpipe/pi-agent`). Ils intègrent aussi **OpenClaw** (plus de 80 mentions) et Hermes.

### Ce qui existe DÉJÀ (à ne pas refaire)
Dans `~/.screenpipe/pipes/` sur le Mac de Youssef, il y a une **chaîne complète de détection de workflows**, désactivée
par défaut : discover → patterns → procedures → deepen → review → maintain → timing.
Plus : automate-my-work, digital-clone (personnes et entreprises), skill-learning (crée des skills à partir de ce
qu'il voit). Côté code, il y a aussi une « team memory » (fichiers markdown partagés) dans `crates/screenpipe-team-memory`.
→ Leur détection de workflows confie tout le tri au LLM. Le prompt dit lui-même « l'enregistrement contient des
  centaines de captures presque identiques, ne les énumère pas ». **Rien ne trie avant le LLM** : c'est exactement
  l'idée du 80/20 (section 7).

### Ce que la communauté et l'équipe demandent
- Priorités officielles pour les contributeurs (ticket #3659) : **performance > précision > fiabilité > SDK >
  plus d'exemples de pipes de bout en bout > confidentialité** (tester le modèle qui masque les données perso).
- Tickets récents :
  - #7364 : le calcul du résumé d'activité tourne en boucle, 4 cœurs occupés, batterie de 100 à 5 % en 107 min.
    Le tri / résumé de l'activité est coûteux aujourd'hui.
  - #7554 : les tâches automatiques inondent le chat de logs au lieu de donner des résultats utiles.
  - #7483 : l'offre gratuite enregistre 24 h/24 mais on ne peut interroger que les dernières 24 h.
  - #7639 : entraîner le masquage pour cacher les montants financiers.
  - #7580 : sur Mac, mauvaise attribution des apps et changements d'app manqués.
- Discussions : analyse vidéo dans le chat, « marquer les moments importants » d'une étoile, tableau de bord
  quotidien monochrome. Concurrent cité par la communauté : **OpenAI Chronicle**.

### Le kit officiel du hackathon (github.com/screenpipe/hackathon-starter)
- `bun run demo` puis `bun start` → http://localhost:4242 : un bureau de revue de workflow, sur données fictives.
- 9 projets de départ, chacun relié à un thème :
  - thème 1 : repetition-finder, evidence-search, work-session-sop ;
  - thème 2 : workflow-review, workflow-replay ;
  - thème 3 : shift-handoff, onboarding, sop-change-review, support-escalation.
- **Leur obsession, visible partout** : séparer ce qui est observé de ce qui est supposé, faire valider par un humain,
  figer une version approuvée, tester sur une 2e entrée ET sur un cas qui doit échouer, ne jamais annoncer un temps
  gagné qui n'a pas été mesuré.
- **À rendre** : démo de 2 minutes + repo + courte description. Problème et utilisateur, installation, coûts,
  données d'exemple, ce qui marche / ce qui ne marche pas, rôle de chacun, et si quelqu'un d'extérieur a reproduit.
  Lieu et heure limite pas encore confirmés.
- Ce qu'ils suggèrent de montrer : l'observation d'origine, la procédure revue, une exception, ce que le relecteur
  a corrigé, une autre personne qui refait la tâche ; et pour une automatisation : une 2e entrée, un cas d'échec,
  et la frontière exacte entre texte généré et code exécuté.

### Sur le Mac de Youssef
- L'app tourne et enregistre depuis environ 9 h ce matin (48 Mo). L'API locale demande une clé
  (Settings > Privacy dans l'app).

## Sources

- Page Luma : https://luma.com/bnre6nou
- YC : https://www.ycombinator.com/companies/screenpipe
- Launch YC : https://www.ycombinator.com/launches/RTT-screenpipe-record-how-you-work-and-turn-that-into-agents
- Launch HN : https://news.ycombinator.com/item?id=49024620
- Site : https://screenpipe.com — pricing : https://screenpipe.com/pricing — entreprise : https://screenpipe.com/enterprise
- Changelog : https://screenpipe.com/changelog
- GitHub : https://github.com/screenpipe/screenpipe — vision : docs/VISION.md
- Docs : https://docs.screenpipe.com (index complet : https://docs.screenpipe.com/llms.txt)

## 10. Recherche approfondie mémoire + jeux de données (16/10, résumé)
Détail complet : `.context/recherche-memoire.md`.
- **Le travail le plus proche de screenpipe : FOCAL** (arXiv 2604.19541, avril 2026). Une chaîne filtrer → attribuer à une
  tâche → journaliser, avec un modèle vision appelé seulement quand il le faut. Résultats : −60 % de tokens, −72 % d'appels
  au modèle vision, rappel de l'info clé de 0,38 à 0,61, et ça tient quand on passe d'une tâche A à B puis revient à A.
  Code non publié.
- NovaCov : garder ce que l'historique ne couvre pas encore. C'est la mesure « 14 % nouveau » transformée en algorithme.
- EM-LLM (ICLR 2025) : découper en épisodes là où il y a de la « surprise ».
- « Retain or Consolidate? » (2607.17545) : garder le brut si le budget est large, consolider s'il est serré.
- LifeDialBench (2026) : sur des journaux de vie, les mémoires sophistiquées ne battent pas un RAG simple.
  → **Toujours comparer à une recherche simple.**
- Empoisonnement : 1,2 % de souvenirs empoisonnés suffit à faire tomber la précision de 0,85 à 0,30.
  → **Étiqueter la provenance.**
- Task Model Induction (2608.20319) : le code est public (github.com/Yucheng-Jiang/task-model-induction).
- Jeux de données : **aucune vraie journée publique**, et aucun avec deux écrans ni chat IA.
  - Les plus proches : GuideBench (67 h de sessions longues, accès sous conditions), AgentNet (arbre d'accessibilité,
    MIT), VideoCUA (55 h, MIT).
  - Recommandation : nos propres journées + une trentaine de questions, et un jeu synthétique A→B→A construit à partir
    d'AgentNet.

## 11. Stratégie double de Youssef (16/10) + vérifications
**Volet 1 — « plus sobre, et prouvé »** : corriger un maximum de choses (dont Windows), puis faire tourner deux
screenpipe côte à côte et mesurer captures, tokens, CPU et qualité des réponses.
- Faisable : le CLI accepte un port et un dossier de données séparés (`crates/screenpipe-engine/src/cli/mod.rs`).
  Mais lancer deux instances en même temps est un problème connu (#7433). À tester en premier.
- Windows : il faut un PC Windows dans l'équipe pour vérifier les correctifs. Le Mac de Youssef ne suffit pas.

**Volet 2 — « le truc impressionnant »** : une version Europe conforme, et/ou enregistrer sur une période limitée
(1 à 2 semaines) puis décomposer le travail, au lieu de tourner 24 h/24.
- **Le marché existe déjà, c'est le « task mining »** : UiPath, Celonis, Mimica, KYP.ai, Skan.ai, SAP Signavio.
  - UiPath recommande environ 2 semaines d'enregistrement pour 2-3 personnes (1 semaine pour 3-5), avec au moins
    10 000 actions (50 000 conseillées). Source : docs.uipath.com/task-mining, page best practices.
  - Mimica : de l'installation aux résultats en environ 2 semaines.
  - L'intuition de Youssef (« une semaine dit ce qui se passera pendant des années ») est la logique même de ce marché.
- **Droit français et européen** (sources : CNIL, articles juridiques) :
  - La CNIL juge les captures d'écran toutes les secondes contraires à la loi.
  - Sanctions : 40 000 € en décembre 2024 contre une agence immobilière pour des captures d'écran régulières ;
    32 M€ contre Amazon en décembre 2023.
  - Une surveillance permanente est en principe disproportionnée (article L. 1121-1 du Code du travail) ; les salariés
    doivent être informés.
  - AI Act (de mémoire, à vérifier) : interdit depuis février 2025 de déduire les émotions des salariés au travail.
  - → screenpipe tel quel, déployé par un employeur français, est juridiquement risqué. **D'où la valeur d'une version
    « campagne »** : limitée dans le temps, volontaire, en local, accessibilité seule possible (sans captures d'écran),
    pause, le salarié relit avant de partager, résultats agrégés sans vue individuelle, effacement automatique à la fin.
- **Importer une longue vidéo existante** : screenpipe ne sait pas importer une vidéo externe (rien trouvé dans le code).
  Il faudrait construire l'import (vidéo → images → texte → base screenpipe).
  - Source de démo légale : `markov-ai/computer-use-large` (12 300 h de vidéos de travail à l'écran, CC-BY-4.0).
    Ce sont des tutoriels, pas de vraies journées.

## 12. Infos officielles (récap du kickoff + site 42, lus le 16/10 à 18h40)
Sources : `~/Downloads/screenpipe_hackathon_kickoff_recap.pdf` et https://42entrepreneurs.com/hackathon-screenpipe (onglets Schedule, Tracks, Resources).

**Programme (heure de Paris)**
- Ven. 16 : 18h00 accueil · 18h25 démo screenpipe · **19h00 briefing (règles, prix, critères, format de rendu)** · 19h15–20h formation des équipes et choix du track · 20h00 début · 20h30 dîner.
- Sam. 17 : **18h00–18h45 office hours techniques screenpipe** (API, MCP, partage d'écran possible).
- Dim. 18 : **14h30 date limite de rendu** · 14h30–16h30 présélection par le jury parisien · 16h30 finalistes annoncés · 16h40–18h finale : **3 min de démo + 2 min de questions** (screenpipe à distance) · 18h25 prix.

**Règles nouvelles par rapport à la fiche**
- **Il faut choisir UN des 3 tracks.**
- **Équipes : 3–5 de préférence, 2 autorisé.** Le solo n'est plus mentionné (Luma le disait) → à confirmer au briefing de 19h.
- **Un agent générique sans lien réel avec screenpipe ne passe pas** le critère du jury.
- Track « trouver quoi automatiser » : **une interface qui montre les tâches répétées, les étapes, les apps et les exceptions peut suffire** ; l'automatisation complète n'est pas exigée.
- **Données synthétiques autorisées** pour une preuve de concept si elles ressemblent aux données screenpipe. Idées similaires entre équipes acceptées : l'exécution et la viabilité comptent.
- Rendu (via un formulaire lié à Kaggle) : **vidéo de 2 min max + lien GitHub + courte description**. Environ 25 équipes, présélection avant la finale.
- Critères de notation, format exact et prix détaillés : annoncés au briefing de vendredi 19h.
- À distance possible, mais les finalistes doivent pitcher sur place dimanche.
- Louis Beaumont et Ezra (« Illette » dans le PDF) sur Discord pour les questions techniques, en général jusqu'à 17–19h.
- « Captured activity stays locally on your device; the screenpipe team cannot view it » (dit par eux ; nuance en 7h pour l'IA cloud).

**Livrables du track 1 (texte officiel)** : « An interface that surfaces repeated tasks and lets the user review their steps and choose what to automate. »

**Checklist de rendu du kit** (`hackathon-starter/docs/submission.md`) : problème et utilisateur visé ; commandes d'installation, OS, modèle et coût ; un exemple d'entrée fictive ou autorisée avec la sortie attendue ; le lien vers la démo qui tourne vraiment ; ce qui marche, ce qui échoue, ce qui reste un prototype ; la contribution de chaque membre ; si quelqu'un d'extérieur a reproduit le résultat. Preuves suggérées : l'observation source, la procédure relue, une exception, ce que le relecteur a corrigé, une 2e entrée, un cas d'échec.

**Conséquence pour notre plan**
- Le dérush colle au **track 1** (« trouver quoi automatiser ») : moments → tâches répétées → étapes → exceptions → l'utilisateur choisit quoi automatiser. Le 80/20 devient la façon de trouver ces tâches avec peu de contexte.
- Les correctifs du cœur (double écran, Windows) ne sont **pas un track à eux seuls** : ils servent de preuve de sérieux dans le pitch, pas de projet principal.

**Benchmark double écran du 16/10 12h31 : raté.** Les deux versions se sont arrêtées au bout d'environ 15 s (le lanceur a été coupé avec la session), donc aucun chiffre. À relancer quand il y a 2 écrans branchés : à 42, le Mac n'a que l'écran intégré. Le correctif et son test restent valides.

## 13. Notes de Youssef sur place (16/10 soir, avec une équipe)
**Ce que dit le fondateur (noté par Youssef)**
- Il demande des choses à son Codex, et screenpipe lui fournit le contexte au moment où il demande (« context sharing »).
- Chaque jour, il tient une to-do dans Obsidian.

**Idées produit de Youssef**
- Intégrer JEPA (UI-JEPA d'Apple / V-JEPA 2, suivis par Louis et Ezra) pour ne traiter que les images pertinentes.
- Onboarding : les gens installent screenpipe et ne savent pas quoi en faire. Ils n'ont pas de prompts et ne savent pas quoi demander.
- Brancher sur Codex et Claude pour que ce soit utile au bon moment.
- Faire du computer use à partir des données screenpipe.
- Un agent de productivité « comme le CEO de screenpipe » (to-do Obsidian du jour).

**Proposition de synthèse (track 1)** : « screenpipe te dit quoi lui demander ».
Le dérush de ta journée donne tes tâches répétées. Pour chacune, on montre les étapes, les apps et les exceptions. Tu choisis, et l'outil génère un prompt ou une skill prête pour Claude Code ou Codex, plus la to-do du lendemain dans Obsidian.
JEPA est une option pour choisir les images, uniquement s'il reste du temps.
**Non vérifié** :
- si l'app propose déjà des prompts suggérés au démarrage ;
- si UI-JEPA tourne sur Mac en moins de 48 h.

## 14. JEPA et computer use — vérifié le 16/10 au soir
- **UI-JEPA (Apple, arXiv 2409.04081)** : il devine l'intention de l'utilisateur à partir d'une vidéo d'écran, avec un modèle léger. Le dépôt `apple/ml-ui-jepa` ne publie **que les données** (IIT : 914 vidéos, 10 intentions ; IIW : 1 600 vidéos de 25 s, 219 intentions), téléchargeables directement. **Les modèles ne sont PAS publiés** (le README le dit).
- **V-JEPA 2 (Meta)** : les poids sont publics sur Hugging Face (`facebook/vjepa2-vitl-fpc64-256`, 326 000 téléchargements). C'est un encodeur vidéo généraliste, non entraîné sur des écrans. Usage possible : des embeddings de courts clips pour repérer les changements de tâche ou dédoublonner. **Pas testé sur le Mac.**
- **Computer use dans screenpipe** : l'API `/elements` propose déjà un mode `computer-use` / `automation` qui renvoie les boutons, leur état et leur position pour les agents (`routes/elements.rs:240`, `cli/mod.rs:167`). screenpipe donne donc déjà la carte de l'écran aux agents. Je n'ai pas vérifié s'il exécute lui-même des clics.
- Autres briques repérées dans le dépôt : `screenpipe-rfdetr-mlx` (un modèle de vision local sur MLX) et `screenpipe-semantic`. Ce qu'elles font exactement n'a pas été lu.

## 15. Idée de l'équipe : une marketplace des données des gens (16/10 soir)
**Avis**
- La version « vendre ses captures » est risquée face à ce jury.
  - Elle contredit le positionnement de screenpipe (« tout reste en local, on ne voit pas tes données »).
  - Les écrans contiennent les données d'autres personnes (mails, clients, collègues), qui n'ont pas consenti. C'est le RGPD, et la CNIL a déjà sanctionné les captures d'écran au travail.
  - Elle ne colle à aucun des 3 tracks.
- **Le marché existe quand même** : les labos qui entraînent des agents de computer use achètent des démonstrations de vraies tâches. Les jeux publics (AgentNet, VideoCUA, computer-use-large) montrent que ce type de données a de la valeur, et aucun jeu de « vraie journée » n'est public (section 10).
- **Version qui passe** : une marketplace de **workflows et de skills**, pas de données brutes.
  - On partage la procédure relue et anonymisée (étapes, apps, exceptions), jamais les captures.
  - Ça colle au track 3 (« un workflow que quelqu'un d'autre peut utiliser »).
  - Option « données » : un don volontaire de journées anonymisées, relues par la personne, pour la recherche.
- **Non vérifié** : si screenpipe a encore son « pipe store », ce qui en ferait le canal naturel.

## 16. Test de JEPA sur une vraie journée (16/10, 20h20, Mac M5 Pro)
**Comment JEPA marche** : au lieu de décrire une image avec des mots ou de redessiner les pixels, le modèle apprend à prédire l'« empreinte » (une liste de nombres) d'un morceau caché à partir du reste. Deux moments qui se ressemblent par le sens ont des empreintes proches. Ça permet de comparer et de trier des images sans appeler une grosse IA.

**Le test** : 927 captures « regardées » de la journée de Youssef (12 apps, 98 fenêtres), comparées avec 3 méthodes. V-JEPA 2 (Meta), SigLIP (un modèle d'image classique de Google) et une simple vignette de pixels. Tout tourne en local. Scripts dans `experiences/jepa/`, pas d'images dans le dépôt.

| | repère un changement de fenêtre (AUC) | reconnaît l'app d'un moment | 20 % des captures gardées → fenêtres couvertes |
|---|---|---|---|
| pixels | 0,774 | 84,7 % | 63,3 % |
| SigLIP | **0,789** | **86,2 %** | **75,5 %** |
| V-JEPA 2 (image) | **0,789** | 80,2 % | 70,4 % |
| V-JEPA 2 en vraie vidéo (8 captures) | — | 70,9 % (SigLIP : 83,9 %) | — |

Références : 20 % au hasard → 52,3 % des fenêtres ; 1 capture sur 5 → 58,2 % ; toujours répondre l'app la plus fréquente → 46,5 %.
Vitesse : V-JEPA 2 environ 10 ms par capture, SigLIP environ 4 ms (GPU du Mac, demi-précision).

**Conclusion**
- **JEPA n'apporte rien de plus ici.** Il fait jeu égal sur les changements et moins bien sur le reste, même dans son vrai mode vidéo. Il est 2,5 fois plus lent que SigLIP.
- Raison probable : il est entraîné sur des vidéos du monde réel (mouvements), pas sur des écrans. Et les captures screenpipe sont espacées d'environ 1,4 s, donc il y a peu de « mouvement » à exploiter.
- **Le résultat utile pour le pitch** : garder seulement 20 % des captures, choisies par nouveauté visuelle (SigLIP), conserve **75 % des fenêtres**, contre 58 % en gardant 1 capture sur 5. Le 80/20 tient aussi sur l'image, avec un petit modèle de 4 ms.

**Limites (non vérifié)** :
- une seule journée, une seule personne ;
- « fenêtre » et « app » ne sont que des approximations de « tâche » ;
- le texte n'a pas été comparé, car l'API refuse de le renvoyer en SQL pour les captures archivées ;
- UI-JEPA d'Apple, entraîné sur des écrans, aurait peut-être fait mieux, mais ses poids ne sont pas publiés.

## 17. Idée de l'équipe : un trackeur de performance (16/10 soir)
**Avis**
- La version « tableau de bord pour un manager » (scores par salarié) est à écarter.
  - Le droit français est contre : la CNIL juge déjà les captures d'écran régulières disproportionnées et a sanctionné (40 000 € en 2024, 32 M€ contre Amazon, section 11).
  - Ça contredit le positionnement de screenpipe et ce que Louis met en avant : le projet qu'il a étoilé (HiddenSteps) dit « pas de vue manager, jamais », chaque chiffre relié à un vrai événement.
- **Version qui passe** : personnel uniquement — « où est passée ma journée », chaque chiffre relié à une capture réelle, aucun score inventé, provenance visible, l'utilisateur peut corriger. C'est la vue de revue du dérush (track 1), pas un projet à part.
- Si « trackeur » veut dire la performance de screenpipe lui-même (CPU, batterie) : c'est le `bench/` et le correctif double écran, une preuve pour le pitch, pas un track.

## 18. Idée de l'équipe : un FDE virtuel (16/10 soir)
Le pitch : la découverte et la construction se font à distance, plus besoin d'aller chez le client en physique.
**Avis**
- C'est la narrative la plus forte des idées d'équipe, à condition de la traiter comme une histoire, pas comme un scope (un FDE virtuel, c'est six métiers).
- Elle tombe pile :
  - c'est le pitch YC de screenpipe côté entreprise (« turn your company's computer work into AI agents ») ;
  - ils recrutent un Forward Deployed Engineer, et leur flux entreprise (Map → Install → Test → Improve → Deploy) est humain et coûteux ; leur page entreprise reconnaît que les SOP générées « ne sont pas des automatisations testées » ;
  - argument Europe : pas de consultant qui regarde les écrans du client à distance, données en local, engagement limité dans le temps (mode campagne, section 11).
- Elle ramasse les autres idées : la marketplace = fin de mission (publier et installer la skill validée), le trackeur = revue de mission.

**La coupe** : un client, un workflow, une boucle complète, mesuré. Promesse défendable : « la découverte et la construction se font à distance ; le FDE humain valide avant toute action » — pas « le FDE ne se déplace plus », la présence physique servant la confiance et l'accès.

**La boucle**
1. Engagement : une machine volontaire, périmètre déclaré façon en-tête de pipe, consentement visible.
2. Map : le dérush sur l'historique du client → tâches répétées avec preuves, séparées des suppositions.
3. Revue : le FDE choisit une tâche.
4. Construction + test : skill/pipe, 2e entrée + cas d'échec, frontière explicite entre texte généré et code exécuté.
5. Déploiement : journal d'audit, approbations, temps gagné calculé (fréquence × durée).

**Track au rendu** : track 2 si une tâche s'exécute vraiment de bout en bout dimanche ; sinon track 1 (interface de revue de déploiement), la narrative FDE restant le pitch.
**Idée de démo** : le premier client est une autre équipe du hackathon (« personne n'est allé les voir »).
**Non vérifié** : comment Louis verrait le projet (un copilote pour ses FDE ?) — à sonder aux office hours de samedi 18h.

## 19. Ce que screenpipe a dit à l'ouverture (micro du Mac, 16/10 18h44–18h48, transcription de mauvaise qualité)
- Le problème qu'ils résolvent : les entreprises veulent utiliser l'IA pour travailler plus, mais l'IA ne sait pas comment les gens travaillent vraiment. Aujourd'hui, elles paient des ingénieurs pour regarder les salariés faire (exemple cité : le traitement des factures). screenpipe capture ce contexte en continu pour le transformer en agents.
- Le track 1, dans leurs mots : trouver les tâches répétées, les découper très précisément en étapes, avec **la logique des décisions à prendre**.
- Ils ont rappelé le mois gratuit de Business et la possibilité d'arrêter l'enregistrement.
- Idée entendue dans la salle : quand on accompagne une entreprise sur l'IA, screenpipe montre « des trucs qu'ils ne m'ont pas dit ». Et quelques jours de capture suffisent, puisque les process ne changent pas tous les jours (même intuition que le volet 2 de Youssef).
- **Le briefing de 19h (critères du jury) n'est pas encore transcrit.** Le son est enregistré, mais screenpipe le transcrit par paquets, plus tard. Les conversations privées de la salle n'ont pas été recopiées ici.

# Retours utilisateurs screenpipe (au 16/10/2026)

Sources couvertes : Hacker News, GitHub (tickets 2026 et Discussions), Product Hunt (2 avis seulement).
Non couverts : Reddit et X (accès bloqué). Les comparatifs trouvés sont surtout écrits par des concurrents, donc biaisés.
Les fréquences sont estimées.

## Plaintes récurrentes
1. **CPU, RAM, batterie** (très fréquent ; environ 14 tickets « CPU » et 19 « memory » en 2026)
   - « made my CPU melt » (M1, Launch HN), CPU à 700 % sur un M3 Max (HN 2024).
   - Batterie : #7364. Gels de 7 à 9 s : #2602. Jusqu'à 12,5 Go sous Windows : #7322, #2380.
2. **Fiabilité, surtout sous Windows et pour l'audio** (environ 110 tickets « windows » et 72 « audio » en 2026)
   - L'app dit « healthy » alors que la capture est arrêtée : #5090. Mise à jour automatique brutale : #3474.
   - Beaucoup de tickets sont fermés par un bot sans être résolus (ex. #3996).
3. **Vie privée et conformité** (dominant sur HN)
   - Employeurs européens, agent compromis qui lirait tout via l'API locale, et en 2024 la collecte d'emails des
     personnes ayant mis une étoile au dépôt (skerritt.blog).
4. **Licence et prix** : passage de MIT à source-available, fin des licences à vie, quotas d'IA cloud faux (#4113, #5765).
5. **Trop de bruit, pas assez de valeur** (le problème de fond)
   - « too much noise vs signal » (HN 2024).
   - #5045 (interne) : le churn vient d'une valeur peu claire, aggravée par les pannes de capture.
   - #2285 : résultats de recherche quasi identiques qui « wasting LLM context ».
   - L'OCR ne distingue pas un message reçu d'un message tapé (HN 47652229).
6. **Premier lancement** : permissions macOS redemandées (#2510), raccourci global qui casse les flèches (#2219).

## Besoins non couverts
- Sources citées : séparer la capture brute de la mémoire dérivée, avec confiance et expiration par souvenir (HN).
- **Mémoire bornée pour les agents** (#5496) : le top 200 des souvenirs pèse environ 283 000 caractères (60 à 75 000
  tokens) injectés dans CLAUDE.md et AGENTS.md, qui restent en place après « stop syncing ».
  - Sur le Mac de Youssef : rien d'injecté dans `~/.claude/CLAUDE.md`, mais environ 22 skills screenpipe installées dans
    `~/.claude/skills/`.
- La date seule ne suffit pas à juger la pertinence (HN 47652265).
- Plusieurs machines et équipe : les souvenirs des pipes ne se synchronisent pas (#3996) ; la base ne se copie pas sans
  corruption (#2907).
- Capture limitée à un périmètre (une app, travail/perso), traitement séparé de la capture (discussion #2686).
- Feuille de temps facturable fiable sur 2 machines (#5620). Tâches Linear automatiques (Product Hunt).
  Agents déclenchés par des événements (#3525).
- Migration depuis Littlebird, Pieces ou Rewind (discussion #5866).

## Ce qu'ils aiment
- Le local, avec un modèle au choix.
- Le seul outil vraiment fait pour tourner 24 h/24.
- Une API et un MCP faciles à brancher.
- Multiplateforme.
- Une équipe réactive.

## Concurrence perçue
- Rewind/Limitless (arrêté), Microsoft Recall (Windows seulement), OpenAI Chronicle (Louis répond dans la
  discussion #3021), Claude CoWork, Littlebird, Pieces, LUCI, Carly.
- Open source : Daydream, OpenRecall, Dayflow, Familiar, DoneThat.

## 5 problèmes pour 48 h
1. **Mémoire bornée et dédoublonnée pour les agents** (#5496, #2285) : budget de tokens, mesure avant et après à qualité
   égale.
2. **Chaque affirmation sourcée**, avec confiance, expiration, et la possibilité d'accepter ou de corriger (HN, #5045).
3. **Workflows repérés en tenant compte du sens** : lu ou tapé, émetteur ou destinataire.
4. **Workflow → skill testée**, avec un aperçu à valider avant exécution.
5. **Mémoire d'équipe respectueuse de la vie privée** : périmètre choisi, synchronisation (#3996), journal d'accès des
   agents.

# Recherche : mémoire persistante et efficacité du contexte pour screenpipe

Rapport du 16/10/2026 (agent de recherche). Points vérifiés et non vérifiés :
- **Vérifié en ligne** : les identifiants arXiv, les dates et les résultats annoncés par les auteurs.
  Je n'ai reproduit aucun résultat moi-même.
- **« (mém.) »** : référence citée de mémoire, non revérifiée.

## A. Compression vidéo en streaming et sélection par nouveauté (étape : capture)
- **STC, CVPR 2026** — https://github.com/lern-to-write/STC
  - Réutilise le calcul des images proches dans le temps et élague les tokens peu utiles. −45 % de préremplissage,
    environ 99 % de la précision.
  - Pour screenpipe : si l'arbre d'accessibilité ne change pas, réutiliser l'extraction précédente au lieu de relancer
    l'OCR.
- **NovaCov, arXiv 2608.01169** (préprint, pas de code)
  - Sélection « par ensemble » : on garde ce que l'historique ne couvre pas encore. Algorithme glouton avec garantie
    (1−1/e).
  - Pour screenpipe : ne stocker que les lignes ou n-grammes qui ajoutent de la couverture à la session. C'est la
    correspondance la plus directe avec ce qu'on a mesuré.
- **FluxMem, CVPR 2026** — https://github.com/ShareLab-SII/FluxMem
  - Mémoire en 3 niveaux avec des seuils qui s'adaptent à la scène. −65 % de tokens.
  - Pour screenpipe : un seuil de nouveauté par app, plus élevé pour un chat IA en train d'écrire.
- **ProtoKV, arXiv 2606.26762** : la fenêtre récente reste exacte, le reste devient des « prototypes » par fenêtre ou
  document.
- **StreamingVLM** (2510.09608, mém.) et **MovieChat** (2307.16449, mém.) : fusionner les images consécutives presque
  identiques.

## B. Mémoire hiérarchique et consolidation
- **MemGPT/Letta** (2310.08560, mém.) : pagination entre le contexte et une mémoire externe.
- **Sleep-time compute** (Letta) : la mémoire est réorganisée pendant les temps morts. Un pipe horaire pourrait
  consolider au lieu de seulement résumer.
- **H-MEM, EACL 2026** : 4 niveaux d'abstraction et une recherche guidée de haut en bas
  (jour → session → épisode → capture).
- **A-Mem** (2502.12110, mém.) et **Mem0** (2504.19413, mém.) : notes reliées entre elles, avec ajout, mise à jour et
  suppression.
- **MemoryOS** (2506.06326, mém.) : court, moyen et long terme.
- **Zep/Graphiti** (2501.13956) : graphe de connaissances temporel ; un fait périmé est marqué invalide, pas supprimé.
- **AgeMem** (2601.01885) : les opérations de mémoire sont apprises par renforcement. Acceptation à ACL non confirmée,
  trop lourd pour 48 h.

## C. Segmentation en événements
- **EM-LLM, ICLR 2025** (2407.09450) : les frontières d'épisode sont placées sur la « surprise ». La recherche combine
  la similarité et la proximité dans le temps.
- **FOCAL** (2604.19541, avril 2026) — **le plus proche de screenpipe**
  - Chaîne : un filtre léger, puis un agent texte qui attribue l'activité à une tâche, puis un modèle vision appelé
    seulement si besoin.
  - Résultats : −60,4 % de tokens, −72,3 % d'appels au modèle vision, rappel de l'info clé de 0,38 à 0,61, robuste aux
    allers-retours A→B→A.
  - Code non publié.

## D. Traces d'usage et induction de tâches
- **Task Model Induction** (2608.20319, EMNLP 2026 selon le dépôt) — https://github.com/Yucheng-Jiang/task-model-induction
  - 74,9 % des étapes retrouvées, contre 30,3 % pour la meilleure méthode concurrente ; +30 % de réussite des skills.
- **Workflow Induction Toolkit** (2510.22780) — https://github.com/zorazrw/workflow-induction-toolkit
- **AWM** (2409.07429, mém.) : routines réutilisables tirées des trajectoires réussies.
- **Watch and Learn, CVPR 2026** (2510.04673) : retrouver les actions à partir des changements d'écran.
- **Task mining / RPA** (2204.00751, 2207.12054) : format standard des journaux d'interface.

## E. Combien garder ?
- **Retain or Consolidate?** (2607.17545) : brut si le budget est large ; consolider s'il est serré (jusqu'à +48 % sur
  LongMemEval).
- **EvoMemBench** (2605.18421) : le contexte long brut reste très compétitif.
- **LifeDialBench** (2604.11182) : sur des journaux de vie, les mémoires sophistiquées ne battent pas un RAG simple.
- **Loi du budget mémoire** (2606.20726) : la précision monte avec le log du budget, et le gain baisse avec
  l'ancienneté de l'événement.
- **Rate-distortion** (2605.10870) : garder ce qui change les décisions.
- **Leçon** : enlever les doublons sans perte d'abord, ne résumer que si le budget l'exige, et garder un lien vers le
  brut.

## F. Sécurité
- **Bad Memory** (2607.14611) : un souvenir piégé compromet les sessions suivantes.
- **Utility Under Attack** (2608.21230) : 1,2 % du corpus empoisonné fait tomber la précision de 0,85 à 0,30.
  Le filtrage à l'écriture n'a rejeté aucun des 360 souvenirs empoisonnés.
- **Empoisonnement depuis des pages web** (2606.04329).
- **Pour screenpipe** : étiqueter la provenance (app, URL, écran regardé ou non) ; rien ne devient un fait sans une
  action de l'utilisateur.

## Shortlist pour 48 h
1. **Filtre de nouveauté + écran regardé + anti-rafale** (NovaCov, STC, FluxMem).
   Mesure : tokens par heure et rappel de l'info clé.
2. **Épisodes découpés sur la surprise** (EM-LLM, FOCAL).
3. **Consolidation pendant les temps morts, en 3 niveaux** (Letta, Retain or Consolidate, Graphiti).
   Mesure : environ 30 questions maison.
4. **Induction de workflows** (TMI, AWM) → skills.
5. **Étiquettes de provenance.**

## Jeux de données
| Jeu | Contenu | Continu ? | Accès |
|---|---|---|---|
| HumanWork (2510.22780) | 38 sessions, 42,8 h, captures + souris/clavier | une tâche par session | lien non trouvé |
| GuideBench, CVPR 2026 (huggingface.co/datasets/saelyne/GuideBench) | 120 enregistrements, 67,5 h | long, ouvert | accès sous conditions |
| VideoCUA (huggingface.co/datasets/ServiceNow/VideoCUA) | environ 10 000 tâches, 55 h, 87 apps | découpé par tâche | MIT |
| AgentNet (huggingface.co/datasets/xlangai/AgentNet) | 22 600 trajectoires, avec arbre d'accessibilité | découpé par tâche | MIT |
| A11y-CUA (2602.09310) | 40,4 h, 60 tâches | découpé par tâche | lien non trouvé |
| computer-use-large (huggingface.co/datasets/markov-ai/computer-use-large) | 12 300 h de tutoriels, sans événements | monté | CC-BY-4.0 |
| Screenomics | une capture toutes les 5 s, surtout sur téléphone | vraiment continu | sur demande |
| NTCIR Lifelog | caméra portée sur soi | continu, pas d'écran | inscription |
| Apple UI-JEPA (IIT et IIW) | environ 2 500 clips d'écran de 25 s | clips | téléchargement direct |

**Conclusion** : aucune vraie journée de travail n'est publique. Aucun jeu ne contient deux écrans ou un chat IA.
→ Utiliser nos propres journées avec une trentaine de questions, plus un jeu synthétique A→B→A construit à partir
d'AgentNet ou VideoCUA.

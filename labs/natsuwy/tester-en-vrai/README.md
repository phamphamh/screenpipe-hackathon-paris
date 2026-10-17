# Tester en vrai (labs/natsuwy/tester-en-vrai)

Le pack de workflows de phamphamh (`labs/phamphamh/workflows/pack.py`) **génère** une skill par tâche répétée, la **teste sur son texte** (chaque étape a une consigne, chaque décision est marquée), puis la **déploie** (copie). Il manquait deux choses : vérifier que Claude **fait la tâche correctement** avec la skill, et le faire **agir dans des apps**. C'est ce dossier.

| Fichier | Ce qu'il fait |
|---|---|
| `bac_a_sable.py` | faux Gmail + faux Sage en ligne de commande (lire les mails, chercher un article, créer/valider une commande, brouillon/envoi). Chaque appel est tracé dans `actions.jsonl`. |
| `scenarios/saisie-commande.json` | 4 cas pour « Saisir une commande reçue par mail dans l'ERP » : commande propre, 2e commande (autre client), référence inconnue (l'exception observée), écart de prix. Données fictives. |
| `tester_en_vrai.py` | pour chaque cas, un dossier jetable avec la skill + le bac à sable, un `claude -p` qui n'a le droit qu'à la skill et au bac à sable, puis on vérifie **l'état final des apps**. Écrit `rapport.json` + `rapport.md`. |
| `exemples/` | deux rapports réels (17/10). |

**Lancer** (il faut la commande `claude`) :
```sh
python3 labs/phamphamh/workflows/pack.py pack labs/phamphamh/demo/resumes --these '{"id":"t2","nom":"Prépare","autonomie":2,"humain":"valide avant envoi","tests_avant":[],"suivi_apres":[]}'
python3 labs/natsuwy/tester-en-vrai/tester_en_vrai.py donnees/workflows/t2/saisir-une-commande-recue-par-mail-dans-l-erp
```
≈ 20 s, les 4 cas en parallèle. Rapport dans `donnees/en-vrai/<skill>/<horodatage>/` (ignoré par git).

**Les règles vérifiées** (selon l'autonomie de la thèse, lue dans `workflow.json`) :
- toujours : la skill a été chargée ; sur une exception, aucune commande validée, aucun mail envoyé, rien d'inventé (ni la référence inconnue, ni le prix contesté) et le compte rendu signale le problème ;
- autonomie 1-2 : la commande est créée **en brouillon** avec les bonnes lignes, un **brouillon** de réponse avec le numéro est prêt dans Gmail, rien n'est envoyé ni validé ;
- autonomie 3-4 : la commande est **validée** et le client **reçoit** le numéro.

**Résultats du 17/10** (skills générées par `pack.py` sur la démo Maison Corvo) :
- autonomie 3 « agit et notifie » : **4/4** — commande saisie, validée, client prévenu ; arrêt net sur la référence inconnue et sur l'écart de prix.
- autonomie 2 « prépare » : **3/4 puis 2/4** — les exceptions sont toujours bien gérées, mais sur les cas propres Claude écrit la réponse **dans son compte rendu** au lieu d'un brouillon Gmail. Cause : la skill dit « Montre exactement ce qui va partir, attends un accord » ; elle devrait dire « prépare-la en brouillon dans Gmail ». Piste pour `pack.py` (non modifié ici).

**Ce que ce n'est pas** : le vrai Gmail ni le vrai Sage. Pour la démo, le bac à sable montre le comportement ; en vrai, il faudrait un connecteur (MCP Gmail, API de l'ERP) à la place de `bac_a_sable.py`, avec les mêmes vérifications. Un seul scénario pour l'instant (la tâche n°1) ; en ajouter un = un fichier JSON dans `scenarios/`.

**Pour le brancher dans le parcours** (`labs/phamphamh/parcours/`) : `tester_en_vrai.py` renvoie 0 si `pret`, 1 sinon, et `rapport.json` a un champ `verdict` (`pret` / `a_revoir`) comme `pack.tester`.

# Pack de workflows (labs/phamphamh/workflows)

Après l'audit, le client choisit une **thèse de déploiement** (autonomie 1 suggère · 2 prépare, l'humain valide · 3 agit et notifie · 4 autonome). Pour chaque tâche répétée, `pack.py` **génère** une skill Claude Code (`SKILL.md` + `tests.json` + `workflow.json`), la **teste** à sec sur des entrées observées, puis la **déploie**. Python 3 seul, sans LLM par défaut.

## Les 4 fonctions (`import pack`)
| Fonction | Renvoie |
|---|---|
| `generer(tache, these, sortie=None, ia=False)` | chemin du dossier de skill (défaut `donnees/workflows/<id thèse>/<nom>/`, ignoré par git). `ValueError` si la tâche n'a aucune étape ou si la thèse est invalide. `ia=True` affine via `claude -p` ; la version affinée n'est gardée que si elle repasse ses tests (sinon gabarit gardé, raison dans `workflow.json` → `ia`). |
| `tester(dossier_skill, entrees=None)` | `{"cas","passes","echecs":[{"cas","raison"}],"avertissements","couverture_etapes","deuxieme_entree","verdict":"pret"|"a_revoir","message"}`, écrit aussi `rapport-tests.json`. `entrees` = liste de tâches au format du résumé (la même tâche chez une autre personne) ou `{"preuves":[…]}`. |
| `deployer(dossier_skill, cible, forcer=False, poste=None)` | reçu `{"deploye": true, "quand","cible","chemin","these","autonomie","tests",…}` ou `{"deploye": false, "raison"}`. Cibles : `local-demo` → `donnees/deploiement/<poste>/skills/<nom>/` ; `equipe` → `labs/phamphamh/workflows/deployes/<nom>/`. Jamais `~/.claude`. Refus si le dernier test n'est pas `pret`, sauf `forcer=True`. |
| `pack(audit_taches, these, sortie=None, ia=False)` | `[{"id","titre","heures_semaine","gain_estime_h","autonomie","verdict","couverture","chemin_skill","personnes","libelles","deuxieme_entree","echecs"}]` trié par gain. `audit_taches` = liste de résumés (seuls les `valide_par_la_personne: true` comptent), un résumé, ou une liste de tâches. |

Règles du test (pas de faux succès) : chaque étape **observée** doit correspondre à une instruction (même verbe + 60 % des mots-clés) ; chaque app utilisée doit être nommée dans la skill ; chaque décision porte « VALIDATION HUMAINE » si autonomie ≤ 3 ; chaque exception connue est traitée. Aucune entrée observée → `a_revoir`, « pas assez de données ». Si la thèse demande de « rejouer sur la 2e entrée » et que personne d'autre ne fait la tâche → `a_revoir`.
Gain estimé = heures/semaine (toutes les personnes) × part automatisable (1 : 25 %, 2 : 50 %, 3 : 75 %, 4 : 90 %), réduite de moitié sur la part des étapes « décision » quand l'autonomie ≤ 3.

## Pour le serveur (`app/serveur.py`, à brancher)
```python
sys.path.insert(0, os.path.join(LAB, "workflows")); import pack as wf
# POST /api/pack              {"campagne": "demo"|"equipe", "these": {...}}      → wf.pack([r for _, r, _ in participants(campagne)], these)
# POST /api/workflow/tester   {"chemin_skill": "...", "entrees": [...] | null}  → wf.tester(chemin_skill, entrees)
# POST /api/workflow/deployer {"chemin_skill": "...", "cible": "local-demo"|"equipe", "forcer": false} → wf.deployer(...)
```
`chemin_skill` est relatif à la racine du dépôt (celui que renvoie `pack`). Côté serveur, n'accepter que des chemins sous `donnees/workflows/` ; `ValueError` → 400.

## En ligne de commande
```sh
python3 pack.py pack labs/phamphamh/demo/resumes --these '{"id":"test","nom":"Test","autonomie":2,"humain":"valide avant envoi","tests_avant":["rejouer sur la 2e entrée"],"suivi_apres":["temps gagné mesuré"]}'
python3 pack.py tester donnees/workflows/test/<nom>
python3 pack.py deployer donnees/workflows/test/<nom> --cible local-demo
python3 -m unittest test_pack     # depuis ce dossier
```
Démo Maison Corvo (thèse ci-dessus) : 3 skills `pret` (saisie de commande, relance de devis, fiche technique), 2 `a_revoir` parce que l'outil change chez la 2e personne (Zendesk, Slack/Sage/Pennylane), 4 `a_revoir` faute de 2e entrée.

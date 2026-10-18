# La démo DeloAI · Atelier Nova

Quatre écrans : **les données** (d'où elles viennent, qui sont les 6 salariés), **l'audit** et **les écarts** (le dashboard d'adamaass renommé DeloAI, `../dashboard-nova/`), puis **les agents** : l'agent « Rapport de ventes » déployé dans le vrai back-office Magento, qui tourne tout seul toutes les 15 min, avec son écran, son journal et ses chiffres.

**Lancer** :
1. la boutique de test : voir `../boutique/README.md` (http://localhost:7780) ;
2. `python3 labs/phamphamh/agents-nova/serveur.py` → http://localhost:8798.

| Fichier | Rôle |
|---|---|
| `agent_rapport.py` | l'agent : rejoue les étapes observées (Reports › Orders, période, Show Report, lecture des totaux, export CSV), une capture et une ligne de journal par action |
| `serveur.py` | la page + le planificateur (variable `INTERVALLE`, en minutes) + `/api/etat` et `/api/lancer` |
| `index.html` | les 4 écrans (flèches ← →) |
| `construire_donnees.py` → `donnees.json` | les 6 salariés et l'extrait brut de Sophie (lit `donnees/nova/`) |
| `script.md` | le texte de la démo, avec les chiffres et leur source |

Journal, captures et rapports : `donnees/agents-nova/` (non commité).

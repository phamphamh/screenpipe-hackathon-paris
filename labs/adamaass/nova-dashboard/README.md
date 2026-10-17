# Dashboard d'audit · Atelier Nova

Le rapport d'audit en **5 questions**, pensé pour un jury sans contexte. Palette d'orja.io (noir `#0a0a0b`, cuivre `#e5a276`) ; thème clair pour un projecteur. Mêmes données que le portail CAIbinet Nova (`../caibinet-nova/data.js`).

**Voir** :
```
python3 -m http.server 8790 --directory labs/adamaass
# → http://localhost:8790/nova-dashboard/index.html
```

## Les écrans
| Menu | Question | Le graphe principal |
|---|---|---|
| 1. Contexte | Ce qu'on a observé | entonnoir : captures → moments → tâches → problèmes → skills |
| 2. État des lieux | Ce qu'on a trouvé | coût annuel (anneau) et problèmes les plus chers |
| 3. Temps perdu | Où part le temps ? | heures par écran Magento, par équipe |
| 4. Manque à gagner | Qu'est-ce qui coûte le plus ? | treemap du coût, causes du temps perdu |
| 5. Recommandation | Que faire, dans quel ordre ? | cascade des heures perdues, skill après skill |
| Annexe · Méthode | Méthode et limites | les deux formules, les 4 limites |

## Les règles de lecture
1. **Trois niveaux** : la réponse de l'écran et son chiffre héros (le plus gros), puis une phrase-clé chiffrée par carte, puis le graphe en retrait. Un seul élément coloré par graphe : celui de la phrase-clé.
2. **Une couleur = un sens** : cuivre = argent, vert = récupéré, rouge = perte, gris chauds = équipes.
3. **Le clic ouvre le détail** (↗ sur ce qui se clique) ; cliquer une équipe dans un graphe filtre tout l'écran, une pastille « Filtre : … ✕ » en haut le retire.
4. **Mode Présenter** : flèches ← →, la carte « preuve » de chaque écran ressort.

## Les chiffres
Simulation ×10 (`construire.py --echelle 10`) : 6 salariés réels WONDERBREAD → 60 salariés. Coût = heures × 46 semaines × 38 €/h ; gain d'une tâche = son coût × la part de son temps que la skill rend. Les goulots ne s'additionnent pas (une tâche peut en cumuler plusieurs) : ils sont montrés en % des heures perdues.

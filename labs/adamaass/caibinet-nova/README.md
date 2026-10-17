# CAIbinet · Atelier Nova (version allégée)

Le portail client **CAIbinet** de tmschrib (`labs/tmschrib/dashboard-client/`), même style et mêmes 6 écrans, rempli avec les **vraies données d'Atelier Nova** : 6 salariés fictifs du back-office e-commerce construits à partir de WONDERBREAD (Stanford, CC-BY-4.0), voir `labs/adamaass/README.md`.

**Voir** : servir le dossier puis ouvrir la page.
```
python3 -m http.server 8790 --directory labs/adamaass
# → http://localhost:8790/caibinet-nova/index.html
```
(`data.js` est déjà généré : pas besoin des données brutes pour regarder.)

**Régénérer** `data.js` (il faut `donnees/nova/`, jamais commité) :
```
python3 labs/adamaass/caibinet-nova/construire.py
```

## D'où viennent les chiffres
| Écran | Source |
|---|---|
| Vue d'ensemble, Problèmes | fusion officielle (`labs/phamphamh/fusion/fusion.py`) des 6 résumés validés : 19 tâches, 11 communes à ≥ 3 personnes (les 8 autres ne sont pas détaillées) |
| Interactions, Temps & outils | moments de la brique A : écran Magento visité (route d'URL), heure, enchaînements d'écrans, par équipe de 3 |
| Business case, Pilotage | coût = heures × 46 semaines × 38 €/h ; gain = coût × score d'automatisation (fusion officielle). Pilotage = **projection**, rien n'est en production |

Ce que Nova ne mesure pas (attentes entre équipes, messagerie, copier-coller) est écrit « Non mesuré », jamais inventé.

## Les règles d'allègement
Inspirées des dashboards d'audit et de pilotage (Drata, CloudBees, Strix, portails clients) :
1. **Un verdict par écran**, en une phrase, en haut : le client lit d'abord « où on en est », pas un mur de cartes.
2. **3 chiffres clés au plus** (`maxKpi`), le plus utile en premier ; un « non mesuré » passe en dernier, donc disparaît.
3. **Le reste replié** sous « Voir le détail » (divulgation progressive) : courbe par jour, couverture, conformité, heatmap, enchaînements, hypothèses, investissement… Rien n'est supprimé.
4. Une grille qui n'a plus qu'une carte prend toute la largeur ; les 3 chiffres restent sur une ligne jusqu'au téléphone.

## Ce qui change par rapport au code de tmschrib
`index.html` et `styles.css` sont copiés (styles ajoutés à la fin), `app.js` est copié avec des retouches ciblées :
- `statRow` limité à `DATA.maxKpi` ; `alleger(route)` après chaque rendu (verdict + détail replié, liste `A_REPLIER`) ;
- textes devenus des données (titres « Copier-coller », « Répartition par application », message sans poste à relancer, matrice d'attente vide, abonnement, nombre de modules) ;
- échelle de la courbe de pilotage calculée (elle était fixée à 80 h) et barres avant/après calculées (elles étaient fixées à 68,5 h → 19,7 h) ;
- 7e couleur pour la catégorie « Accueil ».
Le portail d'origine dans `labs/tmschrib/` n'est pas modifié.

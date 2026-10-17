# La 2e entrée — la même tâche chez plusieurs personnes

**La pièce de 09125o.** Le kit de rendu exige « une 2e entrée » (et le storyboard de la vidéo, plan 1:25–1:45 : *la skill tourne sur une 2e entrée*). La fusion du produit regroupe bien les tâches faites par plusieurs personnes, mais rien ne montrait **les deux façons de faire côte à côte** — ni ce que la skill doit encore absorber quand une personne fait la même tâche autrement.

## Ce que ça fait
`construire.py` relit les **résumés validés** d'une campagne (la démo Maison Corvo par défaut), refait tourner **le regroupement officiel** (`labs/phamphamh/fusion/fusion.py`, importé tel quel — rien n'est recalculé à la main) et produit :

- `resultat.html` — la page : pour chaque tâche commune, le tableau des étapes personne par personne (badges observé / supposé, app de chaque étape, mention « outil différent »), puis le bloc « Ce que ça change pour la skill » (la façon de référence que la skill reprend + l'écart à couvrir pour les autres) ;
- `RESULTAT.md` — le même résultat en chiffres (pour le pitch ou le journal).

## Ce que ça montre sur la démo (17/10)
- **5 tâches** faites par ≥ 2 personnes ; 5 salariés concernés ; **2 tâches à outil variable** ; **0 étape hors de la façon de référence**.
- L'exemple qui parle : « Préparer le reporting hebdo » — 4 personnes, mêmes 3 étapes, mais l'export change (HubSpot / Sage / Pennylane) et l'envoi aussi (Gmail / Slack). « Répondre aux demandes de délai » — même texte d'étape, Gmail vs Zendesk.
- Conclusion assumée : sur la démo, les **étapes** sont couvertes (la façon de référence suffit), ce sont les **outils** qui ne le sont pas. C'est la liste de courses pour la skill — pas une promesse.

## Lancer
```sh
python3 labs/09125o/deuxieme-entree/construire.py
# autre campagne : --resumes donnees/<pseudo>   (les résumés non validés ne comptent jamais)
```

## Limites (écrites dans la page elle-même)
- Démo fictive, étiquetée ; sur une campagne réelle la page s'affiche « à relire avant tout partage ».
- Relecture individuelle d'abord : seuls les résumés `valide_par_la_personne: true` comptent ; le Wrapped n'affiche que des agrégats (« moins de 3 personnes → masqué »), cette page-ci est une vue de travail.
- La skill actuelle reprend **une** façon de référence → idée transmise à phamphamh : fusionner les étapes (union des façons) au lieu de la référence seule.

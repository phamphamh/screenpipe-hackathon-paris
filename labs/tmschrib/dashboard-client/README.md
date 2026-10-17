# Dashboard client — Étude & Pilotage

Portail client en HTML/CSS/JS vanilla (zéro dépendance), pour un cabinet de conseil qui vend des
études d'efficacité opérationnelle (façon screenpipe) et veut que son client suive l'avancement
jour par jour, puis le pilotage continu une fois le logiciel sur mesure livré.

Construit à partir d'une maquette fournie (`Dashboard client — Étude & Pilotage.pdf`), avec les
mêmes données de démonstration : client fictif « Maison Verlaine », 52 postes, 6 équipes.

## Lancer

```sh
cd labs/tmschrib/dashboard-client
bun server.js        # ou : bun run start
```

→ http://localhost:4300

## Les 6 écrans
1. **Vue d'ensemble** — stepper d'avancement de l'étude, KPIs, collecte en direct, couverture par équipe, premiers signaux, postes à relancer, conformité RGPD.
2. **Problèmes détectés** — liste filtrable + détail (maître-détail), validation de constat.
3. **Interactions & goulots** — carte réseau entre équipes, matrice des temps d'attente.
4. **Temps & outils** — répartition du temps par application, heatmap des tâches répétitives.
5. **Business case** — feuille de route des modules par rentabilité, avant/après, ROI.
6. **Pilotage continu** — vue post-étude (sidebar en mode « archives »), courbe de gains, demandes d'évolution.

Toutes les données sont statiques (`data.js`), générées pour la démo — rien de réel.

## Lien avec le reste de l'équipe
Proche dans l'esprit du « cabinet IA automatisé » de `labs/phamphamh/parcours/` (étude côté
consultant → rapport → déploiement d'agents) mais vu côté **client final** : ce portail est la
page que le client du cabinet ouvrirait pour suivre sa propre étude, pas l'outil du consultant.
Les deux pourraient se brancher l'un sur l'autre (ce portail consommant les sorties du parcours
de phamphamh) si ça sert le produit — à discuter avant de fusionner quoi que ce soit.

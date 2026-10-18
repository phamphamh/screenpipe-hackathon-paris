# Logo DeloAI — concepts, round 2 (checkpoint)

Faits avec le skill **logo-design** de kaankiziltug (`git@github.com:kaankiziltug/logo-design-skill.git`, version `0ecf52e`) — méthode : brief → conventions de la catégorie (bibliothèque de 1 400+ logos) → concepts en SVG noir → audit + rendus + loupé d'œil → planche de checkpoint. **Arrêt volontaire au checkpoint** : le kit (couleur, lockups, favicon/app-icons, planche de présentation, guide) ne se construit qu'après le choix d'une direction.

## Brief (hypothèses, à corriger)
- **Nom** : DeloAI (Delo + AI), casse « DeloAI » comme les slides.
- **Quoi** : un cabinet de conseil IA natif + des agents qui travaillent dans les outils (« votre cabinet et votre ESN, dans votre poche »).
- **Public** : dirigeants, équipes ; jury 42 Paris.
- **Adjectifs** : précis, tranquille, agentique, proche.
- **Contraintes** : monochrome d'abord (UI de la démo + README), tenir à 16 px, éviter les clichés de la catégorie (cerveaux, sparkles, bleu, nœuds neuronaux).
- **Retour d'équipe après le round 1** : « aucun ne convient » ; besoin reformulé = **une icône produit** + **plus parlant** (les agents qui agissent). Le round 1 (D tracé / boucle / poche) est resté dans l'historique git, écarté le 18/10.

## Les 3 concepts
| | Concept | Type | L'idée | Risque |
|---|---|---|---|---|
| **D** | `d-le-run.svg` — **Le Run** (recommandé) | lettreform + produit | Le D de DeloAI avec le bouton Run dans son creux : le travail part tout seul (le bouton de la démo). | Le triangle peut se lire « lecteur vidéo » ; à 16 px il ne reste qu'un point clair dans le D. |
| **E** | `e-le-curseur-trace.svg` — **Le curseur tracé** | symbole | Le clic de l'agent et la trace de ses étapes : la démo en une image. | Très explicite (proche d'autres logos de curseurs) ; s'écrase en dessous de 32 px. |
| **F** | `f-la-tuile.svg` — **La tuile** | icône produit | Le produit tel qu'il vit : une icône d'app sombre, le D dedans (et son point). | Le blanc est posé sur le noir pour le concept — au kit, il devient un vrai « trou » (evenodd). |

La planche (`concepts.png`) montre chaque piste en grand et en vraies tailles 64 / 32 / 16 px. Rendus 512 px dans `renders/`. Audit du skill : D et E à **100/100**, F à 91/100 (unique alerte : le blanc de la tuile — voulu, signalé pour le kit).

## Régénérer
```sh
git clone git@github.com:kaankiziltug/logo-design-skill.git
python3 logo-design-skill/skills/logo-design/scripts/svg_audit.py labs/09125o/logo-deloai/*.svg
python3 logo-design-skill/skills/logo-design/scripts/render_png.py labs/09125o/logo-deloai/d-le-run.svg --out-dir /tmp/rendus --size 512
```

## Statut
- 18/10 — round 2 montré à l'équipe. En attente : le choix d'une direction pour construire le kit (couleur + versions inversées, lockups horizontal et empilé, favicon + app-icons, planche de présentation avec mockups, guide d'usage d'une page).

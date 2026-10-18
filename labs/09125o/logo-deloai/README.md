# Logo DeloAI — concepts (checkpoint)

3 concepts faits avec le skill **logo-design** de kaankiziltug (`git@github.com:kaankiziltug/logo-design-skill.git`, version `0ecf52e`) — méthode : brief → recherche des conventions de la catégorie (bibliothèque de 1 400+ logos) → concepts en SVG noir d'abord → audit + rendus + loupé d'œil → planche de checkpoint. **Arrêt volontaire au checkpoint** : le kit complet (couleur, lockups, favicon/app-icons, planche de présentation, guide) ne se construit qu'après le choix d'une direction.

## Brief (hypothèses, à corriger)
- **Nom** : DeloAI (Delo + AI), casse « DeloAI » comme les slides.
- **Quoi** : un cabinet de conseil IA natif + des agents qui travaillent dans les outils (« votre cabinet et votre ESN, dans votre poche »). Audit de ce que l'équipe fait vraiment, puis déploiement d'agents.
- **Public** : dirigeants, équipes ; jury 42 Paris.
- **Adjectifs** : précis, tranquille, agentique, proche.
- **Contraintes** : doit vivre en noir (UI de la démo + README), tenir à 16 px, éviter les clichés de la catégorie (cerveaux, sparkles, bleu, nœuds neuronaux).
- **Conventions vues dans la bibliothèque (ai-ml)** : abstrait, bleu, lignes monolinéaires, symétrie radiale, répétition modulaire — on s'en écarte en restant monochrome et sobre.

## Les 3 concepts (noir & blanc)
| | Concept | Type | L'idée | Risque |
|---|---|---|---|---|
| **A** | `a-le-d-trace.svg` — **Le D tracé** (recommandé) | lettreform | Un D d'un seul trait, ponctué : chaque action est tracée — point final aux tâches répétées. | Le point peut se lire comme une ponctuation d'abréviation. |
| **B** | `b-la-boucle.svg` — **La boucle tracée** | abstrait | Les tâches répétées (points) deviennent une boucle qui tourne toute seule (trait). | Lit « chargement / spinner » ; faiblit à 16 px. |
| **C** | `c-la-poche.svg` — **La poche** | pictural | Le cabinet dans votre poche : une tuile, une ouverture, l'agent dedans. | Peut se lire comme un appareil plutôt qu'une poche. |

La planche (`concepts.png`) montre chaque piste en grand et en vraies tailles 64 / 32 / 16 px. Rendus 512 px dans `renders/`. Audit du skill : 1 seule couleur, aucun texte vivant, géométrie propre (aucune alerte bloquante — seulement des notes « étendre les traits en contours pour le master »).

## Régénérer
```sh
git clone git@github.com:kaankiziltug/logo-design-skill.git
python3 logo-design-skill/skills/logo-design/scripts/svg_audit.py labs/09125o/logo-deloai/*.svg
python3 logo-design-skill/skills/logo-design/scripts/render_png.py labs/09125o/logo-deloai/a-le-d-trace.svg --out-dir /tmp/rendus --size 512
```

## Statut
- 18/10 — checkpoint montré à l'équipe. En attente : le choix d'une direction pour construire le kit (couleur, lockups, favicon + app-icons, planche de présentation avec mockups, guide d'usage).

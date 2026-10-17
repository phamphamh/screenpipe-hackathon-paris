# Kit tournage — vidéo Wrapped (2 min) — pour JA

Extrait prêt à tourner de la section 23 du brief (`.context/hackathon-brief.md`). Objectif : **prise n°1 aujourd'hui 10h**, vidéo finie dimanche matin.

## Avant de tourner (5 min)
- [ ] L'app tourne : double-clic sur `labs/phamphamh/ouvrir-wrapped.command` → http://localhost:8787. Sur le Mac de 09125o, elle tourne déjà.
- [ ] **Deux campagnes, deux usages** :
  - **Démo · Maison Corvo** : entreprise fictive complète → tous les plans du Wrapped dès maintenant. Pour rejouer une prise : `POST /api/reinitialiser-demo`.
  - **Notre équipe** : les plans « vrais » (relecture, dérush, chiffres). Le Wrapped d'équipe n'apparaît qu'à **3 validations** (1 pour l'instant). S'il en manque, ne pas filmer cette page — garder Maison Corvo.
- [ ] screenpipe tourne sur ≥ 2 machines — lancez le B-roll **maintenant** (règle 7 : l'outil en marche vaut mieux que des slides).
- [ ] Choisir le présentateur (voix off) avec JA.
- [ ] Repère : app `labs/phamphamh/app/`, démo `labs/phamphamh/demo/`, mon résumé validé `labs/09125o/campagne/resume-valide.json`.

## Prise par prise
| Temps | À tourner | Notes |
|---|---|---|
| 0:00–0:12 | Plan réel : les 5 machines dans la salle | phrase d'ouverture : « Les entreprises paient des ingénieurs pour regarder leurs salariés travailler. » |
| 0:12–0:22 | Surimpression de chiffres (montage) | 5 personnes, 48 h ; 1 machine en 3 h : 970 captures ≈ 1 M tokens, dont 59 % de copies exactes |
| 0:22–0:45 | Le dérush en vrai | stats du collecteur (24 % gardées sur ce Mac), 44 % d'écrans non regardés, preuve que la chaîne de workflows existante ticke à vide |
| 0:45–1:00 | Relecture : retirer une ligne → « Valider et partager » | à rejouer en direct — c'est le moment « rien ne part sans ce clic » |
| 1:00–1:25 | Wrapped : top 3 des tâches, chiffres cliquables, badges observé/estimé | aucun chiffre par personne |
| 1:25–1:45 | Cas d'échec : score contesté → le classement change ; puis la 2e entrée : la même tâche chez plusieurs personnes (leurs étapes, leurs outils, ce que la skill doit absorber) — écran à filmer : `labs/09125o/deuxieme-entree/resultat.html` | bouton « Créer la skill » (télécharge un SKILL.md ; le fichier généré est aussi au dépôt : `docs/skill-exemple/SKILL.md`) ; puis la page « 2e entrée » |
| 1:45–2:00 | Fin + lien du repo | « Une semaine, sans consultant sur place. Données locales, supprimées à la fin. » |

## Les chiffres à l'écran (relevé du 16/10, 18h52–21h54, 1 Mac, 970 captures)
| Chiffre | Valeur |
|---|---|
| Copies exactes jetables sans perte | 59 % des captures |
| Captures sans nom d'app (écran non regardé, OCR seul) | 44 % |
| Volume brut d'une machine en 3 h | 4,3 M caractères ≈ 1 M tokens |
| 20 % des captures gardées → fenêtres couvertes | 75 % (1/5 au hasard : 58 %) — SigLIP ~4 ms |
| Chaîne de workflows existante | ticke toutes les ~5 min, 0 octet de sortie ; `discover` en échec 3/3 |
| Trous de capture | 63 min en 3 h (écran verrouillé — comportement voulu) |

## Les 7 règles (à ne pas perdre en route)
1. Tout ce qui s'affiche est **réel** (synthétique uniquement si étiqueté — aucun mockup présenté comme fini).
2. **Observé vs estimé** distingués à l'écran.
3. **Aucun temps gagné non mesuré** : gain = fréquence × durée × personnes, preuve cliquable.
4. Boucle complète + **cas d'échec** + **2e entrée** : exigés, pas en option.
5. Confidentialité à l'image : chaque membre ne montre que ce qu'il accepte.
6. Sobre, monochrome, sans emoji ; musique discrète (les voix portent).
7. **Tournage continu** dès maintenant ; déclencher la prise « ligne retirée en relecture ».

## Portes
| Porte | Quand | Fini |
|---|---|---|
| 1 | Sam. 10h | Take 1 sur écrans réels (dérush sur ≥ 2 machines, Wrapped même moche) |
| — | Sam. 18h | Office hours : montrer la boucle (dernière fenêtre pour recadrer le récit) |
| 2 | Sam. 23h | v1 montée, **voix off gelée** |
| 3 | Dim. 10h | Finale exportée + README + description |
| — | Dim. 14h30 | Rendu |

## Pas encore tranché
- **FR ou EN** (sous-titré) selon le jury — décider avant la voix off.
- Les ~20 s flexibles (« premier client ») : seulement si un volontaire se présente, sinon on coupe.

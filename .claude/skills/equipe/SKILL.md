---
name: equipe
description: Règles de travail de l'équipe hackathon screenpipe (chacun construit ce qu'il veut, sans écraser les autres). À utiliser au début de chaque session dans ce dépôt, avant chaque push, quand quelqu'un demande « qui fait quoi », « où en sont les autres », « note ce que j'ai fait », ou veut démarrer une nouvelle idée.
---

# Équipe : chacun construit, personne n'écrase

L'équipe n'a pas de chef de projet. Chacun construit ce qu'il veut et contribue comme il peut. Ce skill fait deux choses :
1. **Savoir ce que font les autres** sans leur demander.
2. **Ne jamais écraser le travail d'un autre.**

## Ton pseudo
`PSEUDO` = le login GitHub de la personne (`gh api user --jq .login`). Sinon, `git config user.name` en minuscules, sans espaces.

## Au début de chaque session (obligatoire)
1. `git pull --rebase origin main`
2. `sh scripts/etat.sh` pour voir qui travaille sur quoi, les dernières entrées du journal et les branches en cours. Résume-le en 3 lignes à la personne.
3. Si l'idée de la personne recoupe le chantier de quelqu'un d'autre, **dis-le-lui avant de coder** (« X fait déjà Y dans `labs/x/` »). Elle décide : rejoindre, se brancher dessus, ou faire autre chose.

## Où écrire (la règle qui évite les conflits)
| Chemin | Qui écrit | Comment |
|---|---|---|
| `labs/<PSEUDO>/...` | **toi seul** | ton bac à sable, tu fais ce que tu veux |
| `chantiers/<PSEUDO>.md` | **toi seul** | ce que tu fais **maintenant** (voir le format plus bas) |
| `journal/AAAA-MM-JJ/HHMM-<PSEUDO>.md` | toi, un **nouveau** fichier à chaque fois | jamais modifier l'entrée d'un autre |
| `labs/<autre>/`, `chantiers/<autre>.md` | **jamais toi** | tu peux lire, copier dans ton lab, ou ouvrir une PR que l'autre accepte |
| fichiers partagés (`produit/`, `README.md`, `.context/`, `app/`…) | tout le monde | une modification **ciblée** juste après un pull, jamais une réécriture complète. Pour un gros changement ou un changement de format : une branche et une PR. |

Promouvoir son travail : quand un truc de ton lab marche et sert à tous, déplace-le dans un dossier partagé, sur une branche avec une PR. Annonce-le dans le journal.

## Le chantier (`chantiers/<PSEUDO>.md`) : mets-le à jour dès que tu changes de sujet
```markdown
# <PSEUDO>
- **En ce moment** : <une phrase>
- **Je touche** : <dossiers ou fichiers>
- **J'ai besoin de** : <rien / quelqu'un qui…>
- **Prêt à réutiliser** : <chemin + une phrase, ou rien>
- Mis à jour : <AAAA-MM-JJ HH:MM>
```

## Le journal : une entrée par avancée qui compte (un truc marche, une décision, un abandon)
Fichier `journal/<date>/<HHMM>-<PSEUDO>.md`, 3 à 6 lignes :
```markdown
# <titre court>
- **Fait** : <ce qui marche maintenant, avec le chemin>
- **Preuve** : <commande lancée, ou résultat mesuré>
- **Pas vérifié** : <ce qui ne l'est pas>
- **Pour les autres** : <ce qu'ils peuvent réutiliser, ou rien>
```
Optionnel, si screenpipe tourne et que la personne est d'accord : `curl -s -H "Authorization: Bearer $SCREENPIPE_API_KEY" "localhost:3030/activity-summary?start_time=<il y a 2 h, UTC>&end_time=<maintenant, UTC>"`. Ajoute **seulement** les noms d'apps et les durées, jamais de texte capturé, et montre-le à la personne avant d'écrire.

## Pousser (toujours de cette façon)
`sh scripts/pousser.sh "<message>"`. Le script :
- récupère le travail des autres, puis rebase ;
- **refuse** si tu as modifié le lab ou le chantier de quelqu'un d'autre ;
- pousse **sans jamais forcer**.
En cas de conflit sur un fichier partagé : garde les deux versions, puis demande à la personne. Ne supprime jamais les lignes d'un autre pour faire passer ton push.

## Interdits
- `git push --force`, `git reset --hard` sur `main`, et réécrire l'historique partagé.
- Un `git stash` sans nom.
- Les clés API, mots de passe, captures d'écran ou transcriptions de qui que ce soit dans le dépôt. Les données screenpipe restent sur les machines, et seuls les résumés validés par la personne concernée peuvent être commités.
- Modifier ce skill sans le dire dans le journal.

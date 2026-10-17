# « Dès que… » — les déclencheurs de la campagne

Le produit ne s'arrête pas à « voici vos tâches répétées ». Pour chaque tâche relue et validée,
cette pièce **détecte et liste les déclencheurs** :

- l'**événement** qui doit lancer l'action (« dès que… ») ;
- la **voie technique** pour y accéder : connecteur entre les apps, appel API ;
- le **cas d'arrêt** : une exception observée → rien d'automatique, quelqu'un est prévenu ;
- l'**info à partager** aux personnes concernées (qui doit savoir, quoi).

Chaque ligne garde sa **preuve** : l'étape observée, son app, observé ou supposé. Rien d'inventé.

## Les fichiers

| Fichier | Quoi |
|---|---|
| `detecter.py` | le détecteur (règles simples sur les étapes relues) |
| `resultat.html` · `RESULTAT.md` · `declencheurs.json` | la **démo Maison Corvo** (6 salariés) |
| `resultat-equipe.html` · `RESULTAT-EQUIPE.md` · `resultat-equipe.json` | la **campagne équipe** (2 résumés validés → regroupement local) |

## Lancer

```sh
python3 detecter.py                       # démo Maison Corvo
python3 detecter.py --resumes labs/09125o/campagne/resume-valide.json \
    labs/adamaass/campagne/resume-valide.json --sortie resultat-equipe.html
```

## Comment c'est détecté

- les étapes **Entrée** de la tâche → l'événement (« dès que… ») ;
- les **exceptions** → le cas qui doit tout arrêter, avec la personne à prévenir ;
- les étapes **Sortie** → l'info à partager à la fin.

Les tâches, les fréquences et le masquage (« moins de 3 personnes ») viennent de la **fusion
officielle** (`labs/phamphamh/fusion/fusion.py`) — mêmes chiffres que le Wrapped. Les formulations
sont proposées par règles à partir des étapes relues : c'est un brouillon à relire comme le reste
(certaines sont marquées « à confirmer »).

## Résultats du 17/10

- **Démo Maison Corvo** : 9 tâches → **22 déclencheurs** (9 connecteurs apps → apps, 8 appels API,
  5 cas d'arrêt). Exemple : *« un bon de commande PDF arrive par mail » → démarrer la saisie
  (connecteur Gmail → Sage) ; « référence inconnue » → appel au commercial, rien d'automatique ;
  fin de tâche → répondre au client avec le numéro de commande.*
- **Campagne équipe** (2 validés) : 6 tâches → 13 déclencheurs, personne par personne
  (la fusion ne force rien sous 3 personnes).

## Où ça se branche (proposition)

**Intégration proposée au produit : [PR #4](https://github.com/phamphamh/screenpipe-hackathon-paris/pull/4)** (branche `integration/declencheurs`) — la fusion porte `declencheurs` par tâche, le Wrapped affiche le bloc dans le zoom de la tâche n°1, et la skill générée gagne la section « Déclencheurs ».

1. **Wrapped** : un bloc « Dès que… » par tâche — le produit dit **quoi brancher**, pas seulement
   quoi automatiser.
2. **SKILL.md** : une section « Déclencheurs » (quand lancer, qui prévenir).
3. **Déploiement** : un connecteur par app (MCP Gmail, API de l'ERP…) — c'est la liste à passer au
   parcours « cabinet IA » (`labs/phamphamh/parcours/`).

Ce n'est pas encore branché pour de vrai : c'est **la liste**. L'exécution en bac à sable est montrée
par `labs/natsuwy/tester-en-vrai/` (faux Gmail + faux Sage, 4/4 en autonomie « agit »).

# Texte de la démo DeloAI (version du 18/10, avec les 3 corrections)

Corrections par rapport au texte de Youssef : (1) Stanford n'a pas filmé ces personnes « au travail » mais sur de vraies tâches de back-office ; (2) « captures » = ce que l'IA a lu, multiplié par 10 ; (3) l'agent montré est celui du rapport de ventes, annoncé à l'étape 1. Ajout d'une phrase sur screenpipe. Les [X] sont remplacés par les chiffres mesurés.

**Écrans** (`python3 labs/phamphamh/agents-nova/serveur.py` → http://localhost:8798) : 1 Les données · 2 L'audit · 3 Les écarts · 4 Les agents. Flèches ← → pour passer de l'un à l'autre.

---

Si vous utilisez screenpipe, vous avez un problème. Et ce n'est pas de votre faute.

Votre ordinateur enregistre tout. Chaque écran. Chaque clic. Chaque réunion. Des milliers de captures par jour.

Et pourtant, vous ne savez toujours pas quoi en faire.

Ce n'est pas nous qui le disons. On a posé la question à Louis, le fondateur de screenpipe. Sa réponse : les utilisateurs ont plein de données, et ils ne savent pas quoi en faire.

La vérité, c'est que le problème n'a jamais été la donnée. C'est le contexte. Savoir quoi regarder. Quoi automatiser. Par où commencer.

Avant, pour ça, il fallait un cabinet de conseil. Des consultants sur place pendant des semaines.

Nous, c'est DeloAI. Un cabinet IA natif. Notre méthode d'analyse vient des grands cabinets. Notre façon de déployer les agents vient des meilleurs laboratoires de recherche. Et personne ne se déplace.

Laissez-moi vous montrer.

**[Écran 1 · Les données]** Atelier Nova. Une boutique en ligne. Ses salariés sont de vraies personnes, filmées par Stanford sur de vraies tâches de back-office. Six personnes, multipliées par dix : 60 salariés. Chez vous, ce seront vos captures screenpipe. Ici, des données publiques, pour ne montrer la vie de personne.

**[Écran 2 · L'audit]** Étape un : l'audit. 55 000 captures lues par l'IA, salarié par salarié.

**[Écran 3 · Les écarts]** Résultat ? 72 000 euros par an partent dans des tâches répétées. Et la première, c'est un rapport de ventes. Toujours le même, sorti 790 fois par semaine. 790.

Étape deux : nos agents en tirent cinq automatisations. La première, ce rapport, s'écrit à partir de ce que les salariés font vraiment.

**[Écran 4 · Les agents]** Étape trois : on l'a déployée ce matin, dans le vrai logiciel de la boutique. Elle tourne en ce moment. Chaque action est tracée. Un rapport en 4 secondes, contre 23 à la main. 790 fois par semaine, c'est 5 heures rendues aux équipes, sans personne au clavier.

Alors la question n'est plus : qu'est-ce que je fais de mes données ?

La question, c'est : qu'est-ce que vous allez faire du temps récupéré ?

DeloAI. Votre cabinet et votre ESN, dans votre poche.

---

**Les chiffres et leur source**
- 6 personnes ×10 = 60 salariés ; 55 510 captures (×10) ; 19 tâches ; 71,7 k€ / an ; 790 rapports / semaine (×10 de 79) : dashboard d'adamaass (`labs/adamaass/caibinet-nova/data.js`).
- 23 s à la main : médiane de 20 enregistrements Stanford « rapport de ventes » (base brute WONDERBREAD).
- 4 s pour l'agent : mesuré à chaque passage dans la boutique de test (affiché en direct sur l'écran 4).
- 5 h / semaine = 790 × 23 s. C'est le temps humain que l'agent remplace, pas un gain en euros.

# Front du Wrapped : relecture (C) et site (E) sur données inventées
- **Fait** : `labs/adamaass/relecture.html` (le salarié masque une app, corrige, retire une tâche, anonymise email / montant / nom de client, puis télécharge `resume-valide-<personne>.json`) et `labs/adamaass/wrapped.html` (10 slides, chaque chiffre cliquable vers son calcul et ses preuves, masquage sous 3 personnes, skill de la tâche n°1, impression en PDF). S'ouvrent par double-clic.
- **Preuve** : vérifié dans le navigateur (bureau et téléphone, pas de défilement horizontal) ; anonymisation testée sur la tâche « devis Brasserie Kléber (18 400 €) » → « devis [client] ([montant]) ».
- **Pas vérifié** : sur un vrai `resume.json` sorti de la brique B ; sur un vrai `insights.json` (la fusion D n'existe pas encore) ; sous Windows.
- **Pour les autres** : le format `insights.json` que le site attend est dans `labs/adamaass/README.md`. Celui ou celle qui fait la fusion (D) peut s'y caler, ou me dire ce qu'il faut changer.

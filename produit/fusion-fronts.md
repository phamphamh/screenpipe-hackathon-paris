# Quel front garde-t-on ? — proposition à trancher par phamphamh et adamaass (5 min)

**État** : deux fronts existent, construits en parallèle hier soir. Ils sont déjà compatibles (même format `resume.json` ; la fusion de phamphamh sait sortir au format d'adamaass). Mais pour la vidéo et la finale, il n'en faut qu'**un**.

## Décision proposée
- **L'app locale de `labs/phamphamh/app/` devient LE produit de démo.** Raisons : elle fait tourner la vraie boucle (onboarding → relecture → fusion → Wrapped) ; c'est elle que la campagne « Notre équipe » utilise déjà (fichiers validés écrits au bon endroit, Wrapped d'équipe à 3 validations) ; ses 10 tests de la section 6 passent.
- **Le front d'adamaass (`labs/adamaass/`) reste dans le dépôt comme référence** et comme source des meilleurs morceaux à porter dans l'app (liste ci-dessous). Rien ne se jette.

## Ce qu'on porte du front d'adamaass dans l'app (par ordre de priorité)
1. **Mode démo « moins de 3 personnes »** (`?seuil=1` chez lui, avec bandeau visible — jamais silencieux) : utile pour filmer le Wrapped aujourd'hui si la 3e validation arrive après la prise.
2. **Masquage par défaut des apps sensibles** en relecture (Spotify, WhatsApp, banque…) : proposées masquées, réactivables par la personne.
3. **Anonymiser un email / un montant / un nom de client** : bouton explicite dans la relecture (l'app actuelle sait retirer et masquer ; elle ne propose pas d'anonymiser).
4. **« Ce qu'on ne sait pas encore »** : la liste des zones d'ombre (tâches vues chez moins de 3 personnes, données manquantes) affichée dans le Wrapped.
5. **Le calcul derrière chaque chiffre** : en plus du moment source, montrer la formule (fréquence × durée × 4,33 × coût horaire).
6. *(si facile)* **Navigation slides** clavier + `#4` dans l'URL, utile pour les prises en direct.

## Ce qui reste chez phamphamh tel quel
- Serveur local (127.0.0.1), bascule de campagne (démo ↔ équipe), onboarding dirigeant.
- Écriture directe du fichier validé au bon endroit (`labs/<pseudo>/campagne/resume-valide.json`) — c'est ce qui a marché pour 09125o.
- Nettoyage liste blanche avant écriture + règles « moins de 3 » dans le code.
- Bouton « Créer la skill » (SKILL.md) — pièce clé du récit.
- Les 10 tests de la section 6 + la démo Maison Corvo (`POST /api/reinitialiser-demo`).

## Ce que ça change pour la vidéo
- JA filme **une seule relecture et un seul Wrapped** : ceux de l'app.
- Si moins de 3 validations à l'heure de la prise : Wrapped filmé avec le **mode démo (bandeau visible)** ou sur **Maison Corvo**.

## Pour trancher
- **phamphamh** : « ok, je porte les morceaux 1→4 avant… »
- **adamaass** : « ok, mon front reste la référence ; j'indique où sont le seuil, la liste des apps masquées, l'anonymisation ».
- Désaccord sur un point : on le note ici, on tranche en 2 minutes en personne.

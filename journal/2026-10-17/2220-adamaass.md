# Dashboard d'audit Atelier Nova : le rapport en 5 questions, prêt pour la vidéo
- **Fait** : `labs/adamaass/nova-dashboard/` — le rapport d'audit lisible sans contexte : Contexte → État des lieux → Temps perdu → Manque à gagner → Recommandation (+ Méthode en annexe). Un chiffre héros par écran, une phrase-clé chiffrée par graphe, détail au clic, mode Présenter (flèches), thème clair pour le projecteur. Palette orja.io. Voir le README du dossier.
- **Données** : `caibinet-nova/data.js` régénéré en **simulation ×10** (60 salariés, `construire.py --echelle 10`). Le portail CAIbinet Nova affiche donc aussi les volumes ×10.
- **Corrigé dans `construire.py`** : le gain d'une tâche pouvait dépasser son coût (gain compté sur 52 semaines, coût sur 46). Le gain = coût × part du temps rendue par la skill. Gain total : 57,0 → **49,3 k€ / an** ; les 5 skills : **30,1 k€** ; skills triées par ce gain.
- **À savoir** : les heures des goulots se recouvrent (une tâche peut avoir plusieurs causes), leur somme (64 h) dépasse les 41 h perdues : ne pas les additionner.
- **Pas vérifié** : l'export PDF (bouton Exporter = impression du navigateur).

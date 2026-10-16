# Briques A et B du Wrapped : elles marchent sur une vraie journée
- **Fait** : `labs/phamphamh/collecteur/collecte.py` (journée → moments, écran regardé seulement, tri 80/20) et `labs/phamphamh/resume/resume.py` (moments → tâches répétées au format commun, un appel `claude -p`). Exemple fictif pour le site : `labs/phamphamh/resume/exemple-resume.json`.
- **Preuve** : journée de Youssef (11h–22h30) → 2 479 captures regardées, 412 moments, 27,7 % des captures gardées, 407 min de travail ; résumé en 30 s → 7 tâches répétées, chacune avec ses preuves horodatées et des limites honnêtes.
- **Pas vérifié** : sur la machine d'un autre ; sur plusieurs jours ; la justesse des fréquences (1 seul jour = extrapolation).
- **Pour les autres** : le site Wrapped peut se brancher dès maintenant sur `exemple-resume.json`. Les vrais résumés restent dans `donnees/` (jamais commités) jusqu'à la relecture.
- **Trouvé** : dans screenpipe 2.7.109, toutes les tâches IA (détection de workflows, Digital Clone, Improve my skills) plantent au démarrage : l'extension `pi-subagents` 0.78 appelle `toToolDeclaration`, absent de la version de `pi-ai` installée. D'où notre propre brique B.

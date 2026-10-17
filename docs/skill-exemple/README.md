# La skill générée, telle quelle

`SKILL.md` est **exactement** ce que produit le bouton « Créer la skill » de l'app (démo Maison Corvo, partie Wrapped), pour la tâche n° 1 : *saisir une commande reçue par mail dans l'ERP* (31 fois/semaine, 11 min à chaque fois, Gmail → Sage).

- Généré le 17/10 en rejouant le code du bouton (`labs/phamphamh/app/wrapped.html`, fonction `telechargerSkill`) sur les insights de la démo servis par l'app locale — mêmes helpers, même gabarit, mêmes données.
- **Testé pour de vrai** : donné à Claude avec une commande piégée (référence inconnue, stock insuffisant, écart de prix) → il s'arrête, applique l'exception prévue (« appel au commercial ») et pose ses questions ; commande propre → tableau de vérification + brouillon de réponse, rien envoyé (journal de Natsuwy, `journal/2026-10-17/1755-natsuwy.md`).
- **Ce qu'il fait / ne fait pas** : lire, vérifier, signaler, préparer. Il n'agit pas tout seul — il faudrait une action branchée (Gmail, ou un ERP de démo).
- Pour le régénérer : lance l'app (`labs/phamphamh/app/serveur.py`), va au **Wrapped** de la démo, clique **« Créer la skill »**.

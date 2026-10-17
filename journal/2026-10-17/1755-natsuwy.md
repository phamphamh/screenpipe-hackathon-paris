# La skill du bouton « Créer la skill » (Wrapped) marche, mais seulement pour préparer
- **Fait** : SKILL.md généré comme `telechargerSkill()` de `labs/phamphamh/app/wrapped.html` sur la démo Maison Corvo (tâche n°1 : saisir une commande mail dans Sage), puis donné à Claude avec une fausse commande et un faux catalogue Sage (CSV).
- **Preuve** : commande piégée (référence inconnue, stock insuffisant, écart de prix) → Claude s'arrête, cite l'exception prévue (« appel au commercial ») et pose 3 questions. Commande propre → tableau de vérification + brouillon de réponse, rien envoyé.
- **Pas vérifié** : la vraie saisie dans Sage et l'envoi Gmail (aucun accès : il faut un connecteur ou une API) ; données de nos vrais postes.
- **Pour les autres** : pour la démo, la skill sait déjà lire, vérifier, signaler et préparer. Pour aller jusqu'à « faire », il manque une action branchée (Gmail, ou un faux ERP de démo).

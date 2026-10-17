# Approbation humaine et journal d'audit
- **Fait** : `--approbation` dans « Tester en vrai » (`labs/natsuwy/tester-en-vrai/`). Valider une commande et envoyer un mail deviennent des demandes en attente ; un humain les approuve ou les refuse avec `approbations.py` (nom obligatoire), et le journal d'audit dit qui a fait quoi et quand.
- **Preuve** : `test_approbations.py` 7/7 (l'agent ne peut pas s'approuver lui-même) ; skill générée à autonomie 3 : 4/4 avec le garde-fou, deux fois de suite, 4/4 sans. Rapport d'exemple : `exemples/rapport-avec-approbation-autonomie3.md`.
- **Pas vérifié** : autonomie 4 ; d'autres tâches que la saisie de commande ; un vrai connecteur (Gmail, ERP) à la place du bac à sable.
- **Pour les autres** : le journal d'audit et la phrase « rien n'est parti sans humain » sont montrables dans la vidéo (09125o) ; le bouton dans le parcours reste à brancher (phamphamh).

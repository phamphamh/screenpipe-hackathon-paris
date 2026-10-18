# La boutique de test (back-office Magento)

Le back-office où travaillent les « salariés d'Atelier Nova » d'adamaass : c'est le site `shopping_admin` de WebArena (Carnegie Mellon), celui sur lequel Stanford a filmé les démos WONDERBREAD. Un vrai Magento 2, rempli de faux produits, clients et commandes.

- **Adresse** : http://localhost:7780/admin (uniquement depuis ce Mac)
- **Identifiants de test** (publics, ceux de WebArena) : `admin` / `admin1234`
- **Installer** : télécharger `shopping_admin_final_0719.tar` (9,6 Go) depuis le lien officiel de la notice WebArena, puis `sh labs/phamphamh/boutique/installer.sh`
- **Docker** : Colima (`colima start --vm-type vz --vz-rosetta`) ; l'image est prévue pour PC, elle tourne via Rosetta. Le script corrige le plantage de php-fpm (opcache sur disque).
- **Arrêter / relancer** : `docker stop shopping_admin` / `docker start shopping_admin` (puis attendre ~1 min ; si la page renvoie 502, relancer `supervisorctl restart php-fpm` dans le conteneur).

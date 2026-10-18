#!/bin/sh
# La boutique de test (back-office Magento de WebArena, CMU) sur ce Mac : http://localhost:7780/admin
# Usage : sh labs/phamphamh/boutique/installer.sh [chemin du .tar]  (par défaut ~/Downloads/shopping_admin_final_0719.tar)
# Il faut Docker (Colima : `colima start --vm-type vz --vz-rosetta`). Identifiants admin : ceux de la notice WebArena.
set -e
TAR="${1:-$HOME/Downloads/shopping_admin_final_0719.tar}"
PORT=7780
if ! docker image inspect shopping_admin_final_0719 >/dev/null 2>&1; then
  echo "Chargement de l'image (plusieurs minutes)…"
  docker load --input "$TAR"
fi
docker rm -f shopping_admin >/dev/null 2>&1 || true
docker run --name shopping_admin --platform linux/amd64 -p 127.0.0.1:$PORT:80 -d shopping_admin_final_0719
echo "Démarrage des services (environ 1 min)…"
sleep 60
# Sur puce Apple (Rosetta), l'opcache en mémoire partagée fait planter php-fpm : cache sur disque à la place.
docker exec shopping_admin sh -c 'mkdir -p /tmp/opcache && chmod 777 /tmp/opcache && printf "pcre.jit=0\nopcache.jit=off\nopcache.jit_buffer_size=0\nopcache.file_cache=/tmp/opcache\nopcache.file_cache_only=1\n" > /usr/local/etc/php/conf.d/zz-rosetta.ini && supervisorctl restart php-fpm'
docker exec shopping_admin /var/www/magento2/bin/magento setup:store-config:set --base-url="http://localhost:$PORT"
docker exec shopping_admin mysql -u magentouser -pMyPassword magentodb -e "UPDATE core_config_data SET value='http://localhost:$PORT/' WHERE path = 'web/secure/base_url';"
docker exec shopping_admin php /var/www/magento2/bin/magento config:set admin/security/password_is_forced 0
docker exec shopping_admin php /var/www/magento2/bin/magento config:set admin/security/password_lifetime 0
docker exec shopping_admin /var/www/magento2/bin/magento cache:flush
echo "Prêt : http://localhost:$PORT/admin"

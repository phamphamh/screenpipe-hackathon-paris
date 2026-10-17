#!/bin/sh
# Met le parcours en ligne sur le VPS (service cabinet-ia, https://cabinet.159-69-41-115.sslip.io).
# Envoie le code et les données déjà agrégées, jamais les exports bruts de donnees/equipe/.
set -e
cd "$(git rev-parse --show-toplevel)"
VPS=root@159.69.41.115
DEST=/opt/cabinet-ia
# photo des postes (heures par personne), calculée ici où sont les exports, pour que le VPS n'en ait pas besoin
python3 -c "import sys, json; sys.path.insert(0, 'labs/phamphamh/parcours'); import serveur; json.dump(serveur.postes('equipe'), open('donnees/audit/postes.json', 'w'), ensure_ascii=False)"
rsync -az --delete --relative \
  --exclude '__pycache__' --exclude 'parcours/etat/' \
  labs/phamphamh/parcours labs/phamphamh/workflows labs/phamphamh/rapport labs/phamphamh/recherche \
  labs/phamphamh/demo labs/phamphamh/audit \
  labs/*/campagne/resume-valide.json equipe/exporter-mon-screenpipe.command \
  donnees/audit/audit.json donnees/audit/postes.json donnees/rapport \
  "$VPS:$DEST/"
ssh "$VPS" "chown -R cabinetia:cabinetia $DEST && systemctl restart cabinet-ia && sleep 1 && systemctl is-active cabinet-ia"

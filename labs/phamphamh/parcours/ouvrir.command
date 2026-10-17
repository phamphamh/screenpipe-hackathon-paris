#!/bin/sh
# Double-clic dans le Finder : lance le parcours « Cabinet IA » et ouvre le navigateur. Fermer cette fenêtre pour l'arrêter.
cd "$(dirname "$0")" || exit 1
if lsof -ti tcp:8790 >/dev/null 2>&1; then open "http://127.0.0.1:8790"; echo "Le parcours tourne déjà : ouvert dans le navigateur."; exit 0; fi
exec python3 serveur.py

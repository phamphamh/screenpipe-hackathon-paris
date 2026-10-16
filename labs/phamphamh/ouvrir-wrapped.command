#!/bin/sh
# Double-clic dans le Finder : lance le Wrapped en local et ouvre le navigateur. Fermer la fenêtre du terminal pour l'arrêter.
cd "$(dirname "$0")/../.." && exec python3 labs/phamphamh/app/serveur.py

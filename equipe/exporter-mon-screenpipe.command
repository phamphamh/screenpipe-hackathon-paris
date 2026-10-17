#!/bin/sh
# Double-clic dans le Finder : exporte ta base screenpipe sur le Bureau, à envoyer à Youssef.
cd "$(dirname "$0")" && python3 -I export_complet.py && open -R "$HOME/Desktop"
echo "Tu peux fermer cette fenêtre."

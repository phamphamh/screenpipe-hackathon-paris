# Export complet de screenpipe, pour tout analyser sur un seul Mac
- **Fait** : `equipe/exporter-mon-screenpipe.command` (double-clic sur Mac) ou `python3 -I equipe/export_complet.py <prenom>` (Windows/WSL). Trouve la clé tout seul, passe par l'API locale, sort `~/Desktop/screenpipe-<prenom>-<date>.jsonl.gz` : texte des écrans, apps, fenêtres, URL, audio, événements d'interface, sans images.
- **Preuve** : sur le Mac de phamphamh, 9 s, 7 842 captures (4 070 écrans, 3 740 audio, 32 UI), 16 M caractères de texte, 1,1 Mo compressé.
- **Pas vérifié** : Windows (chemin de la CLI screenpipe supposé) ; 755 captures de la base absentes de l'API (sans texte ?).
- **Pour les autres** : lancez-le et envoyez le fichier à phamphamh (AirDrop/Drive). Il ne va jamais dans le dépôt (contenu brut).

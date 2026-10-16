# Mission Windows — à coller dans Claude Code sur le PC Windows

```
Contexte : je participe au hackathon screenpipe (42 Paris, 16-18 oct.). Le but est d'améliorer le produit
(github.com/screenpipe/screenpipe) et d'arriver avec des correctifs mesurés.
Le thème : screenpipe capture trop de choses inutiles, ce qui coûte en CPU, en batterie et en contexte pour l'IA.

1. Installe screenpipe (https://screenpipe.com/download) s'il n'est pas déjà installé, lance-le, puis
   vérifie http://localhost:3030/health. La clé d'API se trouve dans Settings > Privacy.
2. Clone github.com/screenpipe/screenpipe et lis CONTRIBUTING.md (section Windows) et CLAUDE.md.
   Respecte leurs règles de contribution dans LEUR repo, mais ne copie pas leur en-tête obligatoire dans des
   fichiers hors de ce repo.
3. Reproduis et mesure ces deux tickets, sans rien corriger avant d'avoir la mesure :
   - #7569 : sous Windows, des événements « window_focus » répétés à environ 4 Hz alors qu'on ne change pas de
     fenêtre. Compte les captures par déclencheur sur 10 min d'usage normal (POST /raw_sql sur la table frames :
     capture_trigger, focused, app_name, timestamp ; ajoute LIMIT).
   - #7560 : des fenêtres console vides (bun.exe) s'ouvrent pour les pipes, pi-agent et MCP. Trouve où ces
     processus sont lancés et s'il manque CREATE_NO_WINDOW.
4. Pour chacun : la cause dans le code (fichier:ligne), un correctif minimal, et une mesure avant/après sur cette
   machine. Lance-le en CLI avec un dossier de données et un port séparés pour ne pas toucher à l'app :
   `screenpipe record --port 3031 --data-dir <dossier>`.
5. Ne pousse rien et n'ouvre pas de PR. Écris le rapport dans un fichier RAPPORT-WINDOWS.md : ce qui est
   prouvé, ce qui ne l'est pas, les chiffres.
```

## Pourquoi ces deux tickets
- **#7569** : un « window_focus » toutes les 0,25 s sous Windows, c'est exactement le thème des captures inutiles.
  Si on le corrige et qu'on le mesure, on a un argument de plus pour le benchmark.
- **#7560** : ça ne coûte rien en CPU, mais ça se voit tout de suite (des fenêtres noires qui pop), et le correctif
  est probablement court. Une victoire rapide pour le pitch.

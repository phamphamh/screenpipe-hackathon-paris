# Front du Wrapped (briques C et E) — adamaass

Deux pages, sans installation : **double-clique sur le fichier** pour l'ouvrir dans le navigateur.

| Fichier | Brique | Ce que c'est |
|---|---|---|
| `relecture.html` | C | Le salarié relit son résumé avant de le partager : masquer une app, renommer, corriger fréquence ou durée, supprimer une étape, retirer une tâche, anonymiser un email, un montant ou un nom de client. « Voir ce qui part » montre le JSON exact. « Valider et partager » télécharge `resume-valide-<personne>.json`. |
| `wrapped.html` | E | Le Wrapped du dirigeant, en 10 slides (flèches du clavier, swipe, ou `#4` dans l'URL). Chaque chiffre souligné ouvre sa preuve (le calcul et les moments sources). Impression = PDF (une slide par page). |

Données inventées : `exemples/resume-exemple.js` (format de la brique B, repris de `labs/phamphamh/resume/exemple-resume.json`, avec une tâche sensible en plus) et `exemples/insights-exemple.js`.
Pour tester de vraies données : bouton « Ouvrir un autre resume.json » ou « Charger un insights.json » en haut de la page.

## Règles déjà appliquées dans le front
- Pas de chiffre par personne. Une tâche ou un outil IA partagé par **moins de 3 personnes** est masqué (et listé comme tel slide 8).
- Badge **observé / supposé / estimé** sur les tâches et les étapes.
- Coût d'une tâche = fréquence par semaine × durée × 4,33 × coût horaire. Gain estimé = coût × score d'automatisation.
- En relecture, Spotify, Doctolib, WhatsApp, etc. sont proposés masqués par défaut ; la personne peut les réafficher.

## Format proposé pour `insights.json` (sortie de la fusion, brique D)
Le front ne calcule que les coûts et les classements. Tout le reste vient de la fusion :

```json
{
  "fictif": false,
  "entreprise": { "nom": "…", "secteur": "…", "cout_horaire_eur": 45 },
  "campagne": { "nom": "…", "debut": "2026-10-12", "fin": "2026-10-16", "suppression_prevue": "2026-10-23" },
  "personnes": { "invitees": 6, "participantes": 5, "validees": 5 },
  "heures_captees": 148,
  "nb_apps": 23,
  "tri_80_20": { "captures_regardees": 61200, "captures_gardees": 16400 },
  "temps_par_categorie": [{ "categorie": "…", "heures_semaine": 31 }],
  "temps_par_app": [{ "app": "Gmail", "heures_semaine": 34 }],
  "taches": [{
    "id": "t1", "titre": "…",
    "personnes": 4,                      // nombre de personnes qui font cette tâche
    "frequence_par_semaine": 38,         // total équipe
    "duree_moyenne_min": 8,
    "apps": ["HubSpot", "Gmail"],
    "etapes": [{ "type": "input|action|output|decision|check", "texte": "…", "app": "…", "statut": "observé|supposé" }],
    "exceptions": ["…"],
    "goulots": [{ "type": "switching|waiting|rework|handoff", "detail": "…" }],
    "score_automatisation": 84, "pourquoi": "…",
    "confiance": 0.8, "statut": "observé|estimé",
    "preuves": [{ "debut": "ISO", "fin": "ISO", "app": "…", "personne": "anonyme-1" }]
  }],
  "goulots": [{ "type": "switching", "detail": "…", "heures_semaine": 6.5 }],
  "usage_ia": [{ "outil": "ChatGPT", "personnes": 4, "heures_semaine": 6, "usages": ["…"] }],
  "questions_ouvertes": ["…"]
}
```
Différences avec un résumé individuel : `personnes` sur chaque tâche et chaque outil IA, `heures_semaine` au lieu de `minutes`, et `automatisable.score` devient `score_automatisation`.

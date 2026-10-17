# Front du Wrapped (briques C et E) — adamaass

Deux pages, sans installation : **double-clique sur le fichier** pour l'ouvrir dans le navigateur.

| Fichier | Brique | Ce que c'est |
|---|---|---|
| `relecture.html` | C | Le salarié relit son résumé avant de le partager : masquer une app, renommer, corriger fréquence ou durée, supprimer une étape, retirer une tâche, anonymiser un email, un montant ou un nom de client. « Voir ce qui part » montre le JSON exact. « Valider et partager » télécharge `resume-valide-<personne>.json`. |
| `wrapped.html` | E | Le Wrapped du dirigeant, en 10 slides (flèches du clavier, swipe, ou `#4` dans l'URL). Chaque chiffre souligné ouvre sa preuve (le calcul et les moments sources). Impression = PDF (une slide par page). |

Données inventées : `exemples/resume-exemple.js` (format de la brique B, repris de `labs/phamphamh/resume/exemple-resume.json`, avec une tâche sensible en plus) et `exemples/insights-exemple.js`.
Pour tester de vraies données : bouton « Ouvrir un autre resume.json » ou « Charger un insights.json » en haut de la page.

## Fusion minimale (brique D) : `fusion.py`
```
python3 fusion.py resume-valide-a.json resume-valide-b.json resume-valide-c.json --entreprise "Nom" --cout-horaire 45 --sortie insights.json
```
Refuse tout résumé non validé par la personne. Regroupe les tâches de personnes différentes par libellé (mots comparés sur leurs 5 premières lettres : « relance » = « relancer »). Puis ouvrir `wrapped.html` → « Charger un insights.json ».

**Démo avec moins de 3 personnes** : `wrapped.html?seuil=1` abaisse le seuil d'anonymat, et un bandeau l'affiche. Sans ça, avec 2 personnes, toutes les tâches sont masquées (c'est voulu).

## Règles déjà appliquées dans le front
- Pas de chiffre par personne. Une tâche, un goulot ou un outil IA partagé par **moins de 3 personnes** est masqué (et listé comme tel dans « Ce qu'on ne sait pas encore »). Si la campagne entière a moins de 3 personnes, un bandeau le dit.
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
  "goulots": [{ "type": "switching", "detail": "…", "personnes": 4, "heures_semaine": 6.5 }],
  "usage_ia": [{ "outil": "ChatGPT", "personnes": 4, "heures_semaine": 6, "usages": ["…"] }],
  "questions_ouvertes": ["…"]
}
```
Différences avec un résumé individuel : `personnes` sur chaque tâche et chaque outil IA, `heures_semaine` au lieu de `minutes`, et `automatisable.score` devient `score_automatisation`.

## Test sur WONDERBREAD : « Atelier Nova », back-office e-commerce (dossier `wonderbread/`)
Données publiques de Stanford ([WONDERBREAD](https://hazyresearch.stanford.edu/wonderbread-website), NeurIPS 2024, CC-BY-4.0) : 2 928 démonstrations humaines de tâches web, chacune avec sa trace d'actions et un **SOP écrit à la main** (la vérité terrain).

**Ce qu'on en fait** : 6 salariés fictifs d'« Atelier Nova », tous sur le back-office Magento. Chacun = les démos d'**un annotateur réel différent**, posées sur la semaine du 13/10, avec des prénoms inventés. La brique B ne voit que ce que screenpipe verrait (titre d'onglet, route d'URL, clics, saisies) ; l'intention et le SOP restent à part (`verite.json`) pour mesurer ensuite.

**Le résultat** : `exemples/nova-backoffice.json` (sortie de la fusion). Pour le voir : servir `labs/adamaass/` (`python3 -m http.server 8790 --directory labs/adamaass`) puis ouvrir `http://localhost:8790/wrapped.html?donnees=exemples/nova-backoffice.json`, ou bouton « Charger un insights.json ».
- 8 tâches visibles (≥ 3 personnes) sur 20 ; n°1 « Générer des rapports de ventes sur une période » (6 personnes, 79 fois/sem.) ; ses étapes (Reports → Bestsellers/Orders → dates → Show Report → lecture) sont celles du SOP humain.

**Rejouer** (données brutes dans `donnees/`, jamais commitées) :
```
python3 -I labs/adamaass/wonderbread/wb_index.py donnees/wonderbread          # démo → annotateur (après téléchargement Zenodo 14094162)
python3 -I labs/adamaass/wonderbread/wb_salaries.py donnees/wonderbread donnees/nova lea,karim,sophie,nadia,julien,emma
python3 labs/adamaass/wonderbread/wb_brique_b.py prompt donnees/nova/<pseudo>/moments.json   # consigne exacte de la brique B
#   → le modèle répond dans donnees/nova/<pseudo>/reponse.json (ici : un agent Claude, `claude -p` n'avait plus de crédit)
python3 labs/adamaass/wonderbread/wb_brique_b.py finir donnees/nova/<pseudo>/moments.json donnees/nova/<pseudo>/reponse.json nova-<pseudo>
python3 -I labs/adamaass/wonderbread/wb_post.py donnees/nova lea,karim,sophie,nadia,julien,emma
python3 labs/adamaass/fusion.py donnees/nova/*/resume-valide.json --entreprise "Atelier Nova (fictive)" --cout-horaire 38 --sortie insights.json
python3 -I labs/adamaass/wonderbread/wb_mesure.py donnees/nova lea,karim,sophie,nadia,julien,emma
```

**Limites (à dire au jury)** : tâches WONDERBREAD courtes (0,3 à 1,4 min), donc des coûts faibles (top 3 ≈ 296 €/mois) ; résumés « validés pour la démo » sans relecture humaine (salariés fictifs) ; mesure grossière : 16 % des éléments d'interface cités dans les SOP humains se retrouvent dans nos étapes (109/703), et 23 tâches sur 47 sont bien isolées (≥ 80 % de leurs démos ont la même intention). Une mesure par juge IA, comme dans le papier (88 % des étapes retrouvées), reste à faire.

**Fusion** : regroupe maintenant aussi par **écrans visités** (champ facultatif `ecrans` = routes d'URL sans identifiants) et fusionne les catégories de temps proches. Sans ça, « Générer un rapport de ventes », « Rapport ventes/produits » et « Sortir le rapport des meilleures ventes » restaient 3 tâches à 1-2 personnes.

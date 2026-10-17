# Wrapped — le FDE virtuel

**Le produit** : une semaine de screenpipe chez des salariés volontaires ; chacun relit et valide son propre résumé ; l'entreprise reçoit son **Wrapped** — ses tâches répétées, leur coût réel, quoi automatiser en premier — **et sa première automatisation** (skill générée, testée sur une seconde personne). Zéro consultant sur place. Le récit complet : [`produit/positionnement.md`](produit/positionnement.md).

Hackathon screenpipe × 42 Paris, 16–18 octobre 2026 (« Build Agents That Remember »). **La vidéo (2 min)** : à venir — dimanche.

## L'essayer en 2 minutes
Rien à installer d'autre que Python 3. Double-clic sur [`labs/phamphamh/ouvrir-wrapped.command`](labs/phamphamh/ouvrir-wrapped.command) (macOS) ou :

```sh
python3 labs/phamphamh/app/serveur.py
```

→ http://localhost:8787. En haut, restez sur **Démo · Maison Corvo** (entreprise fictive complète, aucune donnée réelle) et suivez : **relecture** d'une salariée → **Wrapped** (10 slides, chaque chiffre cliquable vers ses preuves) → bouton **« Créer la skill »**. `POST /api/reinitialiser-demo` remet la démo à zéro.

| Accueil | Relecture | Wrapped |
|---|---|---|
| ![accueil](docs/captures/accueil.png) | ![relecture](docs/captures/relecture.png) | ![wrapped](docs/captures/wrapped.png) |

## Ce qui est construit et vérifié
- **La boucle complète, en local** : dérush 80/20 (screenpipe → moments) → résumé des tâches → **relecture par la personne** (corriger, retirer, masquer, contester) → fusion (agrégats seulement) → Wrapped → skill.
- **Tests** : `cd labs/phamphamh/fusion && python3 -m unittest test_fusion` — 10 cas de la section 6 du découpage, passent en 0,01 s.
- **La confidentialité est dans le code, pas dans une charte** : seuls les résumés validés comptent ; moins de 3 participants → pas de Wrapped ; une app ou une tâche vue chez moins de 3 personnes est fondue ; aucune capture brute ne circule ; le serveur n'écoute que sur 127.0.0.1.
- **Pas de dépendance à `claude` pour la démo** : l'IA est optionnelle (brique résumé et `fusion --ia` ; un appel LLM, remplaçable).
- **Vérifié depuis un clone neuf** (17/10) : serveur lancé, démo complète, API répondent, sans rien installer.

## L'utiliser pour de vrai (votre entreprise)
1. screenpipe tourne chez les volontaires, durée annoncée (une semaine dans notre scénario).
2. `python3 labs/phamphamh/collecteur/collecte.py --sortie donnees/<pseudo>` — tri 80/20 local.
3. `python3 labs/phamphamh/resume/resume.py` — un appel LLM (`claude -p` par défaut) → tâches répétées avec preuves horodatées.
4. Chacun relit et valide dans l'app → `labs/<pseudo>/campagne/resume-valide.json`.
5. Dès 3 validations : le Wrapped de l'équipe apparaît, et « Créer la skill » génère la première automatisation (SKILL.md).

## Travailler dans ce dépôt (l'équipe — rien à taper, tout est automatique)
Pas de chef de projet : chacun construit ce qu'il veut. **Tu n'as aucune commande à taper.**

**La première fois (5 min)**
1. Installe Claude Code : https://claude.com/download (ou l'app Claude, onglet « Code »).
2. Accepte l'invitation GitHub reçue par email.
3. Dans Claude, colle ce message :
   > Clone https://github.com/phamphamh/screenpipe-hackathon-paris dans mon dossier Documents, connecte-moi à GitHub si besoin, puis dis-moi comment ouvrir une nouvelle session Claude dans ce dossier.
4. Ouvre une nouvelle session dans ce dossier. Si Claude demande s'il peut faire confiance au dossier, réponds **oui**.

**Ensuite, à chaque fois** : ouvre Claude dans ce dossier et dis ce que tu veux faire, en français normal.
- Au démarrage, Claude récupère tout seul le travail des autres et te résume qui fait quoi.
- Il range ton travail dans ton coin (`labs/<ton-pseudo>/`) et tient à jour ta fiche (`chantiers/`) et le journal.
- **À la fin de chacune de ses réponses, tout est sauvegardé et partagé automatiquement.** Les clés API, les vidéos et les fichiers des autres sont bloqués.

(Pour les curieux : les hooks sont dans `.claude/settings.json`, les règles dans `.claude/skills/equipe/`, et les scripts dans `scripts/`. Si tu utilises Codex, il lit `AGENTS.md`.)

## Le projet
- [`produit/decoupage.md`](produit/decoupage.md) : **le découpage du produit « FDE en produit / Wrapped »** (parcours, briques, contrat de données, cas à tester, répartition, planning, pitch).
- [`produit/positionnement.md`](produit/positionnement.md) : le récit du produit, la description du rendu (prête à coller) et les repères de marché sourcés.
- [`produit/charte-campagne.md`](produit/charte-campagne.md) : consentement, anonymisation, droits des participants.
- [`produit/fusion-fronts.md`](produit/fusion-fronts.md) : décision « un seul front » (l'app + les meilleurs morceaux du front d'adamaass).

## Les notes
- [`.context/hackathon-brief.md`](.context/hackathon-brief.md) : **la fiche principale**. Elle couvre l'événement, le produit, la roadmap, les critiques, comment gagner, les mesures sur une vraie journée, la confidentialité, les étoiles GitHub des fondateurs, les infos officielles du kickoff (section 12), les idées de l'équipe (section 13), JEPA et le computer use (section 14).
- [`.context/recherche-memoire.md`](.context/recherche-memoire.md) : la recherche récente sur la mémoire des agents, la compression vidéo et l'extraction de workflows, plus les jeux de données disponibles.
- [`.context/retours-utilisateurs.md`](.context/retours-utilisateurs.md) : les plaintes et les besoins des utilisateurs de screenpipe (HN, GitHub, Product Hunt).
- [`.context/mission-windows.md`](.context/mission-windows.md) : une consigne à donner à un agent sur un PC Windows pour reproduire deux bugs Windows.

## Le reste
- [`pages/derush.html`](pages/derush.html) : une page qui montre l'architecture actuelle de screenpipe, puis la version « dérush » qu'on propose. Ouvre-la dans un navigateur.
- [`correctifs/double-ecran.patch`](correctifs/double-ecran.patch) : un correctif pour screenpipe. Quand on reste plus de 30 s sur un écran, l'autre écran se remettait à tout capturer. Il est livré avec un test qui échoue sans le correctif. Pour l'appliquer, depuis un clone de `screenpipe/screenpipe` au commit `1ebd12a` : `git apply double-ecran.patch`.
- [`bench/`](bench/) : un script qui lance la version d'origine et la version corrigée côte à côte pour les comparer. **Aucun résultat pour l'instant** : le premier essai s'est arrêté au bout de 15 s, et il faut 2 écrans pour le relancer.

## Les dates clés
- **Rendu : dimanche 18 à 14h30.** Il faut une vidéo de 2 min maximum, le lien GitHub et une courte description.
- Finale : 3 min de démo et 2 min de questions.

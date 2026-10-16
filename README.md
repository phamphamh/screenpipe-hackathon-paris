# Hackathon screenpipe × 42 Paris (16–18 oct. 2026)

Tout ce qu'on a appris et préparé pour le hackathon « Build Agents That Remember ».

## Le projet
- [`produit/decoupage.md`](produit/decoupage.md) : **le découpage du produit « FDE en produit / Wrapped »** (parcours, briques, contrat de données, cas à tester, répartition, planning, pitch).

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

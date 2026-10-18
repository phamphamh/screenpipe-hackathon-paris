# Positionnement : le FDE virtuel (SaaS)

Texte source pour la **description du rendu** et le **pitch** (section 9 du découpage). Aligné sur la section 21 du brief (« le FDE en produit, clé en main »). Rien à reconstruire : le produit déjà construit EST ce SaaS — il lui manquait le nom et le récit.

**Nom du rendu (18/10)** : **DeloAI** — « votre cabinet et votre ESN, dans votre poche » ; dans le dépôt, le produit garde son nom de travail « Wrapped ».

**Validations** : ✅ 09125o (17/10, 10h42) — en attente : phamphamh, adamaass, JA.

## En une phrase
Un forward deployed engineer virtuel : screenpipe tourne une semaine chez des volontaires, le produit découvre ce que l'entreprise fait vraiment, le fait valider par chacun — puis livre le diagnostic **et la première automatisation**, personnalisés aux vraies tâches, sans consultant sur place.

## Le paragraphe (description du rendu)
Les entreprises paient des ingénieurs très chers pour s'asseoir à côté de leurs équipes et regarder comment elles travaillent (« les entreprises paient des ingénieurs pour regarder leurs salariés travailler » — screenpipe). Notre produit fait ce travail tout seul : une semaine de capture **locale**, un tri 80/20 avant toute IA, chaque personne **relit et valide son propre résumé**, puis la fusion produit le **Wrapped de l'entreprise** — les tâches répétées, leur coût réel, ce qui vaut le coup d'être automatisé — et génère l'**automatisation (skill)** de la tâche choisie, testée sur une seconde personne. Aujourd'hui il faut des semaines et un consultant sur place ; ici : une semaine, zéro consultant, des données validées par les intéressés et supprimées à la fin. Et l'étape d'après est déjà montrée pour de vrai : dans la démo, des agents tournent dans le vrai back-office de la boutique, sur de vraies demandes — chaque action tracée, personne au clavier.

## Pour le formulaire de rendu (prêt à coller — récit final du 18/10, celui de la vidéo)
- **Une phrase** : DeloAI, un cabinet IA natif : une semaine de screenpipe, le Wrapped de l'entreprise — tâches répétées, coût réel — et ses agents déployés dans ses vrais outils, sans consultant sur place.
- **Version courte (~300 caractères)** : Le problème de screenpipe n'est pas la donnée, c'est le contexte. DeloAI le transforme en produit : capture locale une semaine, chaque salarié relit et valide son résumé, le Wrapped de l'entreprise — puis ses agents déployés dans ses outils. Une semaine, zéro consultant sur place.
- **Version longue** : le paragraphe ci-dessus. Texte de la démo et sources (validé par Youssef) : [`labs/phamphamh/agents-nova/script.md`](../labs/phamphamh/agents-nova/script.md).

## Pourquoi c'est un FDE virtuel (et pas un simple task mining)
Un FDE fait quatre choses : **Map** (voir le travail réel), **Installer** (mettre les capteurs), **Improve** (chiffrer ce qui peut être automatisé), **Deploy** (livrer l'automatisation). Le produit reprend les quatre :
1. **Map** → dérush local 80/20 + résumé des tâches répétées (l'IA est là : analyse des moments, déduction des tâches et de leurs étapes).
2. **Installer/Relire** → l'app : onboarding du dirigeant, puis chaque salarié corrige et valide — la confiance est dans le produit, pas dans une charte.
3. **Improve** → la fusion croise les résumés : tâches communes, coût = fréquence × durée × coût horaire, classement des automatisations, badges observé/estimé.
4. **Deploy** → bouton « Créer la skill » : la tâche validée devient une skill (SKILL.md), testée sur une 2e entrée.

## Où est l'IA, concrètement
- Résumé des journées en tâches (ce que l'écran seul ne raconte pas).
- Regroupement des tâches entre personnes (« relancer » = « relance »).
- Génération de la skill à partir de la tâche et de ses étapes réelles.

## La personnalisation (le « pain client »)
Tout est calculé sur **leurs** données : leurs tâches, leurs outils, leur coût horaire, leurs exceptions, leurs façons de faire différentes. Le produit ne vend pas un catalogue d'automatisations : il trouve **le** pain qui coûte, le prouve (preuves horodatées, cliquables), le fait confirmer par la personne concernée, puis construit la solution pour ce pain-là. Modèle : vendu **par campagne** (par entreprise), pas par siège — l'unité vendue, c'est la mission FDE, pas un logiciel de surveillance.

## Le garde-fou RGPD = argument de vente Europe
Durée annoncée, volontaires seulement, **relecture individuelle obligatoire** (aucune capture brute ne circule), agrégats seulement (moins de 3 personnes → masqué), aucun chiffre par personne, suppression à la fin. C'est ce qui rend le produit vendable là où la CNIL sanctionne le « screenpipechez tous les salariés ».

## Aujourd'hui / la suite
- **Construit et montré au hackathon** : la boucle complète (dérush → relecture → fusion → Wrapped → skill) sur de vraies données de l'équipe.
- **Suite SaaS** : multi-entreprises, exécution des skills directement, historique entre campagnes, marketplace de skills.

## Combien ça coûte, un FDE — chiffres sourcés (relevé du 17/10, pour le pitch)
La phrase « des semaines et des dizaines de milliers d'euros » tient sur ces repères de **marché** (pas des devis client — à présenter comme tels) :

| Référence | Chiffre | Source |
|---|---|---|
| Forward deployed engineer (Palantir, US) | médiane **255 k$/an** de rémunération totale (185–620 k$) | Levels.fyi, 227 déclarations, relevé 06/10/2026 |
| Freelance IA / LLM (France) | **800 €/jour** — TJM médian | TJMètre, relevé 21/09/2026 |
| Consultant senior (France) | **600–1 200 €/jour** (jusqu'à 2 400 € sur missions complexes) | Indy, 07/03/2025 |
| Data engineer / data scientist (France) | 640 € / 680 € par jour | TJMètre, 2026 |
| **Un mois d'un profil IA déployé** (4 sem. × 5 j) | **≈ 16 000 € HT minimum** — avant marge d'un cabinet | calcul sur TJMètre |
| Le rôle décolle | 401 offres FDE ouvertes, médiane 185–300 k$ | Rung, census oct. 2026 |

Lecture pour le pitch : une mission « à la main » = **des semaines de facturation d'un profil rare** → dizaines de milliers d'euros, souvent avant la marge d'un cabinet. Notre produit : la même semaine de terrain, **zéro consultant sur place**. À l'oral comme à l'écran : « repères de marché 2026, sourcés » — jamais présenté comme un devis client ni comme un temps gagné.

## Non vérifié
- ce que screenpipe Business/Enterprise couvre déjà (module team-memory) — à ne pas revendiquer à tort ;
- validation du texte : 09125o ✅ ; phamphamh, adamaass, JA à relire avant le rendu.

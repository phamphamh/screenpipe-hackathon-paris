# Positionnement : le FDE virtuel (SaaS)

Texte source pour la **description du rendu** et le **pitch** (section 9 du découpage). Aligné sur la section 21 du brief (« le FDE en produit, clé en main »). Rien à reconstruire : le produit déjà construit EST ce SaaS — il lui manquait le nom et le récit.

**Validations** : ✅ 09125o (17/10, 10h42) — en attente : phamphamh, adamaass, JA.

## En une phrase
Un forward deployed engineer virtuel : screenpipe tourne une semaine chez des volontaires, le produit découvre ce que l'entreprise fait vraiment, le fait valider par chacun — puis livre le diagnostic **et la première automatisation**, personnalisés aux vraies tâches, sans consultant sur place.

## Le paragraphe (description du rendu)
Les entreprises paient des ingénieurs très chers pour s'asseoir à côté de leurs équipes et regarder comment elles travaillent (« les entreprises paient des ingénieurs pour regarder leurs salariés travailler » — screenpipe). Notre produit fait ce travail tout seul : une semaine de capture **locale**, un tri 80/20 avant toute IA, chaque personne **relit et valide son propre résumé**, puis la fusion produit le **Wrapped de l'entreprise** — les tâches répétées, leur coût réel, ce qui vaut le coup d'être automatisé — et génère l'**automatisation (skill)** de la tâche choisie, testée sur une seconde personne. Aujourd'hui il faut des semaines et un consultant sur place ; ici : une semaine, zéro consultant, des données validées par les intéressés et supprimées à la fin.

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

## Non vérifié
- Prix d'une mission FDE (à sourcer avant la finale, section 21) ;
- ce que screenpipe Business/Enterprise couvre déjà (module team-memory) — à ne pas revendiquer à tort ;
- validation du texte : 09125o ✅ ; phamphamh, adamaass, JA à relire avant le rendu.

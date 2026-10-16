# Découpage produit : « le FDE en produit » (nom de travail : **Wrapped**)

Version du 16/10, 22h. L'idée de départ se trouve dans la section 21 de la fiche (`.context/hackathon-brief.md`).

## 1. En une phrase
Une entreprise installe screenpipe chez des salariés volontaires pendant une semaine. On lui rend ensuite un **« Wrapped » de l'entreprise** : où part le temps, les tâches répétées qui coûtent le plus, ce qu'il faut confier à l'IA en premier, avec une preuve pour chaque chiffre. Le tout sans consultant sur place, et aucune capture ne quitte les machines.

- **Qui achète** : le dirigeant ou le responsable des opérations d'une PME de 10 à 200 personnes, qui « veut faire de l'IA » sans savoir par où commencer.
- **Qui l'utilise** : les salariés volontaires (ils capturent puis relisent leur propre résumé) et le dirigeant (il lit le Wrapped).
- **Track** : 1, « trouver quoi automatiser ».

## 2. Ce que screenpipe a DÉJÀ (testé le 16/10 au soir, ne pas le refaire)
| Brique | Où | Ce qu'elle fait |
|---|---|---|
| Questions d'onboarding | page **Context** de l'app Workflows (`apps/screenpipe-workflows-web`, `/enterprise-preview`) | présentation de l'organisation, priorités, indicateurs de succès, **coût horaire moyen** |
| Bibliothèque de workflows | même app, page Home | une fiche par workflow : déclencheur, étapes, apps, captures, bouton « Create skill » |
| Format de workflow | `GET /workflows/context` → `outputContract` | étapes (`action/input/output/decision/check`), goulots (`waiting/switching/rework/handoff`), durées, preuves horodatées, questions ouvertes |
| Détection de workflows | pipes `workflow-discover → patterns → procedures → deepen → review → timing` | **désactivée par défaut**, derrière un interrupteur (`/workflows/rollout`, réservé à l'app). Le catalogue de Youssef est vide. |
| Temps par app | `GET /activity-summary` | minutes et nombre de captures par app sur une période (testé : fonctionne) |
| Mémoire d'équipe | `crates/screenpipe-team-memory` | fichiers markdown partagés, avec la provenance (cloud / tinfoil / local) |

**Ce qui manque, et c'est notre projet :**
1. **La vue entreprise qui raconte quelque chose** : leur app est une bibliothèque de fiches, pas un livrable de dirigeant. Rien n'agrège plusieurs salariés en heures, en euros et en priorités.
2. **Le mode campagne** : volontariat, durée limitée, relecture par le salarié, chiffres agrégés seulement, suppression à la fin. Rien de tout ça n'existe dans leur code (j'ai cherché « consent » et « campaign »).
3. **Le tri 80/20 avant l'IA** : sans lui, une semaine × N salariés coûte cher à analyser. Mesuré sur Youssef : 20 % des captures conservent 75 % des fenêtres (section 16 de la fiche).

## 3. Le parcours
| Quand | Qui | Ce qui se passe |
|---|---|---|
| J0 | dirigeant | **Onboarding** : 5 questions (activité, priorités, coût horaire, outils, ce qui l'agace). On reprend les champs de leur page Context. |
| J0 | salariés | Ils reçoivent un lien : la charte de la campagne (ce qui est capté, pendant combien de temps, qui voit quoi) et un bouton « je participe ». |
| J1 → J5 | salariés | screenpipe tourne normalement. Rien ne sort de la machine. |
| J5 | chaque salarié | **Relecture** : son résumé de la semaine (tâches, temps, outils). Il coche, corrige ou retire des éléments, puis il valide. **Seul le résumé validé est partagé.** |
| J5 | nous (automatique) | **Fusion** des résumés validés, puis calcul des insights. |
| J6 | dirigeant | **Le Wrapped** : un site, slide par slide, et un PDF. |
| J6+ (bonus) | dirigeant | « Automatise ça » : la tâche n°1 devient une skill pour Claude ou Codex (leur bouton « Create skill »). |
| Fin | tout le monde | Suppression des données de campagne, avec un reçu. |

## 4. Les 5 briques à construire
```
[A] Collecteur local ──► [B] Résumé salarié ──► [C] Relecture ──► [D] Fusion + insights ──► [E] Wrapped
   (sur chaque Mac)       (JSON, sur le Mac)    (page locale)      (serveur ou dossier)      (site)
```

### A. Collecteur local (sur chaque machine)
- **Entrée** : l'API locale screenpipe (`/activity-summary`, `/search`, `/frames/*`, `/elements`), sur la période de la campagne.
- **Travail** : découper la journée en **moments** (même fenêtre et même tâche, avec des pauses de moins de 2 min), puis garder les 20 % de captures les plus nouvelles (tri visuel SigLIP ou texte nouveau, voir la section 16). Les moments d'inactivité, de musique ou de perso sont écartés.
- **Sortie** : une liste de moments `{début, fin, app, fenêtre, url, extrait de texte, 1 à 3 captures clés}`. Elle reste sur la machine.

### B. Résumé salarié (sur chaque machine)
- **Entrée** : les moments.
- **Travail** : un seul appel au LLM par jour, sur les moments déjà triés et non sur les captures brutes. Il regroupe les moments en **tâches répétées**, avec la fréquence, la durée moyenne, les étapes et les exceptions, au **format workflow de screenpipe** (`outputContract`). Chaque affirmation pointe vers ses moments sources, et on sépare `observé` de `supposé`.
- **Sortie** : `resume-<prenom>.json` (schéma en 5).

### C. Relecture par le salarié (page locale)
- La page affiche le résumé en clair. Le salarié peut renommer, corriger ou supprimer une tâche, et masquer une app ou une période. Rien ne part sans un clic sur « Valider et partager ».
- Le fichier validé ne contient ni capture, ni texte brut, ni nom de client. Il garde des libellés, des durées, des apps et des étapes.

### D. Fusion et insights
- **Entrée** : les résumés validés + l'onboarding (coût horaire, priorités).
- **Calculs** :
  - temps par catégorie et par app, en heures par semaine ;
  - **tâches communes** à plusieurs personnes, regroupées par similarité de libellé et d'étapes ;
  - **coût de chaque tâche** = fréquence × durée × nombre de personnes × coût horaire ;
  - **score d'automatisation** = coût × régularité des étapes × part de copier-coller entre apps, moins les décisions humaines ;
  - goulots (attente, allers-retours entre apps, reprises) ;
  - usage actuel de l'IA (Claude, ChatGPT, Codex : qui, combien, pour quoi) ;
  - carte des connaissances : quel outil est maîtrisé par qui, au niveau de l'équipe seulement.
- **Règle** : pas de chiffre par personne dans le Wrapped. Un minimum de 3 personnes par agrégat, sinon le chiffre est masqué.

### E. Le Wrapped (site)
| # | Slide | Source |
|---|---|---|
| 1 | « Votre semaine en chiffres » : heures captées, nombre de personnes, nombre d'apps | D |
| 2 | Où part le temps (catégories) | D |
| 3 | Votre top 3 des tâches répétées, avec heures et € par mois | D |
| 4 | Zoom sur la tâche n°1 : étapes, apps, exceptions, captures preuves | B + D |
| 5 | Les goulots : attente, allers-retours, reprises | D |
| 6 | L'IA chez vous aujourd'hui : qui l'utilise et pour quoi | D |
| 7 | **Ce qu'on automatise en premier** (classement par score), avec le gain estimé | D |
| 8 | Ce qu'on ne sait pas encore (questions ouvertes, faible confiance) | B |
| 9 | « Lancer l'automatisation n°1 » (skill) + la suppression des données | bonus |

Chaque chiffre est cliquable et mène à sa preuve. Un badge distingue **observé** de **estimé**.

## 5. Le contrat de données (à figer en premier, pour que tout le monde code en parallèle)
```json
{
  "campagne": "hackathon-42",
  "personne": "anonyme-3",
  "periode": {"debut": "2026-10-16T18:00:00+02:00", "fin": "2026-10-18T12:00:00+02:00"},
  "heures_captees": 21.5,
  "temps_par_app": [{"app": "Google Chrome", "minutes": 312}],
  "temps_par_categorie": [{"categorie": "code", "minutes": 410}],
  "usage_ia": [{"outil": "Claude", "minutes": 95, "usages": ["code", "rédaction"]}],
  "taches": [{
    "titre": "Relancer un client par mail",
    "frequence_par_semaine": 6, "duree_moyenne_min": 9,
    "apps": ["Gmail", "HubSpot"],
    "etapes": [{"type": "action", "texte": "Ouvrir la fiche client", "app": "HubSpot", "statut": "observé"}],
    "exceptions": ["client sans email → appel"],
    "goulots": [{"type": "switching", "detail": "copier-coller HubSpot → Gmail"}],
    "confiance": 0.7,
    "preuves": [{"debut": "...", "fin": "...", "app": "Gmail"}]
  }],
  "valide_par_la_personne": true
}
```
Les champs `etapes`, `goulots` et `preuves` reprennent le vocabulaire de leur `outputContract`, ce qui rend le projet intégrable dans leur produit.

## 6. Les cas à tester (avant de dire que ça marche)
- **Cas normal** : 3 à 5 personnes, environ 1 jour chacune → un Wrapped complet.
- **Une personne refuse ou ne valide pas** → elle est absente du Wrapped, et les agrégats de moins de 3 personnes sont masqués.
- **Journée vide ou très courte** (moins de 30 min captées) → « pas assez de données », pas de tâche inventée.
- **Une seule app toute la journée** (que du code, par exemple) → pas de fausse « tâche répétée ».
- **Double écran** : l'écran qui n'est pas regardé ne compte pas (voir notre correctif).
- **Musique, perso, pauses** → exclus du temps de travail.
- **Données sensibles** dans un résumé (nom de client, montant) → visibles en relecture, et retirables.
- **Cas d'échec à montrer dans la démo** : une tâche que l'outil classe à tort comme automatisable, que le relecteur corrige, et le classement qui change.
- **2e entrée** : refaire tourner sur les données d'une autre personne, ou sur une journée synthétique.

## 7. Les rôles possibles (rien d'imposé)
Pas de chef de projet : chacun prend ce qu'il veut et le déclare dans `chantiers/<pseudo>.md` (voir le skill `equipe`). Le tableau ci-dessous sert seulement à voir les trous.

| Rôle | Briques | Livrable de samedi midi |
|---|---|---|
| **Data** (Youssef + Claude) | A + B | `resume-*.json` produit sur 2 vraies machines |
| **Back** | D | fusion → `insights.json`, testée sur 3 résumés, dont 1 synthétique |
| **Front** | C + E | Wrapped qui tourne sur un `insights.json` d'exemple (on peut commencer **ce soir** avec des données inventées) |
| **Pitch / produit** | onboarding, charte de campagne, script vidéo | pitch de 2 min + vidéo |

## 8. Le planning jusqu'au rendu (dimanche 14h30)
- **Ven. 22h–minuit** : figer le contrat (section 5). Le front démarre sur des données inventées. A tourne sur le Mac de Youssef.
- **Sam. matin** : B sort un vrai résumé. Le back fusionne 3 résumés.
- **Sam. 14h** : **première boucle complète** (vraies données → Wrapped), même moche.
- **Sam. 18h** : office hours screenpipe. Leur montrer la boucle et demander : « est-ce que vous l'intégreriez ? ».
- **Sam. soir** : relecture (C), finition du Wrapped, cas d'échec.
- **Dim. 10h** : gel des fonctionnalités. Tourner la vidéo de 2 min et écrire le README (checklist du kit, section 12 de la fiche).
- **Dim. 14h30** : rendu.

## 9. Le pitch en 2 minutes (brouillon)
1. « Les entreprises paient des ingénieurs pour regarder leurs salariés travailler » (leur propre phrase à l'ouverture).
2. Nous : une semaine de screenpipe chez des volontaires → le Wrapped de l'entreprise.
3. Démo : l'équipe a joué l'entreprise pendant le hackathon. Montrer le Wrapped, puis le top 3, puis une correction par le salarié.
4. Pourquoi c'est faisable en Europe : relecture par le salarié, agrégats seulement, suppression à la fin.
5. Pourquoi c'est rentable : le tri 80/20 avant l'IA (20 % des captures → 75 % des fenêtres).

## 10. Non vérifié / questions ouvertes
- **La qualité de leur détection de workflows** sur une vraie journée : elle n'a jamais tourné chez Youssef. À tester ce soir, car c'est le plus gros inconnu. Si elle est bonne, B l'utilise au lieu de la refaire.
- Leur détection passe par leur IA cloud : il faut voir si une campagne peut tourner en local (Ollama) pour l'argument européen.
- Le regroupement des « tâches communes » entre personnes aux libellés différents : la méthode reste à valider sur de vraies données.
- Le prix d'une mission de FDE ou de task mining, pour la comparaison : à sourcer.
- La position de Louis sur ce projet : copilote pour leurs FDE, ou concurrent ? À demander samedi à 18h.

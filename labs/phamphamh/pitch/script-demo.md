# Script de la démo — finale (3 min + 2 min de questions)

Base : l'enregistrement du 18/10 (11h24), recalé sur les vrais chiffres du dashboard Atelier Nova (`labs/adamaass/nova-dashboard/`, données `labs/adamaass/caibinet-nova/data.js`).

**Le plan** (demandé le 18/10 midi) : l'intro → l'entreprise et l'étude → **la preuve qu'on n'a rien écrit en dur** → ce qu'on a trouvé → les agents qu'on recommande → **ces agents, déployés ce matin, en direct**.

**Le style** (inspiré de Tugan Bara) : une promesse dans les 10 premières secondes, tenue à la fin ; des phrases courtes ; un ennemi clair (l'agent que personne n'utilise) ; des chiffres précis ; on parle au jury (« vous »).

**Le dispositif** : une personne parle, une autre clique. `labs/phamphamh/pitch/intro.html` (4 écrans, la flèche → fait apparaître les lignes une par une), puis le dashboard Atelier Nova (bouton **☀︎ Clair**, mode Présenter).

**Environ 320 mots** : environ 2 min 10 à voix haute, ce qui laisse 50 s pour les deux moments en direct.

Les passages marqués **[À CONSTRUIRE]** n'existent pas encore : on ne les dit pas tant qu'ils ne tournent pas pour de vrai.

---

## 0:00 – 0:10 · La promesse
**À l'écran** : `intro.html`, écran A, encore vide.

> « Ce matin, on a lancé des agents dans une entreprise. Ils tournent en ce moment. Dans trois minutes, vous verrez ce qu'ils ont fait. Mais d'abord, une question. »

*Si les agents ne tournent pas encore pour de vrai, on coupe cette phrase et on commence directement à l'écran A.* **[À CONSTRUIRE]**

## 0:10 – 0:45 · L'intro (`intro.html`)
**Écran A — Louis.**
> « Au début du hackathon, on a demandé à Louis le plus gros problème de ses utilisateurs. Sa réponse : ils ont plein de données, et ils ne savent pas quoi en faire. »

**Écran B — screenpipe.**
> « screenpipe enregistre tout ce qui se passe sur l'ordinateur. En local. »

**Écran C — le problème.**
> « Des milliers de captures par jour. Personne ne les relit. Personne ne sait quoi automatiser. L'outil existe. Il manque le cabinet. »

**Écran D — ce qu'on a construit.**
> « Alors on l'a construit. Un cabinet IA natif. Il observe. Il analyse avec les méthodes des grands cabinets. Il déploie les agents. Et il vérifie qu'ils servent. Parce que le vrai problème, ce n'est pas l'IA qui ne marche pas. C'est l'agent que personne n'utilise. »

## 0:45 – 1:00 · L'entreprise et l'étude
**À l'écran** : dashboard, écran 1. Pointer « Simulation ×10 » en bas à gauche.

> « Voici Atelier Nova. Une boutique en ligne, 60 salariés. Ce sont des gens réels : Stanford les a enregistrés au travail, c'est le jeu de données WONDERBREAD. On en a pris six, et on a multiplié par dix. »

## 1:00 – 1:20 · La preuve qu'on n'a rien écrit en dur — **[À CONSTRUIRE]**
**À l'écran** : un bouton « Retirer un salarié » ; le dashboard se recalcule en quelques secondes.

> « Vous vous demandez si on a tapé ces chiffres à la main. Choisissez un salarié. N'importe lequel. *(le juré choisit)* On le retire, on relance. Tout se recalcule à partir des enregistrements bruts. »

## 1:20 – 1:45 · Ce qu'on a trouvé
**À l'écran** : écrans 2, 3 et 4, un chiffre chacun.

> « 55 000 captures. 19 tâches qui reviennent. Coût : 72 000 euros par an. 40 % du temps dans un seul écran, le catalogue. Et un rapport de ventes, toujours le même, sorti 790 fois par semaine. »

## 1:45 – 2:10 · Ce que nos agents recommandent
**À l'écran** : écran 5. Cliquer **Prix produit**, puis **Créer la skill (SKILL.md)**.

> « Nos agents en tirent cinq automatisations. On commence par la modification des prix : c'est elle qui rend le plus d'heures. Un clic, et elle est écrite, à partir des étapes réellement observées. »

## 2:10 – 2:45 · En direct : les agents déployés ce matin — **[À CONSTRUIRE]**
**À l'écran** : le journal des actions de l'agent, dans une copie de Magento.

> « Et maintenant, ce que je vous ai promis. Cette automatisation, on l'a lancée ce matin. Voici son journal : [X] actions, chacune tracée. [X] prix modifiés en [X] secondes, contre [X] minutes à la main. Et quand une information manquait, l'agent s'est arrêté pour demander à un humain. »

## 2:45 – 3:00 · La fin
> « Louis, vos utilisateurs ont les données. Nous, on leur apporte le cabinet. Merci. »

**À trancher** : le nom de l'équipe ; la réponse de Louis, avec ses mots exacts si l'un de vous s'en souvient.

---

## Ce qui change par rapport à l'enregistrement (à ne pas redire)
| Dit à l'oral | Le vrai chiffre | Pourquoi c'est important |
|---|---|---|
| « 60 salariés observés » | 6 vraies personnes, simulées ×10 | Si un juré le découvre en question, toute la démo perd sa crédibilité. On le dit d'entrée. |
| « outil CRM Magneto » | **Magento**, un back-office de boutique en ligne | — |
| « 71 000 dollars » | **71 668 €** | euros, pas dollars |
| « 30 000 €, un temps plein » | Les 5 skills = **17 h / semaine**, un mi-temps | Le temps plein (0,8, soit 28 h / semaine et 49 300 €) suppose d'automatiser les 19 tâches. |
| « 24 heures par jour » | **17 h par semaine** (5 skills) | — |
| « 40 % … catalogue … 48 % » mélangés | 40 % = temps dans le **catalogue** (écran 3) ; 48 % = part du **coût** des 3 premiers problèmes (écran 4) | Deux écrans, deux chiffres. |
| « on peut dire avec certitude » | C'est une **estimation** | Le gain = le coût de la tâche × la part de son temps que la skill rend. Ne pas promettre. |
| « plusieurs centaines d'heures » (WONDERBREAD) | **Pas vérifié** | Ne pas le dire tant qu'on n'a pas le chiffre. |

## Les questions probables du jury (2 min)
- **« C'est des vraies données ? »** De vraies personnes au travail (WONDERBREAD, Stanford, licence ouverte), dans une entreprise fictive. 6 personnes réelles, volumes ×10. Nos propres Mac ont aussi tourné tout le week-end : la chaîne marche sur de vraies captures screenpipe.
- **« Comment vous calculez les euros ? »** Heures par semaine × 46 semaines × 38 € de l'heure. Le gain d'une tâche = son coût × la part de son temps que la skill rend. Les deux formules sont dans l'annexe « Méthode ».
- **« Et la vie privée ? »** Chaque salarié relit et valide son résumé, seul le résumé part (ni capture, ni texte d'écran). Aucun chiffre par personne, et tout ce qui touche moins de 3 personnes est masqué.
- **« Ça coûte cher en IA, une semaine × 60 personnes ? »** On trie avant : garder 20 % des captures conserve 75 % des fenêtres de travail (mesuré sur nos Mac). Puis un seul appel à l'IA par jour et par personne.
- **« La skill fonctionne vraiment ? »** Testée en vrai sur une autre tâche (saisie de commande dans un faux Gmail + Sage) : 4 cas sur 4, avec arrêt sur les exceptions et validation humaine. Pas encore testée dans Magento : à dire tel quel.
- **« Pourquoi des montants si petits par tâche ? »** Les tâches WONDERBREAD sont courtes (moins d'1 min 30). Chez une vraie PME, les tâches durent plus longtemps.
- **« Quel lien avec screenpipe ? »** On utilise sa capture, son format de workflow, et on ajoute ce qui leur manque : la campagne avec relecture par le salarié, la fusion de plusieurs personnes, et le rapport pour le dirigeant.

## Avant de monter sur scène
- [ ] `intro.html` ouvert en plein écran sur l'écran A ; le dashboard ouvert dans un 2e onglet.
- [ ] Dashboard : bouton **☀︎ Clair** cliqué (il s'ouvre en sombre), **mode Présenter**, écran 1 affiché.
- [ ] Répéter les 2 clics : Rapport ventes (écran 4) ; Prix produit puis Créer la skill (écran 5). Vérifiés le 18/10 : ils marchent.
- [ ] Chronométrer une fois en entier : viser 2 min 50.
- [ ] Choisir qui parle et qui clique.

# Script de la démo — finale (3 min + 2 min de questions)

Base : l'enregistrement du 18/10 (11h24), recalé sur les vrais chiffres du dashboard Atelier Nova (`labs/adamaass/nova-dashboard/`, données `labs/adamaass/caibinet-nova/data.js`).

**Le dispositif** : une personne parle, une autre clique. Dashboard en **mode Présenter** (flèches ← →), thème clair pour le projecteur. On suit les 5 écrans dans l'ordre, rien d'autre à ouvrir.

**Environ 420 mots** : ça tient en 2 min 50 à un rythme posé. Les chiffres se disent arrondis, comme écrits ci-dessous.

---

## 0:00 – 0:20 · L'accroche
**À l'écran** : le dashboard, écran 1 « Contexte », pas encore commenté.

> « Une PME qui veut "faire de l'IA" ne sait pas par où commencer. Aujourd'hui, elle paie des consultants pour venir regarder ses équipes travailler pendant des semaines. Nous, on a remplacé les consultants par screenpipe : il tourne une semaine sur les postes des volontaires, et on rend au dirigeant ce rapport. »

## 0:20 – 0:40 · D'où viennent les données (à dire, pas à cacher)
**À l'écran** : pointer l'étiquette « Simulation ×10 » en haut.

> « On ne pouvait pas filmer les écrans d'une vraie entreprise ce week-end. On a pris WONDERBREAD, un jeu de données de Stanford : de vraies personnes, enregistrées pendant qu'elles travaillent dans le back-office d'une boutique en ligne, sur Magento. C'est exactement ce que screenpipe capte. Six de ces personnes forment notre entreprise fictive, Atelier Nova, et on a multiplié par dix pour simuler 60 salariés. C'est écrit sur chaque écran. »

## 0:40 – 1:00 · Écran 1 — Ce qu'on a observé
**À l'écran** : l'entonnoir captures → skills.

> « 60 salariés, 2 équipes, 5 jours. 55 000 captures d'écran. L'IA ne les lit pas toutes : on trie d'abord, puis on regroupe en 14 000 moments de travail, puis en 19 tâches qui se répètent. 11 sont de vrais problèmes. 5 peuvent devenir des skills Claude. Et avant que quoi que ce soit parte, chaque salarié relit son résumé et le valide. Aucune capture ne quitte son ordinateur. »

## 1:00 – 1:15 · Écran 2 — Ce qu'on a trouvé
**À l'écran** : l'anneau du coût annuel.

> « Ces tâches répétées coûtent 72 000 euros par an à Atelier Nova. On peut en récupérer 49 000. Les 5 premières skills, à elles seules : 30 000. »

## 1:15 – 1:35 · Écran 3 — Où part le temps ?
**À l'écran** : heures par écran Magento. Cliquer sur l'équipe **Opérations**.

> « 40 % du temps passe dans un seul écran : le catalogue produits. Chez l'équipe Opérations, c'est presque la moitié de la journée. »

## 1:35 – 2:00 · Écran 4 — Qu'est-ce qui coûte le plus ?
**À l'écran** : le treemap. Cliquer sur **Rapport ventes**.

> « Trois problèmes font 48 % du coût. Un : sortir le même rapport de ventes, 790 fois par semaine. Deux : vérifier les commandes annulées. Trois : modifier le prix d'un produit. Je clique sur le rapport : voici les étapes qu'on a vues, les cinq noms différents que les gens lui donnent, et les exceptions. Chaque chiffre mène à ce qui a été observé. »

## 2:00 – 2:35 · Écran 5 — Que faire, dans quel ordre ?
**À l'écran** : la cascade skill après skill. Puis cliquer **Créer la skill (SKILL.md)** sur la première.

> « Notre recommandation, dans l'ordre. On commence par la modification de prix : c'est elle qui rend le plus d'heures, et elle se construit en une semaine. Les 5 skills rendent 17 heures par semaine à l'équipe, soit 30 000 euros par an. Et la skill sort d'ici, en un clic, écrite à partir des étapes réelles. Il reste à la relire avant de l'activer. »

## 2:35 – 2:55 · La fin
**À l'écran** : retour sur l'écran 1, ou le lien du dépôt.

> « Un audit de cabinet, en une semaine, sans consultant sur place. Les données restent sur les machines, chaque salarié valide ce qui part, et rien n'est montré par personne. Tout part de screenpipe, tout finit en skill Claude. Merci. »

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
- [ ] Dashboard ouvert, thème clair, **mode Présenter**, écran 1 affiché.
- [ ] Répéter les 3 clics : équipe Opérations (écran 3), Rapport ventes (écran 4), Créer la skill (écran 5).
- [ ] Chronométrer une fois en entier : viser 2 min 50.
- [ ] Choisir qui parle et qui clique.

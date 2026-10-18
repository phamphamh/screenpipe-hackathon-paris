# DeloAI — dossier de scène (pitch 3 à 5 min)

Texte à dire : `prompteur.md` (3:00). Si le créneau fait 4 ou 5 min, ajouter le bloc **[+40 s]** sur la slide « How it works » (déjà dans le prompteur) → 3:40, avec de la marge pour les clics.

---

## 1. 15 min avant de monter

1. **Mac branché sur secteur.** Mode « Ne pas déranger » (Centre de contrôle → Concentration). Quitter WhatsApp, Slack, Mail.
2. **Internet** : les agents Claude en ont besoin. Tester le Wi-Fi de la salle ; garder le partage de connexion du téléphone prêt.
3. **Écran** : Réglages → Écrans → « Recopier » (le même écran sur le projecteur et sur le Mac).
4. **Deux onglets Chrome, rien d'autre** :
   - onglet 1 : les slides → https://claude.ai/artifact/JRtx9pRtEfhgrDfK1sEPJf
   - onglet 2 : la démo → http://localhost:8798/agents-nova/#audit
   - Chrome en plein écran (⌃⌘F), zoom à 100 % (⌘0).
5. **Une répétition à blanc** : Karim → Product pricing → Deploy workflow → Run it live. La fenêtre de l'agent s'ouvre à gauche, ~50 s, « 3 prices updated ». Les prix se remettent tout seuls avant chaque passage en direct.
6. Revenir sur l'onglet 1, slide 1. Prompteur sur le téléphone (`~/Desktop/prompteur-deloai.md`, par AirDrop).

Si on te demande de présenter depuis **un autre ordinateur** : la démo en direct ne marche que sur ton Mac. Ouvre alors les deux liens en ligne (slides + démo rejouée https://claude.ai/artifact/CtLUkz619Yk81w7mjWV4A2) — ils doivent être partagés « toute personne disposant du lien » avant.

---

## 2. Si ça casse sur scène

| Ce qui arrive | Ce que tu fais | Ce que tu dis |
|---|---|---|
| L'agent met plus de 40 s | Repasser sur les slides, revenir pour la réponse | "While it finishes…" |
| Rien ne s'ouvre / pas d'internet | Office → bureau de l'agent → ses derniers passages | "Here's this morning's run — it runs every five minutes." |
| La page de démo est blanche | Ouvrir la démo en ligne (lien ci-dessus) | "Here's the same audit, replayed." |
| Le Mac est mort | Slides en ligne depuis n'importe quel ordi | Raconter la démo sur la slide « Before / After » |

Un clic « Run it live » pendant qu'un agent tourne en fond attend maintenant son tour (avant : il ne se passait rien).

---

## 3. Questions probables du jury (réponses à dire en anglais)

**"Is this real screenpipe data?"**
The pipeline runs on screenpipe captures, we tested it on our own machines. For the client, no company gives you a week of its staff's screens in 48 hours, so we used Stanford's recordings of real people doing real back-office work, converted to screenpipe's format.

**"Is the agent real, or a recording?"**
Real. A Claude agent, a real Magento store, a real request from the Stanford dataset. It's been running every five minutes since this morning, every action logged with a screenshot.

**"Is it computer use?"**
Claude decides what to do. It acts through the store's API and a real browser it drives. Faster and more reliable than clicking pixels, and you can watch it.

**"Does it work beyond Magento?"**
The audit works on any software: screenpipe sees every app. Deploying needs one connector per tool: an API, or the browser. Today we wired Magento; the next tool is a new connector, not a new product.

**"What about privacy?"**
Everything stays on the laptop. The employee sees their own summary and validates it before anything is shared. No screenshot leaves the machine.

**"What if the agent makes a mistake?"**
Every action is logged with a screenshot, and prices can be restored in one command. Next step: a human approves risky actions before they run. *(Honnête : l'approbation existe dans le prototype de Natsuwy, pas encore branchée dans cette démo.)*

**"Why not just give people Claude + screenpipe?"**
Because the data was never the problem. Nobody knows what to look at. We tell you which tasks cost the most, put a price on them, and deploy the agent.

**"Business model?"**
Like a consulting firm, minus the weeks on site: a fixed fee for the audit, then a monthly fee per agent running. *(Proposition, pas encore validée en équipe.)*

**"Where do the numbers come from?"**
One week of six real people, scaled to a 60-person company. Hours times 46 weeks times €38 an hour: €71,700 a year lost to repeated tasks, €30,000 recoverable with five workflows.

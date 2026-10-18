# DeloAI — pitch script, 3:00 (English, matched to the deck and the demo of 18/10)

**Setup**: tab 1 = the deck (artifact, → to advance; each slide appears in full). Tab 2 = the demo, http://localhost:8798/agents-nova/#audit (`python3 labs/phamphamh/agents-nova/serveur.py`, test store running). One "Run it live" right before going on stage. Product pricing resets the prices by itself before each live run. Keep the left half of the screen free: the agent's browser window opens there.

Pace: about 150 words a minute. Spoken text: 350 words (≈ 2:20) + ~35 s of clicks and tab switches, with ~5 s of margin. Timed section by section at 150 words a minute.

---

### 0:00 – 0:09 · Slide 1
If you use screenpipe, you have a problem. *(→ "And it's not your fault." appears by itself.)* And it's not your fault.

### 0:09 – 0:18 · Slide 2 · screenpipe
screenpipe records everything on your computer. Every screen, every click, every meeting. Locally. Searchable. Plugged into Claude and Cursor.

### 0:18 – 0:29 · Slide 3 · Louis
So we asked Louis, screenpipe's founder, what his users' biggest problem was. His answer: they have tons of data, and they don't know what to do with it.

### 0:29 – 0:49 · Slide 4 · data vs context
On the left, what people do today. A consulting firm on site for weeks. A 50-page report that ends up in a drawer. Or screenpipe alone, and nobody reads the captures. The problem was never the data. It's the context: what to look at, what to automate, where to start.

### 0:49 – 0:53 · Slide 5 · DeloAI
That's DeloAI. An AI-native consulting firm.

### 0:53 – 1:07 · Slide 6 · Atelier Nova
Our test client: Atelier Nova, an online sportswear store, 60 employees. The experiment: we replayed a real week of back-office work, as if they had run screenpipe on every desk. Real people, recorded by Stanford.

### 1:07 – 1:10 · Slide 7 · Live demo
Let's look inside. *(switch to tab 2)*

### 1:10 – 1:20 · Demo · Audit (top)
One week, and the audit says: €71,700 a year lost to tasks people repeat by hand. €30,000 we can get back.

### 1:20 – 1:30 · Demo · Audit, scroll to "One employee, step by step", click KARIM
Let's take Karim, catalog manager. What screenpipe captured, his week, his top repetitive tasks. *(click "Open in the office →" on Product pricing)*

### 1:30 – 1:40 · Demo · Office, Karim's panel → click "Product pricing"
Here's the workflow, built from the steps he actually performs. *(click "Deploy workflow", then "Run it live")*

### 1:40 – 2:30 · Demo · the agent runs (~50 s on screen)
Now the agent does it, in the store's real back-office. *(the browser opens on the left)* A real request, recorded by Stanford: cut the price of the yellow Gwyn tees, below size L, by 15%. Claude finds the products, opens each one, types the new price, saves. Every action is logged. We slowed it down so you can follow; in production it takes fifteen seconds. *(the answer appears)* Three prices updated. Nobody touched the keyboard.

### 2:30 – 2:37 · Slide 8 · How it works *(back to tab 1)*
No magic. Observe with screenpipe, audit, deploy. It all runs on a laptop.

### 2:37 – 2:44 · Slide 9 · Before / after
Before: weeks on site and a report. After: one week of screenpipe, and agents already running.

### 2:44 – 2:52 · Slide 10
So the question is no longer what to do with your data. It's what you'll do with the time you get back.

### 2:52 – 3:00 · Slide 11
DeloAI. Your consulting firm and your IT team, in your pocket.

---

**If the agent is slow** (more than 40 s): keep talking over slide 8 ("while it finishes…") and come back to tab 2 for the answer, or skip the answer.
**If the live run fails**: say "here's this morning's run" and click a deployed agent (Office, agent desk) to show its last runs.

**Numbers and sources**
- €71.7k / year, 790× / week (79 × 10), €30.1k / year, 60 employees (6 real people × 10), 55,510 captures: adamaass's audit (`labs/adamaass/caibinet-nova/data.js`).
- Karim: sales report 17×, product pricing 5× this week (`personnes.json`, from his real Stanford recordings). Live pricing run measured: 54 s (slowed), 11–25 s in production mode; by hand 58 s.
- Agent times measured on the test store: sales report ~10 s in production mode, ~33 s in live (slowed) mode; by hand 23 s (median of 20 Stanford recordings). Price update ~15 s vs 58 s by hand.

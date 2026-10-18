# DeloAI — pitch script, 3:00 (English, matched to the deck and the demo of 18/10)

**Setup**: tab 1 = the deck (artifact, → to advance; each slide appears in full). Tab 2 = the demo, http://localhost:8798/agents-nova/#audit (`python3 labs/phamphamh/agents-nova/serveur.py`, test store running). One "Run it live" right before going on stage. Keep the left half of the screen free: the agent's browser window opens there.

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

### 1:10 – 1:23 · Demo · Audit (top)
One week, and the audit says: €71,700 a year lost to tasks people repeat by hand. The same sales report, pulled 790 times a week. €30,000 a year we can get back.

### 1:23 – 1:38 · Demo · Audit, scroll to "One employee, step by step" (Sophie)
Let's take one person. Sophie, sales analyst. Here's what screenpipe captured, her week task by task, and her top repetitive tasks. From these, we automate two. *(click "Open in the office →")*

### 1:38 – 1:51 · Demo · Office, Sophie's panel → click "Sales report"
This is her desk. Here's the workflow, built from the steps she actually performs: trigger, steps, output. *(click "Deploy workflow", then "Run it live")*

### 1:51 – 2:26 · Demo · the agent runs (~35 s on screen)
And now an agent runs it, in the store's real back-office. *(the browser opens on the left)* This is a real request, recorded by Stanford. Claude reads it, opens Reports, sets the dates, runs the report. Every action is logged. We slowed it down so you can follow; in production it takes ten seconds. *(the answer appears in the panel)* There's the answer. Nobody touched the keyboard.

### 2:26 – 2:34 · Slide 8 · How it works *(back to tab 1)*
No magic. Observe with screenpipe, audit, deploy. It all runs on a laptop.

### 2:34 – 2:41 · Slide 9 · Before / after
Before: weeks on site and a report. After: one week of screenpipe, and agents already running.

### 2:41 – 2:50 · Slide 10
So the question is no longer what to do with your data. It's what you'll do with the time you get back.

### 2:50 – 3:00 · Slide 11
DeloAI. Your consulting firm and your IT team, in your pocket.

---

**If the agent is slow** (more than 40 s): keep talking over slide 8 ("while it finishes…") and come back to tab 2 for the answer, or skip the answer.
**If the live run fails**: say "here's this morning's run" and click a deployed agent (Office, agent desk) to show its last runs.

**Numbers and sources**
- €71.7k / year, 790× / week (79 × 10), €30.1k / year, 60 employees (6 real people × 10), 55,510 captures: adamaass's audit (`labs/adamaass/caibinet-nova/data.js`).
- Sophie: 39 min, 667 captures, 221 moments; cancelled orders 8×, sales report 7× (`personnes.json`, from her real Stanford recordings).
- Agent times measured on the test store: sales report ~10 s in production mode, ~33 s in live (slowed) mode; by hand 23 s (median of 20 Stanford recordings). Price update ~15 s vs 58 s by hand.

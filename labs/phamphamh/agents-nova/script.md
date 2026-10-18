# DeloAI — pitch script (English, 18/10)

**Setup**: tab 1 = the pitch deck (artifact, arrows to advance). Tab 2 = the live demo, `python3 labs/phamphamh/agents-nova/serveur.py` → http://localhost:8798 (the test store must be running, see `labs/phamphamh/boutique/README.md`). Do one "Run live" right before going on stage: the browser window takes ~10 s to open the first time.

---

## Deck — opening

**[1]** If you use screenpipe, you have a problem. *(press)* And it's not your fault.

**[2 · screenpipe]** Your computer records everything. Every screen. Every click. Every meeting. Thousands of captures a day. Searchable, local, plugged into Claude and Cursor.

**[3 · Louis]** And yet, you still don't know what to do with it. That's not us saying it. We asked Louis, screenpipe's founder, what his users' biggest problem was. His answer: they have tons of data, and they don't know what to do with it.

**[4 · what doesn't work]** Today you have two options. A consulting firm: consultants on site for weeks, a 50-page report that ends up in a drawer. Or screenpipe alone: thousands of captures a day that nobody reads. The truth is, the problem was never the data. It's the context. What to look at. What to automate. Where to start.

**[5 · DeloAI]** So we built the missing piece. We're DeloAI, an AI-native consulting firm. Our analysis method comes from the big firms. The way we deploy agents comes from the best research labs. And nobody travels.

**[6 · Atelier Nova]** Our first client: Atelier Nova. An online sportswear store, 60 employees, everything runs in their Magento back-office. One week of screenpipe on every desk: 55,000 captures. To be clear: these are 6 real people, recorded by Stanford doing real back-office work, multiplied by ten. In a real engagement, it's your own team running screenpipe for a week.

**[7 · demo]** Let me show you. *(switch to tab 2)*

## Live demo

**[Audit]** Step one, the audit. The AI read every capture, employee by employee. Result: €71,700 a year goes into repetitive tasks. 41 hours lost every week. 40% of the time in a single screen, the catalog. And one sales report, always the same, pulled 790 times a week. We found five workflows worth automating. We deploy three.

**[Office]** Step two: the office. Here are the employees. Let's click on Sophie, a sales analyst. *(click)* These are her workflows, found by the audit: the sales report she runs again and again. *(Create workflow)* The workflow is written from the steps she actually performs. *(Run live)* And now the agent runs it, in the real back-office, right in front of you. Every action is traced. No one at the keyboard.

*(while it runs)* This is a real request, recorded by Stanford. The agent reads it, opens the store, does the job, and reports back.

## Deck — closing *(back to tab 1)*

**[8 · how it works]** And it's not magic. Three steps. Observe: screenpipe on every desk, we filter 55,000 captures down to the moments that matter, Claude reads each employee, and the employee validates before anything is shared. Audit: we merge the team, put a price on every repeated task, and rank what to automate. Deploy: the workflow is written from the observed steps, a Claude agent runs it with the store's tools, and every action is logged. All of it runs on a laptop.

**[8 · before / after]** Before: weeks on site, a 50-page report, no agent deployed. After: one week of screenpipe, the audit in a day, agents already running.

**[9]** So the question is no longer: what do I do with my data? The question is: what will you do with the time you get back?

**[10]** DeloAI. Your consulting firm and your IT team, in your pocket.

---

**Numbers and sources**
- 6 real people × 10 = 60 employees; 55,510 captures (×10); 19 repeated tasks; €71.7k / year; 41 h lost / week; 40% in the catalog; sales report 790× / week (79 × 10): adamaass's audit (`labs/adamaass/caibinet-nova/data.js`).
- Human time per task: sales report 23 s, price change 58 s, cancelled orders 36 s (medians of the Stanford WONDERBREAD recordings).
- Agent requests: real WONDERBREAD requests (`labs/phamphamh/agents-nova/demandes.json`), run by Claude in the Magento test store.
- Don't claim the agent is faster in live mode: it is slowed down on purpose so the audience can follow. The point is zero human time.

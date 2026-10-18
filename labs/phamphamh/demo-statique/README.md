# DeloAI · quick demo (static)

The DeloAI demo without installing anything: the audit, one employee step by step, and the 3D office where the agents replay their real runs of 18/10 (journal, screenshots of the Magento store, answers).

```sh
python3 -m http.server 8000 --directory labs/phamphamh/demo-statique
# → http://localhost:8000
```

"Run it live" replays the last real run of the workflow: launching a new agent needs the test store and the server (`labs/phamphamh/agents-nova/`).

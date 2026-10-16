# Récupère les captures « regardées » de la journée + leur texte, depuis l'API locale screenpipe.
import json, os, sys, urllib.request, io
from PIL import Image
KEY = os.environ["SP_KEY"]; OUT = sys.argv[1]
def post(q):
    r = urllib.request.Request("http://localhost:3030/raw_sql", data=json.dumps({"query": q}).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))
rows = post("""SELECT id, timestamp, app_name, window_name, device_name, capture_trigger
  FROM frames WHERE focused = 1 AND app_name IS NOT NULL
  AND strftime('%H', timestamp) IN ('09','10','16','17','18') ORDER BY timestamp LIMIT 2000""")
ok = []
for i, r in enumerate(rows):
    p = f"{OUT}/frames/{r['id']}.jpg"
    if not os.path.exists(p):
        try:
            req = urllib.request.Request(f"http://localhost:3030/frames/{r['id']}", headers={"Authorization": f"Bearer {KEY}"})
            im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read())).convert("RGB")
            im.thumbnail((512, 512)); im.save(p, quality=85)
        except Exception as e:
            print("skip", r["id"], e); continue
    ok.append(r)
    if i % 100 == 0: print(i, len(rows), flush=True)
json.dump(ok, open(f"{OUT}/meta.json", "w"))
print("frames:", len(ok), "apps:", len({r['app_name'] for r in ok}), "windows:", len({(r['app_name'], r['window_name']) for r in ok}))

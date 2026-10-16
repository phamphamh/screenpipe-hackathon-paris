# Compare deux dossiers de données screenpipe (origine vs correctif) enregistrés en même temps.
import sqlite3, sys, collections, os
def stats(d):
    db = sqlite3.connect(f"file:{os.path.join(d,'db.sqlite')}?mode=ro", uri=True)
    rows = db.execute("SELECT device_name, focused, capture_trigger, app_name, "
                      "length(COALESCE(full_text,'')) + length(COALESCE(accessibility_text,'')) FROM frames").fetchall()
    n = len(rows); unf = sum(1 for r in rows if r[1] == 0); noapp = sum(1 for r in rows if not r[3])
    chars = sum(r[4] or 0 for r in rows); unf_chars = sum(r[4] or 0 for r in rows if r[1] == 0)
    trig = collections.Counter((r[2], 'focus' if r[1] else 'autre écran') for r in rows)
    size = sum(os.path.getsize(os.path.join(p, f)) for p, _, fs in os.walk(d) for f in fs)
    return dict(captures=n, autre_ecran=unf, sans_app=noapp, texte=chars, texte_autre_ecran=unf_chars, disque_mo=round(size/1e6,1)), trig
o, ot = stats(sys.argv[1]); f, ft = stats(sys.argv[2])
print(f"{'':22}{'origine':>10}{'correctif':>11}{'écart':>9}")
for k in o:
    a, b = o[k], f[k]; pct = f"{100*(b-a)/a:+.0f}%" if a else "-"
    print(f"{k:22}{a:>10}{b:>11}{pct:>9}")
print("\ndéclencheurs origine :", ot.most_common(8)); print("déclencheurs correctif :", ft.most_common(8))

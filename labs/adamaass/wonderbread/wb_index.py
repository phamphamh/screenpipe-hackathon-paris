"""Index WONDERBREAD : chaque démo -> annotateur, site, tâche, modèle d'intention, dossier local.
Usage : python3 -I wb_index.py <dossier wonderbread> -> écrit index.json dans ce dossier."""
import collections, json, os, re, sys, zipfile

base = sys.argv[1]
z = zipfile.ZipFile(os.path.join(base, "pm.xlsx"))
ss = [re.sub(r"<[^>]+>", "", m) for m in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), re.S)]
rels = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', z.read("xl/_rels/workbook.xml.rels").decode()))
feuilles = re.findall(r'<sheet name="([^"]+)"[^>]*r:id="([^"]+)"', z.read("xl/workbook.xml").decode())

def lignes(cible):
    x = z.read("xl/" + cible.replace("/xl/", "")).decode()
    out = []
    for r in re.findall(r"<row[^>]*>(.*?)</row>", x, re.S):
        row = {}
        for ref, t, v in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(?:<f>.*?</f>)?<v>(.*?)</v>', r, re.S):
            row[ref] = ss[int(v)] if 't="s"' in t else v
        out.append(row)
    return out

meta = json.load(open(os.path.join(base, "metadata.json")))["results"]
par_id = {m["folder_id"]: m["folder_name"] for m in meta if m}
racine = os.path.join(base, "traces", "demos_sop_and_trace_only")
locaux = set(os.listdir(racine))

demos, variations = [], {}
for nom, rid in feuilles:
    rows = lignes(rels[rid])
    h = {v: k for k, v in rows[0].items()}
    for r in rows[1:]:
        if nom == "Gold SOPs":
            if r.get(h["Incorrect Demos"]):
                variations[r.get(h["Task ID"])] = r[h["Incorrect Demos"]]
            continue
        lien, qui = r.get(h["Gdrive link"], ""), r.get(h["Person"])
        m = re.search(r"folders/([\w-]+)", lien)
        dossier = par_id.get(m.group(1)) if m else None
        if not (qui and dossier and dossier in locaux):
            continue
        demos.append({"feuille": nom, "personne": qui, "task_id": r.get(h["Task ID"]), "site": r.get(h["Site"]),
                      "intention": r.get(h["Task"]), "modele": r.get(h["Intent Template"]), "dossier": dossier,
                      "possible": r.get(h["Possible?"])})

json.dump({"demos": demos, "variations": variations}, open(os.path.join(base, "index.json"), "w"), ensure_ascii=False, indent=1)
print(len(demos), "démos reliées à un annotateur ;", len(locaux), "dossiers locaux ;", len(variations), "tâches avec variations notées")
par_p = collections.defaultdict(list)
for d in demos:
    par_p[d["personne"]].append(d)
for p, ds in sorted(par_p.items(), key=lambda x: -len(x[1])):
    sites = collections.Counter(d["site"] for d in ds)
    modeles = collections.Counter(d["modele"] for d in ds)
    rep = sum(1 for n in modeles.values() if n >= 2)
    print(f"{p[:3]}… {len(ds):4d} démos · sites {dict(sites.most_common(3))} · {rep} modèles faits ≥2 fois")

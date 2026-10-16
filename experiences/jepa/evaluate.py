# Compare les 3 empreintes sur 3 questions utiles pour screenpipe.
import json, sys, numpy as np
from datetime import datetime
from sklearn.metrics import roc_auc_score
D = sys.argv[1]; meta = json.load(open(f"{D}/meta.json")); E = dict(np.load(f"{D}/embs.npz"))
ts = np.array([datetime.fromisoformat(r["timestamp"]).timestamp() for r in meta])
win = [(r["app_name"], r["window_name"]) for r in meta]; app = np.array([r["app_name"] for r in meta])
order = np.argsort(ts); ts, app = ts[order], app[order]; win = [win[i] for i in order]
def norm(x): x = x - x.mean(0); return x / (np.linalg.norm(x, axis=1, keepdims=True) + 1e-9)
print(f"{len(meta)} captures, {len(set(app))} apps, {len(set(win))} fenêtres")
change = np.array([win[i] != win[i+1] for i in range(len(win) - 1)])
print(f"paires consécutives : {len(change)}, dont {change.sum()} changements de fenêtre\n")
rng = np.random.default_rng(0)
for k in ["pixels", "siglip", "vjepa2"]:
    X = norm(E[k][order]); S = X @ X.T
    # 1. repérer un changement de tâche entre deux captures qui se suivent
    auc = roc_auc_score(change, 1 - np.array([S[i, i+1] for i in range(len(X) - 1)]))
    # 2. reconnaître l'activité : le voisin le plus proche à plus de 10 min est-il dans la même app ?
    far = np.abs(ts[:, None] - ts[None, :]) > 600; S2 = np.where(far, S, -9); nn = S2.argmax(1); valid = far.any(1)
    knn = (app[nn] == app)[valid].mean()
    # 3. le 80/20 : on ne garde que 20 % des captures (les plus nouvelles), combien de fenêtres reste-t-il ?
    def keep(th):
        kept = [0]
        for i in range(1, len(X)):
            if 1 - S[i, kept].max() > th: kept.append(i)
        return kept
    lo, hi = 0.0, 2.0
    for _ in range(25):
        mid = (lo + hi) / 2; n = len(keep(mid))
        lo, hi = (mid, hi) if n > 0.2 * len(X) else (lo, mid)
    kept = keep(hi); cov = len({win[i] for i in kept}) / len(set(win))
    print(f"{k:7s} | repère les changements (AUC) {auc:.3f} | reconnaît l'app {knn:.1%} | 20 % gardé ({len(kept)}) -> {cov:.1%} des fenêtres")
rand = np.mean([len({win[i] for i in rng.choice(len(win), int(0.2*len(win)), replace=False)}) / len(set(win)) for _ in range(200)])
step = len({win[i] for i in range(0, len(win), 5)}) / len(set(win))
print(f"\nréférence : 20 % au hasard -> {rand:.1%} des fenêtres ; 1 capture sur 5 -> {step:.1%}")
vals, cnt = np.unique(app, return_counts=True); print(f"référence : toujours répondre l'app la plus fréquente -> {cnt.max()/len(app):.1%}")
print("temps par capture :", json.load(open(f"{D}/times.json")))

# V-JEPA 2 dans son vrai mode : une vraie mini-vidéo de 8 captures qui se suivent = un « moment ».
# On compare à SigLIP moyenné sur les mêmes 8 captures. Question : le moment est-il reconnu (même app ailleurs dans la journée) ?
import json, sys, numpy as np, torch
from collections import Counter
from datetime import datetime
from PIL import Image
from transformers import AutoModel, AutoVideoProcessor
D = sys.argv[1]; meta = json.load(open(f"{D}/meta.json"))
order = np.argsort([datetime.fromisoformat(r["timestamp"]).timestamp() for r in meta]); meta = [meta[i] for i in order]
ts = np.array([datetime.fromisoformat(r["timestamp"]).timestamp() for r in meta])
sig = dict(np.load(f"{D}/embs.npz"))["siglip"][order]
starts = list(range(0, len(meta) - 8, 4))
lab = [Counter(meta[j]["app_name"] for j in range(s, s + 8)).most_common(1)[0][0] for s in starts]
name = "facebook/vjepa2-vitl-fpc64-256"; proc = AutoVideoProcessor.from_pretrained(name)
model = AutoModel.from_pretrained(name, dtype=torch.float16).to("mps").eval(); V = []
for s in starts:
    clip = np.stack([np.asarray(Image.open(f"{D}/frames/{meta[j]['id']}.jpg").convert("RGB").resize((448, 280))) for j in range(s, s + 8)])
    x = proc([clip], return_tensors="pt")["pixel_values_videos"].to("mps", torch.float16)
    with torch.no_grad(): V.append(model.get_vision_features(x).float().mean(1).cpu().numpy()[0])
def score(X):
    X = X - X.mean(0); X /= np.linalg.norm(X, axis=1, keepdims=True); S = X @ X.T
    t = ts[starts]; far = np.abs(t[:, None] - t[None, :]) > 600; nn = np.where(far, S, -9).argmax(1)
    return np.mean([lab[i] == lab[nn[i]] for i in range(len(starts)) if far[i].any()])
print(f"{len(starts)} moments de 8 captures")
print(f"V-JEPA 2 (vraie vidéo) reconnaît l'app : {score(np.array(V)):.1%}")
print(f"SigLIP (moyenne des 8)  reconnaît l'app : {score(np.stack([sig[s:s+8].mean(0) for s in starts])):.1%}")

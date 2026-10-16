# Calcule une empreinte par capture avec 3 méthodes : V-JEPA 2, SigLIP (référence image classique), pixels bruts.
import json, sys, time, numpy as np, torch
from PIL import Image
from transformers import AutoModel, AutoVideoProcessor, AutoImageProcessor
D = sys.argv[1]; meta = json.load(open(f"{D}/meta.json")); dev = "mps"
imgs = lambda batch: [Image.open(f"{D}/frames/{r['id']}.jpg").convert("RGB") for r in batch]
out, times = {}, {}
# pixels : vignette 32x32 en gris
out["pixels"] = np.stack([np.asarray(Image.open(f"{D}/frames/{r['id']}.jpg").convert("L").resize((32, 32)), dtype=np.float32).ravel() for r in meta])
# V-JEPA 2 : on donne l'image comme une mini-vidéo de 2 images identiques (taille minimale du modèle)
name = "facebook/vjepa2-vitl-fpc64-256"
proc = AutoVideoProcessor.from_pretrained(name); model = AutoModel.from_pretrained(name, dtype=torch.float16).to(dev).eval()
embs, t0 = [], time.time()
for i in range(0, len(meta), 16):
    vids = [np.stack([np.asarray(im)] * 2) for im in imgs(meta[i:i+16])]
    x = proc(vids, return_tensors="pt")["pixel_values_videos"].to(dev, torch.float16)
    with torch.no_grad(): f = model.get_vision_features(x)
    embs.append(f.float().mean(1).cpu().numpy())
torch.mps.synchronize(); times["vjepa2"] = (time.time() - t0) / len(meta); out["vjepa2"] = np.concatenate(embs)
del model; torch.mps.empty_cache()
# SigLIP
name = "google/siglip-base-patch16-224"
proc = AutoImageProcessor.from_pretrained(name); model = AutoModel.from_pretrained(name, dtype=torch.float16).to(dev).eval()
embs, t0 = [], time.time()
for i in range(0, len(meta), 32):
    x = proc(images=imgs(meta[i:i+32]), return_tensors="pt")["pixel_values"].to(dev, torch.float16)
    with torch.no_grad(): f = model.get_image_features(pixel_values=x)
    f = f.pooler_output if hasattr(f, "pooler_output") else f
    embs.append(f.float().cpu().numpy())
torch.mps.synchronize(); times["siglip"] = (time.time() - t0) / len(meta); out["siglip"] = np.concatenate(embs)
np.savez(f"{D}/embs.npz", **out); json.dump(times, open(f"{D}/times.json", "w")); print(times, {k: v.shape for k, v in out.items()})

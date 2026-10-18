#!/usr/bin/env python3
"""Les outils des agents IA d'Atelier Nova dans la vraie boutique de test (back-office Magento).

L'API REST pour aller vite, Playwright seulement pour les rapports et les captures (on VOIT le résultat).
Chaque appel écrit une ligne dans donnees/agents-nova/journal.jsonl (agent et run : variables AGENT_ID, AGENT_RUN).
La sortie sur stdout est un JSON court, lu par l'agent.

  python3 boutique.py chercher "gwyn endurance yellow"
  python3 boutique.py prix WS01-XS-Yellow 20.40
  python3 boutique.py restaurer-prix
  python3 boutique.py commandes --statut canceled --limite 5 [--client "Lily Potter"]
  python3 boutique.py rapport orders --du 02/01/2023 --au 02/28/2023   (orders | refunded | tax | bestsellers)
"""
import argparse, json, os, re, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
SORTIE = os.path.join(RACINE, "donnees", "agents-nova")
BOUTIQUE = os.environ.get("BOUTIQUE_URL", "http://127.0.0.1:7780")
# identifiants de test publics de WebArena (voir labs/phamphamh/boutique/README.md)
COMPTE = (os.environ.get("BOUTIQUE_USER", "admin"), os.environ.get("BOUTIQUE_PASS", "admin1234"))
AGENT = os.environ.get("AGENT_ID", "manuel")
RUN = os.environ.get("AGENT_RUN", "manuel")
RAPPORTS = {  # type → (chemin dans l'admin, libellé)
    "orders": ("reports/report_sales/sales/", "Ventes (Orders)"),
    "refunded": ("reports/report_sales/refunded/", "Remboursements (Refunds)"),
    "tax": ("reports/report_sales/tax/", "Taxes (Tax)"),
    "bestsellers": ("reports/report_sales/bestsellers/", "Meilleures ventes (Bestsellers)"),
}


def maintenant():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def euros(p):
    """24.0 → « 24,00 $ » (la boutique est en dollars)."""
    return f"{float(p):,.2f}".replace(",", " ").replace(".", ",") + " $"


# ---------- journal ----------

def numero_suivant():
    chemin = os.path.join(SORTIE, "journal.jsonl")
    if not os.path.exists(chemin):
        return 1
    n = 0
    for l in open(chemin):
        if f'"run": "{RUN}"' in l and '"type": "outil"' in l:
            n += 1
    return n + 1


def journal(etape, detail="", capture=None, **extra):
    os.makedirs(SORTIE, exist_ok=True)
    ligne = {"ts": maintenant(), "agent": AGENT, "run": RUN, "n": numero_suivant(), "type": "outil",
             "etape": etape, "detail": detail, "capture": capture, **extra}
    with open(os.path.join(SORTIE, "journal.jsonl"), "a") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def nom_capture():
    dossier = os.path.join(SORTIE, "captures", RUN)
    os.makedirs(dossier, exist_ok=True)
    n = len([f for f in os.listdir(dossier) if f.endswith(".jpg")]) + 1
    return f"{RUN}/{n:02d}.jpg"


# ---------- API REST ----------

_jeton = None


def jeton():
    global _jeton
    if not _jeton:
        _jeton = appel("POST", "integration/admin/token", {"username": COMPTE[0], "password": COMPTE[1]}, auth=False)
    return _jeton


def appel(methode, chemin, corps=None, params=None, auth=True, magasin=""):
    url = f"{BOUTIQUE}/rest/{magasin + '/' if magasin else ''}V1/{chemin}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method=methode, data=json.dumps(corps).encode() if corps is not None else None)
    req.add_header("Content-Type", "application/json")
    if auth:
        req.add_header("Authorization", f"Bearer {jeton()}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(json.dumps({"erreur": f"HTTP {e.code}", "detail": e.read().decode()[:300]}, ensure_ascii=False))
    except urllib.error.URLError as e:
        raise SystemExit(json.dumps({"erreur": "boutique injoignable", "detail": str(e.reason)}, ensure_ascii=False))


def criteres(groupes, tri=None, limite=None, champs=None):
    """groupes = [[(champ, valeur, condition), ...], ...] : ET entre groupes, OU dans un groupe."""
    p = {}
    for i, g in enumerate(groupes):
        for j, (champ, valeur, cond) in enumerate(g):
            base = f"searchCriteria[filterGroups][{i}][filters][{j}]"
            p[base + "[field]"], p[base + "[value]"], p[base + "[conditionType]"] = champ, valeur, cond
    if tri:
        p["searchCriteria[sortOrders][0][field]"], p["searchCriteria[sortOrders][0][direction]"] = tri
    p["searchCriteria[pageSize]"] = limite or 100
    if champs:
        p["fields"] = champs
    return p


# ---------- outils ----------

def chercher(mots):
    morceaux = [m for m in re.split(r"[\s\-]+", mots) if m]
    r = appel("GET", "products", params=criteres([[("name", f"%{m}%", "like")] for m in morceaux], limite=60,
                                                  champs="items[id,sku,name,price,type_id],total_count"))
    produits = [{"sku": p["sku"], "nom": p["name"], "prix": p.get("price"), "id": p["id"], "type": p.get("type_id")}
                for p in r.get("items") or []]
    journal("Cherche dans le catalogue", f"« {mots} » · {len(produits)} produit(s)")
    return {"total": r.get("total_count", len(produits)), "produits": produits}


def lire_produit(sku):
    return appel("GET", f"products/{urllib.parse.quote(sku, safe='')}")


def prix(sku, nouveau):
    nouveau = round(float(nouveau), 2)
    p = lire_produit(sku)
    ancien = float(p.get("price") or 0)
    chemin_origine = os.path.join(SORTIE, "prix-origine.json")
    origine = json.load(open(chemin_origine)) if os.path.exists(chemin_origine) else {}
    origine.setdefault(sku, ancien)  # on garde le tout premier prix connu, pour pouvoir tout restaurer
    os.makedirs(SORTIE, exist_ok=True)
    json.dump(origine, open(chemin_origine, "w"), ensure_ascii=False, indent=1)
    appel("PUT", f"products/{urllib.parse.quote(sku, safe='')}", {"product": {"sku": sku, "price": nouveau}}, magasin="all")
    verifie = float(lire_produit(sku).get("price") or 0)
    capture = capturer_fiche(p["id"], sku)
    journal("Change le prix", f"{sku} · {euros(ancien)} → {euros(verifie)}", capture=capture,
            sku=sku, ancien=ancien, nouveau=verifie)
    return {"sku": sku, "nom": p.get("name"), "ancien": ancien, "nouveau": verifie, "capture": capture}


def restaurer_prix():
    chemin = os.path.join(SORTIE, "prix-origine.json")
    origine = json.load(open(chemin)) if os.path.exists(chemin) else {}
    for sku, p in origine.items():
        appel("PUT", f"products/{urllib.parse.quote(sku, safe='')}", {"product": {"sku": sku, "price": p}}, magasin="all")
    if origine:
        os.remove(chemin)
    journal("Restaure les prix d'origine", f"{len(origine)} produit(s)")
    return {"restaures": origine}


def commandes(statut=None, client=None, limite=10):
    groupes = []
    if statut:
        groupes.append([("status", statut, "eq")])
    for mot in (client or "").split():
        groupes.append([("customer_firstname", f"%{mot}%", "like"), ("customer_lastname", f"%{mot}%", "like")])
    r = appel("GET", "orders", params=criteres(groupes, tri=("created_at", "DESC"), limite=limite,
              champs="items[increment_id,created_at,customer_firstname,customer_lastname,customer_email,status,"
                     "grand_total,items[sku,product_type,qty_ordered,parent_item_id]],total_count"))
    liste = []
    for c in r.get("items") or []:
        # une variante achetée apparaît deux fois (le configurable et le simple) : on ne garde que les lignes « parent »
        skus = [f"{a['sku']} ×{int(a.get('qty_ordered') or 1)}" for a in c.get("items", []) if not a.get("parent_item_id")]
        liste.append({"numero": c["increment_id"], "date": c["created_at"],
                      "client": f"{c.get('customer_firstname') or ''} {c.get('customer_lastname') or ''}".strip(),
                      "email": c.get("customer_email"), "statut": c["status"], "total": c.get("grand_total"), "skus": skus})
    filtre = " · ".join(x for x in [f"statut {statut}" if statut else "", f"client « {client} »" if client else ""] if x)
    journal("Consulte les commandes", f"{filtre or 'toutes'} · {r.get('total_count', len(liste))} trouvée(s), "
            f"{len(liste)} lue(s)" + (f" · la plus récente : n° {liste[0]['numero']} ({liste[0]['client']})" if liste else ""))
    return {"total": r.get("total_count"), "commandes": liste}


# ---------- Playwright : rapports et captures ----------

def navigateur(p):
    nav = p.chromium.launch(headless=True)
    etat = os.path.join(SORTIE, "session-admin.json")
    ctx = nav.new_context(viewport={"width": 1400, "height": 850},
                          storage_state=etat if os.path.exists(etat) else None)
    page = ctx.new_page()
    return nav, ctx, page, etat


def ouvrir(page, ctx, etat, chemin):
    """Ouvre une page de l'admin ; se connecte si la session a expiré."""
    page.goto(f"{BOUTIQUE}/admin/{chemin}", timeout=120000, wait_until="domcontentloaded")
    if page.locator("#username").count():
        page.fill("#username", COMPTE[0]); page.fill("#login", COMPTE[1])
        page.click(".action-login"); page.wait_for_load_state("domcontentloaded", timeout=120000)
        ctx.storage_state(path=etat)
        if chemin not in page.url:
            page.goto(f"{BOUTIQUE}/admin/{chemin}", timeout=120000, wait_until="domcontentloaded")


def capturer_fiche(produit_id, sku):
    from playwright.sync_api import sync_playwright
    nom = nom_capture()
    try:
        with sync_playwright() as p:
            nav, ctx, page, etat = navigateur(p)
            try:
                ouvrir(page, ctx, etat, f"catalog/product/edit/id/{produit_id}/")
                champ = page.locator("input[name='product[price]']")
                champ.wait_for(state="visible", timeout=60000)
                page.wait_for_timeout(600)
                champ.scroll_into_view_if_needed()
                page.evaluate("window.scrollBy(0, -250)")
                page.screenshot(path=os.path.join(SORTIE, "captures", nom), type="jpeg", quality=70)
            finally:
                nav.close()
        return nom
    except Exception as e:  # la capture est un bonus : le prix est déjà changé et vérifié par l'API
        print(f"capture impossible : {str(e).splitlines()[0][:120]}", file=sys.stderr)
        return None


def rapport(type_, du, au, periode="month"):
    from playwright.sync_api import sync_playwright
    chemin, libelle = RAPPORTS[type_]
    nom = nom_capture()
    with sync_playwright() as p:
        nav, ctx, page, etat = navigateur(p)
        try:
            ouvrir(page, ctx, etat, chemin)
            page.wait_for_selector("#sales_report_from", timeout=60000)
            page.fill("#sales_report_from", du); page.fill("#sales_report_to", au)
            page.select_option("#sales_report_period_type", periode)
            page.click("#filter_form_submit"); page.wait_for_load_state("networkidle", timeout=120000)
            grille = page.locator("table.data-grid").first
            entetes = [t.strip() for t in grille.locator("thead th").all_inner_texts()]
            pied = grille.locator("tfoot tr").first
            totaux = dict(zip(entetes, [t.strip() for t in pied.locator("th, td").all_inner_texts()])) if pied.count() else {}
            lignes = []
            for tr in grille.locator("tbody tr").all()[:12]:
                cellules = [t.strip() for t in tr.locator("td").all_inner_texts()]
                if len(cellules) > 1:
                    lignes.append(dict(zip(entetes, cellules)))
            grille.scroll_into_view_if_needed()
            page.screenshot(path=os.path.join(SORTIE, "captures", nom), type="jpeg", quality=70)
        finally:
            nav.close()
    resume = ", ".join(f"{k} {v}" for k, v in totaux.items()
                       if k not in ("Interval", "Period") and v and v not in ("0", "$0.00"))[:160]
    journal("Génère le rapport", f"{libelle} du {du} au {au} · {resume or ('aucune donnée sur la période' if not lignes else str(len(lignes)) + ' ligne(s)')}", capture=nom,
            totaux=totaux)
    return {"rapport": type_, "du": du, "au": au, "totaux": totaux, "lignes": lignes, "capture": nom}


if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Outils de l'agent dans le back-office Magento d'Atelier Nova")
    s = a.add_subparsers(dest="cmd", required=True)
    s.add_parser("chercher").add_argument("mots")
    sp = s.add_parser("prix"); sp.add_argument("sku"); sp.add_argument("nouveau_prix", type=float)
    s.add_parser("restaurer-prix")
    sc = s.add_parser("commandes"); sc.add_argument("--statut"); sc.add_argument("--client")
    sc.add_argument("--limite", type=int, default=10)
    sr = s.add_parser("rapport"); sr.add_argument("type", choices=list(RAPPORTS))
    sr.add_argument("--du", required=True); sr.add_argument("--au", required=True)
    sr.add_argument("--periode", default="month", choices=["day", "month", "year"])
    r = a.parse_args()
    if r.cmd == "chercher":
        out = chercher(r.mots)
    elif r.cmd == "prix":
        out = prix(r.sku, r.nouveau_prix)
    elif r.cmd == "restaurer-prix":
        out = restaurer_prix()
    elif r.cmd == "commandes":
        out = commandes(r.statut, r.client, r.limite)
    else:
        out = rapport(r.type, r.du, r.au, r.periode)
    print(json.dumps(out, ensure_ascii=False))

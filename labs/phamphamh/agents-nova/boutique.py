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
from contextlib import contextmanager
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
    "orders": ("reports/report_sales/sales/", "Orders report"),
    "refunded": ("reports/report_sales/refunded/", "Refunds report"),
    "tax": ("reports/report_sales/tax/", "Tax report"),
    "bestsellers": ("reports/report_sales/bestsellers/", "Bestsellers report"),
}


def maintenant():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def euros(p):
    """24.0 → « $24.00 » (la boutique est en dollars ; journal en anglais pour le jury)."""
    return f"${float(p):,.2f}"


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
    journal("Searches the catalog", f"“{mots}” · {len(produits)} product(s)")
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
    if CDP or VISIBLE:
        capture = prix_par_admin(p["id"], sku, nouveau)
    else:
        appel("PUT", f"products/{urllib.parse.quote(sku, safe='')}", {"product": {"sku": sku, "price": nouveau}},
              magasin="all")
    verifie = float(lire_produit(sku).get("price") or 0)
    if not (CDP or VISIBLE):
        capture = capturer_fiche(p["id"], sku)
    journal("Changes the price", f"{sku} · {euros(ancien)} → {euros(verifie)}", capture=capture,
            sku=sku, ancien=ancien, nouveau=verifie)
    return {"sku": sku, "nom": p.get("name"), "ancien": ancien, "nouveau": verifie, "capture": capture}


def restaurer_prix():
    chemin = os.path.join(SORTIE, "prix-origine.json")
    origine = json.load(open(chemin)) if os.path.exists(chemin) else {}
    for sku, p in origine.items():
        appel("PUT", f"products/{urllib.parse.quote(sku, safe='')}", {"product": {"sku": sku, "price": p}}, magasin="all")
    if origine:
        os.remove(chemin)
    journal("Restores original prices", f"{len(origine)} product(s)")
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
    capture = montrer_commandes(statut, client) if (CDP or VISIBLE) else None
    filtre = " · ".join(x for x in [f"statut {statut}" if statut else "", f"client « {client} »" if client else ""] if x)
    journal("Consulte les commandes", f"{filtre or 'toutes'} · {r.get('total_count', len(liste))} trouvée(s), "
            f"{len(liste)} lue(s)" + (f" · la plus récente : n° {liste[0]['numero']} ({liste[0]['client']})" if liste else ""),
            capture=capture)
    return {"total": r.get("total_count"), "commandes": liste}


# ---------- Playwright : rapports, captures et mode visible ----------
# Mode visible (démo en direct) : BOUTIQUE_VISIBLE=1. Les actions passent par l'interface d'admin dans une fenêtre
# Chromium qu'on voit, au ralenti, avec un bandeau et un curseur. Pendant un passage, agents_ia.py ouvre UNE fenêtre
# et donne son adresse dans BOUTIQUE_CDP : chaque appel de l'outil s'y reconnecte au lieu d'en ouvrir une autre.
VISIBLE = os.environ.get("BOUTIQUE_VISIBLE") == "1"
CDP = os.environ.get("BOUTIQUE_CDP")
BANDEAU = os.environ.get("AGENT_BANDEAU", f"Agent DeloAI · {AGENT}")
RALENTI_MS = 700   # chaque geste se voit
FRAPPE_MS = 80     # frappe caractère par caractère
PAUSE_PAGE_MS = 1000
HABILLAGE = """(texte => { const f = () => {
  if (document.getElementById('deloai-bandeau')) return;
  const b = document.createElement('div'); b.id = 'deloai-bandeau'; b.textContent = texte;
  b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:2147483647;background:#0f172a;color:#fff;'
    + 'font:600 14px -apple-system,Helvetica,sans-serif;padding:9px 16px;box-shadow:0 2px 10px rgba(0,0,0,.35);'
    + 'pointer-events:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-bottom:3px solid #f97316';
  document.body.appendChild(b);
  const c = document.createElement('div'); c.id = 'deloai-curseur';
  c.style.cssText = 'position:fixed;z-index:2147483647;width:22px;height:22px;border-radius:50%;left:-60px;top:-60px;'
    + 'background:rgba(249,115,22,.45);border:2px solid #f97316;pointer-events:none;transform:translate(-50%,-50%);'
    + 'transition:left .12s,top .12s,transform .1s';
  document.body.appendChild(c);
  addEventListener('mousemove', e => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; }, true);
  addEventListener('mousedown', () => c.style.transform = 'translate(-50%,-50%) scale(1.7)', true);
  addEventListener('mouseup', () => c.style.transform = 'translate(-50%,-50%)', true);
}; document.body ? f() : addEventListener('DOMContentLoaded', f); })"""


def montre():
    return bool(CDP or VISIBLE)


def cliquer(page, cible):
    """Clic ; en mode visible, l'élément s'entoure d'un contour cyan juste avant."""
    if montre():
        try:
            cible.scroll_into_view_if_needed(timeout=5000)
            cible.evaluate("el => { el.style.outline = '3px solid #06b6d4'; el.style.outlineOffset = '2px'; }")
            page.wait_for_timeout(450)
        except Exception:
            pass
    cible.click()


def saisir(page, cible, texte):
    if montre():
        cliquer(page, cible)
        cible.fill("")
        cible.type(texte, delay=FRAPPE_MS)
    else:
        cible.fill(texte)


def habiller(ctx, page):
    """Bandeau « Agent DeloAI · … » et curseur visible, sur la page actuelle et les suivantes."""
    script = f"{HABILLAGE}({json.dumps(BANDEAU)})"
    ctx.add_init_script(script)
    try:
        page.evaluate(script)
    except Exception:
        pass


@contextmanager
def admin():
    """(page, ctx, etat) : fenêtre partagée du passage, fenêtre visible seule, ou navigateur invisible."""
    from playwright.sync_api import sync_playwright
    etat = os.path.join(SORTIE, "session-admin.json")
    with sync_playwright() as p:
        if CDP:
            nav = p.chromium.connect_over_cdp(CDP, slow_mo=RALENTI_MS)
            ctx = nav.contexts[0]
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
        elif VISIBLE:
            nav = p.chromium.launch(headless=False, slow_mo=RALENTI_MS,
                                    args=["--window-position=0,0", "--window-size=1280,800"])
            ctx = nav.new_context(no_viewport=True, storage_state=etat if os.path.exists(etat) else None)
            page = ctx.new_page()
        else:
            nav = p.chromium.launch(headless=True)
            ctx = nav.new_context(viewport={"width": 1400, "height": 850},
                                  storage_state=etat if os.path.exists(etat) else None)
            page = ctx.new_page()
        if CDP or VISIBLE:
            habiller(ctx, page)
        try:
            yield page, ctx, etat
        finally:
            if not CDP:  # la fenêtre partagée reste ouverte : agents_ia.py la ferme à la fin du passage
                nav.close()


def ouvrir(page, ctx, etat, chemin):
    """Ouvre une page de l'admin ; se connecte si la session a expiré."""
    page.goto(f"{BOUTIQUE}/admin/{chemin}", timeout=120000, wait_until="domcontentloaded")
    if page.locator("#username").count():
        page.fill("#username", COMPTE[0]); page.fill("#login", COMPTE[1])
        page.click(".action-login"); page.wait_for_load_state("domcontentloaded", timeout=120000)
        try:
            ctx.storage_state(path=etat)
        except Exception:
            pass
        if chemin not in page.url:
            page.goto(f"{BOUTIQUE}/admin/{chemin}", timeout=120000, wait_until="domcontentloaded")
    if montre():
        page.wait_for_timeout(PAUSE_PAGE_MS)


def accueil():
    """Début d'un passage visible : la fenêtre se connecte et montre le tableau de bord."""
    with admin() as (page, ctx, etat):
        ouvrir(page, ctx, etat, "dashboard/")
        page.wait_for_timeout(800)
    journal("Opens the admin panel", BOUTIQUE.replace("http://", "") + "/admin")
    return {"ok": True}


def montrer_prix(page, produit_id):
    champ = page.locator("input[name='product[price]']")
    champ.wait_for(state="visible", timeout=60000)
    page.wait_for_timeout(500)
    champ.scroll_into_view_if_needed()
    page.evaluate("window.scrollBy(0, -250)")
    return champ


def capturer_fiche(produit_id, sku):
    nom = nom_capture()
    try:
        with admin() as (page, ctx, etat):
            ouvrir(page, ctx, etat, f"catalog/product/edit/id/{produit_id}/")
            montrer_prix(page, produit_id)
            page.screenshot(path=os.path.join(SORTIE, "captures", nom), type="jpeg", quality=70)
        return nom
    except Exception as e:  # la capture est un bonus : le prix est déjà changé et vérifié par l'API
        print(f"capture impossible : {str(e).splitlines()[0][:120]}", file=sys.stderr)
        return None


def prix_par_admin(produit_id, sku, nouveau):
    """Mode visible : Catalog › Products › recherche du SKU › fiche › champ Prix › Save, comme un salarié."""
    nom = nom_capture()
    with admin() as (page, ctx, etat):
        try:
            ouvrir(page, ctx, etat, "catalog/product/")
            recherche = page.locator("#fulltext").first
            recherche.wait_for(state="visible", timeout=30000)
            saisir(page, recherche, sku); recherche.press("Enter")
            ligne = page.locator("tr.data-row", has_text=sku).first
            ligne.wait_for(state="visible", timeout=30000)
            page.wait_for_timeout(PAUSE_PAGE_MS)
            cliquer(page, ligne.locator("a", has_text="Edit").first)
            page.wait_for_url("**/catalog/product/edit/**", timeout=60000)
        except Exception:  # la grille n'a pas coopéré : on ouvre la fiche directement
            ouvrir(page, ctx, etat, f"catalog/product/edit/id/{produit_id}/")
        champ = montrer_prix(page, produit_id)
        page.wait_for_timeout(PAUSE_PAGE_MS)
        saisir(page, champ, f"{nouveau:.2f}")
        page.wait_for_timeout(400)
        cliquer(page, page.locator("#save-button"))
        page.locator(".message-success", has_text="You saved the product").first.wait_for(timeout=120000)
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(SORTIE, "captures", nom), type="jpeg", quality=70)
        montrer_prix(page, produit_id)
        page.wait_for_timeout(1200)
    return nom


def montrer_commandes(statut, client):
    """Mode visible : Sales › Orders, filtre par statut (et recherche du client) ; les données viennent de l'API."""
    nom = nom_capture()
    try:
        with admin() as (page, ctx, etat):
            ouvrir(page, ctx, etat, "sales/order/")
            page.locator("tr.data-row").first.wait_for(state="visible", timeout=60000)
            vider = page.locator("button[data-action='grid-filter-reset']").first
            if vider.count() and vider.is_visible():
                cliquer(page, vider); page.wait_for_timeout(1500)
            if statut:
                cliquer(page, page.locator("button[data-action='grid-filter-expand']").first)
                choix = page.locator("select[name='status']").first
                cliquer(page, choix); choix.select_option(statut)
                cliquer(page, page.locator("button[data-action='grid-filter-apply']").first)
                page.wait_for_timeout(2000)
            if client:
                recherche = page.locator("#fulltext").first
                saisir(page, recherche, client); recherche.press("Enter")
                page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(SORTIE, "captures", nom), type="jpeg", quality=70)
        return nom
    except Exception as e:
        print(f"affichage des commandes impossible : {str(e).splitlines()[0][:120]}", file=sys.stderr)
        return None


def rapport(type_, du, au, periode=None):
    # meilleures ventes : un classement par année se lit mieux qu'un classement par mois
    periode = periode or ("year" if type_ == "bestsellers" else "month")
    chemin, libelle = RAPPORTS[type_]
    nom = nom_capture()
    with admin() as (page, ctx, etat):
        if True:
            ouvrir(page, ctx, etat, chemin)
            page.wait_for_selector("#sales_report_from", timeout=60000)
            if montre():
                cliquer(page, page.locator("#sales_report_period_type"))
            page.select_option("#sales_report_period_type", periode)
            saisir(page, page.locator("#sales_report_from"), du); saisir(page, page.locator("#sales_report_to"), au)
            cliquer(page, page.locator("#filter_form_submit")); page.wait_for_load_state("networkidle", timeout=120000)
            if montre():
                page.wait_for_timeout(PAUSE_PAGE_MS)
            grille = page.locator("table.data-grid").first
            entetes = [t.strip() for t in grille.locator("thead th").all_inner_texts()]
            pied = grille.locator("tfoot tr").first
            totaux = dict(zip(entetes, [t.strip() for t in pied.locator("th, td").all_inner_texts()])) if pied.count() else {}
            lignes = []
            for tr in grille.locator("tbody tr").all()[:20]:
                cellules = [t.strip() for t in tr.locator("td").all_inner_texts()]
                if len(cellules) == len(entetes) - 1 and lignes:  # cellule « période » fusionnée (rowspan)
                    cellules = [lignes[-1][entetes[0]]] + cellules
                if len(cellules) > 1:
                    lignes.append(dict(zip(entetes, cellules)))
            grille.scroll_into_view_if_needed()
            page.screenshot(path=os.path.join(SORTIE, "captures", nom), type="jpeg", quality=70)
            if CDP or VISIBLE:
                page.wait_for_timeout(1500)
    resume = ", ".join(f"{k} {v}" for k, v in totaux.items()
                       if k not in ("Interval", "Period") and v and v not in ("0", "$0.00"))[:160]
    journal(f"Opens the {libelle}", f"{du} → {au} · {resume or ('no data for this period' if not lignes else str(len(lignes)) + ' row(s)')}", capture=nom,
            totaux=totaux)
    return {"rapport": type_, "du": du, "au": au, "totaux": totaux, "lignes": lignes, "capture": nom}


if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Outils de l'agent dans le back-office Magento d'Atelier Nova")
    s = a.add_subparsers(dest="cmd", required=True)
    s.add_parser("chercher").add_argument("mots")
    sp = s.add_parser("prix"); sp.add_argument("sku"); sp.add_argument("nouveau_prix", type=float)
    s.add_parser("restaurer-prix")
    s.add_parser("accueil")
    sc = s.add_parser("commandes"); sc.add_argument("--statut"); sc.add_argument("--client")
    sc.add_argument("--limite", type=int, default=10)
    sr = s.add_parser("rapport"); sr.add_argument("type", choices=list(RAPPORTS))
    sr.add_argument("--du", required=True); sr.add_argument("--au", required=True)
    sr.add_argument("--periode", choices=["day", "month", "year"])
    r = a.parse_args()
    if r.cmd == "chercher":
        out = chercher(r.mots)
    elif r.cmd == "prix":
        out = prix(r.sku, r.nouveau_prix)
    elif r.cmd == "accueil":
        out = accueil()
    elif r.cmd == "restaurer-prix":
        out = restaurer_prix()
    elif r.cmd == "commandes":
        out = commandes(r.statut, r.client, r.limite)
    else:
        out = rapport(r.type, r.du, r.au, r.periode)
    print(json.dumps(out, ensure_ascii=False))

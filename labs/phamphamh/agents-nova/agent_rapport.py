#!/usr/bin/env python3
"""L'agent « Rapport de ventes » d'Atelier Nova : refait dans le vrai back-office Magento les étapes observées chez les salariés.

Étapes apprises (tâche t2 de la fusion d'adamaass, 6 personnes, 79 fois / semaine) : ouvrir Reports > Orders,
saisir la période, lancer le rapport, lire les totaux. L'agent les rejoue, trace chaque action dans le journal
(donnees/agents-nova/journal.jsonl), fait une capture par étape, exporte le CSV et écrit le résultat.

Usage : python3 agent_rapport.py [--debut 02/01/2023 --fin 02/28/2023]
Il faut la boutique de test (labs/phamphamh/boutique/) sur http://localhost:7780 et Playwright.
"""
import argparse, csv, json, os, re, time, uuid
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
SORTIE = os.path.join(RACINE, "donnees", "agents-nova")
BOUTIQUE = os.environ.get("BOUTIQUE_URL", "http://localhost:7780")
# identifiants de test publics de WebArena (voir labs/phamphamh/boutique/README.md)
COMPTE = (os.environ.get("BOUTIQUE_USER", "admin"), os.environ.get("BOUTIQUE_PASS", "admin1234"))
AGENT = "rapport-ventes"


def maintenant():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class Journal:
    def __init__(self, run, page):
        self.run, self.page, self.n, self.t0 = run, page, 0, time.time()
        os.makedirs(os.path.join(SORTIE, "captures", run), exist_ok=True)

    def ecrire(self, etape, detail="", capture=True, **extra):
        self.n += 1
        nom = None
        if capture:
            nom = f"{self.run}/{self.n:02d}.jpg"
            self.page.screenshot(path=os.path.join(SORTIE, "captures", nom), type="jpeg", quality=70)
        ligne = {"ts": maintenant(), "agent": AGENT, "run": self.run, "n": self.n, "etape": etape, "detail": detail,
                 "t": round(time.time() - self.t0, 2), "capture": nom, **extra}
        with open(os.path.join(SORTIE, "journal.jsonl"), "a") as f:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
        print(f"[{ligne['t']:6.2f}s] {etape} {detail}")


def lancer(debut, fin, visible=False):
    run = datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
    os.makedirs(SORTIE, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=not visible)
        ctx = nav.new_context(viewport={"width": 1400, "height": 850}, accept_downloads=True)
        page = ctx.new_page()
        j = Journal(run, page)
        try:
            page.goto(f"{BOUTIQUE}/admin", timeout=120000)
            j.ecrire("Ouvre le back-office", BOUTIQUE.replace("http://", "") + "/admin")
            page.fill("#username", COMPTE[0]); page.fill("#login", COMPTE[1])
            page.click(".action-login"); page.wait_for_load_state("networkidle", timeout=120000)
            j.ecrire("Se connecte", "compte de service de l'agent")

            page.click("#menu-magento-reports-report"); page.wait_for_timeout(400)
            j.ecrire("Ouvre le menu Reports", "étape observée chez les 6 salariés")
            page.locator("#menu-magento-reports-report a").filter(has_text=re.compile(r"^\s*Orders\s*$")).first.click()
            page.wait_for_load_state("networkidle", timeout=120000)
            j.ecrire("Ouvre le rapport Orders", "Reports › Sales › Orders")

            page.fill("#sales_report_from", debut); page.fill("#sales_report_to", fin)
            page.select_option("#sales_report_period_type", "day")
            j.ecrire("Saisit la période", f"du {debut} au {fin}, par jour")

            page.click("#filter_form_submit"); page.wait_for_load_state("networkidle", timeout=120000)
            j.ecrire("Lance le rapport", "Show Report")

            page.locator("table.data-grid").first.scroll_into_view_if_needed()
            totaux = lire_totaux(page)
            j.ecrire("Lit les totaux", f"{totaux.get('commandes', '?')} commandes · {totaux.get('ventes', '?')} de ventes", totaux=totaux)

            csv_nom = None
            try:
                page.select_option("select[id$='_export']", label="CSV")
                with page.expect_download(timeout=60000) as dl:
                    page.click("button[title='Export']")
                csv_nom = f"rapport-ventes-{run}.csv"
                os.makedirs(os.path.join(SORTIE, "rapports"), exist_ok=True)
                dl.value.save_as(os.path.join(SORTIE, "rapports", csv_nom))
                j.ecrire("Exporte le rapport", csv_nom, capture=False)
            except Exception as e:  # l'export est un bonus : le rapport est déjà lu
                j.ecrire("Export CSV impossible", str(e)[:120], capture=False)

            resultat = {"run": run, "agent": AGENT, "statut": "ok", "debut": debut, "fin": fin, "totaux": totaux,
                        "csv": csv_nom, "duree_s": round(time.time() - j.t0, 1), "actions": j.n, "fini": maintenant()}
        except Exception as e:
            j.ecrire("Échec", str(e).splitlines()[0][:160])
            resultat = {"run": run, "agent": AGENT, "statut": "echec", "erreur": str(e).splitlines()[0][:300],
                        "duree_s": round(time.time() - j.t0, 1), "actions": j.n, "fini": maintenant()}
        finally:
            nav.close()
    with open(os.path.join(SORTIE, "runs.jsonl"), "a") as f:
        f.write(json.dumps(resultat, ensure_ascii=False) + "\n")
    return resultat


def lire_totaux(page):
    """Ligne « Total » du tableau : nombre de commandes et ventes totales."""
    pied = page.locator("table.data-grid tfoot tr").first
    entetes = [t.strip() for t in page.locator("table.data-grid thead th").all_inner_texts()]
    valeurs = [t.strip() for t in pied.locator("th, td").all_inner_texts()] if pied.count() else []
    brut = dict(zip(entetes, valeurs))
    trouve = lambda motif: next((v for k, v in brut.items() if re.search(motif, k, re.I)), None)
    return {"commandes": trouve(r"^Orders$"), "ventes": trouve(r"Sales Total"), "articles": trouve(r"Sales Items"),
            "facture": trouve(r"Invoiced"), "colonnes": brut}


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--debut", default="02/01/2023"); a.add_argument("--fin", default="02/28/2023")
    a.add_argument("--visible", action="store_true")
    r = a.parse_args()
    print(json.dumps(lancer(r.debut, r.fin, r.visible), ensure_ascii=False, indent=1))

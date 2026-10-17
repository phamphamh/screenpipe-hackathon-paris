// ====================== helpers ======================
const $ = (sel, root) => (root || document).querySelector(sel);
const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
const euro = (v) => v.toLocaleString("fr-FR") + "  €".replace(" ", " ");
const fmtEur = (v) => v.toLocaleString("fr-FR") + " €";

function svgEl(tag, attrs) {
  const e = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  return e;
}
function textEl(x, y, str, cls, extra) {
  const t = svgEl("text", Object.assign({ x, y, class: cls }, extra || {}));
  t.textContent = str;
  return t;
}

const tooltipEl = document.getElementById("tooltip");
function showTooltip(x, y, html) {
  tooltipEl.innerHTML = html;
  tooltipEl.style.left = x + "px";
  tooltipEl.style.top = (y - 10) + "px";
  tooltipEl.classList.add("show");
}
function hideTooltip() { tooltipEl.classList.remove("show"); }

let toastTimer = null;
function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2400);
}

const CAT_CLASS = {
  "Ressaisie": "tag-ressaisie",
  "Attente d'info": "tag-attente",
  "Répétition": "tag-repetition",
  "Hors outil": "tag-horsoutil",
  "Goulot": "tag-goulot",
  "Recherche": "tag-recherche",
};
const STATUS_CLASS = { "À valider": "", "Validé": "status-validated", "En automatisation": "status-automating" };
const REQ_STATUS_CLASS = { "En étude": "rs-etude", "Planifié · S11": "rs-planifie", "Reçu": "rs-recu", "Livré": "rs-livre" };

// ====================== routes / sidebar ======================
const ROUTES = [
  { path: "overview", label: "Vue d'ensemble", icon: "▦", group: "study" },
  { path: "problems", label: "Problèmes détectés", icon: "⚠", group: "study", badge: () => DATA.problemsMeta.total },
  { path: "interactions", label: "Interactions & goulots", icon: "⇄", group: "study" },
  { path: "tools", label: "Temps & outils", icon: "◴", group: "study" },
  { path: "business", label: "Business case", icon: "€", group: "study" },
  { path: "piloting", label: "Pilotage continu", icon: "⌁", group: "after", extra: "après J+10" },
];

function overviewBadge(route) {
  // The overview snapshot (day 3) predates the final problem count seen on every other page.
  if (route === "overview") return DATA.overview.stats[3].value;
  return String(DATA.problemsMeta.total);
}

function renderSidebar(route) {
  const onPiloting = route === "piloting";
  const studyItems = ROUTES.filter(r => r.group === "study");
  const nav = (r) => {
    const active = r.path === route;
    const disabled = onPiloting; // archived once piloting is active
    let badge = "";
    if (r.path === "problems" && !onPiloting) badge = `<span class="badge">${overviewBadge(route)}</span>`;
    return `<div class="nav-item ${active ? "active" : ""} ${disabled && !active ? "disabled" : ""}" data-route="${r.path}">
      <span class="nb"><span class="icon">${r.icon}</span>${r.label}</span>${badge}
    </div>`;
  };
  const pilotingItem = `<div class="nav-item ${route === "piloting" ? "active" : ""}" data-route="piloting">
      <span class="nb"><span class="icon">⌁</span>Pilotage continu</span>
    </div>`;
  const studyGroup = `<div class="nav-group-label">${onPiloting ? "Archives de l'étude" : "L'étude"}</div>${studyItems.map(nav).join("")}`;
  const afterGroup = `<div class="nav-group-label">Après l'étude</div>${pilotingItem}`;
  return `
    <div class="sidebar-brand">
      <div class="mark">${DATA.firm[0]}</div>
      <div class="name">${DATA.firm}</div>
    </div>
    <div class="sidebar-client">
      <div class="k">Client</div>
      <div class="name">${DATA.client.name}</div>
      <div class="sub">${DATA.client.postes} postes · ${DATA.client.equipes} équipes</div>
      ${onPiloting ? `<div class="badge-active">Abonnement actif</div>` : ""}
    </div>
    ${onPiloting ? afterGroup + studyGroup : studyGroup + afterGroup}
    <div class="sidebar-spacer"></div>
    <div class="sidebar-footer">
      ${onPiloting ? `
        <div class="sidebar-footer-card">
          <div style="font-weight:650; margin-bottom:4px;">Abonnement</div>
          <div style="font-size:13px; font-weight:650;">[VOTRE PRIX] / mois</div>
          <div style="color:var(--text-muted); margin-bottom:6px;">Prochaine facture le 1er décembre</div>
          <a href="#" id="manage-sub">Gérer l'abonnement</a>
        </div>
      ` : `
        <div class="sidebar-footer-card">
          <div class="ok">Collecte conforme</div>
          <div class="consultant">Votre consultant : ${DATA.consultant}</div>
          <a href="#" id="write-consultant">Écrire au consultant</a>
        </div>
      `}
    </div>`;
}

function renderTopbar(route) {
  const tag = route === "piloting" ? "Logiciel sur mesure" : DATA.studyLabel;
  return `<span class="study-label">${tag}</span><span class="pill-tag">${DATA.demoTag}</span>`;
}

// ====================== shared mini components ======================
function statTile(s) {
  return `<div class="card stat-tile">
    <div class="label">${s.label}</div>
    <div class="value ${s.accent === "good" ? "good" : ""}">${s.value}</div>
    ${s.sub ? `<div class="sub">${s.sub}</div>` : ""}
    ${typeof s.progress === "number" ? `<div class="mini-progress"><div class="mini-progress-track"><div class="mini-progress-fill" style="width:${Math.min(100, s.progress * 100)}%"></div></div></div>` : ""}
  </div>`;
}
function statRow(stats, cols) {
  return `<div class="grid grid-${cols}">${stats.map(statTile).join("")}</div>`;
}

// ====================== PAGE: overview ======================
function viewOverview() {
  const o = DATA.overview;
  const maxH = Math.max(...o.dailyHours.filter(d => d.known).map(d => d.value)) * 1.15;
  return `
    <div class="view-head">
      <div>
        <h1>Vue d'ensemble</h1>
        <p class="desc">${o.dayLabel}</p>
      </div>
      <div class="view-head-actions">
        <button class="btn" id="btn-validate">Valider les constats</button>
        <button class="btn btn-primary" id="btn-share">Partager le point d'étape</button>
      </div>
    </div>

    <div class="card" style="margin-bottom:14px;">
      <div class="card-head">
        <h2>Avancement de l'étude</h2>
        <div style="font-size:12.5px; color:var(--text-muted);">Avancement global <b style="color:var(--text-primary)">${DATA.advancementPct} %</b></div>
      </div>
      <div class="stepper">
        ${DATA.steps.map(s => `
          <div class="step ${s.status}">
            <div class="step-bar ${s.status}"></div>
            <div class="num">${s.status === "done" ? "✓" : s.n}</div>
            <div class="label">${s.label}</div>
            <div class="date">${s.date}</div>
            <div class="status">${s.sub}</div>
          </div>`).join("")}
      </div>
    </div>

    ${statRow(o.stats, 4)}

    <div class="grid grid-2">
      <div class="card">
        <h2>Collecte en direct</h2>
        <p class="sub">Heures observées par jour, tous postes</p>
        <div class="chart-wrap"><svg id="daily-chart"></svg></div>
        <h2 style="margin-top:18px;">Couverture par équipe</h2>
        <div style="margin-top:10px;">
          ${o.teamCoverage.map(t => {
            const pct = (t.have / t.total) * 100;
            const complete = t.have === t.total;
            return `<div class="coverage-row">
              <div class="team">${t.team}</div>
              <div class="mini-progress-track"><div class="mini-progress-fill ${complete ? "good" : ""}" style="width:${pct}%"></div></div>
              <div class="status ${complete ? "" : "warn"}">${t.have}/${t.total} ${complete ? "Complet" : "1 à relancer"}</div>
            </div>`;
          }).join("")}
        </div>
      </div>
      <div class="card">
        <div class="card-head"><h2>Premiers signaux</h2><div class="sub">mis à jour ${o.signalsUpdated}</div></div>
        <p class="sub">Constats provisoires : ils se confirment ou s'écartent d'ici la fin de l'observation.</p>
        ${o.signals.map(s => `
          <div class="signal-card">
            <div class="top-row"><span class="tag ${CAT_CLASS[s.tag]}">${s.tag}</span><span class="path-tag">${s.path}</span></div>
            <p class="text">${s.text}</p>
            <div class="meta">${s.meta}</div>
            <div class="confidence ${s.confidence.includes("élevée") ? "high" : ""}">${s.confidence}</div>
          </div>`).join("")}
        <div style="margin-top:10px;"><a href="#/problems">Voir les ${o.stats[3].value} problèmes détectés →</a></div>
      </div>
    </div>

    <div class="grid grid-half">
      <div class="card">
        <h2>Postes à relancer</h2>
        ${o.toRelaunch.map(r => `
          <div class="relaunch-row" data-id="${r.id}">
            <div><div class="id">${r.id}</div><div class="txt">${r.text}</div></div>
            <button class="btn btn-sm relaunch-btn" data-id="${r.id}">Relancer</button>
          </div>`).join("")}
      </div>
      <div class="card">
        <h2>Conformité de la collecte</h2>
        ${o.compliance.map(c => `<div class="check-row">${c}</div>`).join("")}
        <a href="#" id="registre-link">Registre de traitement et note d'information (PDF)</a>
      </div>
    </div>

    <div class="card">
      <h2>Prochaines étapes</h2>
      ${o.nextSteps.map(s => `<div class="timeline-row"><div class="date">${s.date}</div><div>${s.text}</div></div>`).join("")}
    </div>
  `;
}

function afterRenderOverview() {
  const o = DATA.overview;
  const svg = document.getElementById("daily-chart");
  const wrap = svg.parentElement;
  const W = wrap.clientWidth || 500, H = 190;
  const margin = { top: 24, right: 10, bottom: 24, left: 10 };
  const innerW = W - margin.left - margin.right, innerH = H - margin.top - margin.bottom;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("width", W); svg.setAttribute("height", H);
  svg.innerHTML = "";
  const n = o.dailyHours.length;
  const bandW = innerW / n;
  const barW = Math.min(30, bandW * 0.5);
  const maxV = Math.max(...o.dailyHours.filter(d => d.known).map(d => d.value)) * 1.2;
  const g = svgEl("g", {});
  o.dailyHours.forEach((d, i) => {
    const cx = margin.left + bandW * (i + 0.5);
    if (d.known) {
      const barH = (d.value / maxV) * innerH;
      const y0 = margin.top + innerH - barH;
      const path = `M${cx - barW/2},${y0+barH} L${cx - barW/2},${y0+4} Q${cx - barW/2},${y0} ${cx - barW/2+4},${y0} L${cx + barW/2-4},${y0} Q${cx + barW/2},${y0} ${cx + barW/2},${y0+4} L${cx + barW/2},${y0+barH} Z`;
      g.appendChild(svgEl("path", { d: path, fill: "#3987e5", class: "bar-rect" }));
      g.appendChild(textEl(cx, y0 - 8, d.value + " h", "bar-value-label", { "text-anchor": "middle" }));
    } else {
      const y0 = margin.top + innerH - innerH * 0.18;
      const path = `M${cx - barW/2},${margin.top+innerH} L${cx - barW/2},${y0+4} Q${cx - barW/2},${y0} ${cx - barW/2+4},${y0} L${cx + barW/2-4},${y0} Q${cx + barW/2},${y0} ${cx + barW/2},${y0+4} L${cx + barW/2},${margin.top+innerH} Z`;
      g.appendChild(svgEl("path", { d: path, fill: "rgba(255,255,255,0.06)", stroke: "rgba(255,255,255,0.15)", "stroke-dasharray": "3,3" }));
      g.appendChild(textEl(cx, y0 - 8, "à venir", "axis-label", { "text-anchor": "middle" }));
    }
    g.appendChild(textEl(cx, H - 4, d.day, "axis-label", { "text-anchor": "middle" }));
  });
  svg.appendChild(g);

  $$(".relaunch-btn").forEach(btn => btn.addEventListener("click", () => {
    toast(`Relance envoyée à ${btn.dataset.id}.`);
    btn.closest(".relaunch-row").classList.add("done");
    btn.textContent = "Relancé"; btn.disabled = true;
  }));
  const vBtn = document.getElementById("btn-validate");
  if (vBtn) vBtn.addEventListener("click", () => toast("Constats marqués comme validés avec le consultant."));
  const sBtn = document.getElementById("btn-share");
  if (sBtn) sBtn.addEventListener("click", () => toast("Point d'étape partagé avec votre équipe."));
  const reg = document.getElementById("registre-link");
  if (reg) reg.addEventListener("click", (e) => { e.preventDefault(); toast("Registre de traitement (PDF) — démo, non disponible."); });
}

// ====================== PAGE: problems ======================
let problemFilter = "Tous";
let selectedProblemId = DATA.problems[0].id;
let showAllProblems = false;

function problemList() {
  let list = DATA.problems;
  if (problemFilter !== "Tous") list = list.filter(p => p.cat === problemFilter);
  return list;
}

function viewProblems() {
  const m = DATA.problemsMeta;
  const list = problemList();
  const shown = list;
  return `
    <div class="view-head">
      <div>
        <h1>Problèmes détectés</h1>
        <p class="desc">Chaque constat est mesuré sur vos postes, chiffré, puis soumis à votre validation avant d'entrer dans le rapport.</p>
      </div>
      <div class="view-head-actions"><button class="btn" id="export-csv">Exporter la liste (CSV)</button></div>
    </div>
    ${statRow([
      { label: "Problèmes", value: String(m.total) },
      { label: "Temps perdu par semaine", value: m.hoursPerWeek },
      { label: "Coût annuel estimé", value: fmtEur(m.annualCost) },
      { label: "Validés par vous", value: `${m.validated} / ${m.total}` },
    ], 4)}

    <div class="filter-row">
      ${m.categories.map(c => `<button class="chip ${c === problemFilter ? "active" : ""}" data-cat="${c}">${c}</button>`).join("")}
    </div>

    <div class="problems-split">
      <div>
        <div class="list-head"><span>${shown.length} problème(s) affiché(s) sur ${m.total}</span><span>Triés par coût annuel</span></div>
        <div class="problem-list" id="problem-list">
          ${shown.map((p, i) => problemCardHtml(p, i)).join("")}
        </div>
        ${problemFilter === "Tous" ? `<div style="margin-top:12px;"><a href="#" id="show-more">Afficher les ${DATA.extraProblemsCount} autres problèmes</a></div>` : ""}
      </div>
      <div class="detail-panel" id="detail-panel"></div>
    </div>
  `;
}

function problemCardHtml(p, i) {
  const selected = p.id === selectedProblemId;
  const statusCls = STATUS_CLASS[p.status] || "";
  return `<div class="problem-card ${selected ? "selected" : ""}" data-id="${p.id}">
    <div class="problem-row-head">
      <div>
        <div class="row1"><span class="idx">${String(p.id).padStart(2, "0")}</span><span class="tag ${CAT_CLASS[p.cat]}">${p.cat}</span><span class="path-tag">${p.path}</span></div>
        <div class="title">${p.title}</div>
        <div class="meta">${p.metaBits.join(" · ")}</div>
      </div>
      <div class="right">
        <div class="cost">${fmtEur(p.annualCost)}/an</div>
        <div class="status-txt ${statusCls}">${p.status}</div>
      </div>
    </div>
  </div>`;
}

function detailPanelHtml(p) {
  if (!p) return `<div class="card"><p class="sub">Sélectionnez un problème pour voir le détail.</p></div>`;
  const d = p.detail;
  return `<div class="card">
    <div class="badges">
      <span class="tag ${CAT_CLASS[p.cat]}">${p.cat}</span>
      <span class="path-tag">${p.status}</span>
      <span class="path-tag">${p.path}</span>
    </div>
    <h3>${p.title}</h3>
    <p class="desc">${d.description}</p>
    <div class="detail-metrics">
      <div class="m"><div class="k">Temps perdu / sem.</div><div class="v">${d.lostPerWeek}</div></div>
      <div class="m"><div class="k">Coût annuel</div><div class="v">${fmtEur(p.annualCost)}</div></div>
    </div>
    <div class="m" style="margin-bottom:14px;"><div class="k">Confiance</div><div class="v conf-${d.confidence === "Élevée" ? "high" : "medium"}">${d.confidence}</div></div>
    <div class="detail-section-title">Ce que nous avons observé</div>
    <ul class="observed-list">${d.observed.map(o => `<li>${o}</li>`).join("")}</ul>
    <div class="detail-section-title">Séquence type</div>
    <div class="sequence-row">${d.sequence.map((s, i) => `${i > 0 ? `<span class="sequence-arrow">→</span>` : ""}<span class="sequence-chip">${s}</span>`).join("")}</div>
    <div class="solution-box"><div class="k">Solution envisagée</div>${d.solution}</div>
    <div class="detail-actions">
      <button class="btn btn-primary" id="validate-constat">Valider le constat</button>
      <button class="btn" id="reject-constat">Ce n'est pas un problème</button>
    </div>
    <div class="detail-section-title">Ajouter du contexte pour l'équipe d'analyse</div>
    <textarea class="ctx" placeholder="Ex. : cette ressaisie est obligatoire pour les clients export"></textarea>
    <div class="privacy-note">Données agrégées par équipe. Aucun salarié n'est identifié dans les constats.</div>
  </div>`;
}

function renderDetailPanel() {
  const p = DATA.problems.find(x => x.id === selectedProblemId);
  $("#detail-panel").innerHTML = detailPanelHtml(p);
  const vBtn = document.getElementById("validate-constat");
  if (vBtn) vBtn.addEventListener("click", () => toast(`Constat « ${p.title} » validé.`));
  const rBtn = document.getElementById("reject-constat");
  if (rBtn) rBtn.addEventListener("click", () => toast(`Constat « ${p.title} » marqué comme non pertinent.`));
}

function afterRenderProblems() {
  renderDetailPanel();
  $$(".chip").forEach(c => c.addEventListener("click", () => { problemFilter = c.dataset.cat; render(); }));
  $$(".problem-card").forEach(c => c.addEventListener("click", () => {
    selectedProblemId = Number(c.dataset.id);
    $$(".problem-card").forEach(x => x.classList.remove("selected"));
    c.classList.add("selected");
    renderDetailPanel();
  }));
  const exportBtn = document.getElementById("export-csv");
  if (exportBtn) exportBtn.addEventListener("click", () => toast("Export CSV généré (démo)."));
  const more = document.getElementById("show-more");
  if (more) more.addEventListener("click", (e) => { e.preventDefault(); toast(`Les ${DATA.extraProblemsCount} autres problèmes (plus faible coût) ne sont pas détaillés dans cette démo.`); });
}

// ====================== PAGE: interactions ======================
function viewInteractions() {
  const i = DATA.interactions;
  return `
    <div class="view-head">
      <div>
        <h1>Interactions & goulots</h1>
        <p class="desc">Qui échange avec qui, et où le travail attend une information. Vue par équipe et par rôle : le détail par personne n'est ni affiché ni conservé.</p>
      </div>
    </div>
    ${statRow(i.stats, 4)}
    <div class="grid grid-2">
      <div class="card">
        <div class="card-head"><h2>Carte des interactions</h2><div class="sub">${i.weekLabel}</div></div>
        <div class="network-wrap" id="network"></div>
        <div class="net-legend">
          ${i.legend.map(l => `<span class="key"><span class="ln" style="background:${legendColor(l.level)}"></span>${l.label}</span>`).join("")}
          <span style="color:var(--text-muted);">Épaisseur du trait = volume d'échanges</span>
        </div>
      </div>
      <div class="card">
        <h2>Goulots détectés</h2>
        ${i.bottlenecks.map(b => `
          <div class="bottleneck-card">
            <div class="tag-label">${b.tag}</div>
            <div class="title">${b.title}</div>
            <p class="text">${b.text}</p>
            ${b.link ? `<a href="#" class="goto-problem" data-id="${b.problemId}">${b.link}</a>` : ""}
          </div>`).join("")}
      </div>
    </div>
    <div class="card">
      <h2>Temps d'attente moyen entre équipes</h2>
      <p class="sub">Ligne : l'équipe qui attend · Colonne : l'équipe attendue</p>
      <div class="scroll-x">
        <table class="matrix-table">
          <thead><tr><th>Attend →</th>${i.waitTeams.map(t => `<th>${t}</th>`).join("")}</tr></thead>
          <tbody>
            ${i.waitMatrix.map(row => `<tr><td class="rowhead">${row.team}</td>${i.waitTeams.map(t => {
              const v = row.cells[t];
              if (!v) return `<td>–</td>`;
              return `<td><span class="matrix-cell ${waitLevel(v)}">${v}</span></td>`;
            }).join("")}</tr>`).join("")}
          </tbody>
        </table>
      </div>
      <div class="matrix-legend">
        <span><span class="sw" style="background:rgba(255,255,255,0.12)"></span>Attente : moins d'1 h</span>
        <span><span class="sw" style="background:var(--warning)"></span>1 à 3 h</span>
        <span><span class="sw" style="background:var(--serious)"></span>3 à 8 h</span>
        <span><span class="sw" style="background:var(--critical)"></span>plus d'une journée</span>
      </div>
    </div>
  `;
}
function legendColor(level) { return level === "goulot" ? "var(--critical)" : level === "attente" ? "var(--warning)" : "var(--text-muted)"; }
function waitLevel(v) {
  if (v.includes("j")) return "l4";
  const h = parseFloat(v);
  if (v.includes("min")) return "l1";
  if (h >= 3) return "l3";
  if (h >= 1) return "l2";
  return "l1";
}

function afterRenderInteractions() {
  const i = DATA.interactions;
  const wrap = document.getElementById("network");
  const W = wrap.clientWidth || 600, H = 340;
  const svg = svgEl("svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}`, style: "position:absolute; inset:0; z-index:1;" });
  const byId = {};
  i.nodes.forEach(n => byId[n.id] = n);
  i.edges.forEach(e => {
    const a = byId[e.from], b = byId[e.to];
    const x1 = (a.x / 100) * W, y1 = (a.y / 100) * H, x2 = (b.x / 100) * W, y2 = (b.y / 100) * H;
    const color = legendColorRaw(e.level);
    svg.appendChild(svgEl("line", { x1, y1, x2, y2, stroke: color, "stroke-width": 2.5 }));
    const hit = svgEl("line", { x1, y1, x2, y2, stroke: "transparent", "stroke-width": 16 });
    hit.style.cursor = "pointer";
    hit.addEventListener("pointermove", (ev) => showTooltip(ev.clientX, ev.clientY, `<div class="tt-val">${e.detail}</div>`));
    hit.addEventListener("pointerleave", hideTooltip);
    svg.appendChild(hit);
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 + (e.labelDy || -6);
    const t = textEl(mx, my, e.label, "annotation-label", { "text-anchor": "middle" });
    t.style.fill = color;
    svg.appendChild(t);
  });
  wrap.appendChild(svg);
  i.nodes.forEach(n => {
    const node = document.createElement("div");
    node.className = "net-node" + (n.highlight ? ` hl-${n.highlight}` : "");
    node.style.left = n.x + "%"; node.style.top = n.y + "%";
    node.innerHTML = `<div class="t">${n.label}</div><div class="s">${n.sub}</div>`;
    wrap.appendChild(node);
  });

  $$(".goto-problem").forEach(a => a.addEventListener("click", (e) => {
    e.preventDefault();
    const id = Number(a.dataset.id);
    selectedProblemId = id;
    location.hash = "#/problems";
  }));
}
function legendColorRaw(level) { return level === "goulot" ? "#e66767" : level === "attente" ? "#e0b24a" : "#70747e"; }

// ====================== PAGE: tools ======================
function viewTools() {
  const t = DATA.tools;
  const colors = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#52555f"];
  return `
    <div class="view-head">
      <div><h1>Temps & outils</h1>
      <p class="desc">Où passe le temps de vos équipes, dans quelles applications, et combien de fois elles passent de l'une à l'autre.</p></div>
    </div>
    ${statRow(t.stats, 4)}
    <div class="card" style="margin-bottom:14px;">
      <div class="card-head"><h2>Répartition du temps par application</h2><div class="sub">Part du temps actif, par équipe</div></div>
      <div class="stack-legend">
        ${t.appCategories.map((c, i) => `<span class="key"><span class="sw" style="background:${colors[i]}"></span>${c}</span>`).join("")}
      </div>
      <div style="margin-top:12px;">
        ${t.byTeam.map(row => `
          <div class="stack-row">
            <div class="team">${row.team}</div>
            <div class="stack-track">
              ${row.values.map((v, i) => v > 0 ? `<div class="stack-seg" style="width:${v}%; background:${colors[i]}" data-label="${t.appCategories[i]}" data-val="${v}" data-team="${row.team}">${v >= 10 ? v + "%" : ""}</div>` : "").join("")}
            </div>
          </div>`).join("")}
      </div>
      <div class="callout-box"><b>À retenir :</b> ${t.callout}</div>
    </div>
    <div class="grid grid-2">
      <div class="card">
        <div class="card-head"><h2>Quand les tâches répétitives ont lieu</h2><div class="sub">Minutes de tâches répétitives, tous postes</div></div>
        <div class="heatmap" style="margin-top:10px;">
          <div></div>
          ${t.heatmapHours.map(h => `<div class="hcol-label">${h}</div>`).join("")}
          ${t.heatmapDays.map((day, r) => `
            <div class="hrow-label">${day}</div>
            ${t.heatmapMatrix[r].map(v => `<div class="hcell" style="background:${heatColor(v)}" data-v="${v}" data-day="${day}"></div>`).join("")}
          `).join("")}
        </div>
        <p class="sub" style="margin-top:10px;">${t.heatmapPeakNote}</p>
      </div>
      <div class="card">
        <h2>Enchaînements les plus fréquents</h2>
        ${t.sequences.map(s => {
          const max = t.sequences[0].count;
          return `<div class="seq-row">
            <div class="top"><span>${s.path}</span><span class="cnt">${s.count.toLocaleString("fr-FR")} / sem.</span></div>
            <div class="seq-bar-track"><div class="seq-bar-fill" style="width:${(s.count/max)*100}%"></div></div>
          </div>`;
        }).join("")}
        <h2 style="margin-top:18px;">Copier-coller entre applications</h2>
        ${t.copyPaste.map(c => `<div class="simple-list-row"><span>${c.path}</span><span class="cnt">${c.count.toLocaleString("fr-FR")}</span></div>`).join("")}
      </div>
    </div>
  `;
}
function heatColor(v) {
  const steps = ["rgba(57,135,229,0.12)", "rgba(57,135,229,0.3)", "rgba(57,135,229,0.48)", "rgba(57,135,229,0.66)", "rgba(57,135,229,0.84)", "rgba(57,135,229,1)"];
  return steps[Math.min(v, steps.length - 1)];
}
function afterRenderTools() {
  $$(".stack-seg").forEach(seg => {
    seg.addEventListener("pointermove", (e) => {
      showTooltip(e.clientX, e.clientY, `<div class="tt-title">${seg.dataset.team} · ${seg.dataset.label}</div><div class="tt-val">${seg.dataset.val} %</div>`);
    });
    seg.addEventListener("pointerleave", hideTooltip);
  });
  $$(".hcell").forEach(c => {
    c.addEventListener("pointermove", (e) => showTooltip(e.clientX, e.clientY, `<div class="tt-title">${c.dataset.day}</div><div class="tt-val">Intensité ${c.dataset.v}/5</div>`));
    c.addEventListener("pointerleave", hideTooltip);
  });
}

// ====================== PAGE: business ======================
function viewBusiness() {
  const b = DATA.businessCase;
  const maxGain = Math.max(...b.modules.map(m => m.gain));
  const beforeH = 68.5 * 60, afterH = 19.67 * 60; // minutes, just for bar width ratio
  const maxMin = beforeH;
  return `
    <div class="view-head">
      <div><h1>Business case</h1>
      <p class="desc">Ce que coûtent les problèmes détectés, ce que chaque module du logiciel permet de récupérer, et dans quel ordre les construire.</p></div>
      <div class="view-head-actions"><button class="btn btn-primary" id="dl-board">Télécharger pour le comité de direction</button></div>
    </div>
    ${statRow(b.stats, 3)}
    <div class="card" style="margin-bottom:14px;">
      <div class="card-head"><h2>Feuille de route des modules, classée par rentabilité</h2><div class="sub">Gain annuel par semaine de développement</div></div>
      <div class="scroll-x">
        <table class="modules-table">
          <thead><tr><th>Ordre</th><th>Module</th><th>Problèmes traités</th><th>Temps récupéré</th><th>Gain annuel</th><th>Délai</th></tr></thead>
          <tbody>
            ${b.modules.map(m => `<tr>
              <td>${String(m.order).padStart(2, "0")}</td>
              <td class="name">${m.name}${m.tag ? `<span class="module-tag">${m.tag}</span>` : ""}</td>
              <td>${m.problems}</td>
              <td>${m.recovered}</td>
              <td><div class="gain-bar-wrap"><div class="gain-bar-track"><div class="gain-bar-fill" style="width:${(m.gain/maxGain)*100}%"></div></div><span class="gain-val">${fmtEur(m.gain)}</span></div></td>
              <td>${m.delay}</td>
            </tr>`).join("")}
          </tbody>
        </table>
      </div>
      <p class="muted-note">${b.modulesNote}</p>
    </div>
    <div class="grid grid-half">
      <div class="card">
        <h2>Temps perdu par semaine, avant et après</h2>
        <div class="before-after-row">
          <div class="top"><span>Aujourd'hui</span><span>${b.beforeAfter.before}</span></div>
          <div class="ba-track"><div class="ba-fill before" style="width:100%"></div></div>
        </div>
        <div class="before-after-row">
          <div class="top"><span>Après les 6 modules</span><span>${b.beforeAfter.after}</span></div>
          <div class="ba-track"><div class="ba-fill after" style="width:${(afterH/maxMin)*100}%"></div></div>
        </div>
        <div class="ba-note">${b.beforeAfter.note}</div>
      </div>
      <div class="card">
        <h2>Investissement et retour</h2>
        <table class="kv-table">
          ${b.investment.map(r => `<tr><td>${r.label}</td><td class="v">${r.value}</td></tr>`).join("")}
        </table>
      </div>
    </div>
    <div class="card">
      <h2>Hypothèses de calcul</h2>
      <div class="assumptions-row">${b.assumptions.map(a => `<span><b>${a.split(" : ")[0]}</b>${a.includes(" : ") ? " : " + a.split(" : ")[1] : ""}</span>`).join("")}</div>
    </div>
  `;
}
function afterRenderBusiness() {
  const dl = document.getElementById("dl-board");
  if (dl) dl.addEventListener("click", () => toast("Export comité de direction généré (démo)."));
}

// ====================== PAGE: piloting ======================
function viewPiloting() {
  const p = DATA.piloting;
  return `
    <div class="view-head">
      <div><h1>Pilotage continu</h1>
      <p class="desc">${p.inProductionSince}</p></div>
      <div class="view-head-actions">
        <button class="btn" id="monthly-report">Rapport mensuel (PDF)</button>
        <button class="btn btn-primary" id="signal-need">Signaler un nouveau besoin</button>
      </div>
    </div>
    ${statRow(p.stats, 4)}
    <div class="card" style="margin-bottom:14px;">
      <div class="card-head">
        <h2>Heures perdues par semaine</h2>
        <div class="sub" style="display:flex; gap:14px;">
          <span><span style="display:inline-block;width:10px;height:2px;background:#3987e5;vertical-align:middle;margin-right:5px;"></span>Mesuré</span>
          <span><span style="display:inline-block;width:10px;height:2px;background:#0ca30c;vertical-align:middle;margin-right:5px;border-top:1px dashed #0ca30c;"></span>Objectif après les 6 modules (${p.chart.objectiveLabel})</span>
        </div>
      </div>
      <div class="chart-wrap"><svg id="loss-chart"></svg></div>
    </div>
    <div class="grid grid-half">
      <div class="card">
        <h2>Modules du logiciel</h2>
        ${p.modules.map(m => `<div class="modules-status-row"><span>${m.name}</span><span class="st">${m.status}</span></div>`).join("")}
      </div>
      <div class="card">
        <h2>À traiter</h2>
        ${p.toHandle.map(h => `<div class="to-handle-row">
          <div class="ic ${h.icon}">${h.icon === "warning" ? "!" : h.icon === "info" ? "i" : "+"}</div>
          <div><div class="title">${h.title}</div><p class="text">${h.text}</p><a href="#" class="handle-link" data-title="${h.title}">${h.link}</a></div>
        </div>`).join("")}
      </div>
    </div>
    <div class="grid grid-half">
      <div class="card">
        <h2>Prochaine mesure d'impact</h2>
        <div class="next-impact-date">${p.nextImpact.dateRange}</div>
        <p class="sub" style="margin:0;">${p.nextImpact.text}</p>
        <div class="note-box-green">${p.nextImpact.note}</div>
      </div>
      <div class="card">
        <div class="card-head"><h2>Vos demandes d'évolution</h2><a href="#" id="new-request">Nouvelle demande</a></div>
        ${p.requests.map(r => `<div class="request-row"><span>${r.name}</span><span class="request-status ${REQ_STATUS_CLASS[r.status]}">${r.status}</span></div>`).join("")}
      </div>
    </div>
  `;
}

function afterRenderPiloting() {
  const p = DATA.piloting;
  const svg = document.getElementById("loss-chart");
  const wrap = svg.parentElement;
  const W = wrap.clientWidth || 640, H = 260;
  const margin = { top: 20, right: 20, bottom: 28, left: 42 };
  const innerW = W - margin.left - margin.right, innerH = H - margin.top - margin.bottom;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("width", W); svg.setAttribute("height", H);
  svg.innerHTML = "";
  const data = p.chart.measured;
  const maxY = 80;
  const x = (i) => margin.left + (i / (data.length - 1)) * innerW;
  const y = (v) => margin.top + innerH - (v / maxY) * innerH;
  const g = svgEl("g", {});
  [0, 20, 40, 60, 80].forEach(v => {
    const yy = y(v);
    g.appendChild(svgEl("line", { x1: margin.left, x2: W - margin.right, y1: yy, y2: yy, class: "grid-line" }));
    g.appendChild(textEl(margin.left - 8, yy + 3, v + " h", "axis-label", { "text-anchor": "end" }));
  });
  p.chart.xLabels.forEach((lb, i) => g.appendChild(textEl(x(i), H - 6, lb, "axis-label", { "text-anchor": "middle" })));
  // objective dashed line
  const oy = y(p.chart.objective);
  g.appendChild(svgEl("line", { x1: margin.left, x2: W - margin.right, y1: oy, y2: oy, stroke: "#0ca30c", "stroke-width": 1.5, "stroke-dasharray": "5,4" }));
  // annotations
  p.chart.annotations.forEach(a => {
    const ax = x(a.atIndex);
    g.appendChild(svgEl("line", { x1: ax, x2: ax, y1: margin.top, y2: margin.top + innerH, stroke: "rgba(255,255,255,0.12)", "stroke-dasharray": "3,3" }));
    g.appendChild(textEl(ax + 4, margin.top + 10, a.label, "annotation-label"));
  });
  const linePath = data.map((v, i) => (i === 0 ? "M" : "L") + x(i) + "," + y(v)).join(" ");
  g.appendChild(svgEl("path", { d: linePath, fill: "none", stroke: "#3987e5", "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" }));
  data.forEach((v, i) => {
    const dot = svgEl("circle", { cx: x(i), cy: y(v), r: 3.5, fill: "#3987e5", stroke: "#141720", "stroke-width": 2 });
    dot.style.cursor = "pointer";
    dot.addEventListener("pointermove", (e) => showTooltip(e.clientX, e.clientY, `<div class="tt-title">${p.chart.xLabels[i]}</div><div class="tt-val">${v.toFixed(1)} h perdues / sem.</div>`));
    dot.addEventListener("pointerleave", hideTooltip);
    g.appendChild(dot);
  });
  svg.appendChild(g);

  $$(".handle-link").forEach(a => a.addEventListener("click", (e) => { e.preventDefault(); toast(`Action : ${a.dataset.title}`); }));
  const mr = document.getElementById("monthly-report");
  if (mr) mr.addEventListener("click", () => toast("Rapport mensuel (PDF) généré (démo)."));
  const sn = document.getElementById("signal-need");
  if (sn) sn.addEventListener("click", () => toast("Formulaire de nouveau besoin ouvert (démo)."));
  const nr = document.getElementById("new-request");
  if (nr) nr.addEventListener("click", (e) => { e.preventDefault(); toast("Nouvelle demande d'évolution (démo)."); });
}

// ====================== router ======================
const PAGES = {
  overview: { render: viewOverview, after: afterRenderOverview },
  problems: { render: viewProblems, after: afterRenderProblems },
  interactions: { render: viewInteractions, after: afterRenderInteractions },
  tools: { render: viewTools, after: afterRenderTools },
  business: { render: viewBusiness, after: afterRenderBusiness },
  piloting: { render: viewPiloting, after: afterRenderPiloting },
};

function currentRoute() {
  const h = location.hash.replace(/^#\/?/, "");
  return PAGES[h] ? h : "overview";
}

function render() {
  const route = currentRoute();
  document.getElementById("sidebar").innerHTML = renderSidebar(route);
  document.getElementById("topbar-meta").innerHTML = renderTopbar(route);
  document.getElementById("view").innerHTML = PAGES[route].render();
  PAGES[route].after();

  $$(".nav-item[data-route]").forEach(item => item.addEventListener("click", () => {
    if (item.classList.contains("disabled")) return;
    location.hash = "#/" + item.dataset.route;
  }));
  const wc = document.getElementById("write-consultant");
  if (wc) wc.addEventListener("click", (e) => { e.preventDefault(); toast("Message au consultant (démo) — non envoyé."); });
  const ms = document.getElementById("manage-sub");
  if (ms) ms.addEventListener("click", (e) => { e.preventDefault(); toast("Gestion de l'abonnement (démo)."); });

  window.scrollTo(0, 0);
}

window.addEventListener("hashchange", render);
window.addEventListener("resize", () => { if (PAGES[currentRoute()].after) PAGES[currentRoute()].after(); });
render();

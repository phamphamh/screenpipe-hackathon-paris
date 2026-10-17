// Dashboard graphique CAIbinet · Atelier Nova.
// Les 6 étapes du portail, chacune tient dans la fenêtre ; une barre de filtres (équipe, jour, type) recalcule tout ;
// le détail s'ouvre au clic (panneau de droite). Données : DATA (labs/adamaass/caibinet-nova/data.js), DATA.dash pour les chiffres bruts.
const D = DATA, X = DATA.dash;
const $ = (s, el = document) => el.querySelector(s);
// une couleur = un sens ; deux palettes (sombre façon orja.io, claire pour un projecteur)
const PALETTES = {
  sombre: {
    cuivre: "#e5a276", vert: "#00c758", rouge: "#e5484d", ambre: "#f59e0b", gris: "#7d756e", fond: "#ffffff12", trait: "#ffffff30",
    texte: "#ece7e2", texteDoux: "#ece7e2b0", fondPage: "#0a0a0b", barreNeutre: "#ffffff52", neutreFonce: "#3a3532",
    cuivreVoile: "#e5a2761a", cuivreBord: "#e5a27666", neutre: a => `rgba(236,231,226,${a})`,
    equipe: { "E-commerce": "#d6cfc8", "Opérations": "#7d756e" },
    type: { "Ressaisie": "#2f7fe0", "Recherche": "#6aa9f5", "Répétition": "#b4d3fb" },
    rouges: ["#e5484d", "#c93c41", "#a83337"],
  },
  clair: {
    cuivre: "#b8692f", vert: "#0f9d4c", rouge: "#d93a40", ambre: "#d98a00", gris: "#9b938c", fond: "#0000000f", trait: "#00000033",
    texte: "#1a1714", texteDoux: "#1a1714b0", fondPage: "#ffffff", barreNeutre: "#00000033", neutreFonce: "#d9d3cc",
    cuivreVoile: "#b8692f14", cuivreBord: "#b8692f66", neutre: a => `rgba(26,23,20,${Math.min(a + .06, 1)})`,
    equipe: { "E-commerce": "#3d3733", "Opérations": "#a8a09a" },
    type: { "Ressaisie": "#1f5fbf", "Recherche": "#4b8de6", "Répétition": "#9cc3f5" },
    rouges: ["#d93a40", "#b8333a", "#932a30"],
  },
};
let THEME = (() => { try { return localStorage.getItem("nova-theme") || "sombre"; } catch (e) { return "sombre"; } })();
let C = PALETTES[THEME];
document.documentElement.dataset.theme = THEME;
const EQUIPES = Object.keys(X.equipes), TYPES = Object.keys(C.type), SEMAINES = 46;

// ---------- formats ----------
const nf = (n, d = 0) => Number(n).toLocaleString("fr-FR", { maximumFractionDigits: d, minimumFractionDigits: d }).replace(/[\u202f\u00a0]/g, " ");  // espace normale : toutes les polices l'affichent
const eur = n => n >= 10000 ? `${nf(n / 1000, n >= 100000 ? 0 : 1)} k€` : `${nf(n)} €`;
const h = n => n >= 1 ? `${nf(n, n >= 10 ? 0 : 1)} h` : `${nf(n * 60)} min`;
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const somme = a => a.reduce((x, y) => x + y, 0);
const enHeures = txt => { const t = String(txt), hh = t.match(/(\d+)\s*h\s*(\d+)?/); if (hh) return +hh[1] + (+(hh[2] || 0)) / 60; const mm = t.match(/(\d+)\s*min/); return mm ? +mm[1] / 60 : 0; };

// ---------- filtres : un seul état, tout est recalculé ----------
const F = { equipe: "Toutes", jour: "Tous", type: "Tous" };
function modele() {
  const eqs = F.equipe === "Toutes" ? EQUIPES : [F.equipe];
  const jours = F.jour === "Tous" ? X.jours.map((_, i) => i) : [X.jours.indexOf(F.jour)];
  const taches = X.taches.filter(t => (F.equipe === "Toutes" || t.equipes.includes(F.equipe)) && (F.type === "Tous" || t.categorie === F.type));
  const visibles = taches.filter(t => t.visible);
  const minutesEcran = X.ecrans.map((_, s) => somme(eqs.flatMap(e => jours.map(j => X.minutes_ecran_jour[e][j][s]))));
  const heuresJour = Object.fromEntries(eqs.map(e => [e, X.heures_par_jour[e]]));
  const chaleur = X.jours.map((_, j) => Array.from({ length: 11 }, (_, k) => somme(eqs.map(e => X.chaleur[e][j][k]))));
  const titres = new Set(taches.map(t => t.titre));
  const skills = D.businessCase.modules.filter(m => titres.has(m.name.replace("Skill · ", "")));
  const coutAn = somme(taches.map(t => t.cout_an)), gainAn = somme(taches.map(t => t.gain_an));
  const heuresSem = somme(taches.map(t => t.heures_semaine)), gagneesSem = gainAn / SEMAINES / X.cout_horaire;
  const gainSkillsH = somme(skills.map(m => enHeures(m.recovered)));
  return {
    eqs, jours, taches, visibles, minutesEcran, heuresJour, chaleur, skills, coutAn, gainAn, heuresSem, gagneesSem, gainSkillsH,
    postes: somme(eqs.map(e => X.equipes[e])),
    heuresObs: somme(eqs.flatMap(e => jours.map(j => X.heures_par_jour[e][j]))),
    recos: X.a_automatiser.filter(t => titres.has(t)),
    filtre: F.equipe !== "Toutes" || F.jour !== "Tous" || F.type !== "Tous",
  };
}

// ---------- graphes SVG (ils remplissent leur carte) ----------
// Chaque graphe est posé comme un emplacement, puis dessiné à la taille réelle de sa carte (et redessiné au redimensionnement).
let GRAPHES = [];
const graphe = fn => `<div class="gph" data-gi="${GRAPHES.push(fn) - 1}"></div>`;
function dessiner() {
  document.querySelectorAll(".gph").forEach(el => {
    const w = Math.max(el.clientWidth, 160), hh = Math.max(el.clientHeight, 140);
    el.innerHTML = GRAPHES[+el.dataset.gi](w, hh);
  });
}
function joli(max) {
  const brut = max / 4, p = Math.pow(10, Math.floor(Math.log10(brut || 1)));
  return [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10].map(k => k * p).find(v => v >= brut) * 4;
}
const axeTxt = v => v >= 1000 ? nf(v / 1000) + "k" : nf(v, v % 1 ? 1 : 0);
function arc(cx, cy, r, a0, a1) {
  const p = a => [cx + r * Math.cos(a), cy + r * Math.sin(a)], [x0, y0] = p(a0), [x1, y1] = p(a1);
  return `M${x0},${y0} A${r},${r} 0 ${a1 - a0 > Math.PI ? 1 : 0} 1 ${x1},${y1}`;
}
function donut(segs, centreV, centreK, { w = 420, hgt = 260, r = null, ep = null, bas = false } = {}) {
  r = r ?? Math.max(40, Math.min(w / 2 - 74, hgt / 2 - 30)); ep = ep ?? Math.max(14, r * .26);
  segs = segs.filter(s => s.v > 0);
  const tot = somme(segs.map(s => s.v)) || 1, cx = w / 2, cy = bas ? (hgt - segs.length * 24) / 2 : hgt / 2;
  let a = -Math.PI / 2, out = "";
  const pris = { true: [], false: [] };  // étiquettes déjà posées de chaque côté : on les écarte pour qu'elles ne se chevauchent pas
  if (!segs.length) out = `<circle cx="${cx}" cy="${cy}" r="${r}" stroke="${C.fond}" stroke-width="${ep}" fill="none"/>`;
  segs.forEach(s => {
    const a1 = a + (s.v / tot) * Math.PI * 2, m = (a + a1) / 2;
    out += `<path class="seg ${s.estompe ? "estompe" : ""}" d="${arc(cx, cy, r, a + .015, a1 - .015)}" stroke="${s.c}" stroke-width="${ep}" fill="none" ${s.clic ? `data-clic="${esc(s.clic)}"` : ""} ${s.ouvre ? `data-ouvre="${esc(s.ouvre)}"` : ""} data-tip="${esc(s.k)} : ${esc(s.vt ?? s.v)}"/>`;
    if (bas) {  // une ligne par part sous l'anneau : pastille, valeur, libellé
      const k = segs.indexOf(s), yy = hgt - (segs.length - k) * 24 + 14, x0 = Math.max(cx - 110, 4);
      out += `<rect x="${x0}" y="${yy - 10}" width="10" height="10" rx="2" fill="${s.c}"/><text x="${x0 + 18}" y="${yy}" class="lbl-v" font-size="15">${esc(s.vt ?? s.v)}</text><text x="${x0 + 90}" y="${yy}" class="lbl-k">${esc(s.k)}</text>`;
    } else if (s.v / tot >= .06) {
      const ex = cx + (r + 18) * Math.cos(m), d = Math.cos(m) >= 0, lx = d ? w - 6 : 6, anc = d ? "end" : "start";
      let ey = Math.min(Math.max(cy + (r + 18) * Math.sin(m), 22), hgt - 18);
      while (pris[d].some(y => Math.abs(y - ey) < 36)) ey += ey < cy ? -36 : 36;
      pris[d].push(ey);
      out += `<polyline points="${cx + (r + ep / 2) * Math.cos(m)},${cy + (r + ep / 2) * Math.sin(m)} ${ex},${ey} ${d ? lx - 64 : lx + 64},${ey}" fill="none" stroke="${C.trait}"/>`;
      out += `<text x="${lx}" y="${ey - 5}" text-anchor="${anc}" class="lbl-v">${esc(s.vt ?? s.v)}</text><text x="${lx}" y="${ey + 11}" text-anchor="${anc}" class="lbl-k">${esc(s.k)}</text>`;
    }
    a = a1;
  });
  return `<svg class="graph" viewBox="0 0 ${w} ${hgt}" preserveAspectRatio="xMidYMid meet">${out}
    <text x="${cx}" y="${cy + r * .12}" text-anchor="middle" class="centre-v" font-size="${Math.round(Math.min(r * .42, ((r - ep / 2) * 1.6) / Math.max(String(centreV).length, 3)))}">${esc(centreV)}</text>
    <text x="${cx}" y="${cy + r * .14 + 20}" text-anchor="middle" class="centre-k">${esc(centreK)}</text></svg>`;
}
function anneau(pct, coul, centre, taille = 132, ep = 10) {
  const r = (taille - ep) / 2, c = taille / 2, p = Math.max(0, Math.min(1, pct)), fin = -Math.PI / 2 + p * Math.PI * 2 - (p >= 1 ? .0001 : 0);
  return `<svg width="${taille}" height="${taille}" viewBox="0 0 ${taille} ${taille}"><circle cx="${c}" cy="${c}" r="${r}" stroke="${C.fond}" stroke-width="${ep}" fill="none"/>
    ${p > 0 ? `<path d="${arc(c, c, r, -Math.PI / 2, fin)}" stroke="${coul}" stroke-width="${ep}" fill="none" stroke-linecap="round"/>` : ""}
    <text x="${c}" y="${c + 8}" text-anchor="middle" class="centre-v" font-size="${taille / 4.6}">${esc(centre)}</text></svg>`;
}
function courbes(series, labels, { w = 560, hgt = 250, pointilleDe = null, objectif = null, surligne = null } = {}) {
  const m = { g: 36, d: 28, h: 14, b: 24 }, iw = w - m.g - m.d, ih = hgt - m.h - m.b;
  const max = joli(Math.max(...series.flatMap(s => s.v), objectif ?? 0, .1) * 1.08);
  const x = i => m.g + (labels.length === 1 ? iw / 2 : (i / (labels.length - 1)) * iw), y = v => m.h + ih - (v / max) * ih;
  let out = surligne != null ? `<rect x="${x(surligne) - iw / labels.length / 2}" y="${m.h}" width="${iw / labels.length}" height="${ih}" fill="${C.cuivreVoile}" rx="6"/>` : "";
  for (let k = 0; k <= 4; k++) { const v = (max / 4) * k; out += `<line class="grille" x1="${m.g}" x2="${w - m.d}" y1="${y(v)}" y2="${y(v)}"/><text class="axe" x="${m.g - 6}" y="${y(v) + 3}" text-anchor="end">${axeTxt(v)}</text>`; }
  labels.forEach((l, i) => out += `<text class="axe" x="${x(i)}" y="${hgt - 6}" text-anchor="middle" ${i === surligne ? `style="fill:${C.cuivre}"` : ""}>${esc(l)}</text>`);
  if (objectif != null) out += `<line x1="${m.g}" x2="${w - m.d}" y1="${y(objectif)}" y2="${y(objectif)}" stroke="${C.vert}" stroke-dasharray="5 4"/>`;
  series.forEach((s, si) => {
    const pts = s.v.map((v, i) => `${x(i)},${y(v)}`);
    if (si === 0) out += `<path d="M${x(0)},${y(0)} L${pts.join(" L")} L${x(s.v.length - 1)},${y(0)} Z" fill="${s.c}" opacity=".08"/>`;
    if (pointilleDe != null) {
      out += `<polyline points="${pts.slice(0, pointilleDe + 1).join(" ")}" fill="none" stroke="${s.c}" stroke-width="2.5"/><polyline points="${pts.slice(pointilleDe).join(" ")}" fill="none" stroke="${s.c}" stroke-width="2.5" stroke-dasharray="6 5"/>`;
    } else out += `<polyline points="${pts.join(" ")}" fill="none" stroke="${s.c}" stroke-width="2.5"/>`;
    s.v.forEach((v, i) => out += `<circle cx="${x(i)}" cy="${y(v)}" r="4" fill="${C.fondPage}" stroke="${s.c}" stroke-width="2" ${s.clic ? `data-clic="${esc(s.clic(i))}"` : ""} data-tip="${esc(s.k)} · ${esc(labels[i])} : ${h(v)}"/>`);
  });
  return `<svg class="graph" viewBox="0 0 ${w} ${hgt}" preserveAspectRatio="xMidYMid meet">${out}</svg>`;
}
function barres(groupes, series, { w = 640, hgt = 260, fmt = v => nf(v), surligne = null, annot = "" } = {}) {
  const m = { g: 38, d: 8, h: 14, b: 28 }, iw = w - m.g - m.d, ih = hgt - m.h - m.b;
  const max = joli(Math.max(...series.flatMap(s => s.v), .1) * 1.08), bande = iw / groupes.length, bw = Math.min(28, (bande * .72) / series.length);
  let out = "";
  for (let k = 0; k <= 4; k++) { const v = (max / 4) * k, yy = m.h + ih - (v / max) * ih; out += `<line class="grille" x1="${m.g}" x2="${w - m.d}" y1="${yy}" y2="${yy}"/><text class="axe" x="${m.g - 6}" y="${yy + 3}" text-anchor="end">${axeTxt(v)}</text>`; }
  if (surligne != null) {  // la preuve : le groupe à regarder est encadré et annoté
    const hautMax = Math.max(...series.map(s => s.v[surligne])), yy = m.h + ih - (hautMax / max) * ih;
    out += `<rect x="${m.g + bande * surligne + 3}" y="${m.h}" width="${bande - 6}" height="${ih}" rx="8" fill="${C.cuivreVoile}" stroke="${C.cuivreBord}"/>`;
    if (annot) out += `<text x="${m.g + bande * surligne + bande / 2}" y="${Math.max(yy - 8, m.h + 14)}" text-anchor="middle" class="lbl-v" style="fill:${C.cuivre}">${esc(annot)}</text>`;
  }
  groupes.forEach((g, i) => {
    const x0 = m.g + bande * i + (bande - bw * series.length) / 2;
    series.forEach((s, si) => {
      const v = s.v[i], bh = (v / max) * ih;
      out += `<rect class="barre-g" x="${x0 + si * bw + 1}" y="${m.h + ih - bh}" width="${bw - 2}" height="${Math.max(bh, 1)}" rx="3" fill="${s.c}" ${s.clic ? `data-clic="${esc(s.clic)}"` : ""} data-tip="${esc(s.k)} · ${esc(g)} : ${fmt(v)}"/>`;
    });
    out += `<text class="axe" x="${m.g + bande * i + bande / 2}" y="${hgt - 9}" text-anchor="middle">${esc(g)}</text>`;
  });
  return `<svg class="graph" viewBox="0 0 ${w} ${hgt}" preserveAspectRatio="xMidYMid meet">${out}</svg>`;
}
function spark(vals, coul = C.cuivre) {
  const w = 120, hh = 34, max = Math.max(...vals, .1), x = i => (i / Math.max(vals.length - 1, 1)) * w, y = v => hh - 3 - (v / max) * (hh - 6);
  return `<svg class="spark" viewBox="0 0 ${w} ${hh}" preserveAspectRatio="none"><polyline points="${vals.map((v, i) => `${x(i)},${y(v)}`).join(" ")}" fill="none" stroke="${coul}" stroke-width="2"/></svg>`;
}
const hbars = (items, coul) => {
  if (!items.length) return `<div class="vide">Rien pour ce filtre</div>`;
  const max = Math.max(...items.map(i => i.v)) || 1;
  return items.map(i => `<div class="hbar ${i.annot ? "annote" : ""}" ${i.ouvre ? `data-ouvre="${esc(i.ouvre)}"` : ""} data-tip="${esc(i.tip || i.k)}"><span class="nom">${esc(i.k)}</span>
    <div class="piste"><div class="rempli" style="width:${(i.v / (i.max || max)) * 100}%;background:${i.c || coul}"></div>${i.annot ? `<span class="annot">${esc(i.annot)}</span>` : ""}</div><span class="val">${esc(i.vt)}</span></div>`).join("");
};
const tuile = (k, v, { s = "", cls = "", vcls = "", ouvre = "", sp = "" } = {}) =>
  `<div class="tile ${cls}" ${ouvre ? `data-ouvre="${ouvre}"` : ""}><span class="k">${k}</span><span class="v ${vcls}">${v}</span>${s ? `<span class="s">${s}</span>` : "<span></span>"}${sp}</div>`;
// lecture en 3 niveaux : surtitre (de quoi parle la carte) → phrase-clé (ce qu'il faut retenir) → le graphe (le détail)
const entete = (titre, cle = "", droite = "") => `<h2><span>${titre}</span>${droite}</h2>${cle ? `<p class="cle">${cle}</p>` : ""}`;
const carte = (span, titre, corps, { defile = false, etale = false, droite = "", cle = "" } = {}) =>
  `<div class="card ${span}">${entete(titre, cle, droite)}<div class="corps ${defile ? "defile" : ""} ${etale ? "etale" : ""}">${corps}</div></div>`;
const legende = items => `<div class="legende">${items.map(([k, c, clic]) => `<span ${clic ? `data-clic="${esc(clic)}" style="cursor:pointer"` : ""}><i style="background:${c}"></i>${esc(k)}</span>`).join("")}</div>`;

// ---------- le rapport : 5 questions dans l'ordre où un nouveau venu les pose, puis la méthode ----------
// Même gabarit partout : la question en titre, la réponse en une phrase, UNE preuve annotée au centre,
// 2-3 chiffres avec leur point de comparaison et leur source à droite, « Suivant → » vers la question d'après.
const GLOSSAIRE = {
  "back-office": "L'interface interne d'une boutique en ligne (ici Magento) : catalogue, prix, commandes, clients, rapports.",
  "tâche répétée": "Une activité qui revient plusieurs fois dans la semaine, repérée dans les captures et confirmée par le salarié.",
  "problème": "Une tâche répétée faite par au moins 3 personnes : en dessous, elle n'est pas détaillée pour protéger l'anonymat.",
  "goulot": "Du temps perdu autour du travail : tâche refaite, allers-retours entre écrans, attente d'un collègue.",
  "automatisable": "Score de 0 à 100 : la part de la tâche qu'un agent IA peut reprendre (étapes fixes, peu de décisions humaines).",
  "skill": "Une automatisation prête à l'emploi pour un agent IA (Claude, Codex) : les étapes observées, les décisions laissées à un humain.",
  "simulation ×10": "Les volumes mesurés sur 6 salariés réels (WONDERBREAD, Stanford) sont multipliés par 10 pour simuler une PME de 60 salariés.",
};
const info = mot => `<span class="info" data-tip="${esc(GLOSSAIRE[mot])}">ⓘ</span>`;
const AUDIT_5J = 5500; // repère de marché : un audit IA de 5 jours chez une agence (Lonestone, 1 100 € HT / jour)
const ICONES = {
  contexte: '<circle cx="12" cy="12" r="9"/><path d="M12 8v.5M12 11v5"/>',
  constat: '<path d="M3 3h7v7H3zM14 3h7v4h-7zM14 10h7v11h-7zM3 13h7v8H3z"/>',
  temps: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
  couts: '<path d="M12 3 2 20h20L12 3zM12 10v4M12 17v.5"/>',
  plan: '<path d="M3 17l5-5 4 4 8-8M15 8h5v5"/>',
  methode: '<path d="M5 4h11l3 3v13H5zM9 9h6M9 13h6M9 17h4"/>',
};
const PAGES = {
  contexte: { n: 1, titre: "Ce qu'on a observé", court: "Contexte", groupe: "Le rapport", lignes: "auto 150px minmax(0,1fr)", vue: vueContexte },
  constat: { n: 2, titre: "Ce qu'on a trouvé", court: "État des lieux", groupe: "Le rapport", lignes: "auto 134px minmax(0,1fr)", vue: vueConstat },
  temps: { n: 3, titre: "Où part le temps ?", court: "Temps perdu", groupe: "Le rapport", lignes: "auto 134px minmax(0,1fr)", vue: vueTemps },
  couts: { n: 4, titre: "Qu'est-ce qui coûte le plus ?", court: "Manque à gagner", groupe: "Le rapport", lignes: "auto 134px minmax(0,1fr)", vue: vueCouts },
  plan: { n: 5, titre: "Que faire, dans quel ordre ?", court: "Recommandation", groupe: "Le rapport", lignes: "auto 134px minmax(0,1fr)", vue: vuePlan },
  methode: { n: null, titre: "Méthode et limites", court: "Méthode", groupe: "Annexe", lignes: "auto minmax(0,1fr)", vue: vueMethode },
};
const ETAPES = Object.keys(PAGES).filter(k => PAGES[k].n);
const parType = M => TYPES.map(k => ({ k, v: M.visibles.filter(t => t.categorie === k).length, c: C.type[k], clic: `type:${k}`, estompe: F.type !== "Tous" && F.type !== k }));
const NIVEAUX = [["Oui", t => t.score >= 75, C.vert], ["Partiel", t => t.score >= 45 && t.score < 75, C.ambre], ["Non", t => t.score < 45, C.gris]];
const reponse = (txt, suite, heros = null) => `<div class="reponse s12"><p>${txt}</p>
  ${heros ? `<div class="heros-v"><span class="v compte ${heros.cls || ""}">${heros.v}</span><span class="k">${heros.k}</span></div>` : ""}
  ${suite ? `<button class="btn plein" data-route="${suite}">${esc(PAGES[suite].court)} →</button>` : ""}</div>`;
const pct = (a, b) => `${nf((a / (b || 1)) * 100)} %`;

// ---------- graphes « diagramme » : entonnoir, treemap, cascade, camembert, pictogrammes ----------
const PICTOS = {
  ecran: '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
  texte: '<path d="M4 6h16M4 10h16M4 14h10"/><path d="M3 3l18 18"/>',
  groupe: '<circle cx="8" cy="9" r="3"/><circle cx="16" cy="9" r="3"/><path d="M3 19c0-3 2.5-5 5-5s5 2 5 5M11 19c0-3 2.5-5 5-5s5 2 5 5"/>',
  cadenas: '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
  multiplier: '<path d="M6 6l12 12M18 6 6 18"/>', oeil: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/><path d="M3 3l18 18"/>',
  calendrier: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>', loupe: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
};
const picto = (k, coul = "currentColor", t = 26) => `<svg width="${t}" height="${t}" viewBox="0 0 24 24" fill="none" stroke="${coul}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${PICTOS[k]}</svg>`;
function cercleKpi(v, k, coul, t = 118) {
  return `<div class="anneau"><svg width="${t}" height="${t}" viewBox="0 0 ${t} ${t}"><circle cx="${t / 2}" cy="${t / 2}" r="${t / 2 - 3}" stroke="${coul}" stroke-width="3" fill="${coul}12"/>
    <text x="${t / 2}" y="${t / 2 + 4}" text-anchor="middle" class="centre-v" font-size="${String(v).length > 5 ? 20 : 28}">${esc(v)}</text>
    <text x="${t / 2}" y="${t / 2 + 24}" text-anchor="middle" class="lbl-k" font-size="10.5">${esc(k)}</text></svg></div>`;
}
// entonnoir horizontal : largeur en échelle logarithmique (55 000 captures → 5 skills tiennent sur le même dessin)
function entonnoir(etapes, { w = 700, hgt = 300 } = {}) {
  const n = etapes.length, bw = w / n, max = Math.log10(etapes[0].v + 1), haut = v => Math.max(72, Math.max(.16, Math.log10(v + 1) / max) * (hgt - 20));
  let out = "";
  etapes.forEach((e, i) => {
    const h0 = haut(e.v), h1 = i < n - 1 ? haut(etapes[i + 1].v) : h0 * .8, x0 = i * bw + 4, x1 = (i + 1) * bw - 4, cy = hgt / 2;
    const coul = i >= n - 2 ? C.cuivre : C.neutre(.18 + i * .09);
    out += `<path d="M${x0},${cy - h0 / 2} L${x1},${cy - h1 / 2} L${x1},${cy + h1 / 2} L${x0},${cy + h0 / 2} Z" fill="${coul}" ${e.ouvre ? `data-ouvre="${e.ouvre}"` : ""} data-tip="${esc(e.k)} : ${nf(e.v)}"/>`;
    const encre = i >= n - 2 ? "#1a0e06" : C.texte;
    out += `<text x="${(x0 + x1) / 2}" y="${cy - 2}" text-anchor="middle" class="centre-v" font-size="${e.v >= 10000 ? 22 : 26}" style="fill:${encre}">${nf(e.v)}</text>`;
    out += `<text x="${(x0 + x1) / 2}" y="${cy + 20}" text-anchor="middle" class="lbl-k" style="fill:${encre};opacity:.8">${esc(e.k)}</text>`;
  });
  return `<svg class="graph" viewBox="0 0 ${w} ${hgt}" preserveAspectRatio="xMidYMid meet">${out}</svg>`;
}
// treemap : chaque problème est un bloc proportionnel à son coût (découpage « squarified »)
function treemap(items, { w = 700, hgt = 380 } = {}) {
  const tot = somme(items.map(i => i.v)) || 1, rects = [];
  const pire = (ligne, cote) => { const s = somme(ligne.map(i => i.a)), mx = Math.max(...ligne.map(i => i.a)), mn = Math.min(...ligne.map(i => i.a)); return Math.max((cote * cote * mx) / (s * s), (s * s) / (cote * cote * mn)); };
  let x = 0, y = 0, rw = w, rh = hgt, reste = items.map(i => ({ ...i, a: (i.v / tot) * w * hgt })), ligne = [];
  const poser = () => {
    const s = somme(ligne.map(i => i.a)), horizontal = rw >= rh, cote = horizontal ? rh : rw, ep = s / cote;
    let p = 0; ligne.forEach(i => { const l = i.a / ep; rects.push(horizontal ? { ...i, x, y: y + p, w: ep, h: l } : { ...i, x: x + p, y, w: l, h: ep }); p += l; });
    if (horizontal) { x += ep; rw -= ep; } else { y += ep; rh -= ep; }
    ligne = [];
  };
  while (reste.length) {
    const i = reste[0], cote = Math.min(rw, rh);
    if (!ligne.length || pire([...ligne, i], cote) <= pire(ligne, cote)) { ligne.push(i); reste.shift(); } else poser();
  }
  if (ligne.length) poser();
  return `<svg class="graph" viewBox="0 0 ${w} ${hgt}" preserveAspectRatio="none">${rects.map(r => `<g ${r.ouvre ? `data-ouvre="${esc(r.ouvre)}"` : ""} data-tip="${esc(r.tip || r.k)} : ${esc(r.vt)}">
    <rect class="seg" x="${r.x + 2}" y="${r.y + 2}" width="${Math.max(r.w - 4, 0)}" height="${Math.max(r.h - 4, 0)}" rx="8" fill="${r.c}"/>
    ${etiquette(r)}</g>`).join("")}</svg>`;
}
// étiquette d'un bloc : chiffre + nom, le nom passe sur deux lignes s'il ne tient pas ; rien si le bloc est trop petit
function etiquette(r) {
  const fv = r.w > 180 ? 18 : 14, fk = r.w > 130 ? 13 : 11.5, place = r.w - 20, larg = (txt, f) => txt.length * f * .56;
  if (r.w < 64 || r.h < 40 || larg(r.vt, fv) > place) return "";
  const cv = r.blanc ? "#fff" : r.fonce ? "#0a0a0b" : C.texte, ck = r.blanc ? "#ffffffd0" : r.fonce ? "#0a0a0bb0" : C.texteDoux;
  let lignes = [r.k];
  if (larg(r.k, fk) > place) { const mots = r.k.split(" "); lignes = [mots[0], mots.slice(1).join(" ")].filter(Boolean); }
  if (lignes.some(l => larg(l, fk) > place) || r.h < 30 + lignes.length * (fk + 4)) lignes = [];
  return `<text x="${r.x + 12}" y="${r.y + 8 + fv}" class="lbl-v" font-size="${fv}" style="fill:${cv}">${esc(r.vt)}</text>` +
    lignes.map((l, i) => `<text x="${r.x + 12}" y="${r.y + 12 + fv + (i + 1) * (fk + 3)}" class="lbl-k" font-size="${fk}" style="fill:${ck}">${esc(l)}</text>`).join("");
}
// cascade : d'aujourd'hui à l'objectif, une marche par skill
function cascade(depart, marches, { w = 700, hgt = 320 } = {}) {
  const m = { g: 40, d: 10, h: 24, b: 54 }, iw = w - m.g - m.d, ih = hgt - m.h - m.b, n = marches.length + 2, bande = iw / n, bw = Math.min(64, bande * .62);
  const max = joli(depart * 1.05), y = v => m.h + ih - (v / max) * ih;
  let out = "", niveau = depart;
  for (let k = 0; k <= 4; k++) { const v = (max / 4) * k; out += `<line class="grille" x1="${m.g}" x2="${w - m.d}" y1="${y(v)}" y2="${y(v)}"/><text class="axe" x="${m.g - 6}" y="${y(v) + 3}" text-anchor="end">${axeTxt(v)} h</text>`; }
  const barre = (i, haut, bas, coul, lbl, val, ouvre) => {
    const x = m.g + bande * i + (bande - bw) / 2;
    out += `<rect class="barre-g" x="${x}" y="${y(haut)}" width="${bw}" height="${Math.max(y(bas) - y(haut), 2)}" rx="5" fill="${coul}" ${ouvre ? `data-ouvre="${ouvre}"` : ""} data-tip="${esc(lbl)} : ${esc(val)}"/>`;
    const [l1, l2] = lbl.includes(". ") ? lbl.split(". ") : [lbl, ""];  // « 1. Prix produit » sur deux lignes
    out += `<text x="${x + bw / 2}" y="${y(haut) - 7}" text-anchor="middle" class="lbl-v" font-size="13">${esc(val)}</text>`;
    const [n1, ...n2] = l2.split(" ");  // « Commandes » / « annulées » : chaque mot entier sur sa ligne
    out += `<text x="${x + bw / 2}" y="${hgt - (l2 ? 34 : 20)}" text-anchor="middle" class="axe" ${l2 ? `style="fill:${C.cuivre}"` : ""}>${esc(l2 ? "Skill " + l1 : l1)}</text>${l2 ? `<text x="${x + bw / 2}" y="${hgt - 19}" text-anchor="middle" class="axe" font-size="11">${esc(n1)}</text><text x="${x + bw / 2}" y="${hgt - 5}" text-anchor="middle" class="axe" font-size="11">${esc(n2.join(" "))}</text>` : ""}`;
  };
  barre(0, depart, 0, C.rouge, "Aujourd'hui", h(depart));
  marches.forEach((mk, i) => { const bas = Math.max(niveau - mk.v, 0); barre(i + 1, niveau, bas, C.cuivre, mk.k, `−${h(mk.v)}`, mk.ouvre); out += `<line x1="${m.g + bande * (i + 1) - (bande - bw) / 2}" x2="${m.g + bande * (i + 1) + (bande - bw) / 2}" y1="${y(niveau)}" y2="${y(niveau)}" stroke="${C.trait}" stroke-dasharray="3 3"/>`; niveau = bas; });
  barre(n - 1, niveau, 0, C.vert, "Après", h(niveau));
  return `<svg class="graph" viewBox="0 0 ${w} ${hgt}" preserveAspectRatio="xMidYMid meet">${out}</svg>`;
}
// camembert : un donut plein
// camembert : l'anneau laisse 120 px à chaque étiquette
const camembert = (segs, centreV, centreK) => graphe((w, hh) => {
  const cote = (w / 2 - 126) / 1.21, bas = cote < 70;  // carte étroite : la légende passe sous l'anneau
  const r = bas ? Math.max(40, Math.min(w / 2 - 20, (hh - segs.length * 24) / 2 - 10) / 1.21) : Math.max(40, Math.min(cote, hh / 2 - 36));
  return donut(segs, centreV, centreK, { w, hgt: hh, r, ep: r * .3, bas });
});

function vueContexte(M) {
  const ch = X.chaine;
  return `
  ${reponse(`Une semaine de travail observée dans le back-office ${info("back-office")} de la boutique en ligne. Rien n'a quitté les ordinateurs sans accord.`, "constat", { v: `${M.postes} salariés`, k: `enregistrés ${X.jours.length} jours` })}
  <div class="card s12"><div class="corps"><div class="anneaux">
    ${cercleKpi(X.postes, "salariés", C.cuivre)}${cercleKpi(`${X.jours.length} j`, "d'observation", C.equipe["E-commerce"])}${cercleKpi(h(X.heures_observees), "enregistrées", C.equipe["E-commerce"])}${cercleKpi(EQUIPES.length, "équipes", C.equipe["Opérations"])}${cercleKpi("1", "outil : Magento", C.equipe["Opérations"])}
  </div></div></div>
  ${carte("s12", "De l'écran au rapport", graphe((w, hh) => entonnoir([{ k: "captures d'écran", v: ch.captures }, { k: "moments de travail", v: ch.moments }, { k: "tâches répétées", v: ch.taches, ouvre: "goto:couts" }, { k: "problèmes", v: ch.problemes, ouvre: "goto:couts" }, { k: "skills", v: ch.skills, ouvre: "goto:plan" }], { w, hgt: hh })), { cle: `<b>${nf(ch.captures)} captures</b> réduites à <b>${ch.skills} skills</b> à construire`, droite: `<span class="chip">échelle log.</span>` })}`;
}

function vueConstat(M) {
  const n1 = X.taches.find(t => t.titre === M.recos[0]) || M.visibles[0], skillsGain = somme(M.skills.map(m => m.gain));
  const top = [...M.visibles].sort((a, b) => b.cout_an - a.cout_an).slice(0, 6);
  return `
  ${reponse(`Les tâches répétées coûtent <b>${eur(M.coutAn)} / an</b>. Les ${M.skills.length} premières skills ${info("skill")} en récupèrent <b>${eur(skillsGain)}</b>.`, "temps", { v: eur(M.gainAn), k: "récupérables / an" })}
  <div class="s4">${tuile("Équivaut à", `${nf(M.coutAn / (X.cout_horaire * 35 * SEMAINES), 1)} temps plein`, { s: "perdus chaque année", vcls: "rouge", ouvre: "goto:couts" })}</div>
  <div class="s4">${tuile("Rapporte", `${nf(M.gainAn / AUDIT_5J)} audits`, { s: "de 5 jours chez une agence IA", vcls: "vert", ouvre: "goto:plan" })}</div>
  <div class="s4">${tuile("Skill n° 1", n1 ? n1.court : "—", { s: n1 ? `+${eur(n1.gain_an)} / an` : "", vcls: "cuivre", ouvre: n1 ? `tache:${n1.titre}` : "" })}</div>
  ${carte("s4", "Le coût annuel", camembert([{ k: "avec les skills", v: skillsGain, vt: eur(skillsGain), c: C.cuivre, ouvre: "goto:plan" }, { k: "autres gains", v: Math.max(M.gainAn - skillsGain, 0), vt: eur(M.gainAn - skillsGain), c: C.vert }, { k: "non récupérable", v: Math.max(M.coutAn - M.gainAn, 0), vt: eur(M.coutAn - M.gainAn), c: C.neutreFonce }], eur(M.coutAn), "par an"), { cle: `Les skills récupèrent <b>${pct(skillsGain, M.coutAn)}</b> du coût` })}
  ${carte("s8", `Problèmes ${info("problème")} les plus chers`, hbars(top.map((t, i) => ({ k: t.court, tip: t.titre, v: t.cout_an, vt: eur(t.cout_an), ouvre: `tache:${t.titre}`, c: i === 0 ? C.rouge : C.barreNeutre, annot: i === 0 ? "n° 1" : "" }))), { etale: true, droite: `<span class="chip">€ / an</span>`, cle: top[0] ? `<b class="rouge">${esc(top[0].court)}</b> coûte le plus : ${eur(top[0].cout_an)} / an` : "" })}`;
}

function vueTemps(M) {
  const tot = somme(M.minutesEcran) || 1, topI = M.minutesEcran.indexOf(Math.max(...M.minutesEcran));
  const parEq = M.eqs.map(e => ({ e, v: somme(M.jours.map(j => somme(X.minutes_ecran_jour[e][j]))) }));
  const topEq = [...parEq].map(x => ({ ...x, s: somme(M.jours.map(j => X.minutes_ecran_jour[x.e][j][topI])) })).sort((a, b) => b.s - a.s)[0];
  return `
  ${reponse(`Le temps passe d'abord dans l'écran <b>${esc(X.ecrans[topI])}</b>${M.eqs.length > 1 ? `, surtout chez <b>${esc(topEq.e)}</b>` : ""}.`, "couts", { v: pct(M.minutesEcran[topI], tot), k: `du temps · ${esc(X.ecrans[topI])}` })}
  <div class="s6">${tuile("Temps enregistré", h(M.heuresObs), { s: F.jour === "Tous" ? `${X.jours.length} jours · ${M.postes} salariés` : F.jour, sp: spark(X.jours.map((_, j) => somme(M.eqs.map(e => X.heures_par_jour[e][j])))) })}</div>
  <div class="s6">${tuile("Changements d'écran", nf(X.bascules / (X.jours.length * X.postes)), { s: "par jour et par salarié" })}</div>
  ${carte("s8", "Heures par écran", graphe((w, hh) => barres(X.ecrans, M.eqs.map(e => ({ k: e, c: C.equipe[e], clic: `equipe:${e}`, v: X.ecrans.map((_, s) => somme(M.jours.map(j => X.minutes_ecran_jour[e][j][s])) / 60) })), { w, hgt: hh, fmt: v => h(v), surligne: topI, annot: pct(M.minutesEcran[topI], tot) })) + legende(M.eqs.map(e => [e, C.equipe[e], `equipe:${e}`])), { droite: `<span class="chip">heures / semaine</span>`, cle: `<b>${esc(X.ecrans[topI])}</b> prend ${pct(M.minutesEcran[topI], tot)} du temps enregistré` })}
  ${carte("s4", "Temps par équipe", camembert(parEq.map(x => ({ k: x.e, v: x.v, vt: pct(x.v, somme(parEq.map(y => y.v))), c: C.equipe[x.e], clic: `equipe:${x.e}` })), h(somme(parEq.map(x => x.v)) / 60), "observées"), { cle: (() => { const t = somme(parEq.map(y => y.v)) || 1, m = [...parEq].sort((a, b) => b.v - a.v)[0]; return m ? `<b>${esc(m.e)}</b> : ${pct(m.v, t)} du temps` : ""; })() })}`;
}

function vueCouts(M) {
  const tri = [...M.visibles].sort((a, b) => b.cout_an - a.cout_an), tot = somme(tri.map(t => t.cout_an)), top3 = somme(tri.slice(0, 3).map(t => t.cout_an));
  const niv = NIVEAUX.map(([k, f, c]) => ({ k, c, l: M.visibles.filter(f) })), n = M.visibles.length || 1, g0 = X.goulots[0];
  const rouges = C.rouges;
  return `
  ${reponse(`<b>3 problèmes</b> concentrent l'essentiel du coût. Le n° 1 : <b>${esc(tri[0] ? tri[0].court.toLowerCase() : "—")}</b>.`, "plan", { v: pct(top3, tot), k: `du coût des ${M.visibles.length} problèmes`, cls: "rouge" })}
  <div class="s4">${tuile(`Coût des ${M.visibles.length} problèmes ${info("problème")}`, `${eur(tot)} / an`, { s: `sur ${eur(M.coutAn)} au total (19 tâches)`, vcls: "rouge" })}</div>
  <div class="s4">${tuile(`Goulot n° 1 ${info("goulot")}`, esc(g0.type), { s: `dans ${g0.taches} tâches sur ${X.taches.length}`, vcls: "rouge", ouvre: "goulot:0" })}</div>
  <div class="card s4">${entete(`Automatisable ${info("automatisable")}`, `<b>${niv[0].l.length} sur ${M.visibles.length}</b> entièrement`)}<div class="corps">
    <div class="segbar">${niv.filter(x => x.l.length).map(x => `<div style="flex:${x.l.length};background:${x.c}" data-ouvre="niveau:${x.k}" data-tip="${x.k} : ${x.l.length} problème(s)">${x.l.length}</div>`).join("") || `<div style="flex:1;background:${C.fond}"></div>`}</div>
    <div class="segleg">${niv.map(x => `<span data-ouvre="niveau:${x.k}" style="cursor:pointer"><i style="display:inline-block;width:9px;height:9px;border-radius:2px;background:${x.c};margin-right:6px"></i>${x.k} ${pct(x.l.length, n)}</span>`).join("")}</div></div></div>
  ${carte("s8", "Coût par problème", graphe((w, hh) => treemap(tri.map((t, i) => ({ k: t.court, tip: t.titre, v: t.cout_an, vt: eur(t.cout_an), ouvre: `tache:${t.titre}`, c: i < 3 ? rouges[i] : C.neutre(.3 - i * .018), fonce: false, blanc: i < 3 })), { w, hgt: hh })), { droite: `<span class="chip">surface = € / an</span>`, cle: `Les 3 blocs rouges font <b class="rouge">${pct(top3, tot)}</b> du coût` })}
  ${carte("s4", "Causes du temps perdu", `${hbars(X.goulots.map((g, i) => ({ k: g.type, v: g.heures_semaine, max: X.heures_semaine, vt: `${pct(g.heures_semaine, X.heures_semaine)}`, tip: `${h(g.heures_semaine)} / sem. dans ${g.taches} tâches`, c: [C.rouge, C.ambre, C.gris][i] || C.gris, ouvre: `goulot:${i}` })))}<p class="note">% des ${h(X.heures_semaine)} perdues / sem. · une tâche peut cumuler plusieurs causes</p>`, { etale: true, cle: `<b class="rouge">${esc(g0.type)}</b> : ${pct(g0.heures_semaine, X.heures_semaine)} du temps perdu` })}`;
}

function vuePlan(M) {
  const avant = M.heuresSem, apres = Math.max(avant - M.gainSkillsH, 0), s1 = M.skills[0];
  const nomSkill = m => { const t = X.taches.find(x => x.titre === m.name.replace("Skill · ", "")); return t ? t.court : m.name; };
  return `
  ${reponse(s1 ? `<b>${M.skills.length} skills</b> ${info("skill")}, dans l'ordre du gain. On commence par <b>${esc(nomSkill(s1).toLowerCase())}</b>, qui rend le plus d'heures.` : "Aucune skill pour ce filtre.", null, { v: eur(somme(M.skills.map(m => m.gain))), k: "récupérés / an", cls: "vert" })}
  <div class="s4">${tuile("Investissement", `${somme(M.skills.map(m => parseInt(m.delay) || 1))} sem.`, { s: "de construction, une skill à la fois" })}</div>
  <div class="s4">${tuile("Heures perdues / sem.", `${h(avant)} → ${h(apres)}`, { s: `−${pct(avant - apres, avant)}`, vcls: "vert" })}</div>
  <div class="s4">${tuile("À lancer d'abord", s1 ? nomSkill(s1) : "—", { s: s1 ? `${s1.delay} · +${eur(s1.gain)} / an` : "", vcls: "cuivre", ouvre: s1 ? `module:${D.businessCase.modules.indexOf(s1)}` : "" })}</div>
  ${carte("s8", "Heures perdues, skill après skill", graphe((w, hh) => cascade(avant, M.skills.map((m, i) => ({ k: `${i + 1}. ${nomSkill(m)}`, v: enHeures(m.recovered), ouvre: `module:${D.businessCase.modules.indexOf(m)}` })), { w, hgt: hh })), { droite: `<span class="chip cuivre">projection</span>`, cle: `De <b class="rouge">${h(avant)}</b> à <b class="vert">${h(apres)}</b> perdues par semaine` })}
  ${carte("s4", "Gain par skill", hbars(M.skills.map((m, i) => ({ k: `${i + 1}. ${nomSkill(m)}`, tip: m.name, v: m.gain, vt: eur(m.gain), ouvre: `module:${D.businessCase.modules.indexOf(m)}`, c: i === 0 ? C.cuivre : C.cuivreBord, annot: i === 0 ? m.delay : "" }))), { etale: true, droite: `<span class="chip">€ / an</span>`, cle: s1 ? `<b>${esc(nomSkill(s1))}</b> rapporte le plus` : "" })}`;
}

function vueMethode() {
  const puce = (t, c = "") => `<span class="eq ${c}">${t}</span>`;
  const limites = [["multiplier", "Simulation ×10", "6 salariés réels × 10"], ["oeil", "Non mesuré", "attentes, messagerie, copier-coller"], ["calendrier", "1 semaine", "pas de saisonnalité"], ["groupe", "Anonymat", `${X.taches.filter(t => !t.visible).length} tâches à moins de 3 pers.`]];
  return `
  ${reponse("Chaque chiffre vient d'une tâche observée : voici les deux formules, et ce que les données ne disent pas.", "contexte")}
  <div class="card s7">${entete("Les formules", `Coût = temps observé × <b>${nf(X.cout_horaire)} € / h</b>`)}<div class="corps etale">
    <div class="equation">${puce("fréquence / sem.")}×${puce("durée")}×${puce(`${SEMAINES} sem.`)}×${puce(`${nf(X.cout_horaire)} € / h`)}=${puce("coût / an", "rouge")}</div>
    <div class="equation">${puce("coût / an", "rouge")}×${puce(`score ${info("automatisable")}`)}=${puce("gain / an", "vert")}</div>
    <div class="legende-statut"><span><i class="obs"></i>observé : fréquence, durée, étapes, temps par écran</span><span><i class="est"></i>estimé : score, gain</span></div>
  </div></div>
  <div class="card s5">${entete("Les limites", `<b>${limites.length} limites</b> à garder en tête`)}<div class="corps limites">${limites.map(([p, t, d]) => `<div class="limite-carte">${picto(p, C.ambre, 26)}<b>${t}</b><span>${d}</span></div>`).join("")}</div></div>`;
}

// ---------- panneau de détail ----------
function skillMd(t) {
  return `---\nname: ${t.court.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-")}\ndescription: ${t.titre}. Générée depuis l'audit CAIbinet (Atelier Nova), à relire avant usage.\n---\n\n# ${t.titre}\n\n## Étapes observées\n${t.etapes.map((e, i) => `${i + 1}. ${e}`).join("\n")}\n\n## Règle\nLes décisions restent humaines : avant toute modification, montrer le résultat et attendre la validation.\n`;
}
function detail(cle) {
  const [type, ...reste] = cle.split(":"), val = reste.join(":");
  if (type === "goto") { location.hash = "#/" + val; return null; }
  if (type === "tache") {
    const t = X.taches.find(x => x.titre === val), p = D.problems.find(x => x.title === val);
    return `<span class="chip">${esc(t.categorie)} · ${esc(t.equipes.join(", ") || "—")}</span><h3>${esc(t.titre)}</h3>
      <div class="kpis"><div><b>${nf(t.frequence)}</b><span>fois / semaine</span></div><div><b>${h(t.heures_semaine)}</b><span>par semaine</span></div><div><b>${t.score}</b><span>score / 100</span></div></div>
      <div class="kpis"><div><b>${t.personnes}</b><span>personnes</span></div><div><b style="color:var(--rouge)">${eur(t.cout_an)}</b><span>coût / an</span></div><div><b style="color:var(--vert)">${eur(t.gain_an)}</b><span>gain / an</span></div></div>
      ${p ? `<span class="sec">Étapes observées</span><ol>${(t.etapes.length ? t.etapes : p.detail.sequence).map(s => `<li>${esc(s)}</li>`).join("")}</ol>
      <span class="sec">Observé</span><ul>${p.detail.observed.map(o => `<li>${esc(o)}</li>`).join("")}</ul>
      <div class="solution">${esc(p.detail.solution)}</div>
      <div class="actions"><button class="btn plein" data-skill="${esc(t.titre)}">Créer la skill (SKILL.md)</button></div>` : `<p style="color:var(--muted)">Moins de 3 personnes : pas de détail, pour l'anonymat.</p>`}`;
  }
  if (type === "niveau") {
    const f = NIVEAUX.find(n => n[0] === val)[1], l = modele().visibles.filter(f);
    return `<span class="chip">Automatisable</span><h3>${esc(val)} · ${l.length} problème(s)</h3>${hbars(l.map(t => ({ k: t.court, tip: t.titre, v: t.cout_an, vt: eur(t.cout_an), ouvre: `tache:${t.titre}`, c: C.type[t.categorie] })))}`;
  }
  if (type === "ecran") {
    const M = modele(), i = X.ecrans.indexOf(val), tot = somme(M.minutesEcran) || 1;
    return `<span class="chip">Écran Magento</span><h3>${esc(val)}</h3><div class="kpis">${M.eqs.map(e => `<div><b>${h(somme(M.jours.map(j => X.minutes_ecran_jour[e][j][i])) / 60)}</b><span>${esc(e)}</span></div>`).join("")}<div><b>${nf((M.minutesEcran[i] / tot) * 100)} %</b><span>du temps</span></div></div>`;
  }
  if (type === "goulot") {
    const g = X.goulots[+val], b = D.interactions.bottlenecks[+val];
    return `<span class="chip">Goulot · toutes équipes</span><h3>${esc(g.type)}</h3><div class="kpis"><div><b style="color:var(--rouge)">${h(g.heures_semaine)}</b><span>par semaine</span></div><div><b>${g.taches}</b><span>tâches</span></div><div><b>${pct(g.heures_semaine, X.heures_semaine)}</b><span>du temps perdu</span></div></div>
      ${b ? `<span class="sec">Exemple observé</span><p style="color:var(--muted);margin:0">${esc(b.text)}</p>` : ""}`;
  }
  if (type === "module") {
    const m = D.businessCase.modules[+val], titre = m.name.replace("Skill · ", ""), t = X.taches.find(x => x.titre === titre);
    return `<span class="chip">Skill n° ${m.order}${m.tag ? " · " + esc(m.tag) : ""}</span><h3>${esc(titre)}</h3>
      <div class="kpis"><div><b style="color:var(--vert)">${eur(m.gain)}</b><span>gain / an</span></div><div><b>${esc(m.recovered.replace(" / sem.", ""))}</b><span>par semaine</span></div><div><b>${esc(m.delay)}</b><span>à construire</span></div></div>
      <div class="actions">${t ? `<button class="btn" data-ouvre="tache:${esc(titre)}">Voir la tâche</button>` : ""}${t && t.etapes.length ? `<button class="btn plein" data-skill="${esc(titre)}">Créer la skill (SKILL.md)</button>` : ""}</div>`;
  }
  return null;
}
function ouvrir(cle) {
  const html = detail(cle);
  if (!html) return fermer();
  $("#drawer").innerHTML = `<div class="haut"><span></span><button class="ferme" id="ferme">Fermer</button></div>${html}`;
  $("#drawer").classList.add("ouvert"); $("#voile").classList.add("ouvert");
}
function fermer() { $("#drawer").classList.remove("ouvert"); $("#voile").classList.remove("ouvert"); }
function toast(msg) { let t = $("#toast"); if (!t) { t = document.createElement("div"); t.id = "toast"; t.className = "toast"; document.body.appendChild(t); } t.textContent = msg; t.classList.add("on"); setTimeout(() => t.classList.remove("on"), 2200); }

// ---------- rendu ----------
const route = () => (PAGES[location.hash.replace(/^#\/?/, "")] ? location.hash.replace(/^#\/?/, "") : "contexte");
let PRESENTATION = false;
const voisin = (r, d) => { const i = ETAPES.indexOf(r); return i < 0 ? null : ETAPES[i + d] || null; };
const choix = (id, label, options, val) => `<div class="filtre ${val !== options[0] ? "actif" : ""}"><label for="${id}">${label}</label><select id="${id}">${options.map(o => `<option ${o === val ? "selected" : ""}>${esc(o)}</option>`).join("")}</select></div>`;
function rendre() {
  const r = route(), p = PAGES[r], M = modele();
  let groupe = "";
  $("#side").innerHTML = `<div class="brand"><span class="mark">C</span><span class="nom">CAIbinet</span></div>
    <div class="client"><b>${esc(D.client.name)}</b><span>${X.postes} salariés · ${EQUIPES.length} équipes</span></div>
    ${Object.entries(PAGES).map(([k, v]) => {
      const g = v.groupe !== groupe ? `<div class="group">${esc(v.groupe)}</div>` : ""; groupe = v.groupe;
      return `${g}<button class="nav ${k === r ? "on" : ""}" data-route="${k}" title="${esc(v.titre)}"><span class="etape-n">${v.n ?? "+"}</span><span class="lbl">${esc(v.court)}</span></button>`;
    }).join("")}
    <div class="foot">${esc(D.demoTag)}</div>`;
  document.body.classList.toggle("pres", PRESENTATION);
  const prec = voisin(r, -1), suiv = voisin(r, 1);
  $("#top").innerHTML = `<span class="chip cuivre">${p.n ? `Étape ${p.n} / ${ETAPES.length}` : "Annexe"}</span>${M.filtre ? `<button class="btn" id="raz" title="Retirer le filtre">Filtre : ${esc([F.equipe, F.jour, F.type].filter(x => x !== "Toutes" && x !== "Tous").join(" · "))} ✕</button>` : ""}
    <div class="droite"><button class="btn" id="theme" title="Thème clair / sombre">${THEME === "sombre" ? "☀︎ Clair" : "☾ Sombre"}</button>
      <button class="btn ${PRESENTATION ? "plein" : ""}" id="presenter">${PRESENTATION ? "Quitter la présentation" : "Présenter"}</button>${PRESENTATION ? "" : `<button class="btn" id="export">Exporter</button>`}</div>`;
  const v = $("#view");
  v.style.gridTemplateRows = p.lignes;
  GRAPHES = [];
  v.innerHTML = p.vue(M);
  const preuve = v.querySelector(".card.s8, .card.s7"); if (preuve) preuve.classList.add("preuve");  // la preuve de l'écran
  requestAnimationFrame(dessiner);
  compter();
  indice();
}
function compter() {  // « 57,0 k€ », « 48 % », « 60 postes » : le nombre monte en 0,7 s, le reste du texte ne bouge pas
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  document.querySelectorAll(".compte, .tile .v").forEach(el => {
    const m = el.textContent.match(/^(\d{1,3}(?: \d{3})*)(,\d+)?(.*)$/s); if (!m) return;
    const cible = parseFloat(m[1].replace(/ /g, "") + "." + (m[2] || ",0").slice(1)), dec = m[2] ? m[2].length - 1 : 0, reste = m[3], t0 = performance.now();
    const pas = t => { const q = Math.min((t - t0) / 700, 1), v = cible * (1 - Math.pow(1 - q, 3)); el.textContent = nf(v, dec) + reste; if (q < 1) requestAnimationFrame(pas); };
    requestAnimationFrame(pas);
    setTimeout(() => { el.textContent = nf(cible, dec) + reste; }, 900);
  });
}
function indice() {  // une seule fois : dire que les chiffres sont cliquables
  try { if (localStorage.getItem("nova-indice")) return; localStorage.setItem("nova-indice", "1"); } catch (e) {}
  setTimeout(() => toast("Astuce : cliquez sur un chiffre, une barre ou un bloc pour voir d'où il vient."), 900);
}
let attente; window.addEventListener("resize", () => { clearTimeout(attente); attente = setTimeout(dessiner, 120); });
document.addEventListener("change", e => {
  const id = e.target.id;
  if (id === "f-equipe") F.equipe = e.target.value; else if (id === "f-jour") F.jour = e.target.value; else if (id === "f-type") F.type = e.target.value; else return;
  rendre();
});
document.addEventListener("click", e => {
  const nav = e.target.closest("[data-route]"); if (nav) { location.hash = "#/" + nav.dataset.route; return; }
  if (e.target.closest("#ferme") || e.target.id === "voile") return fermer();
  if (e.target.closest("#raz")) { F.equipe = "Toutes"; F.jour = "Tous"; F.type = "Tous"; return rendre(); }
  if (e.target.closest("#export")) return window.print();
  if (e.target.closest("#theme")) { THEME = THEME === "sombre" ? "clair" : "sombre"; C = PALETTES[THEME]; document.documentElement.dataset.theme = THEME; try { localStorage.setItem("nova-theme", THEME); } catch (err) {} return rendre(); }
  if (e.target.closest("#presenter")) { PRESENTATION = !PRESENTATION; if (PRESENTATION) { F.equipe = "Toutes"; F.jour = "Tous"; F.type = "Tous"; location.hash = "#/" + ETAPES[0]; } return rendre(); }
  const sk = e.target.closest("[data-skill]");
  if (sk) {
    const t = X.taches.find(x => x.titre === sk.dataset.skill);
    const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(new Blob([skillMd(t)], { type: "text/markdown" })), download: `SKILL-${t.court.replace(/\s+/g, "-")}.md` });
    a.click(); return toast("SKILL.md téléchargé : à relire avant de l'activer.");
  }
  const c = e.target.closest("[data-clic]");  // un clic sur un graphe pose un filtre (type, équipe, jour)
  if (c) {
    const [k, ...r] = c.dataset.clic.split(":"), val = r.join(":");
    if (k === "type") F.type = F.type === val ? "Tous" : val;
    if (k === "equipe") F.equipe = F.equipe === val ? "Toutes" : val;
    if (k === "jour") F.jour = F.jour === val ? "Tous" : val;
    return rendre();
  }
  const o = e.target.closest("[data-ouvre]"); if (o) ouvrir(o.dataset.ouvre);
});
document.addEventListener("keydown", e => {
  if (e.key === "Escape") { if ($("#drawer").classList.contains("ouvert")) return fermer(); if (PRESENTATION) { PRESENTATION = false; return rendre(); } }
  if (e.target instanceof Element && e.target.matches("select, input")) return;
  const r = route(), cible = e.key === "ArrowRight" || e.key === " " ? voisin(r, 1) : e.key === "ArrowLeft" ? voisin(r, -1) : null;
  if (cible) { e.preventDefault(); location.hash = "#/" + cible; }
});
const tip = $("#tip");
document.addEventListener("mousemove", e => {
  const t = e.target.closest("[data-tip]");
  if (!t) return tip.classList.remove("on");
  tip.textContent = t.dataset.tip; tip.style.left = Math.min(e.clientX + 14, innerWidth - 290) + "px"; tip.style.top = e.clientY + 14 + "px"; tip.classList.add("on");
});
window.addEventListener("hashchange", () => { fermer(); rendre(); });
rendre();

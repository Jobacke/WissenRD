// Text-Hilfsfunktionen – ohne Firebase, damit sie einzeln testbar sind.
import { BEREICHE } from "./bereiche.js";

// Normalisierung für Suchschlüssel.
// MUSS exakt dem Siri-Kurzbefehl entsprechen:
// Kleinbuchstaben → ä/ö/ü/ß ersetzen → alles außer a–z und 0–9 entfernen.
export function norm(s) {
  return String(s || "")
    .toLowerCase()
    .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
    .replace(/[^a-z0-9]/g, "");
}

export function schluesselFuer(e) {
  const roh = [e.kurz, e.titel, ...(e.suchbegriffe || [])];
  return [...new Set(roh.map(norm).filter(k => k.length > 0))];
}

export function slugFuer(e) {
  return norm(e.kurz || e.titel).slice(0, 40) || "eintrag";
}

// ---------- Markdown (für Kurzbefehl-Anzeige) ----------
export function markdownFuer(e) {
  const b = BEREICHE[e.bereich] || { name: e.bereich, icon: "" };
  let md = `# ${e.titel}${e.kurz && e.kurz !== e.titel ? " (" + e.kurz + ")" : ""}\n`;
  md += `${b.icon} ${b.name}\n\n`;
  const funk = funkListe(e);
  if (funk.length) md += `## Funkgruppen\n${funk.map(f => "- " + f).join("\n")}\n\n`;
  for (const a of e.abschnitte || []) {
    if (!a.text || !a.text.trim()) continue;
    md += `## ${a.titel}\n${a.text.trim()}\n\n`;
  }
  const fuss = [e.quelle && "Quelle: " + e.quelle, e.stand && "Stand: " + e.stand, "Rev. " + (e.revision || 1)]
    .filter(Boolean).join(" · ");
  md += `---\n${fuss}\n`;
  return md;
}

// ---------- Vorlesetext ----------
const SPRECH_ERSATZ = [
  [/(\d+(?:,\d+)?(?:\/\d+)?\s?(?:mg|g|IE|µg))\s?\/\s?(\d+(?:,\d+)?\s?ml)/g, "$1 in $2"],
  [/(\d)\s?l\/min/g, "$1 Liter pro Minute"], [/mg\/dl/g, "Milligramm pro Deziliter"],
  [/mg\/kg\s?KG/g, "Milligramm pro Kilogramm Körpergewicht"], [/\bkg\s?KG\b/g, "Kilogramm Körpergewicht"],
  [/\bRR\s?syst\.?/g, "systolischer Blutdruck"], [/\bBZ\b/g, "Blutzucker"], [/\bAF\b/g, "Atemfrequenz"],
  [/\bNotSan\b/g, "Notfallsanitäter"], [/\bLJ\b/g, "Lebensjahr"], [/\bKOF\b/g, "Körperoberfläche"],
  [/§\s?2a/g, "Paragraf 2 a"], [/\b2c\b/g, "2 c"], [/\bca\b/g, "circa"],
  [/\bi\.\s?v\./gi, "intravenös"], [/\bi\.\s?o\./gi, "intraossär"], [/\bi\.\s?m\./gi, "intramuskulär"],
  [/\bs\.\s?l\./gi, "sublingual"], [/\bp\.\s?o\./gi, "oral"], [/\bi\.\s?n\./gi, "intranasal"],
  [/\bs\.\s?c\./gi, "subkutan"], [/\bz\.\s?B\./g, "zum Beispiel"], [/\bggf\./g, "gegebenenfalls"],
  [/\bbzw\./g, "beziehungsweise"], [/\bu\.\s?a\./g, "unter anderem"], [/\bca\./g, "circa"],
  [/(\d)\s?µg\b/g, "$1 Mikrogramm"], [/(\d)\s?mcg\b/g, "$1 Mikrogramm"], [/(\d)\s?mg\b/g, "$1 Milligramm"],
  [/(\d)\s?ml\b/gi, "$1 Milliliter"], [/(\d)\s?g\b/g, "$1 Gramm"], [/(\d)\s?IE\b/g, "$1 internationale Einheiten"],
  [/\/\s?kg\s?KG\b/g, " pro Kilogramm Körpergewicht"], [/\/\s?kg\b/g, " pro Kilogramm"],
  [/\/\s?min\b/g, " pro Minute"], [/(\d)\s?mmHg\b/g, "$1 Millimeter Quecksilbersäule"],
  [/\bSpO2\b/g, "Sauerstoffsättigung"], [/\bRR\b/g, "Blutdruck"], [/\bsyst\./g, "systolisch"],
  [/(\d)\s?mm\b/g, "$1 Millimeter"], [/\s\/\s/g, " oder "], [/(\w)–(\w)/g, "$1 bis $2"],
  [/≥/g, " mindestens "], [/≤/g, " höchstens "], [/>/g, " über "], [/</g, " unter "],
  [/→|->/g, ", dann "], [/\+/g, " plus "], [/%/g, " Prozent"], [/&/g, " und "],
  [/\bSonderbetten\b/gi, "Sonder-Betten"]
];

export function sprechbar(text) {
  let t = String(text || "")
    .replace(/\*\*|__|`|#/g, "")
    .replace(/^\s*[-•*]\s+/gm, "")       // Aufzählungszeichen
    .replace(/\n+/g, ". ")
    .replace(/(?:\.\s*){2,}/g, ". ");
  for (const [re, ers] of SPRECH_ERSATZ) t = t.replace(re, ers);
  return t.replace(/(?:\.\s*){2,}/g, ". ").replace(/:\s*\.\s*/g, ": ").replace(/\s{2,}/g, " ").replace(/\s+([.,])/g, "$1").trim();
}

// ---------- Funkgruppen (Leitstellen) ----------
export const funkListe = e => (Array.isArray(e?.funk) ? e.funk : []).filter(x => typeof x === "string" && x.trim());
// Ansage wie im ZNA-Navi-Kurzbefehl „Aktuelle Leitstelle“: RD_Betten_… = Bettenkanal, RD_ILS_…/RD_1_… = Rettungsdienst,
// Kurzwahl Ziffer für Ziffer als Wörter mit Pausen (1913 → eins, neun, eins, drei)
const ZIFFERN = ["null", "eins", "zwo", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun"];
export function funkSprechtext(funk) {
  const f = (funk || []).filter(x => x && x.trim());
  if (!f.length) return "";
  return f.join(". ")
    .replace(/RD_Sonderbetten_[A-Za-z0-9]+/gi, "Sonder-Betten")
    .replace(/RD_Betten_[A-Za-z0-9]+/g, "Bettenkanal").replace(/RD_ILS_[A-Za-z0-9]+/g, "Rettungsdienst")
    .replace(/RD_[0-9]+_[A-Za-z0-9]+/g, "Rettungsdienst").replace(/\s*[–-]?\s*\(?Bettenanforderung\)?/g, "")
    .replace(/\s*[–-]?\s*\(Sonderbetten\)/gi, "").replace(/[()]/g, "")
    .replace(/\s*–\s*|\s+-\s+/g, ", ").replace(/_/g, " ").replace(/\bSonderbetten\b/gi, "Sonder-Betten")
    .replace(/([0-9])(?=[0-9])/g, "$1, ")
    .replace(/[0-9]/g, z => ZIFFERN[z]) + ".";   // Ziffern als Wörter wie im Funk – sonst „3. Rettungsdienst“ = Aufzählung
}

export function vorlesetextFuer(e) {
  const funk = funkListe(e).length ? "Funkgruppen: " + funkSprechtext(funkListe(e)) : "";
  if (e.sprechtext && e.sprechtext.trim()) {
    const st = e.sprechtext.trim(), titel = st.startsWith(e.titel) ? "" : e.titel + ". ";   // Titel nicht doppelt
    return sprechbar(titel + st + (funk ? " " + funk : ""));
  }
  const teile = [e.titel + "."];
  if (funk) teile.push(funk);
  for (const a of e.abschnitte || []) {
    if (!a.text || !a.text.trim()) continue;
    teile.push(a.titel + ":\n" + a.text.trim() + ".");
  }
  return sprechbar(teile.join("\n"));
}

// ---------- Anzeige (sicheres Mini-Markdown) ----------
function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function inline(s, telefon) {
  let h = esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/_(.+?)_/g, "<em>$1</em>");
  if (telefon) {
    h = h.replace(/(\+?\d[\d \/-]{5,}\d)/g, m => `<a href="tel:${m.replace(/[^\d+]/g, "")}">${m}</a>`);
  }
  return h;
}
export function htmlAusText(text, telefon = false) {
  const zeilen = String(text || "").split("\n");
  let html = "", inListe = false;
  for (const z of zeilen) {
    const m = z.match(/^\s*[-•*]\s+(.*)$/);
    if (m) {
      if (!inListe) { html += "<ul>"; inListe = true; }
      html += `<li>${inline(m[1], telefon)}</li>`;
    } else {
      if (inListe) { html += "</ul>"; inListe = false; }
      if (z.trim()) html += `<p>${inline(z, telefon)}</p>`;
    }
  }
  if (inListe) html += "</ul>";
  return html;
}

// ---------- Kölner Phonetik (Klangähnlichkeit, für deutsche Aussprache) ----------
export function koelner(wort) {
  const t = String(wort || "").toLowerCase()
    .replace(/ä/g, "a").replace(/ö/g, "o").replace(/ü/g, "u").replace(/ß/g, "s").replace(/[^a-z]/g, "");
  const hat = (menge, z) => !!z && menge.includes(z);
  let code = "";
  for (let i = 0; i < t.length; i++) {
    const c = t[i], v = t[i - 1] || "", n = t[i + 1] || "";
    if (hat("aeijouy", c)) code += "0";
    else if (c === "h") continue;
    else if (c === "b") code += "1";
    else if (c === "p") code += n === "h" ? "3" : "1";
    else if (c === "d" || c === "t") code += hat("csz", n) ? "8" : "2";
    else if (hat("fvw", c)) code += "3";
    else if (hat("gkq", c)) code += "4";
    else if (c === "c") {
      if (i === 0) code += hat("ahkloqrux", n) ? "4" : "8";
      else code += hat("sz", v) ? "8" : (hat("ahkoqux", n) ? "4" : "8");
    }
    else if (c === "x") code += hat("ckq", v) ? "8" : "48";
    else if (c === "l") code += "5";
    else if (c === "m" || c === "n") code += "6";
    else if (c === "r") code += "7";
    else if (c === "s" || c === "z") code += "8";
  }
  let out = "";
  for (const z of code) if (z !== out[out.length - 1]) out += z;
  return out ? out[0] + out.slice(1).replace(/0/g, "") : "";
}

// ---------- Suche ----------
function levenshtein(a, b) {
  if (Math.abs(a.length - b.length) > 2) return 99;
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
  for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++)
    for (let j = 1; j <= b.length; j++)
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
  return d[a.length][b.length];
}

export function suche(eintraege, anfrage) {
  const q = norm(anfrage);
  if (!q) return [];
  const qKlang = q.length >= 3 ? koelner(q) : "";
  const treffer = [];
  for (const e of eintraege) {
    const keys = e.schluessel || schluesselFuer(e);
    let p = 0;
    if (keys.includes(q)) p = 100;
    else if (keys.some(k => k.startsWith(q))) p = 70;
    else if (keys.some(k => k.includes(q))) p = 50;
    else if (qKlang.length >= 2 && keys.some(k => koelner(k) === qKlang)) p = 45;
    else if (q.length >= 5 && keys.some(k => levenshtein(k, q) <= (q.length > 8 ? 2 : 1))) p = 40;
    else if (q.length >= 3 && norm((e.abschnitte || []).map(a => a.text).join(" ")).includes(q)) p = 10;
    if (p) treffer.push({ e, p });
  }
  return treffer.sort((a, b) => b.p - a.p || a.e.titel.localeCompare(b.e.titel, "de")).map(t => ({ ...t.e, _punkte: t.p }));
}

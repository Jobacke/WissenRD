// Wissen RD – Hauptlogik
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js";
import {
  getAuth, onAuthStateChanged, signInWithEmailAndPassword, signOut, sendPasswordResetEmail,
  setPersistence, browserLocalPersistence
} from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";
import {
  initializeFirestore, persistentLocalCache, persistentMultipleTabManager,
  collection, doc, onSnapshot, writeBatch, serverTimestamp, increment
} from "https://www.gstatic.com/firebasejs/10.12.4/firebase-firestore.js";
import { firebaseConfig } from "./firebase-config.js";
import { BEREICHE } from "./bereiche.js";
import {
  norm, schluesselFuer, slugFuer, markdownFuer, vorlesetextFuer, htmlAusText, suche
} from "./text.js";

const VERSION = `v${self.APP_VERSION} (Build ${self.APP_BUILD})`;
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = initializeFirestore(app, {
  localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() })
});

const $ = s => document.querySelector(s);
const inhalt = $("#inhalt");
const st = { user: null, eintraege: [], geladen: false, datenversion: 0, abmelden: [],
  reihenfolge: lokaleReihenfolge(), anordnen: false };

// ---------------- Reihenfolge der Bereiche (frei anordnbar, in meta/einstellungen gespeichert) ----------------
function lokaleReihenfolge() {
  try { return JSON.parse(localStorage.getItem("wrd-reihenfolge")) || []; } catch { return []; }
}
function bereicheSortiert(reihenfolge = st.reihenfolge) {
  const alle = Object.keys(BEREICHE);
  const ord = [...reihenfolge.filter(k => alle.includes(k)), ...alle.filter(k => !reihenfolge.includes(k))];
  return ord.map(k => [k, BEREICHE[k]]);
}

const esc = s => String(s ?? "").replace(/[&<>"']/g, c =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function hinweis(text, fehler = false) {
  const t = $("#toast");
  t.textContent = text;
  t.className = "toast sichtbar" + (fehler ? " fehler" : "");
  clearTimeout(hinweis._t);
  hinweis._t = setTimeout(() => (t.className = "toast"), 3500);
}

// ---------------- Start & Anmeldung ----------------
$("#version").textContent = VERSION;

// ?q=ACS aus dem Kurzbefehl → Suche
const startParam = new URLSearchParams(location.search).get("q");
if (startParam) {
  history.replaceState(null, "", location.pathname + "#/suche/" + encodeURIComponent(startParam));
}

setPersistence(auth, browserLocalPersistence).catch(() => {});
onAuthStateChanged(auth, user => {
  st.abmelden.forEach(f => f());
  st.abmelden = [];
  st.user = user;
  document.body.classList.toggle("angemeldet", !!user);
  if (!user) { st.eintraege = []; st.geladen = false; zeigeLogin(); return; }
  st.syncGeprueft = false;
  setTimeout(() => { st.syncGeprueft = true; zeigeStand(); }, 4000);
  st.abmelden.push(onSnapshot(collection(db, "eintraege"), { includeMetadataChanges: true }, snap => {
    // Offline-Status: Daten liegen dauerhaft im Gerätespeicher (persistentLocalCache)
    st.ausCache = snap.metadata.fromCache;
    if (!snap.metadata.fromCache) merkeSync();
    zeigeStand();
    if (st.geladen && snap.docChanges().length === 0) return; // nur Statuswechsel, nichts neu zeichnen
    st.eintraege = snap.docs.map(d => ({ id: d.id, ...d.data() }))
      .sort((a, b) => a.titel.localeCompare(b.titel, "de"));
    const ersterLauf = !st.geladen;
    st.geladen = true;
    // Formulare nicht durch Live-Updates überschreiben
    if (ersterLauf || !/^#\/(neu|bearbeiten|einstellungen)/.test(location.hash)) route();
  }, err => hinweis("Laden fehlgeschlagen: " + err.message, true)));
  st.abmelden.push(onSnapshot(doc(db, "meta", "einstellungen"), d => {
    const r = d.exists() ? d.data().bereichReihenfolge || [] : [];
    if (JSON.stringify(r) === JSON.stringify(st.reihenfolge)) return;
    st.reihenfolge = r;
    try { localStorage.setItem("wrd-reihenfolge", JSON.stringify(r)); } catch { /* egal */ }
    if (st.geladen && !st.anordnen) route();
  }, () => {}));
  st.abmelden.push(onSnapshot(doc(db, "meta", "stand"), d => {
    st.datenversion = d.exists() ? d.data().datenversion || 0 : 0;
    zeigeStand();
  }));
});

// ---------------- Offline-Anzeige ----------------
function merkeSync() {
  try { localStorage.setItem("wrd-sync", new Date().toISOString()); } catch { /* egal */ }
}
function letzterSync() {
  try {
    const v = localStorage.getItem("wrd-sync");
    return v ? new Date(v).toLocaleString("de-DE", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }) : "";
  } catch { return ""; }
}
function zeigeStand() {
  const el = $("#datenstand");
  if (!el) return;
  const offline = !navigator.onLine || (st.ausCache && st.syncGeprueft);
  let t = "Daten #" + st.datenversion;
  if (offline) {
    const s = letzterSync();
    t += " · offline" + (s ? " (Stand " + s + ")" : "");
  }
  el.textContent = t;
  el.classList.toggle("offline", offline);
}
window.addEventListener("online", zeigeStand);
window.addEventListener("offline", zeigeStand);

function zeigeLogin() {
  inhalt.innerHTML = `
    <section class="karte login">
      <h2>Anmelden</h2>
      <p class="leise">Die Wissensdatenbank ist nur für dich zugänglich.</p>
      <label>E-Mail<input id="l-mail" type="email" autocomplete="username"></label>
      <label>Passwort<input id="l-pw" type="password" autocomplete="current-password"></label>
      <button id="l-go" class="primaer">Anmelden</button>
      <button id="l-reset" class="link">Passwort vergessen?</button>
    </section>`;
  $("#l-go").onclick = async () => {
    try { await signInWithEmailAndPassword(auth, $("#l-mail").value.trim(), $("#l-pw").value); }
    catch (e) { hinweis("Anmeldung fehlgeschlagen", true); }
  };
  $("#l-pw").onkeydown = ev => { if (ev.key === "Enter") $("#l-go").click(); };
  $("#l-reset").onclick = async () => {
    const m = $("#l-mail").value.trim();
    if (!m) return hinweis("Bitte zuerst E-Mail eintragen", true);
    await sendPasswordResetEmail(auth, m).catch(() => {});
    hinweis("Falls die Adresse existiert, kommt eine E-Mail.");
  };
}

// ---------------- Routing ----------------
window.addEventListener("hashchange", () => { stoppeVorlesen(); route(); });
function route() {
  if (!st.user) return;
  const h = decodeURIComponent(location.hash.slice(1) || "/");
  const [, teil, rest = ""] = h.split("/");
  const sucheFeld = $("#suche");
  if (teil !== "suche" && document.activeElement !== sucheFeld) sucheFeld.value = "";
  if (teil) st.anordnen = false;
  setzeZurueck(teil, rest);
  setzeBereichsleiste(teil, rest);
  if (teil === "suche" && rest) oeffneSuche(false); else if (document.activeElement !== sucheFeld) schliesseSuche();
  if (!st.geladen) { inhalt.innerHTML = `<p class="leise mitte">Lade Wissen …</p>`; return; }
  switch (teil) {
    case "": return zeigeStart();
    case "suche": sucheFeld.value = rest; return zeigeSuche(rest);
    case "b": return zeigeBereich(rest);
    case "e": return zeigeEintrag(rest);
    case "neu": return zeigeEditor(null, rest);
    case "bearbeiten": return zeigeEditor(rest);
    case "einstellungen": return zeigeEinstellungen();
    default: return zeigeStart();
  }
}

// Zurück-Button: Eintrag → sein Bereich (bzw. Bearbeiten → Eintrag), alles andere → Startseite
function setzeZurueck(teil, rest) {
  const z = $("#zurueck");
  if (!z) return;
  let ziel = "#/";
  if (teil === "e") {
    const e = st.eintraege.find(x => x.id === rest);
    if (e && BEREICHE[e.bereich]) ziel = "#/b/" + e.bereich;
  } else if (teil === "bearbeiten" && rest) ziel = "#/e/" + rest;
  else if (teil === "neu" && BEREICHE[rest]) ziel = "#/b/" + rest;
  z.href = ziel;
  z.hidden = !teil;
}

// ---------------- Bereichsleiste: direkt in jeden Bereich springen ----------------
const KURZNAME = { diagnose: "Diagnosen", algorithmus: "Algorithmen" };
function setzeBereichsleiste(teil, rest) {
  const nav = $("#bereichsleiste");
  if (!nav) return;
  const zeigen = ["b", "e", "suche", "neu", "bearbeiten"].includes(teil);
  nav.hidden = !zeigen;
  if (!zeigen) return;
  let aktiv = "";
  if (teil === "b") aktiv = rest;
  else if (teil === "e" || teil === "bearbeiten") aktiv = st.eintraege.find(x => x.id === rest)?.bereich || "";
  else if (teil === "neu") aktiv = rest;
  nav.innerHTML = bereicheSortiert().map(([k, b]) =>
    `<a class="bchip${k === aktiv ? " aktiv" : ""}" data-b="${k}" href="#/b/${k}"><span>${b.icon}</span>${esc(KURZNAME[k] || b.name)}</a>`).join("");
  const a = nav.querySelector(".aktiv");
  if (a) a.scrollIntoView({ block: "nearest", inline: "center" });
}

// ---------------- Suche: Lupe → Feld, Suchverlauf ----------------
const kopf = $(".kopf");
const VERLAUF = "wrd-suchverlauf";
const TAG = 864e5;
function verlaufLaden() {
  try { return JSON.parse(localStorage.getItem(VERLAUF)) || []; } catch { return []; }
}
function verlaufSpeichern(l) {
  try { localStorage.setItem(VERLAUF, JSON.stringify(l.slice(0, 40))); } catch { /* egal */ }
}
function merkeSuche(q) {
  q = String(q || "").trim();
  if (norm(q).length < 2) return;
  const l = verlaufLaden().filter(x => norm(x.q) !== norm(q));
  l.unshift({ q, t: Date.now() });
  verlaufSpeichern(l);
}
function tagesbeginn(versatz = 0) {
  const d = new Date(); d.setHours(0, 0, 0, 0);
  return d.getTime() - versatz * TAG;
}
// art: "heute" | "gestern" | "7tage" | "alles" → Anzahl gelöschter Einträge
function loescheVerlauf(art) {
  const l = verlaufLaden(), heute = tagesbeginn(0), gestern = tagesbeginn(1), sieben = Date.now() - 7 * TAG;
  const weg = {
    heute: x => x.t >= heute,
    gestern: x => x.t >= gestern && x.t < heute,
    "7tage": x => x.t >= sieben,
    alles: () => true
  }[art];
  const rest = l.filter(x => !weg(x));
  verlaufSpeichern(rest);
  return l.length - rest.length;
}
const VERLAUF_ARTEN = [["heute", "Heute"], ["gestern", "Gestern"], ["7tage", "Letzte 7 Tage"], ["alles", "Alles"]];
function verlaufLoeschenFragen(art) {
  const name = VERLAUF_ARTEN.find(a => a[0] === art)[1];
  if (!confirm(`Suchverlauf „${name}“ löschen?`)) return false;
  const n = loescheVerlauf(art);
  hinweis(n ? `${n} Suche${n === 1 ? "" : "n"} gelöscht` : "Nichts zu löschen");
  return true;
}
function zeitText(t) {
  const d = new Date(t);
  if (t >= tagesbeginn(0)) return "heute " + d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" });
  if (t >= tagesbeginn(1)) return "gestern";
  return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit" });
}
function zeigeVerlauf() {
  const box = $("#verlauf");
  if (!box) return;
  if ($("#suche").value.trim()) { box.hidden = true; return; }
  const l = verlaufLaden().slice(0, 8);
  box.innerHTML = (l.length ? `<div class="v-titel">Zuletzt gesucht</div>` + l.map(x =>
      `<button type="button" class="v-zeile" data-q="${esc(x.q)}"><span>🕘 ${esc(x.q)}</span><small>${zeitText(x.t)}</small></button>`).join("")
      : `<div class="v-leer">Noch kein Suchverlauf</div>`) +
    `<div class="v-loeschen"><span>Löschen:</span>${VERLAUF_ARTEN.map(([k, n]) =>
      `<button type="button" class="v-weg" data-art="${k}">${n}</button>`).join("")}</div>`;
  box.hidden = false;
}
function oeffneSuche(fokus = true) {
  kopf.classList.add("sucht");
  if (fokus) { $("#suche").focus(); zeigeVerlauf(); }
}
function schliesseSuche() {
  if ($("#suche").value.trim()) return;
  kopf.classList.remove("sucht");
  $("#verlauf").hidden = true;
}
$("#such-knopf").onclick = () => oeffneSuche(true);
$("#suche").addEventListener("focus", zeigeVerlauf);
$("#suche").addEventListener("blur", () => setTimeout(() => {
  if (document.activeElement !== $("#suche")) { $("#verlauf").hidden = true; schliesseSuche(); }
}, 150));
// Klicks im Verlauf dürfen das Suchfeld nicht schließen
$("#verlauf").addEventListener("pointerdown", ev => ev.preventDefault());
$("#verlauf").addEventListener("click", ev => {
  const z = ev.target.closest(".v-zeile"), w = ev.target.closest(".v-weg");
  if (z) {
    const q = z.dataset.q;
    $("#suche").value = q;
    merkeSuche(q);
    $("#verlauf").hidden = true;
    location.hash = "#/suche/" + encodeURIComponent(q);
  } else if (w) {
    if (verlaufLoeschenFragen(w.dataset.art)) zeigeVerlauf();
  }
});

let merkTimer;
$("#suche").addEventListener("input", ev => {
  const q = ev.target.value;
  history.replaceState(null, "", "#/suche/" + encodeURIComponent(q));
  zeigeVerlauf();
  zeigeSuche(q);
  clearTimeout(merkTimer);
  merkTimer = setTimeout(() => merkeSuche(q), 2000);   // nach kurzer Tipp-Pause merken
});
$("#suche").addEventListener("keydown", ev => {
  if (ev.key === "Enter") { clearTimeout(merkTimer); merkeSuche(ev.target.value); ev.target.blur(); }
  if (ev.key === "Escape") { ev.target.value = ""; ev.target.blur(); location.hash = "#/"; }
});
// Treffer aus der Suche geöffnet → Suchbegriff merken
document.addEventListener("click", ev => {
  if (ev.target.closest("#inhalt .zeile") && location.hash.startsWith("#/suche/")) {
    clearTimeout(merkTimer); merkeSuche($("#suche").value);
  }
});
if (startParam) merkeSuche(startParam);

// ---------------- Ansichten ----------------
function eintragZeile(e, mitBereich = true) {
  const b = BEREICHE[e.bereich] || { icon: "📌", name: e.bereich };
  return `<a class="zeile" data-b="${esc(e.bereich)}" href="#/e/${esc(e.id)}">
    <span class="z-icon">${b.icon}</span>
    <span class="z-text"><strong>${esc(e.titel)}</strong>${e.kurz && e.kurz !== e.titel ? ` <span class="kurz">${esc(e.kurz)}</span>` : ""}
    ${mitBereich ? `<small>${esc(b.name)}</small>` : ""}</span><span class="pfeil">›</span></a>`;
}

function zeigeStart() {
  const liste = st.anordnen ? st.anordnenListe.map(k => [k, BEREICHE[k]]) : bereicheSortiert();
  const kacheln = liste.map(([k, b]) => {
    const n = st.eintraege.filter(e => e.bereich === k).length;
    const name = b.name.replace("Verdachtsdiagnosen", "Verdachts\u00ADdiagnosen").replace("Abkürzungen", "Abkür\u00ADzungen");
    return `<a class="kachel" data-b="${k}" ${st.anordnen ? "" : `href="#/b/${k}"`}><span class="k-icon">${b.icon}</span>
      <span class="k-name">${name}</span><small>${st.anordnen ? "⠿" : n}</small></a>`;
  }).join("");
  const zuletzt = [...st.eintraege]
    .sort((a, b) => (b.geaendert?.seconds || 0) - (a.geaendert?.seconds || 0)).slice(0, 5);
  if (st.anordnen) {
    inhalt.innerHTML = `
      <p class="anordnen-hinweis">Kacheln an die gewünschte Stelle ziehen</p>
      <section class="kacheln anordnen" id="kacheln">${kacheln}</section>
      <div class="start-leiste">
        <button id="ord-fertig" class="primaer">✓ Fertig</button>
        <button id="ord-reset" class="sekundaer">Standard</button>
        <button id="ord-abbruch" class="link">Abbrechen</button>
      </div>`;
    aktiviereZiehen($("#kacheln"));
    $("#ord-fertig").onclick = speichereReihenfolge;
    $("#ord-reset").onclick = () => { st.anordnenListe = Object.keys(BEREICHE); zeigeStart(); };
    $("#ord-abbruch").onclick = () => { st.anordnen = false; zeigeStart(); };
    return;
  }
  inhalt.innerHTML = `
    <section class="kacheln">${kacheln}</section>
    <div class="start-leiste">
      ${zuletzt.length ? `<details class="zuletzt"><summary>🕘 Zuletzt geändert</summary>
        <section class="liste">${zuletzt.map(eintragZeile).join("")}</section></details>` : ""}
      <button id="anordnen" class="pille">↕ Anordnen</button>
    </div>
    ${zuletzt.length ? "" : `<p class="leise">Noch keine Einträge – lege den ersten an oder importiere Daten (⚙️).</p>`}
    <a class="fab" href="#/neu/" title="Neuer Eintrag" aria-label="Neuer Eintrag">＋</a>`;
  $("#anordnen").onclick = () => {
    st.anordnen = true;
    st.anordnenListe = bereicheSortiert().map(([k]) => k);
    zeigeStart();
  };
}

// Ziehen per Finger oder Maus (Pointer-Events), ohne Bibliothek
function aktiviereZiehen(box) {
  let zieht = null;
  box.addEventListener("pointerdown", ev => {
    const k = ev.target.closest(".kachel");
    if (!k) return;
    ev.preventDefault();
    zieht = k;
    k.classList.add("zieht");
    k.setPointerCapture(ev.pointerId);
  });
  box.addEventListener("pointermove", ev => {
    if (!zieht) return;
    const unter = document.elementFromPoint(ev.clientX, ev.clientY)?.closest(".kachel");
    if (!unter || unter === zieht || unter.parentNode !== box) return;
    const kinder = [...box.children];
    if (kinder.indexOf(zieht) < kinder.indexOf(unter)) unter.after(zieht); else unter.before(zieht);
    if (navigator.vibrate) navigator.vibrate(8);
  });
  const ende = () => {
    if (!zieht) return;
    zieht.classList.remove("zieht");
    zieht = null;
    st.anordnenListe = [...box.children].map(k => k.dataset.b);
  };
  box.addEventListener("pointerup", ende);
  box.addEventListener("pointercancel", ende);
}

async function speichereReihenfolge() {
  const r = [...st.anordnenListe];
  st.reihenfolge = r;
  st.anordnen = false;
  try { localStorage.setItem("wrd-reihenfolge", JSON.stringify(r)); } catch { /* egal */ }
  zeigeStart();
  try {
    const b = writeBatch(db);
    b.set(doc(db, "meta", "einstellungen"), { bereichReihenfolge: r, geaendert: serverTimestamp() }, { merge: true });
    await b.commit();
    hinweis("Reihenfolge gespeichert – gilt auf allen Geräten");
  } catch (err) {
    hinweis("Nur auf diesem Gerät gespeichert: " + err.message, true);
  }
}

function zeigeSuche(q) {
  const t = suche(st.eintraege, q);
  if (!norm(q)) return zeigeStart();
  // Genau ein exakter Treffer (z. B. vom Kurzbefehl) → direkt öffnen
  const exakt = t.filter(x => x._punkte === 100);
  const vonSiri = !!startParam && norm(q) === norm(startParam);
  if (vonSiri && exakt.length === 1) {
    history.replaceState(null, "", "#/e/" + exakt[0].id);
    return zeigeEintrag(exakt[0].id);
  }
  // Lernschleife: kein exakter Treffer → Begriff einem Eintrag zuordnen
  const lernen = !exakt.length && norm(q).length >= 2 && st.eintraege.length ? lernBlock(q, t, vonSiri) : "";
  inhalt.innerHTML = `
    ${vonSiri ? lernen : ""}
    <h3>${t.length} Treffer für „${esc(q)}“</h3>
    <section class="liste">${t.map(eintragZeile).join("")}</section>
    ${t.length ? "" : `<p class="leise">Nichts gefunden.</p>`}
    ${!vonSiri && lernen ? `<details class="lernen-klein"><summary>„${esc(q)}“ einem Eintrag als Suchbegriff zuordnen</summary>${lernen}</details>` : ""}
    <a class="sekundaer breit" id="neu-aus-suche" href="#/neu/">＋ „${esc(q)}“ neu anlegen</a>`;
  $("#neu-aus-suche").onclick = () => { sessionStorage.setItem("neuTitel", q); };
  inhalt.querySelectorAll("button.lern").forEach(b => (b.onclick = () => lerneBegriff(b.dataset.id, q)));
  const ok = $("#lern-ok");
  if (ok) ok.onclick = () => {
    const id = $("#lern-auswahl").value;
    if (!id) return hinweis("Bitte einen Eintrag auswählen", true);
    lerneBegriff(id, q);
  };
}

function lernBlock(q, treffer, prominent) {
  const vorschlaege = treffer.slice(0, 4);
  const optionen = Object.entries(BEREICHE).map(([k, b]) => {
    const l = st.eintraege.filter(e => e.bereich === k);
    return l.length ? `<optgroup label="${b.icon} ${esc(b.name)}">${l.map(e =>
      `<option value="${esc(e.id)}">${esc(e.titel)}${e.kurz && e.kurz !== e.titel ? " (" + esc(e.kurz) + ")" : ""}</option>`).join("")}</optgroup>` : "";
  }).join("");
  return `<section class="karte lernen${prominent ? " siri" : ""}">
    <h3>${prominent ? `🎙️ Siri hat „${esc(q)}“ verstanden` : `„${esc(q)}“ zuordnen`}</h3>
    <p class="leise">Zu welchem Eintrag gehört das? „${esc(q)}“ wird dort als Suchbegriff gespeichert – beim nächsten Mal findet Siri den Eintrag direkt.</p>
    ${vorschlaege.length ? `<div class="chips">${vorschlaege.map(e =>
      `<button class="chip lern" data-id="${esc(e.id)}">${esc(e.kurz || e.titel)}</button>`).join("")}</div>` : ""}
    <div class="lern-zeile"><select id="lern-auswahl"><option value="">anderer Eintrag …</option>${optionen}</select>
      <button id="lern-ok" class="sekundaer">Zuordnen</button></div>
  </section>`;
}

async function lerneBegriff(id, begriff) {
  const alt = st.eintraege.find(x => x.id === id);
  if (!alt) return;
  begriff = begriff.trim();
  if ((alt.schluessel || []).includes(norm(begriff))) { location.hash = "#/e/" + id; return; }
  try {
    await speichere({ ...alt, suchbegriffe: [...(alt.suchbegriffe || []), begriff] }, alt);
    hinweis(`„${begriff}“ gehört jetzt zu ${alt.kurz || alt.titel}`);
    location.hash = "#/e/" + id;
  } catch (err) {
    hinweis("Speichern fehlgeschlagen: " + (err.code === "permission-denied" ? "keine Schreibrechte" : err.message), true);
  }
}

function zeigeBereich(k) {
  const b = BEREICHE[k];
  if (!b) return zeigeStart();
  const liste = st.eintraege.filter(e => e.bereich === k);
  inhalt.innerHTML = `
    <h2>${b.icon} ${b.name} <span class="kurz">${liste.length}</span></h2>
    <section class="liste">${liste.map(e => eintragZeile(e, false)).join("") || `<p class="leise">Noch leer.</p>`}</section>
    <a class="fab" href="#/neu/${k}" title="Neuer Eintrag in ${esc(b.name)}" aria-label="Neuer Eintrag">＋</a>`;
}

function zeigeEintrag(id) {
  const e = st.eintraege.find(x => x.id === id);
  if (!e) { inhalt.innerHTML = `<p class="leise mitte">Eintrag nicht gefunden.</p>`; return; }
  const b = BEREICHE[e.bereich] || { icon: "📌", name: e.bereich };
  const tel = !!b.telefon;
  const abschnitte = (e.abschnitte || []).filter(a => a.text && a.text.trim()).map(a => `
    <section class="abschnitt"><h4>${esc(a.titel)}</h4>${htmlAusText(a.text, tel)}</section>`).join("");
  const siehe = (e.siehe || []).map(s => `<a class="chip" href="#/suche/${encodeURIComponent(s)}">${esc(s)}</a>`).join("");
  const geaendert = e.geaendert?.toDate ? e.geaendert.toDate().toLocaleString("de-DE") : "";
  inhalt.innerHTML = `
    <article class="eintrag">
      <a class="badge" href="#/b/${esc(e.bereich)}">${b.icon} ${esc(b.name)}</a>
      <h2>${esc(e.titel)}${e.kurz && e.kurz !== e.titel ? ` <span class="kurz">${esc(e.kurz)}</span>` : ""}</h2>
      <div class="aktionen">
        <button id="vorlesen" class="primaer">🔊 Vorlesen</button>
        <a class="sekundaer" href="#/bearbeiten/${esc(e.id)}">✏️ Bearbeiten</a>
      </div>
      ${abschnitte || `<p class="leise">Noch kein Inhalt.</p>`}
      ${siehe ? `<section class="abschnitt"><h4>Siehe auch</h4><div class="chips">${siehe}</div></section>` : ""}
      <footer class="meta">${e.quelle ? "Quelle: " + esc(e.quelle) + "<br>" : ""}
        ${e.stand ? "Stand: " + esc(e.stand) + " · " : ""}Rev. ${e.revision || 1}${geaendert ? " · geändert " + geaendert : ""}</footer>
    </article>`;
  $("#vorlesen").onclick = () => {
    if (speechSynthesis.speaking) { stoppeVorlesen(); return; }
    vorlesen(e.vorlesen || vorlesetextFuer(e));
  };
}

// ---------------- Editor ----------------
function zeigeEditor(id, bereichVorgabe) {
  const alt = id ? st.eintraege.find(x => x.id === id) : null;
  if (id && !alt) return zeigeStart();
  const startBereich = alt?.bereich || (BEREICHE[bereichVorgabe] ? bereichVorgabe : "diagnose");
  const neuTitel = sessionStorage.getItem("neuTitel") || "";
  sessionStorage.removeItem("neuTitel");
  const e = alt ? structuredClone({ ...alt, geaendert: null, erstellt: null }) : {
    bereich: startBereich, titel: neuTitel, kurz: "", suchbegriffe: [], siehe: [],
    abschnitte: BEREICHE[startBereich].vorlage.map(t => ({ titel: t, text: "" })),
    sprechtext: "", quelle: "", stand: new Date().toISOString().slice(0, 7)
  };
  let abschnitteBeruehrt = !!alt;

  inhalt.innerHTML = `
    <section class="karte editor">
      <h2>${alt ? "Eintrag bearbeiten" : "Neuer Eintrag"}</h2>
      <label>Bereich<select id="f-bereich">${bereicheSortiert().map(([k, b]) =>
        `<option value="${k}" ${k === e.bereich ? "selected" : ""}>${b.icon} ${b.name}</option>`).join("")}</select></label>
      <label>Titel<input id="f-titel" value="${esc(e.titel)}" placeholder="z. B. Akutes Koronarsyndrom"></label>
      <label>Kurzform / Abkürzung<input id="f-kurz" value="${esc(e.kurz)}" placeholder="z. B. ACS"></label>
      <label>Weitere Suchbegriffe <small>(kommagetrennt – so, wie du es zu Siri sagen würdest)</small>
        <input id="f-such" value="${esc((e.suchbegriffe || []).join(", "))}" placeholder="Herzinfarkt, STEMI, Brustschmerz"></label>
      <div id="f-abschnitte"></div>
      <button id="f-plus" class="sekundaer">＋ Abschnitt</button>
      <p class="leise">Formatierung: Zeile mit „- “ = Aufzählung, **fett**.</p>
      <label>Eigener Vorlesetext <small>(optional – sonst wird der Inhalt vorgelesen)</small>
        <textarea id="f-sprech" rows="3">${esc(e.sprechtext)}</textarea></label>
      <label>Siehe auch <small>(kommagetrennt)</small><input id="f-siehe" value="${esc((e.siehe || []).join(", "))}"></label>
      <label>Quelle<input id="f-quelle" value="${esc(e.quelle)}" placeholder="z. B. SAA ÄLRD Bayern 2025"></label>
      <label>Stand<input id="f-stand" value="${esc(e.stand)}" placeholder="JJJJ-MM"></label>
      <div class="aktionen">
        <button id="f-speichern" class="primaer">💾 Speichern</button>
        <a class="sekundaer" href="${alt ? "#/e/" + esc(alt.id) : "#/"}">Abbrechen</a>
        ${alt ? `<button id="f-loeschen" class="gefahr">🗑 Löschen</button>` : ""}
      </div>
    </section>`;

  const box = $("#f-abschnitte");
  const zeichne = () => {
    box.innerHTML = e.abschnitte.map((a, i) => `
      <div class="abschnitt-edit">
        <div class="ae-kopf">
          <input data-i="${i}" data-f="titel" value="${esc(a.titel)}">
          <button data-i="${i}" data-a="hoch" title="nach oben">↑</button>
          <button data-i="${i}" data-a="runter" title="nach unten">↓</button>
          <button data-i="${i}" data-a="weg" title="entfernen">✕</button>
        </div>
        <textarea data-i="${i}" data-f="text" rows="${Math.max(3, (a.text.match(/\n/g) || []).length + 2)}">${esc(a.text)}</textarea>
      </div>`).join("");
  };
  zeichne();
  box.addEventListener("input", ev => {
    const i = ev.target.dataset.i, f = ev.target.dataset.f;
    if (i !== undefined && f) { e.abschnitte[i][f] = ev.target.value; abschnitteBeruehrt = true; }
  });
  box.addEventListener("click", ev => {
    const i = +ev.target.dataset.i, a = ev.target.dataset.a;
    if (!a) return;
    const L = e.abschnitte;
    if (a === "weg") L.splice(i, 1);
    if (a === "hoch" && i > 0) [L[i - 1], L[i]] = [L[i], L[i - 1]];
    if (a === "runter" && i < L.length - 1) [L[i + 1], L[i]] = [L[i], L[i + 1]];
    abschnitteBeruehrt = true;
    zeichne();
  });
  $("#f-plus").onclick = () => { e.abschnitte.push({ titel: "Neuer Abschnitt", text: "" }); zeichne(); };
  $("#f-bereich").onchange = ev => {
    e.bereich = ev.target.value;
    if (!abschnitteBeruehrt) {
      e.abschnitte = BEREICHE[e.bereich].vorlage.map(t => ({ titel: t, text: "" }));
      zeichne();
    }
  };
  const liste = s => s.split(",").map(x => x.trim()).filter(Boolean);

  $("#f-speichern").onclick = async () => {
    e.titel = $("#f-titel").value.trim();
    if (!e.titel) return hinweis("Titel fehlt", true);
    e.kurz = $("#f-kurz").value.trim();
    e.suchbegriffe = liste($("#f-such").value);
    e.siehe = liste($("#f-siehe").value);
    e.sprechtext = $("#f-sprech").value.trim();
    e.quelle = $("#f-quelle").value.trim();
    e.stand = $("#f-stand").value.trim();
    try {
      const neueId = await speichere(e, alt);
      hinweis("Gespeichert");
      location.hash = "#/e/" + neueId;
    } catch (err) {
      hinweis("Speichern fehlgeschlagen: " + (err.code === "permission-denied" ? "keine Schreibrechte" : err.message), true);
    }
  };
  if (alt) $("#f-loeschen").onclick = async () => {
    if (!confirm(`„${alt.titel}“ endgültig löschen?`)) return;
    try {
      const b = writeBatch(db);
      b.delete(doc(db, "eintraege", alt.id));
      b.set(doc(db, "meta", "stand"), { datenversion: increment(1), geaendert: serverTimestamp() }, { merge: true });
      await b.commit();
      hinweis("Gelöscht");
      location.hash = "#/b/" + alt.bereich;
    } catch (err) { hinweis("Löschen fehlgeschlagen: " + err.message, true); }
  };
}

function bereinigt(e) {
  return {
    bereich: e.bereich, titel: e.titel, kurz: e.kurz || "",
    suchbegriffe: e.suchbegriffe || [], siehe: e.siehe || [],
    abschnitte: (e.abschnitte || []).map(a => ({ titel: a.titel || "", text: a.text || "" })),
    sprechtext: e.sprechtext || "", quelle: e.quelle || "", stand: e.stand || ""
  };
}

function eindeutigeId(e) {
  const basis = slugFuer(e);
  let id = basis, n = 2;
  while (st.eintraege.some(x => x.id === id)) id = basis + "-" + n++;
  return id;
}

// Speichert einen Eintrag inkl. der für Siri vorberechneten Felder
async function speichere(e, alt, batch = null) {
  const id = alt?.id || e.id && !st.eintraege.some(x => x.id === e.id) && e.id || eindeutigeId(e);
  const daten = bereinigt(e);
  daten.revision = (alt?.revision || 0) + 1;
  daten.schluessel = schluesselFuer(daten);
  daten.markdown = markdownFuer(daten);
  daten.vorlesen = vorlesetextFuer(daten);
  daten.geaendert = serverTimestamp();
  daten.geaendertVon = st.user?.email || "";
  if (!alt) daten.erstellt = serverTimestamp();
  const eigen = !batch;
  const b = batch || writeBatch(db);
  b.set(doc(db, "eintraege", id), daten, { merge: true });
  if (eigen) {
    b.set(doc(db, "meta", "stand"), { datenversion: increment(1), geaendert: serverTimestamp() }, { merge: true });
    await b.commit();
  }
  return id;
}

// ---------------- Einstellungen ----------------
function zeigeEinstellungen() {
  const rate = localStorage.getItem("rate") || "1.0";
  inhalt.innerHTML = `
    <section class="karte">
      <h2>⚙️ Einstellungen</h2>
      <dl class="info">
        <dt>App-Version</dt><dd>${VERSION} · ${self.APP_DATUM}</dd>
        <dt>Datenstand</dt><dd>#${st.datenversion} · ${st.eintraege.length} Einträge</dd>
        <dt>Angemeldet</dt><dd>${esc(st.user.email)}</dd>
      </dl>
      <h3>Vorlesen</h3>
      <label>Geschwindigkeit <output id="rate-w">${rate}</output>
        <input id="rate" type="range" min="0.7" max="1.5" step="0.1" value="${rate}"></label>
      <label>Stimme<select id="stimme"></select></label>
      <button id="test-stimme" class="sekundaer">🔊 Test</button>

      <h3>Suchverlauf</h3>
      <p class="leise" id="verlauf-anzahl">${verlaufLaden().length} gespeicherte Suchen (nur auf diesem Gerät)</p>
      <div class="aktionen">${VERLAUF_ARTEN.map(([k, n]) =>
        `<button class="sekundaer v-weg-e" data-art="${k}">🗑 ${n}</button>`).join("")}</div>

      <h3>Daten</h3>
      <div class="aktionen">
        <button id="export" class="sekundaer">⬇️ Export (JSON)</button>
        <label class="sekundaer datei">⬆️ Import (JSON)<input id="import" type="file" accept=".json,application/json" hidden></label>
      </div>
      <p class="leise">Import überschreibt Einträge mit gleicher ID (eigene Suchbegriffe bleiben erhalten). ÄLRD-Bayern-Daten: <code>daten/aelrd-bayern-import.json</code></p>

      <h3>Für den Siri-Kurzbefehl</h3>
      <dl class="info klein">
        <dt>API-Key</dt><dd><code>${esc(firebaseConfig.apiKey)}</code></dd>
        <dt>Projekt-ID</dt><dd><code>${esc(firebaseConfig.projectId)}</code></dd>
        <dt>App-URL</dt><dd><code>${esc(location.origin + location.pathname)}</code></dd>
      </dl>

      <h3>Änderungsprotokoll</h3>
      <pre id="changelog" class="changelog">lädt …</pre>
      <button id="abmelden" class="gefahr">Abmelden</button>
    </section>`;

  inhalt.querySelectorAll(".v-weg-e").forEach(b => (b.onclick = () => {
    if (verlaufLoeschenFragen(b.dataset.art))
      $("#verlauf-anzahl").textContent = `${verlaufLaden().length} gespeicherte Suchen (nur auf diesem Gerät)`;
  }));
  $("#rate").oninput = ev => { localStorage.setItem("rate", ev.target.value); $("#rate-w").textContent = ev.target.value; };
  const fuelleStimmen = () => {
    const sel = $("#stimme"); if (!sel) return;
    const gew = localStorage.getItem("stimme") || "";
    const st2 = speechSynthesis.getVoices().filter(v => v.lang.replace("_", "-").startsWith("de"));
    const auto = besteStimme();
    sel.innerHTML = `<option value="">Automatisch (${esc(auto ? auto.name : "Deutsch")})</option>` +
      st2.map(v => `<option value="${esc(v.name)}" ${v.name === gew ? "selected" : ""}>${esc(v.name)}${v.localService ? "" : " ☁️"}</option>`).join("");
  };
  fuelleStimmen();
  speechSynthesis.onvoiceschanged = fuelleStimmen;
  $("#stimme").onchange = ev => localStorage.setItem("stimme", ev.target.value);
  $("#test-stimme").onclick = () => vorlesen("Akutes Koronarsyndrom. 12-Kanal-EKG innerhalb von 10 Minuten.");

  $("#export").onclick = () => {
    const daten = st.eintraege.map(e => ({ id: e.id, ...bereinigt(e) }));
    const blob = new Blob([JSON.stringify({ app: "Wissen RD", version: self.APP_VERSION,
      exportiert: new Date().toISOString(), eintraege: daten }, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `wissen-export-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
  };
  $("#import").onchange = async ev => {
    const datei = ev.target.files[0]; if (!datei) return;
    try {
      const json = JSON.parse(await datei.text());
      const liste = Array.isArray(json) ? json : json.eintraege;
      if (!Array.isArray(liste)) throw new Error("Keine Einträge in der Datei");
      if (!confirm(`${liste.length} Einträge importieren?`)) return;
      for (let i = 0; i < liste.length; i += 400) {
        const b = writeBatch(db);
        for (const roh of liste.slice(i, i + 400)) {
          const alt = roh.id ? st.eintraege.find(x => x.id === roh.id) : null;
          // eigene / per Siri gelernte Suchbegriffe beim Überschreiben behalten
          if (alt) roh.suchbegriffe = [...new Set([...(roh.suchbegriffe || []), ...(alt.suchbegriffe || [])])];
          await speichere(roh, alt, b);
        }
        b.set(doc(db, "meta", "stand"), { datenversion: increment(1), geaendert: serverTimestamp() }, { merge: true });
        await b.commit();
      }
      hinweis(`${liste.length} Einträge importiert`);
    } catch (err) { hinweis("Import fehlgeschlagen: " + err.message, true); }
    ev.target.value = "";
  };
  fetch("CHANGELOG.md", { cache: "no-store" }).then(r => r.text())
    .then(t => { const c = $("#changelog"); if (c) c.textContent = t; })
    .catch(() => { const c = $("#changelog"); if (c) c.textContent = "offline nicht verfügbar"; });
  $("#abmelden").onclick = () => signOut(auth);
}

// ---------------- Vorlesen ----------------
// Beste deutsche Stimme: gewählte > Premium/Erweitert > Google > irgendeine deutsche
function besteStimme() {
  const alle = speechSynthesis.getVoices().filter(v => v.lang.replace("_", "-").startsWith("de"));
  const name = localStorage.getItem("stimme");
  return alle.find(v => v.name === name)
    || alle.find(v => /premium|erweitert|enhanced|siri/i.test(v.name + " " + v.voiceURI))
    || alle.find(v => /google/i.test(v.name))
    || alle.find(v => v.lang.replace("_", "-") === "de-DE") || alle[0] || null;
}
// Text in größere Stücke teilen (ca. 250 Zeichen, an Satzgrenzen) – flüssiger als Satz für Satz,
// aber kurz genug, dass Chrome/iOS lange Texte nicht abbrechen
function stuecke(text, max = 250) {
  const saetze = text.match(/[^.!?]+[.!?]*\s*/g) || [text];
  const out = []; let akt = "";
  for (const s of saetze) {
    if ((akt + s).length > max && akt) { out.push(akt.trim()); akt = ""; }
    akt += s;
  }
  if (akt.trim()) out.push(akt.trim());
  return out;
}
function vorlesen(text) {
  stoppeVorlesen();
  const rate = parseFloat(localStorage.getItem("rate") || "1.0");
  const stimme = besteStimme();
  const teile = stuecke(text);
  teile.forEach((s, i) => {
    const u = new SpeechSynthesisUtterance(s);
    u.lang = "de-DE"; u.rate = rate; if (stimme) u.voice = stimme;
    if (i === teile.length - 1) u.onend = setzeKnopf;
    speechSynthesis.speak(u);
  });
  setzeKnopf(true);
}
function stoppeVorlesen() { if (speechSynthesis.speaking || speechSynthesis.pending) speechSynthesis.cancel(); setzeKnopf(); }
function setzeKnopf(laeuft = false) {
  const k = $("#vorlesen"); if (k) k.textContent = laeuft === true ? "⏹ Stopp" : "🔊 Vorlesen";
}

// ---------------- Service Worker & Updates ----------------
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("sw.js").then(reg => {
    const zeigeUpdate = w => {
      const leiste = $("#update");
      leiste.hidden = false;
      leiste.onclick = () => w.postMessage("skipWaiting");
    };
    if (reg.waiting) zeigeUpdate(reg.waiting);
    reg.addEventListener("updatefound", () => {
      const w = reg.installing;
      w.addEventListener("statechange", () => {
        if (w.state === "installed" && navigator.serviceWorker.controller) zeigeUpdate(w);
      });
    });
    document.addEventListener("visibilitychange", () => { if (!document.hidden) reg.update(); });
  });
  let neuGeladen = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (!neuGeladen) { neuGeladen = true; location.reload(); }
  });
}

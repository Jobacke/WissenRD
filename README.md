# Wissen RD 🩺💬

Persönliche Wissensdatenbank für den Rettungsdienst – per Siri abrufbar, auf allen Geräten synchron, mit Sprachausgabe.

- Konzept: [`docs/KONZEPT.md`](docs/KONZEPT.md)
- Siri-Kurzbefehl: [`docs/KURZBEFEHL.md`](docs/KURZBEFEHL.md)
- Änderungen: [`CHANGELOG.md`](CHANGELOG.md)

---

## Umsetzung Schritt für Schritt

Jede Phase endet mit einem ✅-Test. Erst weitermachen, wenn der Test klappt.

### Phase 1 – Firebase einrichten (ca. 15 min)

1. <https://console.firebase.google.com> → **Projekt hinzufügen** → Name `wissen-rd` → Google Analytics **aus**.
2. **Authentication** → *Jetzt starten* → Anmeldemethode **E-Mail/Passwort** aktivieren.
3. Authentication → **Nutzer** → *Nutzer hinzufügen*:
   - dein Konto (deine E-Mail + sicheres Passwort)
   - das **Siri-Lesekonto**, z. B. `siri@wissen-rd.app` mit eigenem Passwort (die Adresse muss nicht existieren)
4. Bei beiden Konten die **Nutzer-UID** kopieren (Spalte rechts).
5. **Firestore Database** → *Datenbank erstellen* → Standort **eur3 (Europe)** → *Produktionsmodus*.
6. Firestore → **Regeln**: Inhalt von `firestore.rules` einfügen, `UID_JOHANNES` und `UID_SIRI` ersetzen → **Veröffentlichen**.
7. Authentication → **Einstellungen** → *Nutzeraktionen*: **„Registrierung aktivieren“ ausschalten** (niemand kann sich selbst Konten anlegen).
8. ⚙️ Projekteinstellungen → *Meine Apps* → **Web-App (</>)** hinzufügen, Name `Wissen RD`, *kein* Hosting → die angezeigte `firebaseConfig` in `js/firebase-config.js` eintragen.

✅ *Test:* In Firestore → Regeln → **Regel-Playground** „get /eintraege/acs“ ohne Anmeldung simulieren → muss **abgelehnt** werden.

### Phase 2 – App veröffentlichen auf GitHub Pages (ca. 10 min)

1. Auf GitHub neues Repository **`WissenRD`** (öffentlich – es enthält nur Programmcode, keine Inhalte).
2. Inhalt dieses Ordners hochladen (GitHub Desktop, `git push` oder per Drag & Drop im Browser).
3. Repository → **Settings → Pages** → Source *Deploy from a branch* → `main` / `(root)` → Save.
4. Nach ca. 1 min erreichbar unter `https://jobacke.github.io/WissenRD/`.

✅ *Test:* Seite im Browser öffnen → Anmeldemaske erscheint, unten steht **v1.0.0 (Build 1)**.

### Phase 3 – Erste Inhalte (ca. 10 min)

1. Mit **deinem** Konto anmelden.
2. ⚙️ → **Import (JSON)** → `daten/beispiel-eintraege.json` wählen → Beispiel „ACS“ und „STEMI“ sind da.
3. Eintrag „ACS“ öffnen → 🔊 **Vorlesen** testen → ✏️ **Bearbeiten** → im Abschnitt *Medikamente* deine SAA-Vorgaben eintragen → Speichern.
4. iPhone: Seite in Safari öffnen → Teilen → **Zum Home-Bildschirm**.

✅ *Test:* Unten zählt **Daten #** hoch, auf einem zweiten Gerät erscheint die Änderung sofort.

### Phase 4 – Siri-Kurzbefehl (ca. 30 min)

Nach [`docs/KURZBEFEHL.md`](docs/KURZBEFEHL.md) bauen. Unbedingt den 🧪 Zwischentest nach Teil D machen.

✅ *Test:* „Hey Siri, Wissen“ → „ACS“ → Anzeige erscheint. „Hey Siri, Wissen“ → „STEMI“ → Siri fragt „Welcher Eintrag?“ (zwei Treffer). „Hey Siri, Wissen“ → „Banane“ → App öffnet die Suche.

### Phase 5 – Wissen aufbauen (laufend)

- **Suchbegriffe** so eintragen, wie du sie sprichst – auch typische Siri-Missverständnisse.
- Bei Kliniken z. B. Suchbegriffe „Herzkatheter“, „Stroke Unit“, „Schockraum“ → Siri bietet dann alle passenden Kliniken zur Auswahl.
- Regelmäßig ⚙️ → **Export** als Sicherung (z. B. monatlich in iCloud Drive).

---

## Änderungen an der App veröffentlichen

```bash
cd ~/Pfad/zu/WissenRD
./version-erhoehen.sh "Was sich geändert hat"          # 1.0.0 → 1.0.1
./version-erhoehen.sh "Neue Funktion" minor           # 1.0.1 → 1.1.0
git add -A && git commit -m "v1.0.1" && git push
```
Beim ersten Mal: `chmod +x version-erhoehen.sh`.
Auf den Geräten erscheint danach eine rote Leiste **„Neue Version verfügbar“**.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html`, `css/style.css` | Oberfläche (hell/dunkel automatisch) |
| `js/app.js` | Logik: Anmeldung, Sync, Ansichten, Editor, Vorlesen |
| `js/text.js` | Suche, Normalisierung, Vorlesetext, Markdown |
| `js/bereiche.js` | Bereiche und Vorlagen – hier neue Bereiche ergänzen |
| `js/firebase-config.js` | deine Firebase-Zugangsdaten |
| `js/version.js` | Versionsnummer (nur per Skript ändern) |
| `sw.js`, `manifest.webmanifest` | Offline-Fähigkeit, Installation als App |
| `firestore.rules` | Zugriffsregeln |
| `daten/beispiel-eintraege.json` | Muster-Einträge zum Import |
| `icons/` | App-Icon (SVG-Vorlage + PNGs) |

> Keine Patientendaten eintragen. Maßgeblich sind immer die aktuell gültigen SAA/ÄLRD-Vorgaben.

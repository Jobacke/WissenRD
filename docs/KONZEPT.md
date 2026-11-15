# Wissen RD – Konzept

**Ziel:** „Hey Siri, Wissen“ → „Welches Thema?“ → „ACS“ → auf dem iPhone erscheint alles Wichtige zum Akuten Koronarsyndrom, auf Wunsch wird es vorgelesen. Die Inhalte pflegst du selbst, sie liegen auf einem Server und sind auf allen Geräten gleich.

## 1. Architektur

```
 ┌──────────────┐  „Hey Siri, Wissen“   ┌──────────────────────┐
 │  iPhone/Watch│ ─────────────────────▶│ Kurzbefehl „Wissen“  │
 │  (Siri)      │◀── Anzeige + Sprache ─│ (Kurzbefehle-App)    │
 └──────────────┘                       └─────────┬────────────┘
                                                  │ REST (Lese-Konto)
 ┌──────────────┐   Firebase-SDK        ┌─────────▼────────────┐
 │  PWA         │ ◀────────────────────▶│ Firebase             │
 │  Wissen RD   │   lesen + schreiben   │ Auth + Firestore     │
 │ (GitHub Pages)│                      │ (Server, EU)         │
 └──────────────┘                       └──────────────────────┘
```

| Baustein | Aufgabe | Warum so |
|---|---|---|
| **Firestore** (Firebase) | Speichert alle Einträge, synchronisiert alle Geräte, offline-fähig | Kennst du aus Zeiterfassung Pro / JUH-App, kostenloser Spark-Tarif reicht locker |
| **PWA „Wissen RD“** auf GitHub Pages | Pflegen, Suchen, Lesen, Vorlesen – auf iPhone, iPad, Mac | Gleicher Weg wie MediFlips, keine App-Store-Hürde |
| **Kurzbefehl „Wissen“** | Sprachabfrage über Siri, zeigt und spricht das Ergebnis | Funktioniert freihändig, auch bei gesperrtem Bildschirm und mit AirPods |
| **Lese-Konto „Siri“** | Eigenes Firebase-Konto, das nur lesen darf | Das Passwort steht im Kurzbefehl – selbst wenn es jemand sieht, kann er nichts ändern |

**Wichtiger Kniff:** Beim Speichern berechnet die App drei Zusatzfelder vor – `schluessel` (Suchbegriffe in Siri-tauglicher Form), `markdown` (fertige Anzeige) und `vorlesen` (sprechoptimierter Text, z. B. „i.v.“ → „intravenös“). Dadurch bleibt der Kurzbefehl einfach: Er sucht nur noch und zeigt an.

## 2. Bereiche

| Bereich | Vorlage-Abschnitte |
|---|---|
| 🩺 Verdachtsdiagnosen | Leitsymptome · Typische Symptome · Diagnostik · Differenzialdiagnosen · Maßnahmen · Medikamente · Zielklinik/Transport · Merke/Red Flags |
| 🔎 Symptome | Beschreibung · Mögliche Ursachen · Gezielt fragen/untersuchen · Red Flags |
| 💊 Medikamente | Wirkstoff/Handelsname · Wirkgruppe · Indikation · KI · Dosierung Erw./Kinder · Applikation · NW · Freigabe NotSan/Arzt |
| 📋 Algorithmen & SAA | Indikation · Ablauf · Besonderheiten |
| 📡 Leitstellen | Zuständigkeitsbereich · Telefon · Funk/Kanäle · Besonderheiten |
| 🏥 Kliniken | Adresse/Anfahrt · Fachbereiche · Zentren/Versorgungsstufe · Anmeldung · Besonderheiten |
| 🔤 Abkürzungen | Bedeutung · Erklärung |
| 📌 Sonstiges | frei |

Neue Bereiche: ein Block in `js/bereiche.js`. Abschnitte sind pro Eintrag frei änderbar (hinzufügen, umbenennen, verschieben).
Bei Leitstellen und Kliniken werden Telefonnummern antippbar.

## 3. Datenmodell (Firestore)

**Sammlung `eintraege`**, Dokument-ID = Kurzform (z. B. `acs`):

| Feld | Inhalt |
|---|---|
| `bereich` | z. B. `diagnose` |
| `titel`, `kurz` | „Akutes Koronarsyndrom“, „ACS“ |
| `suchbegriffe[]` | Herzinfarkt, STEMI, Brustschmerz … – so, wie du es zu Siri sagen würdest |
| `abschnitte[]` | `{titel, text}` – Text mit „- “ für Aufzählungen und `**fett**` |
| `siehe[]` | Querverweise (anklickbar) |
| `sprechtext` | optional eigene Kurzfassung zum Vorlesen |
| `quelle`, `stand` | z. B. „SAA ÄLRD Bayern 2025“, „2026-11“ |
| `revision` | zählt bei jeder Änderung des Eintrags hoch |
| `schluessel[]`, `markdown`, `vorlesen` | automatisch berechnet (für Siri) |
| `erstellt`, `geaendert`, `geaendertVon` | automatisch |

**Dokument `meta/stand`:** `datenversion` zählt bei jeder Änderung der Datenbank hoch.

## 4. Suche – so wird aus „A C S“ ein Treffer

Gesagter Text wird normalisiert: Kleinbuchstaben → ä/ö/ü/ß ersetzen → alles außer a–z und 0–9 entfernen.
„A C S“, „ACS“, „a.c.s.“ → `acs` · „Akutes Koronarsyndrom“ → `akuteskoronarsyndrom`.
App und Kurzbefehl verwenden exakt dieselbe Regel. Mehrere Treffer (z. B. „Herzkatheter“ bei mehreren Kliniken) → Siri fragt „Welcher Eintrag?“. Kein Treffer → die App öffnet sich mit einer unscharfen Suche (verzeiht auch Diktierfehler wie „Herzinfakt“).

**Suche nach Versorgungsmöglichkeit (ab v1.4):** Für Fragen wie „Wo ist die nächste Stroke Unit?“ gibt es eigene Übersichtseinträge im Bereich Kliniken (Stroke Units, Chest Pain Units, Traumazentren, Kinderkliniken, Cardiac Arrest Center, Neurochirurgie, Geburtshilfe). Die Suchbegriffe liegen nur auf der Übersicht, nicht auf den einzelnen Kliniken – so liefert „Hey Siri, Wissen → Stroke“ genau einen Treffer und liest die Liste mit Telefonnummern vor, ohne Rückfrage. Aufgenommen sind nur belegte Häuser; die Listen sind nicht abschließend, Zuweisung immer über ILS / IVENA.

## 5. Versionierung – Änderungen sofort erkennen

| Was | Wo sichtbar | Wie es hochzählt |
|---|---|---|
| **App-Version** `v1.0.0 (Build 1)` | Fußzeile, Einstellungen, Änderungsprotokoll | `./version-erhoehen.sh "Beschreibung"` – ändert Version, Build, Datum, Cache-Name und CHANGELOG in einem Schritt |
| **Datenstand** `Daten #47` | Fußzeile, Einstellungen | automatisch bei jedem Speichern/Löschen/Import |
| **Eintrags-Revision** `Rev. 3` | unter jedem Eintrag, auch in der Siri-Anzeige | automatisch beim Speichern des Eintrags |
| **Kurzbefehl-Version** | Kommentar-Aktion oben im Kurzbefehl | von Hand bei Änderungen |

Schema: `MAJOR.MINOR.PATCH` – Patch = Fehlerkorrektur, Minor = neue Funktion, Major = grundlegender Umbau. Neue App-Version → rote Leiste „Neue Version verfügbar“.

### Offline (ab v1.4)

Alle Einträge liegen dauerhaft im Gerätespeicher (Firestore `persistentLocalCache`), App-Dateien und Firebase-SDK im Service-Worker-Cache. Ohne Netz zeigt die Fußzeile „offline (Stand TT.MM. hh:mm)“. Änderungen im Editor werden offline vorgemerkt und beim nächsten Netzkontakt übertragen. Der Siri-Kurzbefehl braucht weiterhin Netz.

## 6. Icon

Variante B „Wissensbuch“ in Neon-Rubin auf dunklem Grund (`#1b1d20`), im Stil von ZNA-Navi, Schichtbuch, Notizen und Mopped. Dateien in `icons/` – SVG als Vorlage, PNG 512/192/180.

## 7. Sicherheit & Datenschutz

- **Keine Patientendaten** – die Datenbank ist reines Fachwissen.
- Lesen nur mit Anmeldung; Schreiben nur dein Konto (UID in `firestore.rules`).
- Siri-Konto darf nur lesen. Registrierung neuer Konten in Firebase abschalten.
- Speicherort Firestore: EU (`eur3`).
- Inhalte sind dein persönliches Nachschlagewerk – maßgeblich bleiben die gültigen SAA/ÄLRD-Vorgaben.

## 8. Ausbaustufen

| Version | Inhalt | Status |
|---|---|---|
| 1.0–1.1 | Kern: Bereiche, Editor, Suche, Vorlesen, Sync, Siri-Kurzbefehl, Export/Import | ✅ |
| 1.1.4–1.2.1 | Kurzbefehl „Wissen vorlesen“, Lernschleife für Siri-Begriffe, Klangsuche (Kölner Phonetik) | ✅ |
| 1.3 | Bereich Maßnahmen, ÄLRD-Bayern-Inhalte (83 Einträge) | ✅ |
| 1.4 | Offline-Anzeige, Kliniken München/Umland, Übersichten nach Versorgungsmöglichkeit | ✅ |
| 1.4 (Daten) | Leitstellen rund um München | ✅ |
| später | Favoriten / „Zuletzt angesehen“; Lernmodus mit Verbindung zur Quiz-App | offen |

## 9. Datenpflege

| Datensatz | Generator | Importdatei | Prüfung |
|---|---|---|---|
| ÄLRD Bayern (Medikamente, Algorithmen, Maßnahmen …) | `daten/gen_aelrd.py` | `daten/aelrd-bayern-import.json` | geplante Aufgabe „ÄLRD-Leitlinien-Check Wissen RD“, monatlich am 1. um 19:37 |
| Kliniken München und Umland inkl. Übersichten | `daten/gen_kliniken.py` | `daten/kliniken-muenchen-import.json` | geplante Aufgabe „Kliniken-Check Wissen RD“, jährlich am 10. Januar |
| Leitstellen (ILS München mit RD_1_M / RD_2_M, FFB, Erding, Oberland, Rosenheim) | `daten/gen_leitstellen.py` | `daten/leitstellen-import.json` | von Hand – Funkgruppen mit der Geräte-Programmierung abgleichen |

Ablauf bei Änderungen: Generator anpassen → `python3 daten/gen_….py daten/….json` → in der App ⚙️ → Import. Der Import überschreibt Einträge mit gleicher ID und behält eigene Suchbegriffe. Nur Angaben aus offiziellen Quellen (ÄLRD Bayern, DKG-Krankenhausverzeichnis, Klinikseiten); nicht Ermittelbares wird ausdrücklich als „nicht ermittelt“ markiert.

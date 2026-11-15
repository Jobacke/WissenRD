# Siri-Kurzbefehl „Wissen“

## Schnellweg: fertige Dateien (empfohlen)

Im Ordner `kurzbefehl/` liegen beide Kurzbefehle fertig gebaut:
`Wissen.unsigned.shortcut` (nur anzeigen) und `Wissen hören.unsigned.shortcut` (anzeigen + vorlesen).

1. Terminal: `cd ~/"Wissen Rettungsdienst/kurzbefehl" && bash signieren.sh`
2. Im Finder doppelt auf `Wissen.shortcut` und `Wissen hören.shortcut` klicken → „Kurzbefehl hinzufügen“.
3. Beim Import fragt die Kurzbefehle-App nach **E-Mail** und **Passwort des Siri-Lesekontos**.
4. Fertig – per iCloud sind die Kurzbefehle auch auf iPhone und Watch.

Geändert wird der Kurzbefehl über `kurzbefehl/gen_shortcut.py` (dann neu erzeugen und signieren).

---

## Manueller Bau (Referenz / Fehlersuche)

Ablauf: *„Hey Siri, Wissen“* → Siri: *„Welches Thema?“* → *„ACS“* → Anzeige (und optional Sprachausgabe).

Du brauchst aus der App (⚙️ Einstellungen → „Für den Siri-Kurzbefehl“): **API-Key**, **Projekt-ID**, **App-URL** sowie E-Mail und Passwort des **Siri-Lesekontos**.

> Tipp: Baue den Kurzbefehl auf dem Mac in der Kurzbefehle-App – er synchronisiert sich per iCloud aufs iPhone. Die Aktionsnamen unten sind die deutschen Namen; über die Suchleiste „Aktion suchen“ findest du jede.

---

## Teil A – Einstellungen

1. **Kommentar**: `Wissen RD – Kurzbefehl v1.0`
2. **Wörterbuch** mit diesen Einträgen (alle Typ *Text*):
   | Schlüssel | Wert |
   |---|---|
   | `apiKey` | dein API-Key |
   | `projekt` | deine Projekt-ID |
   | `email` | E-Mail des Siri-Lesekontos |
   | `passwort` | Passwort des Siri-Lesekontos |
   | `url` | App-URL, z. B. `https://jobacke.github.io/WissenRD/` |
   | `vorlesen` | `nein` (beim Kurzbefehl „Wissen hören“: `ja`) |
3. **Variable festlegen** → Name `K`

## Teil B – Thema erfragen und normalisieren

4. **Nach Eingabe fragen** – Typ *Text*, Frage: `Welches Thema?`
5. **Variable festlegen** → `Frage`
6. **Groß-/Kleinschreibung ändern** → *Kleinbuchstaben*
7. **Text ersetzen**: `ä` → `ae`
8. **Text ersetzen**: `ö` → `oe`
9. **Text ersetzen**: `ü` → `ue`
10. **Text ersetzen**: `ß` → `ss`
11. **Text ersetzen**: `[^a-z0-9]` → *(leer lassen)* – Optionen aufklappen: **Regulärer Ausdruck = an**
12. **Variable festlegen** → `Schluessel`

## Teil C – Mit dem Lesekonto anmelden

13. **Text**: `https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=` und dahinter die Variable **K → apiKey** einfügen
    (Variable antippen → *Wörterbuchwert abrufen* → Schlüssel `apiKey`)
14. **Inhalte von URL abrufen** – URL = Text aus 13, aufklappen:
    - Methode: **POST**
    - Hauptteil anfordern: **JSON**
    - Felder: `email` (Text) = K→email · `password` (Text) = K→passwort · `returnSecureToken` (Boolescher Wert) = **an**
15. **Wörterbuchwert abrufen** – Schlüssel `idToken`
16. **Variable festlegen** → `Token`

## Teil D – In der Datenbank suchen

17. **Text** (genau so, nur `Schluessel` als Variable einsetzen):
    ```json
    {"structuredQuery":{"from":[{"collectionId":"eintraege"}],"where":{"fieldFilter":{"field":{"fieldPath":"schluessel"},"op":"ARRAY_CONTAINS","value":{"stringValue":"⟨Schluessel⟩"}}},"select":{"fields":[{"fieldPath":"titel"},{"fieldPath":"markdown"},{"fieldPath":"vorlesen"}]},"limit":10}}
    ```
18. **Text**: `https://firestore.googleapis.com/v1/projects/` + **K→projekt** + `/databases/(default)/documents:runQuery`
19. **Inhalte von URL abrufen** – URL = Text aus 18:
    - Methode: **POST**
    - Header: `Authorization` = `Bearer ` + **Token** (Leerzeichen nach Bearer!) · `Content-Type` = `application/json`
    - Hauptteil anfordern: **Datei** → Datei = **Text aus 17**
20. **Variable festlegen** → `Antwort`

> 🧪 **Zwischentest:** Füge hier vorübergehend **Ergebnis anzeigen** (Antwort) ein und starte mit „ACS“. Du solltest einen Block mit `document` → `fields` → `titel` sehen. Danach die Testaktion wieder löschen.

## Teil E – Treffer sammeln

21. **Wörterbuch** (leer lassen) → 22. **Variable festlegen** → `Treffer`
23. **Wiederholen mit jedem Objekt** in `Antwort`
    24. **Wörterbuchwert abrufen** – Schlüssel `document.fields.titel.stringValue` aus *Wiederholungsobjekt*
    25. **Wenn** *Wörterbuchwert* **hat einen Wert**
        26. **Zu Variable hinzufügen** → `Titel` (Wörterbuchwert)
        27. **Wörterbuchwert festlegen** – Schlüssel = *Wörterbuchwert*, Wert = *Wiederholungsobjekt*, in `Treffer`
        28. **Variable festlegen** → `Treffer` (Ergebnis aus 27)
    **Ende Wenn**
**Ende Wiederholen**

## Teil F – Kein Treffer → App-Suche öffnen

29. **Wenn** `Titel` **hat keinen Wert**
    30. **Text sprechen**: `Nichts zu ⟨Frage⟩ gefunden. Ich öffne die Suche.`
    31. **URL codieren** → `Frage`
    32. **URLs öffnen**: K→url + `?q=` + *codierter Text*
    33. **Kurzbefehl stoppen**
**Ende Wenn**

## Teil G – Auswählen, anzeigen, vorlesen

34. **Anzahl** → Objekte in `Titel`
35. **Wenn** Anzahl **ist größer als** `1`
    36. **Aus Liste auswählen** – `Titel`, Hinweis: `Welcher Eintrag?`
    **Sonst**
    37. **Objekt aus Liste abrufen** – *Erstes Objekt* aus `Titel`
**Ende Wenn** → 38. **Variable festlegen** → `Gewaehlt` (Ergebnis von *Wenn*)
39. **Wörterbuchwert abrufen** – Schlüssel = `Gewaehlt` aus `Treffer` → 40. **Variable festlegen** → `Eintrag`
41. **Wenn** K→vorlesen **ist** `ja`
    42. **Wörterbuchwert abrufen** `document.fields.vorlesen.stringValue` aus `Eintrag`
    43. **Text sprechen** – Sprache *Deutsch*, aufklappen: **Warten bis fertig = aus** (so läuft die Anzeige parallel)
**Ende Wenn**
44. **Wörterbuchwert abrufen** `document.fields.markdown.stringValue` aus `Eintrag`
45. **Rich Text aus Markdown erstellen**
46. **Schnellansicht**

## Teil H – Siri & zweite Variante

- Kurzbefehl **„Wissen“** nennen → *„Hey Siri, Wissen“*.
- Kurzbefehl duplizieren, **„Wissen hören“** nennen, in Schritt 2 `vorlesen` = `ja`.
- Optional: Aktionstaste (iPhone 15 Pro und neuer) oder *Bedienungshilfen → Tippen → Rückseite antippen* auf „Wissen hören“ legen.

## Fehlersuche

| Symptom | Ursache / Lösung |
|---|---|
| Schritt 15 leer | E-Mail/Passwort/API-Key prüfen; in Firebase E-Mail/Passwort-Anmeldung aktiv? |
| Antwort enthält `PERMISSION_DENIED` | UID des Siri-Kontos in `firestore.rules` fehlt oder Regeln nicht veröffentlicht |
| Antwort enthält `API key not valid` / `referer` | API-Key ist in der Google Cloud auf Websites (HTTP-Referrer) beschränkt → Beschränkung auf „APIs“ statt „Websites“ umstellen |
| Schritt 24 liefert nie einen Wert | Falls deine iOS-Version keine Punkt-Pfade kennt: vier einzelne *Wörterbuchwert abrufen* hintereinander (`document` → `fields` → `titel` → `stringValue`) |
| Siri versteht Abkürzung falsch | In der App weitere Suchbegriffe ergänzen, z. B. bei „ACS“ zusätzlich „AZS“ oder „Akutes Koronar“ |

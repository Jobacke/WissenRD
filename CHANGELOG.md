# Änderungsprotokoll Wissen RD

## v1.11.0 (Build 24) – 2026-11-16
- Meldung bei Wechsel der zuständigen Leitstelle (solange die App geöffnet ist, abschaltbar in den Einstellungen); Funkgruppen je Leitstelle

## v1.10.0 (Build 23) – 2026-11-16
- Leitstellen: zuständige ILS am eigenen Standort (Landkreis über OpenStreetMap, Zuordnung nach AVBayRDG Anlage 1), alle 25 ILS Bayerns, Sortierung nächste zuerst

## v1.9.2 (Build 22) – 2026-11-16
- Symptom-Check: Sortierung nach Anzahl passender Symptome, dann alphabetisch

## v1.9.1 (Build 21) – 2026-11-16
- Symptom-Check: widersprüchliche Symptome (Puls schnell/langsam, Blutdruck hoch/niedrig, Atmung, Temperatur, Pupillen) nur entweder/oder wählbar

## v1.9.0 (Build 20) – 2026-11-16
- „Siehe auch“ springt direkt zum verwiesenen Eintrag; Symptom-Check im Bereich Symptome: Symptome antippen → mögliche Verdachtsdiagnosen; Symptome bei allen Verdachtsdiagnosen, 12 neue Verdachtsdiagnosen

## v1.8.1 (Build 19) – 2026-11-16
- Kliniken: Entfernung jetzt als Fahrstrecke mit Fahrzeit (Straßennetz OpenStreetMap, Pkw, ohne Verkehr/Sonderrechte); Luftlinie nur noch als gekennzeichnete Notlösung ohne Netz

## v1.8.0 (Build 18) – 2026-11-16
- Kliniken nach Entfernung: nächste Klinik zuerst (Luftlinie, Standort des iPhones), Entfernung je Klinik, Route-Knopf, Position vor Ort speichern

## v1.7.2 (Build 17) – 2026-11-16
- Farbkonzept Nachtblau & Gold; Bereiche per langem Drücken anordnen, speichert sofort; Standard-Reihenfolge in den Einstellungen

## v1.7.1 (Build 16) – 2026-11-16
- Farbkonzept Nachtblau & Gold; Bereiche per langem Drücken anordnen, speichert sofort; Standard-Reihenfolge in den Einstellungen

## v1.7.0 (Build 15) – 2026-11-16
- Warme Farbwelt (Apricot/Koralle/Rosé, warmes Nachtdesign); Bereiche per Ziehen individuell anordnen, Reihenfolge geräteübergreifend gespeichert

## v1.6.0 (Build 14) – 2026-11-16
- Feinschliff: Suche nur als Lupe (öffnet schmales Feld), Suchverlauf mit Löschen nach Heute/Gestern/7 Tage/Alles (auch in den Einstellungen), Bereichsleiste zum direkten Wechsel zwischen den Bereichen, schmalere Kacheln (3 Spalten), Telefonnummern ohne Zeilenumbruch

## v1.5.0 (Build 13) – 2026-11-16
- Neues Design: frische Farben (Türkis → Indigo, Farbe je Bereich), kompakte Kopfzeile mit kleiner Suche und Zurück-Button, schlanke Kacheln und Buttons, schwebender Plus-Button, „Zuletzt geändert“ eingeklappt

## v1.4.0 (Build 12) – 2026-11-15
- Offline: Anzeige „offline (Stand …)“, Firebase-SDK wird für den Offline-Start vorgeladen. Daten: 19 Kliniken (München, Ebersberg, Starnberg, Erding, Agatharied, kbo Haar) plus 7 Übersichten nach Versorgungsmöglichkeit (Stroke, Chest Pain, Trauma, Kinder, CAC, Neurochirurgie, Geburtshilfe)

## v1.3.0 (Build 11) – 2026-11-15
- Neuer Bereich Maßnahmen; Import behält eigene Suchbegriffe; Vorlesen verbessert (Dosierungen, Abkürzungen); Importdatei ÄLRD Bayern (83 Einträge)

## v1.2.1 (Build 10) – 2026-11-15
- Siri-Kurzbefehl v1.5: Absturz bei „kein Treffer“ behoben (Schlüsselpfad „document“)

## v1.2.0 (Build 9) – 2026-11-15
- Lernschleife: nicht erkannte Siri-Begriffe per Tipp einem Eintrag zuordnen; Klangsuche (Kölner Phonetik)

## v1.1.5 (Build 8) – 2026-11-15
- Siri-Kurzbefehl v1.4: Frage „Wie lautet das Thema?“

## v1.1.4 (Build 7) – 2026-11-15
- Kurzbefehl „Wissen hören“ in „Wissen vorlesen“ umbenannt (Siri startete sonst Musik)

## v1.1.3 (Build 6) – 2026-11-15
- Siri-Kurzbefehl v1.3: Eingabe über Siri-Sprachdialog („Hey Siri, Wissen“), Diktat-Aktion entfernt

## v1.1.2 (Build 5) – 2026-11-15
- Siri-Kurzbefehl v1.2: Thema per Spracheingabe (Diktat) statt Tippen

## v1.1.1 (Build 4) – 2026-11-15
- Siri-Kurzbefehl v1.1: ohne Textvergleiche (Fehler „Wähle einen Wert für jeden Parameter“ behoben)

## v1.1.0 (Build 3) – 2026-11-15
- Neues App-Icon im Stil von Mopped/Schichtbuch (Wissensbuch, Neon-Rubin); fertige Siri-Kurzbefehle „Wissen“ und „Wissen hören“

## v1.0.1 (Build 2) – 2026-11-15
- Vorlesen flüssiger (größere Textstücke), beste deutsche Stimme wird automatisch gewählt

## v1.0.0 (Build 1) – 2026-11-15
- Erste Version: Bereiche, Suche (auch bei Diktierfehlern), Eintrag anlegen/bearbeiten/löschen
- Vorlesen mit einstellbarer Geschwindigkeit und Stimme
- Firebase-Sync über alle Geräte, offline nutzbar
- Siri-Anbindung: ?q=Suchbegriff und vorberechnete Felder für den Kurzbefehl
- Export/Import als JSON, Versions- und Datenstandsanzeige, Dunkelmodus für Nachtdienste

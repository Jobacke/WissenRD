"""Erzeugt daten/leitstellen-import.json – Integrierte Leitstellen rund um München (Bereich „leitstelle“).
Nur belegte Angaben; Funkgruppen/Telefonnummern mit Stand der Quelle. Recherche 15.11.2026."""
import json, sys

STAND = "2026-11"
NE = "nicht ermittelt – bei der ILS bzw. Wache erfragen"
HINWEIS = ("Telefonnummern und Funkgruppen ohne Gewähr – Stand der jeweiligen Quelle beachten und mit der aktuellen "
           "Funkgeräte-Programmierung / Wachen-Info abgleichen. Notruf immer 112.")
E = []

def ls(id, titel, kurz, such, bereich, telefon, funk, besonders, kliniken, quellen, sprech, siehe=()):
    ab = [("Zuständigkeitsbereich", bereich), ("Telefon", telefon), ("Funk / Kanäle", funk),
          ("Besonderheiten", besonders)]
    if kliniken:
        ab.append(("Kliniken aus der App im Bereich", "\n".join("- " + k for k in kliniken)))
    ab.append(("Hinweis", HINWEIS))
    E.append({"id": "leitstelle-" + id, "bereich": "leitstelle", "titel": titel, "kurz": kurz,
              "suchbegriffe": list(such), "siehe": list(siehe) + list(kliniken),
              "abschnitte": [{"titel": t, "text": x.strip()} for t, x in ab if x and x.strip()],
              "sprechtext": sprech, "quelle": " · ".join(quellen), "stand": STAND})

Q_TK = "ILS München: Taschenkarte Einsatzablauf Rettungsdienst (Stand Juni 2017, stadt.muenchen.de)"
STATUS = """- **Einsatzübernahme:** Status 3 (Status 0 nur bei Rückfragen oder Datenübertragungsstörung, dann Sprechaufforderung abwarten)
- **Nach Transport:** zurück auf die Original-Digitalfunkgruppe, Status 1
- **Ohne Transport:** auf RD_Betten_M, Status 5 → Rückmeldung (z. B. kein Eingreifen, Einsatznummer von der ILS) → zurück auf Original-Gruppe, Status 1
- **Dringender Sprechwunsch:** digital Status 0
- **Bettenanforderung:** RD_Betten_M, Status 5; Sonderbetten: Status 0 bzw. 089 515191-66666
- **Angaben für IVENA:** Fachbereich, Fachgebiet, Behandlungsdringlichkeit (Notfallversorgung / stationär / ambulant), voraussichtliche Eintreffzeit, Geschlecht, Alter, Name"""

# ------------------------------------------------------------------ ILS München
ls("muenchen", "Integrierte Leitstelle München", "ILS München",
 ["Leitstelle München", "ILS M", "Rettungsleitstelle München", "Leitstelle Feuerwache 4", "RD Betten M", "RD_Betten_M"],
 """- Rettungsdienst: Stadt **und** Landkreis München (Rettungsdienstbereich München)
- Feuerwehr: Stadt München
- Betrieb durch die Berufsfeuerwehr München; Sitz seit 2017 in der Feuerwache 4""",
 """- **Notfallrettung (Disponent):** 089 515191-66943
- **Krankentransport:** 089 515191-66941
- **Betten / MANV / Sonderbetten:** 089 515191-66666
- Feuerwehr: 089 515191-66966
(Servicenummern laut Taschenkarte, Stand Juni 2017 – Aktualität prüfen)""",
 """- **RD_1_M** – Rettungsdienst Nord, Kurzwahl **2513**
- **RD_2_M** – Rettungsdienst Süd, Kurzwahl **2514**
(Kurzwahlen laut eigener Geräteprogrammierung, Stand 11/2026; die Taschenkarte von 2017 nennt noch 2766/2767)
- **RD_Betten_M** – Bettenanforderung / Rückmeldung ohne Transport (Kurzwahl in der Quelle nicht angegeben)
- BF_1_M (FW Nord) 2751 · BF_2_M (FW Süd) 2752
Die zugeteilte Gruppe steht im Navi-Datensatz des Einsatzes.""",
 STATUS + """
- Patientennummer und Transportziel kommen über die Dat-Box ans Navi
- Führt eine Übersicht über freie Betten für Brandverletzte an bayerischen Krankenhäusern
- In die ILS eingebettet: Koordinierungsstelle für die bayerischen Intensivtransporthubschrauber (KITH)""",
 ["LMU Klinikum – Campus Großhadern", "LMU Klinikum – Campus Innenstadt", "TUM Klinikum Rechts der Isar",
  "München Klinik Bogenhausen", "München Klinik Harlaching", "München Klinik Neuperlach", "München Klinik Schwabing",
  "Rotkreuzklinikum München", "Klinikum Dritter Orden München-Nymphenburg", "Krankenhaus Barmherzige Brüder München",
  "Helios Klinikum München West", "Helios Klinik München Perlach", "Krankenhaus Martha-Maria München",
  "TUM Klinikum Deutsches Herzzentrum", "kbo-Isar-Amper-Klinikum Haar (Neurologie / Psychiatrie)"],
 [Q_TK, "stadt.muenchen.de – Integrierte Leitstelle", "bayern.de – Einweihung ILS München 27.07.2017", "lmu-klinikum.de – Notfallmedizin (KITH)"],
 "Integrierte Leitstelle München. Rettungsdienst Nord R D 1 M, Kurzwahl 2513. Rettungsdienst Süd R D 2 M, Kurzwahl 2514. "
 "Betten über R D Betten M, Status 5. Notfallrettung 089 515191 66943. Betten und MANV 089 515191 66666.",
 siehe=["RD_1_M – Rettungsdienst Nord (ILS München)", "RD_2_M – Rettungsdienst Süd (ILS München)", "Übersicht Leitstellen"])

for nr, seite, kw in [(1, "Nord", "2513"), (2, "Süd", "2514")]:
    ls(f"rd{nr}m", f"RD_{nr}_M – Rettungsdienst {seite} (ILS München)", f"RD_{nr}_M",
     [f"RD {nr} M", f"RD{nr}M", f"RD {nr}", f"Rettungsdienst {seite}", f"RD {seite} München", f"Gruppe RD {nr} M"],
     f"Digitalfunkgruppe Rettungsdienst **{seite}** der Integrierten Leitstelle München (Stadt und Landkreis München). "
     "Welche Wachen / Gebiete Nord bzw. Süd zugeordnet sind: " + NE + ".",
     """- Notfallrettung (Disponent): 089 515191-66943
- Betten / MANV: 089 515191-66666""",
     f"""- **RD_{nr}_M** – Kurzwahl Sepura **{kw}**
- Gegenstück: RD_{2 if nr == 1 else 1}_M (Kurzwahl {"2514" if nr == 1 else "2513"})
- Betten / Rückmeldung ohne Transport: **RD_Betten_M**""",
     STATUS, [], [Q_TK, "Kurzwahl: eigene Angabe (Geräteprogrammierung, Stand 11/2026)"],
     f"R D {nr} M, Rettungsdienst {seite} der Leitstelle München, Kurzwahl {' '.join(kw)}. "
     "Betten über R D Betten M mit Status 5. Nach Transport zurück auf die Original-Gruppe, Status 1.",
     siehe=["Integrierte Leitstelle München"])

# ------------------------------------------------------------------ ILS Fürstenfeldbruck
ls("ffb", "Integrierte Leitstelle Fürstenfeldbruck", "ILS FFB",
 ["Leitstelle FFB", "Leitstelle Fürstenfeldbruck", "ILS Fürstenfeldbruck", "Leitstelle Maisach", "ILS Maisach", "RD FFB", "RD_FFB"],
 """- Landkreise **Dachau, Fürstenfeldbruck, Landsberg am Lech und Starnberg** (Zweckverband für Rettungsdienst und Feuerwehralarmierung Fürstenfeldbruck)
- rund 641.000 Einwohner, 84 Städte und Gemeinden, 14 Rettungswachen, 32 RTW, 10 Notarztstandorte
- **Neuer Standort Maisach / Gernlinden:** eingeweiht am 09.05.2026, Echtbetrieb laut Landratsamt spätestens ab Juli 2026 (vorher Fürstenfeldbruck)""",
 """- Leitstelle: 08141 22700-600
- Alarm-Anrufe: 08141 22700-651
(beide laut Taschenkarte KFV Landsberg, Stand April 2021 – nach dem Umzug nach Maisach prüfen)
- Krankentransport: 19222 (Notruftafel Landratsamt Fürstenfeldbruck)""",
 """- **RD_FFB** – Kurzwahl 2063 (Taschenkarte KFV Landsberg, Stand Dezember 2018)
- Rettungsdienst-Gruppen für Dachau, Landsberg, Starnberg: """ + NE,
 """- Die 2024 geplante Fusion mit der ILS Oberland in Maisach wurde abgesagt – die ILS Oberland bleibt in Weilheim
- Klinikum Starnberg liegt im Bereich der ILS FFB, nicht der ILS München""",
 ["Klinikum Starnberg (Kreisklinik Starnberg)"],
 ["Verbandssatzung ZRF Fürstenfeldbruck (Oberbayerisches Amtsblatt 2020)", "Landratsamt Fürstenfeldbruck – Einweihung ILS Maisach (Mai 2026)",
  "KFV Landsberg – Taschenkarte Digitalfunk (12/2018, 04/2021)", "Kreisbote – Fusion ILS Oberland/FFB abgesagt"],
 "Integrierte Leitstelle Fürstenfeldbruck, seit 2026 in Maisach. Zuständig für Dachau, Fürstenfeldbruck, Landsberg und Starnberg. "
 "Telefon 08141 22700 600. Funkgruppe R D F F B, Kurzwahl 2063.")

# ------------------------------------------------------------------ ILS Erding
ls("erding", "Integrierte Leitstelle Erding", "ILS Erding",
 ["Leitstelle Erding", "ILS ED", "Leitstelle ED", "RD Erding Leitstelle"],
 """- Landkreise **Erding, Freising und Ebersberg**
- Gebäude 2009 in Erding angebaut; Umbau / Erweiterung geplant (Ausschreibungen 2022 und 2023)""",
 """- Krankentransport: 08123 19222 (seit 19.05.2015 nur mit Vorwahl, für die Landkreise Erding, Freising und Ebersberg)
- Direktnummer für Rettungsdienst-Rückfragen: """ + NE,
 "- Digitalfunkgruppen Rettungsdienst: " + NE,
 "- Klinikum Ebersberg und Klinikum Erding liegen im Bereich der ILS Erding",
 ["Klinikum Ebersberg München Ost (Kreisklinik Ebersberg)", "Klinikum Landkreis Erding"],
 ["EU-Ausschreibung Fachplanung Leitstellentechnik ILS Erding (TED 2022 und 2023)", "Landkreis Erding – Amtsblatt Nr. 22 vom 27.05.2015"],
 "Integrierte Leitstelle Erding. Zuständig für Erding, Freising und Ebersberg. Krankentransport 08123 19222.")

# ------------------------------------------------------------------ ILS Oberland
ls("oberland", "Integrierte Leitstelle Oberland", "ILS Oberland",
 ["Leitstelle Oberland", "Leitstelle Weilheim", "ILS Weilheim", "RD WM", "RD_WM"],
 """- Landkreise **Bad Tölz-Wolfratshausen, Garmisch-Partenkirchen und Weilheim-Schongau** (ZRF Oberland)
- Sitz: Weilheim, Johannes-Damrich-Straße 5a; betrieben vom BRK
- Die geplante Zusammenlegung mit der ILS Fürstenfeldbruck wurde abgesagt – die ILS bleibt in Weilheim""",
 """- Leitstelle Oberland: 08861 9258-5100 (Taschenkarte KFV Landsberg, Stand Dezember 2018 – prüfen)""",
 """- **RD_WM** (Landkreis Weilheim) – Kurzwahl 3073 (Taschenkarte KFV Landsberg, Stand Dezember 2018)
- Gruppen für Bad Tölz-Wolfratshausen und Garmisch-Partenkirchen: """ + NE,
 """- Landkreis **Miesbach gehört nicht** zur ILS Oberland, sondern zur ILS Rosenheim""",
 [],
 ["Landkreis Weilheim-Schongau – Antworten zur ILS / Pressemitteilung 177/2024", "Bayerischer Landtag Drucksache 19/4346",
  "Kreisbote – Fusion ILS Oberland/FFB abgesagt", "KFV Landsberg – Taschenkarte Digitalfunk (12/2018)"],
 "Integrierte Leitstelle Oberland in Weilheim. Zuständig für Bad Tölz Wolfratshausen, Garmisch Partenkirchen und Weilheim Schongau. "
 "Telefon 08861 9258 5100. Funkgruppe R D W M, Kurzwahl 3073.")

# ------------------------------------------------------------------ ILS Rosenheim
ls("rosenheim", "Integrierte Leitstelle Rosenheim", "ILS Rosenheim",
 ["Leitstelle Rosenheim", "ILS RO", "Leitstelle RO", "Leitstelle Miesbach"],
 """- **Stadt Rosenheim, Landkreis Rosenheim und Landkreis Miesbach** (Zweckverband für Rettungsdienst und Feuerwehralarmierung Rosenheim)
- Organisatorisch Stabsstelle der Stadt Rosenheim""",
 "- Telefon für Rettungsdienst-Rückfragen / Krankentransport: " + NE,
 "- Digitalfunkgruppen Rettungsdienst: " + NE,
 "- Krankenhaus Agatharied (Landkreis Miesbach) liegt im Bereich der ILS Rosenheim",
 ["Krankenhaus Agatharied"],
 ["Pressemitteilung daxenfeuer.de (Landratsamt Rosenheim)", "Stadt Rosenheim – Organigramm Stand 01.01.2026"],
 "Integrierte Leitstelle Rosenheim. Zuständig für Stadt und Landkreis Rosenheim sowie Landkreis Miesbach.")

# ------------------------------------------------------------------ Übersicht
E.append({"id": "leitstelle-uebersicht", "bereich": "leitstelle", "titel": "Übersicht Leitstellen", "kurz": "Leitstellen",
 "suchbegriffe": ["Leitstellen", "ILS", "Integrierte Leitstellen", "Welche Leitstelle", "Leitstelle Landkreis", "Leitstellenbereiche"],
 "siehe": [e["titel"] for e in E],
 "abschnitte": [
  {"titel": "Welcher Landkreis – welche ILS", "text": """- **ILS München:** Stadt München, Landkreis München (Rettungsdienst) – RD_1_M (Nord, 2513), RD_2_M (Süd, 2514)
- **ILS Fürstenfeldbruck (Maisach):** Dachau, Fürstenfeldbruck, Landsberg am Lech, Starnberg
- **ILS Erding:** Erding, Freising, Ebersberg
- **ILS Oberland (Weilheim):** Bad Tölz-Wolfratshausen, Garmisch-Partenkirchen, Weilheim-Schongau
- **ILS Rosenheim:** Stadt und Landkreis Rosenheim, Landkreis Miesbach"""},
  {"titel": "Merke", "text": "- Starnberg → ILS FFB · Ebersberg → ILS Erding · Miesbach / Agatharied → ILS Rosenheim\n- In Bayern gibt es eine Integrierte Leitstelle je Rettungsdienstbereich"},
  {"titel": "Hinweis", "text": HINWEIS}],
 "sprechtext": "Leitstellen. München: Stadt und Landkreis München. Fürstenfeldbruck in Maisach: Dachau, Fürstenfeldbruck, Landsberg, Starnberg. "
               "Erding: Erding, Freising, Ebersberg. Oberland in Weilheim: Bad Tölz Wolfratshausen, Garmisch Partenkirchen, Weilheim Schongau. "
               "Rosenheim: Stadt und Landkreis Rosenheim und Miesbach.",
 "quelle": "Zusammenstellung aus den Leitstellen-Einträgen", "stand": STAND})

if __name__ == "__main__":
    ids = [e["id"] for e in E]
    assert len(ids) == len(set(ids))
    json.dump({"app": "Wissen RD", "titel": "Import Leitstellen",
               "hinweis": "Integrierte Leitstellen München, Fürstenfeldbruck, Erding, Oberland, Rosenheim. Recherche 15.11.2026 – Funkgruppen und Nummern mit Stand der Quelle prüfen.",
               "eintraege": E}, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(E), "Leitstellen-Einträge")

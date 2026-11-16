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
- **Bettenanforderung:** RD_Betten_M (Kurzwahl 2511), Status 5; Sonderbetten: Status 0 bzw. 089 515191-66666
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
 """- Rettungsdienst-Gruppen und Bettenkanal: siehe **Funkgruppen** oben
- **RD_Betten_M** auch für die Rückmeldung ohne Transport (Status 5)
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
 "Integrierte Leitstelle München. Betten über R D Betten M mit Status 5. Notfallrettung 089 515191 66943. Betten und MANV 089 515191 66666.",
 siehe=["RD_1_M – Rettungsdienst Nord (ILS München)", "RD_2_M – Rettungsdienst Süd (ILS München)", "Übersicht Leitstellen"])

ZW = dict(zip("0123456789", ["null", "eins", "zwo", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun"]))
for nr, seite, kw in [(1, "Nord", "2513"), (2, "Süd", "2514")]:
    ls(f"rd{nr}m", f"RD_{nr}_M – Rettungsdienst {seite} (ILS München)", f"RD_{nr}_M",
     [f"RD {nr} M", f"RD{nr}M", f"RD {nr}", f"Rettungsdienst {seite}", f"RD {seite} München", f"Gruppe RD {nr} M"],
     f"Digitalfunkgruppe Rettungsdienst **{seite}** der Integrierten Leitstelle München (Stadt und Landkreis München). "
     "Welche Wachen / Gebiete Nord bzw. Süd zugeordnet sind: " + NE + ".",
     """- Notfallrettung (Disponent): 089 515191-66943
- Betten / MANV: 089 515191-66666""",
     f"""- **RD_{nr}_M** – Kurzwahl Sepura **{kw}**
- Gegenstück: RD_{2 if nr == 1 else 1}_M (Kurzwahl {"2514" if nr == 1 else "2513"})
- Betten / Rückmeldung ohne Transport: **RD_Betten_M** (Kurzwahl 2511)""",
     STATUS, [], [Q_TK, "Kurzwahl: eigene Angabe (Geräteprogrammierung, Stand 11/2026)"],
     f"R D {nr} M, Rettungsdienst {seite} der Leitstelle München, Kurzwahl {', '.join(ZW[z] for z in kw)}. "
     "Betten über R D Betten M, Kurzwahl zwo, fünf, eins, eins, mit Status 5. Nach Transport zurück auf die Original-Gruppe, Status 1.",
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
 "Telefon 08141 22700 600.")

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
 "Telefon 08861 9258 5100.")

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

# ------------------------------------------------------------------ alle 25 ILS Bayerns: Zuständigkeit + Ort
# Zuständigkeit: AVBayRDG Anlage 1 (Rettungsdienstbereiche), Text gilt ab 15.04.2026 – je Rettungsdienstbereich genau eine ILS.
# Position: Ort der ILS (Ortsmitte, ungefähr) – reicht für die Sortierung „nächste zuerst“. München: Feuerwache 4 (ZNA-Navi).
Q_ANL1 = "AVBayRDG Anlage 1 – Rettungsdienstbereiche und Rettungsdienstbezirke (gesetze-bayern.de, Text gilt ab 15.04.2026)"
Q_ORT = "Ort der ILS: Ortsmitte (ungefähr) für die Entfernungssortierung"
ILS = [
 # id, Name, Sitz, lat, lon, Regierungsbezirk, Landkreise / kreisfreie Städte
 ("erding", "Erding", "Erding", 48.306, 11.907, "Oberbayern", ["Ebersberg", "Erding", "Freising"]),
 ("oberland", "Oberland", "Weilheim i. OB", 47.840, 11.142, "Oberbayern", ["Bad Tölz-Wolfratshausen", "Garmisch-Partenkirchen", "Weilheim-Schongau"]),
 ("rosenheim", "Rosenheim", "Rosenheim", 47.856, 12.128, "Oberbayern", ["Miesbach", "Rosenheim (Stadt)", "Rosenheim (Landkreis)"]),
 ("traunstein", "Traunstein", "Traunstein", 47.868, 12.643, "Oberbayern", ["Altötting", "Berchtesgadener Land", "Mühldorf a.Inn", "Traunstein"]),
 ("ffb", "Fürstenfeldbruck", "Maisach", 48.217, 11.258, "Oberbayern", ["Dachau", "Fürstenfeldbruck", "Landsberg am Lech", "Starnberg"]),
 ("muenchen", "München", "München (Feuerwache 4)", 48.156007, 11.555468, "Oberbayern", ["München (Stadt)", "München (Landkreis)"]),
 ("ingolstadt", "Region Ingolstadt", "Ingolstadt", 48.766, 11.426, "Oberbayern", ["Eichstätt", "Ingolstadt", "Neuburg-Schrobenhausen", "Pfaffenhofen a.d.Ilm"]),
 ("landshut", "Landshut", "Landshut", 48.537, 12.152, "Niederbayern", ["Dingolfing-Landau", "Kelheim", "Landshut (Stadt)", "Landshut (Landkreis)"]),
 ("passau", "Passau", "Passau", 48.575, 13.461, "Niederbayern", ["Freyung-Grafenau", "Passau (Stadt)", "Passau (Landkreis)", "Rottal-Inn"]),
 ("straubing", "Straubing", "Straubing", 48.881, 12.574, "Niederbayern", ["Deggendorf", "Regen", "Straubing", "Straubing-Bogen"]),
 ("oberpfalz-nord", "Oberpfalz-Nord", "Amberg", 49.445, 11.858, "Oberpfalz", ["Amberg", "Amberg-Sulzbach", "Neustadt a.d.Waldnaab", "Schwandorf", "Tirschenreuth", "Weiden i.d.OPf."]),
 ("regensburg", "Regensburg", "Regensburg", 49.013, 12.101, "Oberpfalz", ["Cham", "Neumarkt i.d.OPf.", "Regensburg (Stadt)", "Regensburg (Landkreis)"]),
 ("bamberg-forchheim", "Bamberg-Forchheim", "Bamberg", 49.892, 10.887, "Oberfranken", ["Bamberg (Stadt)", "Bamberg (Landkreis)", "Forchheim"]),
 ("bayreuth-kulmbach", "Bayreuth/Kulmbach", "Bayreuth", 49.945, 11.576, "Oberfranken", ["Bayreuth (Stadt)", "Bayreuth (Landkreis)", "Kulmbach"]),
 ("coburg", "Coburg", "Coburg", 50.258, 10.965, "Oberfranken", ["Coburg (Stadt)", "Coburg (Landkreis)", "Kronach", "Lichtenfels"]),
 ("hochfranken", "Hochfranken", "Hof", 50.313, 11.912, "Oberfranken", ["Hof (Stadt)", "Hof (Landkreis)", "Wunsiedel i.Fichtelgebirge"]),
 ("ansbach", "Ansbach", "Ansbach", 49.302, 10.572, "Mittelfranken", ["Ansbach (Stadt)", "Ansbach (Landkreis)", "Neustadt a.d.Aisch-Bad Windsheim"]),
 ("mittelfranken-sued", "Mittelfranken Süd", "Schwabach", 49.329, 11.022, "Mittelfranken", ["Roth", "Schwabach", "Weißenburg-Gunzenhausen"]),
 ("nuernberg", "Nürnberg", "Nürnberg", 49.454, 11.077, "Mittelfranken", ["Erlangen", "Erlangen-Höchstadt", "Fürth (Stadt)", "Fürth (Landkreis)", "Nürnberg", "Nürnberger Land"]),
 ("untermain", "Bayerischer Untermain", "Aschaffenburg (Feuerwache)", 49.977, 9.152, "Unterfranken", ["Aschaffenburg (Stadt)", "Aschaffenburg (Landkreis)", "Miltenberg"]),
 ("schweinfurt", "Schweinfurt", "Schweinfurt", 50.049, 10.234, "Unterfranken", ["Bad Kissingen", "Haßberge", "Rhön-Grabfeld", "Schweinfurt (Stadt)", "Schweinfurt (Landkreis)"]),
 ("wuerzburg", "Würzburg", "Würzburg", 49.791, 9.953, "Unterfranken", ["Würzburg (Stadt)", "Würzburg (Landkreis)", "Kitzingen", "Main-Spessart"]),
 ("allgaeu", "Allgäu", "Kempten", 47.728, 10.315, "Schwaben", ["Kempten (Allgäu)", "Kaufbeuren", "Lindau (Bodensee)", "Oberallgäu", "Ostallgäu"]),
 ("augsburg", "Augsburg", "Augsburg", 48.371, 10.898, "Schwaben", ["Augsburg (Stadt)", "Augsburg (Landkreis)", "Aichach-Friedberg", "Dillingen a.d.Donau", "Donau-Ries"]),
 ("donau-iller", "Donau-Iller", "Krumbach", 48.244, 10.364, "Schwaben", ["Memmingen", "Günzburg", "Neu-Ulm", "Unterallgäu"]),
]
assert len(ILS) == 25
# Funkgruppen (Digitalfunk) je ILS – nur belegte Angaben; ergänzen aus eigener Geräteprogrammierung / BOS-Funk-App
FUNK = {   # eigene Angaben (Excel „Funkgruppen_Leitstellen_Bayern“, BOS-Funk-App / Geräteprogrammierung, Stand 16.11.2026)
 "muenchen": ["RD_1_M (Nord) – Kurzwahl 2513", "RD_2_M (Süd) – Kurzwahl 2514", "RD_Betten_M – Kurzwahl 2511 (Bettenanforderung)"],
 "erding": ["RD_ILS_ED – Kurzwahl 1913", "RD_Betten_ED – Kurzwahl 1912 (Bettenanforderung)"],
 "ffb": ["RD_ILS_FFB – Kurzwahl 2013", "RD_Betten_FFB – Kurzwahl 2012 (Bettenanforderung)"],
 "oberland": ["RD_ILS_WM – Kurzwahl 3013", "RD_Betten_WM – Kurzwahl 3012 (Bettenanforderung)"],
 "rosenheim": ["RD_ILS_RO – Kurzwahl 3313", "RD_Betten_RO – Kurzwahl 3312 (Bettenanforderung)"],
 "traunstein": ["RD_ILS_TS – Kurzwahl 3613", "RD_Betten_TS – Kurzwahl 3612 (Bettenanforderung)"],
}
FUNK_Q = "Funkgruppen: eigene Angabe (BOS-Funk-App / Geräteprogrammierung, Stand 16.11.2026)"
FUNK_ALT = {}   # frühere abweichende Angaben – entfernt, Kurzwahlen haben sich geändert (eigene Angabe ist aktuell)
vorhanden = {e["id"]: e for e in E}
for iid, name, sitz, lat, lon, bez, kreise in ILS:
    geo = {"lat": lat, "lon": lon, "quelle": "Feuerwache 4, eigener Zielpunkt (ZNA-Navi)" if iid == "muenchen" else Q_ORT + f" – {sitz}"}
    e = vorhanden.get("leitstelle-" + iid)
    if e:
        e.update(geo=geo, kreise=kreise)
        if iid in FUNK: e["funk"] = FUNK[iid]
        if Q_ANL1 not in e["quelle"]: e["quelle"] += " · " + Q_ANL1
        continue
    E.append({"id": "leitstelle-" + iid, "bereich": "leitstelle", "titel": f"Integrierte Leitstelle {name}", "kurz": f"ILS {name}",
              "suchbegriffe": [f"Leitstelle {name}", f"ILS {sitz.split(' (')[0]}", f"Leitstelle {sitz.split(' (')[0]}"],
              "siehe": [], "geo": geo, "kreise": kreise, **({"funk": FUNK[iid]} if iid in FUNK else {}),
              "abschnitte": [
                {"titel": "Zuständigkeitsbereich", "text": f"Rettungsdienstbereich {name} ({bez}):\n" + "\n".join("- " + k for k in kreise)},
                {"titel": "Sitz", "text": sitz},
                {"titel": "Telefon / Funk", "text": NE},
                {"titel": "Hinweis", "text": "Eintrag nur zur Zuordnung „welche ILS ist hier zuständig“. Notruf immer 112."}],
              "sprechtext": f"Integrierte Leitstelle {name}, Sitz {sitz.split(' (')[0]}. Zuständig für " + ", ".join(k.replace(" (Stadt)", " Stadt").replace(" (Landkreis)", " Landkreis") for k in kreise) + ".",
              "quelle": Q_ANL1 + " · " + Q_ORT, "stand": STAND})
# Funkgruppen (Feld „funk“) zeigt die App als eigenen Block oben im Eintrag, liest sie vor und nutzt sie in
# Standort-Karte und Wechselmeldung – der Abschnitt „Funk / Kanäle“ entfällt daher (München: nur Zusatzhinweise)
for e in E:
    iid = e["id"].removeprefix("leitstelle-")
    if iid not in FUNK or iid == "muenchen": continue
    e["funk"] = FUNK[iid]
    neu = []
    for a in e["abschnitte"]:
        if a["titel"] == "Funk / Kanäle": continue
        if a["titel"] == "Telefon / Funk": a = {"titel": "Telefon", "text": NE}
        neu.append(a)
    e["abschnitte"] = neu
    if FUNK_Q not in e["quelle"]: e["quelle"] += " · " + FUNK_Q

# RD-Kanäle der ILS München an deren Ort einsortieren
for rid in ("leitstelle-rd1m", "leitstelle-rd2m"):
    if rid in vorhanden: vorhanden[rid]["geo"] = {"lat": 48.156007, "lon": 11.555468, "quelle": "ILS München, Feuerwache 4"}

# ------------------------------------------------------------------ Übersicht
E.append({"id": "leitstelle-uebersicht", "bereich": "leitstelle", "titel": "Übersicht Leitstellen", "kurz": "Leitstellen",
 "suchbegriffe": ["Leitstellen", "ILS", "Integrierte Leitstellen", "Welche Leitstelle", "Leitstelle Landkreis", "Leitstellenbereiche"],
 "siehe": [e["titel"] for e in E if e["id"] in ("leitstelle-muenchen", "leitstelle-rd1m", "leitstelle-rd2m", "leitstelle-ffb", "leitstelle-erding", "leitstelle-oberland", "leitstelle-rosenheim")],
 "abschnitte": [
  {"titel": "Welcher Landkreis – welche ILS", "text": """- **ILS München:** Stadt München, Landkreis München (Rettungsdienst) – RD_1_M (Nord, 2513), RD_2_M (Süd, 2514), RD_Betten_M (2511)
- **ILS Fürstenfeldbruck (Maisach):** Dachau, Fürstenfeldbruck, Landsberg am Lech, Starnberg
- **ILS Erding:** Erding, Freising, Ebersberg
- **ILS Oberland (Weilheim):** Bad Tölz-Wolfratshausen, Garmisch-Partenkirchen, Weilheim-Schongau
- **ILS Rosenheim:** Stadt und Landkreis Rosenheim, Landkreis Miesbach"""},
  {"titel": "Merke", "text": "- Starnberg → ILS FFB · Ebersberg → ILS Erding · Miesbach / Agatharied → ILS Rosenheim\n- In Bayern gibt es eine Integrierte Leitstelle je Rettungsdienstbereich (25 Rettungsdienstbereiche, AVBayRDG Anlage 1)\n- Alle 25 ILS sind als eigene Einträge enthalten; im Bereich „Leitstellen“ zeigt die App die am Standort zuständige ILS an"},
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

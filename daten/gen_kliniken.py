"""Erzeugt daten/kliniken-muenchen-import.json – Münchner Kliniken mit Notaufnahme (Bereich „klinik“).

Nur belegte Angaben. Quellen: DKG Deutsches Krankenhausverzeichnis (Kurzprofile aus den
gesetzlichen Qualitätsberichten), muenchen.de „Medizinische Notdienste“ (Stand 23.12.2025),
Internetseiten / Flyer der Kliniken. Prüfdatum 15.11.2026.
"""
import json, sys

STAND = "2026-11"
DKG = "DKG Deutsches Krankenhausverzeichnis, Kurzprofil"
MUC = "muenchen.de – Medizinische Notdienste München (Stand 23.12.2025)"
HINWEIS = ("Zuweisung grundsätzlich über ILS / IVENA. Telefonnummern ohne Gewähr – recherchiert am 15.11.2026, "
           "vor dem Einsatz prüfen. Nicht ermittelte Angaben sind ausdrücklich gekennzeichnet.")
NE = "nicht ermittelt – über IVENA / Klinik prüfen"
NA = " – mit Notfallambulanz"

E = []

def klinik(id, titel, kurz, such, adresse, anmeldung, zentren, fach, fach_quelle, besonders, quellen, sprech):
    ab = [("Adresse / Anfahrt", adresse),
          ("Anmeldung (Telefon)", anmeldung),
          ("Zentren / Versorgungsstufe", zentren),
          ("Fachbereiche", fach_quelle + "\n" + "\n".join("- " + f for f in fach)),
          ("Besonderheiten", besonders),
          ("Hinweis", HINWEIS)]
    E.append({"id": "klinik-" + id, "bereich": "klinik", "titel": titel, "kurz": kurz,
              "suchbegriffe": list(such), "siehe": [],
              "abschnitte": [{"titel": t, "text": x.strip()} for t, x in ab if x and x.strip()],
              "sprechtext": sprech, "quelle": " · ".join(quellen), "stand": STAND})

# ------------------------------------------------------------------ LMU Großhadern
klinik("lmu-grosshadern", "LMU Klinikum – Campus Großhadern", "Großhadern",
 ["Großhadern", "Grosshadern", "Klinikum Großhadern", "LMU Großhadern", "Hadern", "Uniklinik Großhadern", "LMU Klinikum"],
 """Marchioninistraße 15, 81377 München
Zentrale: 089 4400-0
Anfahrt: Beschilderung „Klinikum der Universität“, dann „Notaufnahme“ – Zufahrt bis direkt vor die ZNA.""",
 """- **Zentrale Notaufnahme (ZNA):** 089 4400-44800
- Notaufnahmestation: 089 4400-44860
- Schockraum / Polytrauma: 089 4400-44878
- Chest-Pain-Telefon (V. a. Myokardinfarkt): 089 4400-75227
- Stroke-Telefon (V. a. Schlaganfall): 0174 3489381
- Dienstarzt MUM (Unfallchirurgie, 24 h): 089 4400-712222
- Rückfragen zu früheren Befunden: 089 4400-44819
- Kinderkardiologie – Notfälle, ECMO, Intensivtransport: 089 4400-72494
Voranmeldung erbeten bei V. a. Myokardinfarkt, V. a. Schlaganfall und Schockraum; ZNA arbeitet mit der ILS München / IVENA.""",
 """- Überregionales Traumazentrum und Versorger im Schwerstverletzungsartenverfahren (SAV) der BG (MUM, Schwerpunkt Unfallchirurgie)
- Universitätsklinikum (Maximalversorgung), 1.164 Betten (QB 2024)""",
 ["Klinik für Anaesthesiologie", "Medizinische Klinik und Poliklinik I", "Medizinische Klinik und Poliklinik II",
  "Medizinische Klinik und Poliklinik III", "Medizinische Klinik und Poliklinik IV", "Medizinische Klinik und Poliklinik V",
  "Herzchirurgische Klinik und Poliklinik", "Abteilung für Gefäßchirurgie", "Abteilung für Thoraxchirurgie" + NA,
  "Klinik für Allgemein-, Viszeral- und Transplantationschirurgie", "Muskuloskelettales Universitätszentrum München (MUM)" + NA,
  "Abteilung für Handchirurgie, Plastische Chirurgie und Ästhetische Chirurgie", "Neurochirurgische Klinik und Poliklinik",
  "Neurologische Klinik und Poliklinik (mit Friedrich-Baur-Institut, Deutschem Schwindel- und Gleichgewichtszentrum, Institut für Schlaganfall- und Demenzforschung)",
  "Institut für Diagnostische und Interventionelle Neuroradiologie", "Klinik und Poliklinik für Radiologie",
  "Klinik und Poliklinik für Nuklearmedizin", "Klinik und Poliklinik für Strahlentherapie und Radioonkologie",
  "Urologische Klinik und Poliklinik", "Klinik und Poliklinik für Frauenheilkunde und Geburtshilfe",
  "Klinik und Poliklinik für Hals-Nasen-Ohrenheilkunde", "Klinik und Poliklinik für Psychiatrie und Psychotherapie",
  "Klinik und Poliklinik für Palliativmedizin", "Kinderklinik im Dr. von Haunerschen Kinderspital – Neonatologie Großhadern",
  "Abteilung für Kinderkardiologie und pädiatrische Intensivmedizin",
  "Abteilung für Transfusionsmedizin, Zelltherapeutika und Hämostaseologie"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, reine Institute ohne Patientenversorgung weggelassen):",
 """- Am Campus stationiert: Intensivtransportwagen (ITW, ASB) und Intensivtransporthubschrauber „Christoph München“ (DRF)
- Notfall-Entbindung: Campus Großhadern
- Notfallversorgung Kinder: nicht hier, sondern im Dr. von Haunerschen Kinderspital (Campus Innenstadt)""",
 [DKG + " LMU Klinikum Campus Großhadern (QB 2024)", "lmu-klinikum.de – ZNA Campus Großhadern, Notfallversorgung, MUM, Anästhesiologie/Notfallmedizin"],
 "LMU Klinikum Großhadern, Marchioninistraße 15. Zentrale Notaufnahme 089 4400 44800. Schockraum 089 4400 44878. "
 "Chest Pain Telefon 089 4400 75227. Stroke Telefon 0174 3489381. Überregionales Traumazentrum.")

# ------------------------------------------------------------------ LMU Innenstadt
klinik("lmu-innenstadt", "LMU Klinikum – Campus Innenstadt", "LMU Innenstadt",
 ["Innenstadt", "LMU Innenstadt", "Klinikum Innenstadt", "Ziemssenstraße", "Nußbaumstraße", "Hauner", "Haunersches Kinderspital",
  "Kinderklinik Innenstadt", "Augenklinik LMU"],
 """Ziemssenstraße 5, 80336 München (ZNA / MUM)
Zentrale: 089 4400-0
Dr. von Haunersches Kinderspital: Lindwurmstraße 4, 80337 München
Parken nur begrenzt; gut mit ÖPNV erreichbar.""",
 """- **Zentrale Notaufnahme (ZNA):** 089 4400-31100
- Notaufnahmestation: 089 4400-31150
- Chirurgische Klinik – Ambulanz und Notaufnahme (24 h): 089 4400-52611
- Dienstarzt MUM (Unfallchirurgie, 24 h): 089 4400-519601
- Kindernotaufnahme Hauner: """ + NE + """
ILS wird über IVENA online über Behandlungskapazitäten informiert und meldet Zuweisungen an.""",
 """- MUM (Muskuloskelettales Universitätszentrum) mit Notfallversorgung inkl. Polytrauma auch am Standort Innenstadt
- Universitätsklinikum, 689 Betten (QB 2024)""",
 ["Institut für Notfallmedizin und Medizinmanagement" + NA, "Klinik für Anaesthesiologie",
  "Medizinische Klinik und Poliklinik I", "Medizinische Klinik und Poliklinik II", "Medizinische Klinik und Poliklinik III",
  "Medizinische Klinik und Poliklinik IV" + NA, "Medizinische Klinik und Poliklinik V",
  "Neurologische Klinik und Poliklinik (mit Friedrich-Baur-Institut)", "Muskuloskelettales Universitätszentrum München (MUM)",
  "Klinik für Allgemeine, Viszeral- und Transplantationschirurgie", "Abteilung für Gefäßchirurgie",
  "Abteilung für Hand-, Plastische und Ästhetische Chirurgie", "Klinik und Poliklinik für Augenheilkunde" + NA,
  "Klinik und Poliklinik für Hals-Nasen-Ohrenheilkunde", "Klinik und Poliklinik für Mund-, Kiefer- und Gesichtschirurgie",
  "Klinik und Poliklinik für Dermatologie und Allergologie", "Klinik und Poliklinik für Frauenheilkunde und Geburtshilfe",
  "Klinik und Poliklinik für Psychiatrie und Psychotherapie" + NA,
  "Klinik und Poliklinik für Kinder- und Jugendpsychiatrie, Psychosomatik und Psychotherapie",
  "Kinderklinik und Kinderpoliklinik im Dr. von Haunerschen Kinderspital",
  "Kinderchirurgische Klinik und Poliklinik im Dr. von Haunerschen Kinderspital",
  "Klinik und Poliklinik für Radiologie", "Klinik und Poliklinik für Nuklearmedizin",
  "Klinik und Poliklinik für Strahlentherapie und Radioonkologie", "Institut für Infektions- und Tropenmedizin",
  "Abteilung für Klinische Pharmakologie", "Abteilung für Transfusionsmedizin, Zelltherapeutika und Hämostaseologie"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, Zahnmedizin und reine Institute weggelassen):",
 """- **Notfallversorgung Kinder** des LMU Klinikums: Kinderklinik und Kinderchirurgische Klinik im Dr. von Haunerschen Kinderspital
- **Notfallversorgung Augenverletzungen:** Augenklinik Campus Innenstadt
- Das Hauner stellt im wöchentlichen Wechsel mit den Kinderkliniken Schwabing, Harlaching und Dritter Orden den Münchner Kindernotarzt""",
 [DKG + " LMU Klinikum Standort Innenstadt (QB 2024)", "lmu-klinikum.de – ZNA Campus Innenstadt, Notfallversorgung, MUM, KIPS", MUC],
 "LMU Klinikum Innenstadt, Ziemssenstraße 5. Zentrale Notaufnahme 089 4400 31100. Chirurgische Notaufnahme 089 4400 52611. "
 "Kindernotfälle im Haunerschen Kinderspital, Lindwurmstraße 4. Augennotfälle in der Augenklinik.")

# ------------------------------------------------------------------ TUM Rechts der Isar
klinik("rechts-der-isar", "TUM Klinikum Rechts der Isar", "Rechts der Isar",
 ["Rechts der Isar", "Klinikum rechts der Isar", "MRI", "TUM Klinikum", "Uniklinik TUM", "Ismaninger Straße"],
 """Ismaninger Straße 22, 81675 München
Zentrale: 089 4140-0
Parksituation angespannt.""",
 """- **Zentrale interdisziplinäre Notaufnahme (24 h, chirurgisch und internistisch):** 089 4140-2222
- Kreißsaal (24 h): 089 4140-2400
- Giftnotruf München (Abteilung Klinische Toxikologie, 24 h): 089 19240""",
 """- Überregionales Traumazentrum
- Cardiac Arrest Center
- Stroke Unit (Klinik für Neurologie, Station L1b)
- Universitätsklinikum (seit 01.08.2024 zusammen mit dem Deutschen Herzzentrum = TUM Universitätsklinikum), 1.094 Betten (QB 2024)""",
 ["Zentrale Interdisziplinäre Notaufnahme" + NA, "Innere Medizin I (Kardiologie, Angiologie, Pneumologie)",
  "Innere Medizin II (Gastroenterologie)", "Innere Medizin III (Hämatologie, Onkologie)", "Nephrologie",
  "Klinische Toxikologie & Giftnotruf München", "Anästhesiologie und Intensivmedizin", "Chirurgie mit Sektion Thoraxchirurgie",
  "Unfallchirurgie", "Orthopädie und Sportorthopädie", "Plastische Chirurgie und Handchirurgie",
  "Vaskuläre und Endovaskuläre Chirurgie", "Neurochirurgie", "Neurologie",
  "Diagnostische und Interventionelle Neuroradiologie" + NA, "Diagnostische und Interventionelle Radiologie",
  "Nuklearmedizin (mit Sektion Theranostik)", "RadioOnkologie und Strahlentherapie", "Urologie",
  "Frauenheilkunde mit Sektion Geburtshilfe und Perinatalmedizin", "Neonatologie", "Kinder- und Jugendmedizin",
  "Hals-, Nasen- und Ohrenheilkunde", "Augenheilkunde", "Mund-, Kiefer- und Gesichtschirurgie",
  "Psychiatrie und Psychotherapie", "Psychosomatische Medizin und Psychotherapie",
  "Präventive Sportmedizin und Sportkardiologie", "Ernährungsmedizin"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 45 Einträge; sinngemäß zusammengefasst, Sektionen zusammengeführt, reine Institute weggelassen):",
 "Gynäkologische Ambulanz nur werktags 8–20 Uhr; danach ist die ZNA erste Anlaufstelle für gynäkologische Notfälle.",
 [DKG + " Klinikum rechts der Isar – Stammgelände (QB 2024)", "tumklinikum.de / frauenklinik.mri.tum.de – Notfall, Wegweiser 06/2025", "neurologie.mri.tum.de – Flyer Stroke Unit L1b"],
 "TUM Klinikum Rechts der Isar, Ismaninger Straße 22. Zentrale interdisziplinäre Notaufnahme 089 4140 2222. "
 "Kreißsaal 089 4140 2400. Überregionales Traumazentrum, Cardiac Arrest Center, Stroke Unit.")

# ------------------------------------------------------------------ München Klinik Bogenhausen
klinik("mk-bogenhausen", "München Klinik Bogenhausen", "Bogenhausen",
 ["Bogenhausen", "Klinikum Bogenhausen", "MüK Bogenhausen", "Englschalkinger Straße", "Verbrennungszentrum", "Verbrennungsklinik", "Brandverletzte", "Schwerbrandverletzte", "Verbrennung Klinik"],
 """Englschalkinger Straße 77, 81925 München
Zentrale: 089 9270-0""",
 """- **Präklinik – Interdisziplinäre Notaufnahme (24 h):** 089 9270-2151""",
 """- Umfassende Notfallversorgung Stufe 3 / überregionales Notfallzentrum (laut Stadtratsvorlage 2019 – aktuelle Einstufung über IVENA prüfen)
- Stroke Unit (im Namen der Neurologischen Klinik)
- 959 Betten (QB 2024)""",
 ["Klinik für Akut- und Notfallmedizin" + NA, "Klinik für Kardiologie und Internistische Intensivmedizin" + NA,
  "Klinik für Herzchirurgie" + NA, "Klinik für Gefäßchirurgie" + NA, "Klinik für Thoraxchirurgie" + NA,
  "Klinik für Allgemein-, Viszeral-, Endokrine und Minimal-invasive Chirurgie" + NA,
  "Zentrum für Orthopädie, Unfallchirurgie und Sportmedizin" + NA,
  "Klinik für Plastische-, Rekonstruktive-, Hand- und Verbrennungschirurgie" + NA,
  "Klinik für Neurologie, Neurophysiologie, Kognitive Neurologie und Stroke Unit" + NA, "Klinik für Neurochirurgie",
  "Klinik für Urologie" + NA, "Klinik für Gastroenterologie, Hepatologie und Gastroenterologische Onkologie" + NA,
  "Klinik für Pneumologie und Pneumologische Onkologie, Lungenkrebszentrum" + NA,
  "Klinik für Endokrinologie, Diabetologie und Angiologie" + NA, "Klinik für Hämatologie und Onkologie" + NA,
  "Klinik für Rheumatologie, Klinische Immunologie und Osteologie" + NA,
  "Klinik für Anästhesiologie, Operative Intensivmedizin und Schmerztherapie",
  "Institut für Radiologie, Neuroradiologie und minimalinvasive Therapie", "Klinik für Frührehabilitation und Physikalische Medizin"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 18 Fachabteilungen; Neurochirurgie dort gesondert genannt):",
 "Verbrennungschirurgie (Brandverletzte) innerhalb der Plastischen Chirurgie; Herz-, Thorax- und Gefäßchirurgie im Haus.",
 [DKG + " München Klinik Bogenhausen (QB 2024)", MUC, "Stadtratsvorlage Bürgerversammlung Schwabing-West 10.10.2019 (risi.muenchen.de)"],
 "München Klinik Bogenhausen, Englschalkinger Straße 77. Interdisziplinäre Notaufnahme 089 9270 2151. "
 "Stroke Unit, Herzchirurgie, Thoraxchirurgie, Verbrennungschirurgie.")

# ------------------------------------------------------------------ München Klinik Harlaching
klinik("mk-harlaching", "München Klinik Harlaching", "Harlaching",
 ["Harlaching", "Klinikum Harlaching", "MüK Harlaching", "Sanatoriumsplatz", "Kinderklinik Harlaching"],
 """Sanatoriumsplatz 2, 81545 München
Zentrale: 089 6210-0""",
 """- **Zentrale Notaufnahme Erwachsene:** 089 6210-6666
- Kinderklinik Harlaching: 089 6210-2717 (englischsprachige Seite muenchen.de, Stand dort nicht datiert – prüfen)""",
 """- Umfassende Notfallversorgung Stufe 3 / überregionales Notfallzentrum (laut Stadtratsvorlage 2019 – aktuelle Einstufung über IVENA prüfen)
- Neurologie mit TEMPiS (Telemedizinisches Schlaganfall-Netzwerk)
- 673 Betten (QB 2024)""",
 ["Klinik für Akut- und Notfallmedizin" + NA, "Klinik für Kardiologie, Rhythmologie und internistische Intensivmedizin" + NA,
  "Klinik für Pneumologie, Internistische Intensiv- und Beatmungsmedizin" + NA,
  "Klinik für Gastroenterologie und Hepatologie" + NA, "Klinik für Nieren-, Hochdruck- und Rheumaerkrankungen" + NA,
  "Klinik für Hämatologie, Onkologie und Palliativmedizin" + NA,
  "Klinik für Neurologie und Neurologische Intensivmedizin – TEMPiS" + NA,
  "Klinik für Unfallchirurgie, Orthopädie und Wiederherstellungschirurgie" + NA,
  "Klinik für Allgemein-, Viszeralchirurgie und Coloproktologie" + NA, "Frauenklinik" + NA,
  "Klinik für Kinder- und Jugendmedizin" + NA, "Klinik für Neonatologie" + NA,
  "Klinik für Anästhesiologie, operative Intensivmedizin und Schmerztherapie",
  "Institut für Diagnostische und Interventionelle Radiologie und Neuroradiologie",
  "Klinik für Physikalische Medizin, Rehabilitation und Schmerzmedizin",
  "Klinik für Psychosomatische Medizin und Psychotherapie"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 16 Fachabteilungen):",
 "Kinderklinik beteiligt sich im wöchentlichen Wechsel am Münchner Kindernotarztdienst; Bereitschaftspraxis der Münchner Kinderärzte in der Kinderklinik Harlaching.",
 [DKG + " München Klinik Harlaching (QB 2024)", MUC, "Stadtratsvorlage 2019 (risi.muenchen.de)", "lmu-klinikum.de – KIPS / Kindernotarzt"],
 "München Klinik Harlaching, Sanatoriumsplatz 2. Zentrale Notaufnahme Erwachsene 089 6210 6666. "
 "Kinderklinik und Neonatologie im Haus. Neurologie mit TEMPiS.")

# ------------------------------------------------------------------ München Klinik Neuperlach
klinik("mk-neuperlach", "München Klinik Neuperlach", "Neuperlach",
 ["Neuperlach", "Klinikum Neuperlach", "MüK Neuperlach", "Oskar-Maria-Graf-Ring"],
 """Oskar-Maria-Graf-Ring 51, 81737 München
ZNA: Haus A, Ebene 1
Zentrale: 089 6794-0""",
 """- **ZNA chirurgisch:** 089 6794-0 (Zentrale)
- **ZNA internistisch:** 089 6794-2572
- Klinik für Akut- und Notfallmedizin (Sekretariat): 089 6794-2741""",
 """- Erweiterte Notfallversorgung (laut Stadtratsvorlage 2019 – aktuelle Einstufung über IVENA prüfen)
- 545 Betten (QB 2023)""",
 ["Klinik für Akut- und Notfallmedizin" + NA, "Klinik für Kardiologie, Pneumologie und Internistische Intensivmedizin" + NA,
  "Klinik für Gastroenterologie und Hepatologie" + NA,
  "Klinik für Nephrologie, Endokrinologie, Diabetologie, Angiologie und Rheumatologie" + NA,
  "Klinik für Hämatologie und Onkologie" + NA, "Klinik für Unfallchirurgie, Orthopädie und Wiederherstellungschirurgie" + NA,
  "Klinik für Allgemein-, Viszeralchirurgie und Koloproktologie" + NA,
  "Klinik für Gefäßchirurgie, vaskuläre und endovaskuläre Chirurgie, Gefäßmedizin" + NA,
  "Frauenklinik" + NA, "Zentrum für Akutgeriatrie und Frührehabilitation" + NA,
  "Klinik für Anästhesiologie, Operative Intensivmedizin und Schmerztherapie",
  "Institut für Diagnostische und Interventionelle Radiologie"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 12 Fachabteilungen):",
 "KVB-Bereitschaftspraxis München Süd-Ost im Klinikum (116117).",
 [DKG + " München Klinik Neuperlach (QB 2024)", MUC, "Stadtratsvorlage 2019 (risi.muenchen.de)", "kliniken.de"],
 "München Klinik Neuperlach, Oskar-Maria-Graf-Ring 51, Notaufnahme Haus A Ebene 1. Chirurgisch über die Zentrale 089 6794 0, "
 "internistisch 089 6794 2572.")

# ------------------------------------------------------------------ München Klinik Schwabing
klinik("mk-schwabing", "München Klinik Schwabing", "Schwabing",
 ["Schwabing", "Klinikum Schwabing", "MüK Schwabing", "Kölner Platz", "Kinderklinik Schwabing", "Parzivalstraße"],
 """Kölner Platz 1, 80804 München
ZNA: Haus 5, EG – Anfahrt über Tor 1, Isoldenstraße
Kinderklinik / Kindernotaufnahme: Parzivalstraße 16, 80804 München
Zentrale: 089 3068-0""",
 """- **ZNA Chirurgie (24 h):** 089 3068-2600 oder 089 3068-5500
- **ZNA Innere Medizin (24 h):** 089 3068-2210
- Kindernotaufnahme: """ + NE,
 """- Basisnotfallversorgung Stufe 1 / lokales Notfallzentrum (Planungsstand Stadtratsvorlage 2019 – aktuelle Einstufung über IVENA prüfen)
- 635 Betten (QB 2024)""",
 ["Klinik für Akut- und Notfallmedizin" + NA, "Klinik für Kardiologie, Pneumologie und Internistische Intensivmedizin" + NA,
  "Klinik für Viszeralmedizin" + NA, "Klinik für Endokrinologie, Diabetologie und Angiologie" + NA,
  "Klinik für Hämatologie, Onkologie, Immunologie, Palliativmedizin, Infektiologie und Tropenmedizin" + NA,
  "Klinik für Unfallchirurgie und Orthopädie" + NA, "Klinik für Neurochirurgie" + NA,
  "Hals-Nasen-Ohrenheilkunde, Kopf-, Hals- und Gesichtschirurgie" + NA, "Frauenklinik" + NA,
  "Klinik für Kinder- und Jugendmedizin" + NA, "Klinik für Kinderchirurgie" + NA, "Klinik für Neonatologie" + NA,
  "Klinik für Kinder- und Jugendpsychosomatik" + NA,
  "Klinik für Anästhesiologie, Kinderanästhesiologie, Operative Intensivmedizin und Schmerztherapie" + NA,
  "Institut für Diagnostische und Interventionelle Radiologie und Kinderradiologie" + NA,
  "Klinik für Physikalische Medizin, Frührehabilitation und Geriatrie" + NA],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 16 Fachabteilungen):",
 """- Kinderklinik und Kinderchirurgie (Kindernotaufnahme, Kinderchirurgische Notaufnahme); beteiligt am Münchner Kindernotarztdienst
- KVB-Bereitschaftspraxis im Klinikum (116117); Bereitschaftspraxis der Münchner Kinderärzte in der Kinderklinik Schwabing""",
 [DKG + " München Klinik Schwabing (QB 2024)", MUC, "Stadtratsvorlage 2019 (risi.muenchen.de)", "lmu-klinikum.de – KIPS / Kindernotarzt"],
 "München Klinik Schwabing, Kölner Platz 1, Notaufnahme Haus 5, Anfahrt Tor 1 Isoldenstraße. Chirurgie 089 3068 2600, "
 "Innere Medizin 089 3068 2210. Kinderklinik und Kinderchirurgie in der Parzivalstraße 16.")

# ------------------------------------------------------------------ Rotkreuzklinikum
klinik("rotkreuzklinikum", "Rotkreuzklinikum München", "Rotkreuz",
 ["Rotkreuzklinikum", "Rotkreuz", "Rotes Kreuz Klinikum", "Nymphenburger Straße", "Neuhausen"],
 """Nymphenburger Straße 163, 80634 München
Zentrale: 089 1303-0""",
 """- **Zentrale Notaufnahme:** 089 1303-2502""",
 """- Lokales Traumazentrum (zertifiziert, Angabe der Klinik)
- 435 Betten (QB 2024)""",
 ["Zentrale Notaufnahme" + NA, "Allgemein-, Viszeral-, Thorax- und Minimalinvasive Chirurgie" + NA,
  "Unfallchirurgie und Orthopädie", "Gefäßchirurgie", "Plastische und Ästhetische Chirurgie",
  "Innere Med. I – Kardiologie und Pneumologie", "Innere Med. II – Gastroenterologie", "Innere Med. III – Hämatologie und Onkologie",
  "Akutgeriatrie", "Gynäkologie (Senologie, Allg. Gyn. und Urogynäkologie, Gyn. Onkologie und Minimalinvasive Chirurgie)",
  "Geburtshilfe", "Neonatologie", "Anästhesiologie und Intensivmedizin", "Diagnostische Radiologie",
  "Belegabteilung Augenheilkunde", "Belegabteilung Urologie"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 16 Fachabteilungen):",
 "Frauenklinik nach eigener Angabe die geburtenstärkste Klinik Bayerns.",
 [DKG + " Rotkreuzklinikum München (QB 2024)", "DKG – Fachabteilung Zentrale Notaufnahme", "krankenhaus.de – Selbstdarstellung der Klinik"],
 "Rotkreuzklinikum München, Nymphenburger Straße 163. Zentrale Notaufnahme 089 1303 2502. Lokales Traumazentrum.")

# ------------------------------------------------------------------ Dritter Orden
klinik("dritter-orden", "Klinikum Dritter Orden München-Nymphenburg", "Dritter Orden",
 ["Dritter Orden", "Klinikum Dritter Orden", "Nymphenburg", "Menzinger Straße", "Kinderklinik Dritter Orden"],
 """Menzinger Straße 44, 80638 München
Zentrale: 089 1795-0""",
 """- **Notaufnahme Erwachsene:** 089 1795-1450
- **Notaufnahme Kinder:** 089 1795-1187
- Chest-Pain-Unit: 089 1795-1449
- Traumatelefon: 089 1795-1122""",
 """- Chest-Pain-Unit (zertifiziert)
- Traumazentrum im Traumanetzwerk München-Oberbayern Süd (zertifiziert nach DGU; Stufe in der Quelle nicht genannt)
- 632 Betten (QB 2023)""",
 ["Klinik für Innere Medizin I", "Klinik für Innere Medizin II" + NA, "Intensivbereich Innere Medizin",
  "Klinik für Allgemein-, Visceral- und Thoraxchirurgie" + NA, "Klinik für Gefäßchirurgie" + NA,
  "Klinik für Orthopädie und Unfallchirurgie" + NA, "Klinik für Gynäkologie und Geburtshilfe" + NA,
  "Klinik für Kinder- und Jugendmedizin" + NA, "Klinik für Kinderchirurgie" + NA, "Neonatologie und pädiatrische Intensivmedizin",
  "Klinik für Anästhesie und Intensivmedizin", "Intensivbereich Anästhesie", "Zentrum für Radiologie und Nuklearmedizin Nymphenburg",
  "Belegärzte HNO (Kinder und Erwachsene)", "Belegärzte Kinderchirurgie", "Belegärzte Mund-, Kiefer- und Gesichtschirurgie (Kinder und Erwachsene)",
  "Belegarzt Plastische und Ästhetische Chirurgie"],
 "Laut Qualitätsbericht 2023 (DKG-Kurzprofil, 17 Fachabteilungen):",
 "Kinderklinik beteiligt sich im wöchentlichen Wechsel am Münchner Kindernotarztdienst; Kinder-Bereitschaftspraxis im Haus.",
 [DKG + " Klinikum Dritter Orden (QB 2023)", "Klinikum Dritter Orden – Medizinisches Leistungsspektrum", MUC],
 "Klinikum Dritter Orden, Menzinger Straße 44. Notaufnahme Erwachsene 089 1795 1450, Kinder 089 1795 1187. "
 "Chest Pain Unit 089 1795 1449. Traumatelefon 089 1795 1122.")

# ------------------------------------------------------------------ Barmherzige Brüder
klinik("barmherzige-brueder", "Krankenhaus Barmherzige Brüder München", "Barmherzige Brüder",
 ["Barmherzige Brüder", "Barmherzige", "Romanstraße", "Romanplatz"],
 """Romanstraße 93, 80639 München
Zentrale: 089 1797-0""",
 """- **Notaufnahme (rund um die Uhr):** Direktnummer """ + NE + """ – über Zentrale 089 1797-0
- Sektion Unfallchirurgie: 089 1797-2535""",
 """- Chest-Pain-Unit (zertifiziert durch die DGK; Flyer 2016)
- Lokales Traumazentrum im Traumanetzwerk München-Oberbayern (Flyer 2016 – aktuellen Status prüfen)
- 404 Betten (QB 2024)""",
 ["Innere Medizin II / Schwerpunkt Kardiologie, Pneumologie und Notaufnahme" + NA,
  "Innere Medizin I / Schwerpunkt Gastroenterologie" + NA, "Allgemein- und Viszeralchirurgie" + NA,
  "Gefäßchirurgie" + NA, "Orthopädie und Unfallchirurgie" + NA, "Urologie" + NA, "Anästhesie" + NA, "Intensivmedizin",
  "Diagnostische und interventionelle Radiologie" + NA, "Geriatrie", "Palliativmedizin"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 11 Fachabteilungen):",
 "Notaufnahme organisatorisch bei der Inneren Medizin II (Kardiologie, Pneumologie und Notaufnahme).",
 [DKG + " Barmherzige Brüder Krankenhaus München (QB 2024)", "Flyer Innere Medizin II (2016)", "Flyer Sektion Unfallchirurgie (2022)"],
 "Krankenhaus Barmherzige Brüder, Romanstraße 93. Notaufnahme rund um die Uhr, über die Zentrale 089 1797 0. "
 "Chest Pain Unit.")

# ------------------------------------------------------------------ Helios West (Pasing)
klinik("helios-west", "Helios Klinikum München West", "Helios West",
 ["Pasing", "Helios Pasing", "Klinikum Pasing", "Helios West", "München West", "Steinerweg"],
 """Steinerweg 5, 81241 München (Pasing)
Zentrale: 089 8892-0""",
 """- **Zentrale Notaufnahme:** Direktnummer """ + NE + """ – über Zentrale 089 8892-0
- Kardiologie / Chest-Pain-Unit: 089 8892-2307
- Neurologie / Stroke Unit: 089 8892-2630
- Orthopädie, Unfallchirurgie (Traumazentrum): 089 8892-2314""",
 """- Chest-Pain-Unit (zertifiziert, DKG)
- Überregionale Stroke Unit (zertifiziert, DSG)
- Regionales Traumazentrum (zertifiziert, DGU)
- 412 Betten (QB 2024)""",
 ["Klinik für Kardiologie und Internistische Intensivmedizin, Chest Pain Unit" + NA,
  "Klinik für Neurologie, überregionale Stroke Unit" + NA, "Klinik für Pneumonologie, Lungenzentrum München West" + NA,
  "Klinik für Gastroenterologie, Diabetologie und Allgemeine Innere Medizin, Diabeteszentrum" + NA,
  "Klinik für Hämatologie, Onkologie und Palliativmedizin" + NA,
  "Klinik für Orthopädie, Unfallchirurgie und Sportorthopädie, regionales Traumazentrum" + NA,
  "Klinik für Allgemein- und Viszeralchirurgie, Minimal-Invasive Chirurgie, Koloproktologie und Klinik für Neurochirurgie" + NA,
  "Klinik für Gefäßchirurgie, Gefäßzentrum und Wundzentrum" + NA, "Klinik für Handchirurgie" + NA,
  "Endoprothetikzentrum, Klinik für Endoprothetik und Orthopädie" + NA,
  "Klinik für Hals-Nasen-Ohrenheilkunde, Kopf-Hals-Chirurgie" + NA, "Klinik für Mund-, Kiefer- und Plastische Gesichtschirurgie",
  "Klinik für Gynäkologie und Geburtshilfe" + NA, "Klinik für Gynäkologie und Gynäkologische Onkologie, Brustkrebszentrum",
  "Klinik für Geriatrie", "Klinik für Anästhesiologie und Intensivmedizin", "Zentrum für Radiologie" + NA],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 18 Einträge; Namen gekürzt, zwei Anästhesie-Einträge zusammengeführt):",
 "Neurochirurgie gemeinsam mit der Allgemein- und Viszeralchirurgie als Fachabteilung geführt.",
 [DKG + " Helios Klinikum München West (QB 2024)", "kliniken.de – Fachabteilungen Helios Klinikum München West"],
 "Helios Klinikum München West in Pasing, Steinerweg 5. Notaufnahme über die Zentrale 089 8892 0. "
 "Chest Pain Unit, überregionale Stroke Unit, regionales Traumazentrum.")

# ------------------------------------------------------------------ Helios Perlach
klinik("helios-perlach", "Helios Klinik München Perlach", "Helios Perlach",
 ["Helios Perlach", "Perlach", "Klinik Perlach", "Schmidbauerstraße"],
 """Schmidbauerstraße 44, 81737 München
Zentrale: 089 67802-1""",
 """- **Notaufnahme:** Direktnummer """ + NE + """ – über Zentrale 089 67802-1
- Chirurgie / Unfallchirurgie: 089 67802-222
- Innere Medizin / Gastroenterologie: 089 67802-221""",
 """- Lokales Traumazentrum im Traumanetzwerk München-Oberbayern-Süd
- Alterstraumazentrum
- Grund- und Regelversorgung, 150 Betten (QB 2024)""",
 ["Klinik für Innere Medizin / Gastroenterologie" + NA, "Klinik für Akutgeriatrie",
  "Klinik für Allgemeine-, Viszeral- und Thoraxchirurgie und Klinik für Gefäßchirurgie" + NA,
  "Klinik für Unfallchirurgie und Orthopädie, Lokales Traumazentrum, Alterstraumazentrum" + NA,
  "Klinik für Handchirurgie (Zentrum Helios Klinikum München West)" + NA,
  "Klinik für Anästhesie und Intensivmedizin", "Zentrum für Radiologie" + NA],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 8 Einträge; zwei Anästhesie-Einträge zusammengeführt):",
 "Nicht verwechseln mit der München Klinik Neuperlach (Oskar-Maria-Graf-Ring).",
 [DKG + " Helios Klinik München Perlach (QB 2024)", "G-BA Qualitätsbericht 2024 (Referenzbericht)", "kliniken.de"],
 "Helios Klinik München Perlach, Schmidbauerstraße 44. Notaufnahme über die Zentrale 089 67802 1. "
 "Lokales Traumazentrum und Alterstraumazentrum.")

# ------------------------------------------------------------------ Martha-Maria
klinik("martha-maria", "Krankenhaus Martha-Maria München", "Martha-Maria",
 ["Martha Maria", "Martha-Maria", "Solln", "Wolfratshauser Straße"],
 """Wolfratshauser Straße 109, 81479 München
Zentrale: 089 7276-0""",
 """- Notfallambulanz Chirurgie: Direktnummer """ + NE + """ – über Zentrale 089 7276-0""",
 """- Keine zentrale Notaufnahme ausgewiesen; Notfallambulanz nur bei der Chirurgie (lt. DKG)
- Zentren / Notfallstufe: """ + NE + """
- 110 Betten (QB 2024)""",
 ["Klinik für Allgemein-, Visceral- und Thoraxchirurgie" + NA, "Innere Medizin", "Hals-, Nasen-, Ohrenheilkunde",
  "Abteilung für Anästhesiologie und Intensivmedizin"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 4 Fachabteilungen):",
 "Kleines Haus; Umfang der Notfallversorgung (z. B. internistische Notfälle) nicht ermittelt – vor Anfahrt über IVENA klären.",
 [DKG + " Krankenhaus Martha-Maria München (QB 2024)"],
 "Krankenhaus Martha-Maria, Wolfratshauser Straße 109 in Solln. Notfallambulanz der Chirurgie, Zentrale 089 7276 0. "
 "Umfang der Notfallversorgung über IVENA klären.")

# ------------------------------------------------------------------ Deutsches Herzzentrum
klinik("dhz", "TUM Klinikum Deutsches Herzzentrum", "Herzzentrum",
 ["Deutsches Herzzentrum", "Herzzentrum", "DHM", "DHZ", "Lazarettstraße", "Kinderkardiologie"],
 """Lazarettstraße 36, 80636 München
Zentrale: 089 1218-0""",
 """- **Chest-Pain-Unit (Notaufnahme für Herzpatienten, 24 h):** 089 1218-4552 oder 089 1218-4551
- Herzchirurgie – Dienstarzt nachts: 089 1218-3106""",
 """- Fachkrankenhaus für Herz- und Kreislauferkrankungen (Kinder und Erwachsene); keine allgemeine interdisziplinäre Notaufnahme
- Chest-Pain-Unit rund um die Uhr; bei kritischem Zustand Aufnahme auf die Intensivstation
- Seit 01.08.2024 Teil des TUM Universitätsklinikums; 197 Betten (QB 2023)""",
 ["Klinik für Herz- und Kreislauferkrankungen", "Klinik für Herz- und Gefäßchirurgie",
  "Klinik für angeborene Herzfehler und Kinderkardiologie", "Klinik für Chirurgie angeborener Herzfehler und Kinderherzchirurgie"],
 "Laut Qualitätsbericht 2023 (DKG-Kurzprofil, 4 Fachabteilungen):",
 "Nur für kardiale Notfälle geeignet (Chest-Pain-Unit mit Herzkatheter).",
 [DKG + " TUM Klinikum Deutsches Herzzentrum (QB 2023)", "deutsches-herzzentrum-muenchen.de – Notfall / Chest Pain Unit"],
 "TUM Klinikum Deutsches Herzzentrum, Lazarettstraße 36. Chest Pain Unit rund um die Uhr, 089 1218 4552. "
 "Nur kardiale Notfälle.")

# ================================================================== UMLAND
# ------------------------------------------------------------------ Ebersberg
klinik("ebersberg", "Klinikum Ebersberg München Ost (Kreisklinik Ebersberg)", "Ebersberg",
 ["Ebersberg", "Kreisklinik Ebersberg", "Klinikum Ebersberg", "München Ost", "Klinik Ebersberg"],
 """Pfarrer-Guggetzer-Straße 3, 85560 Ebersberg
Zentrale: 08092 82-0""",
 """- **Zentrale Notaufnahme:** Direktnummer """ + NE + """ – über Zentrale 08092 82-0""",
 """- Erweiterte Notfallversorgung (Selbstdarstellung der Klinik)
- Regionales Traumazentrum (DGU, zertifiziert bis 02.2028) – in Kooperation mit der Neurochirurgie des TUM Klinikums Rechts der Isar
- Chest Pain Unit (bis 01.2027), Cardiac Arrest Center (bis 04.2027), Stroke Unit (bis 07.2027), Heart Failure Unit
- 328 Betten (QB 2024)""",
 ["Klinische Akut- und Notfallmedizin" + NA, "Innere Medizin / Schwerpunkt Kardiologie" + NA,
  "Innere Medizin / Schwerpunkt Gastroenterologie" + NA, "Innere Medizin / Schwerpunkt Hämatologie und internistische Onkologie",
  "Akutgeriatrie", "Palliativmedizin", "Allgemein-, Visceral- und Gefäßchirurgie" + NA, "Gefäßchirurgie & Gefäßmedizin" + NA,
  "Unfallchirurgie & Orthopädie, Wiederherstellungschirurgie und Sportmedizin" + NA,
  "Plastische Chirurgie & Handchirurgie", "Urologie", "Gynäkologie (inkl. Brustzentrum)" + NA, "Geburtshilfe" + NA,
  "Hals-, Nasen-, Ohrenheilkunde", "Anästhesie und Intensivmedizin", "Diagnostische und Interventionelle Radiologie",
  "Belegabteilung für Orthopädie", "Belegabteilung Herz-Lungen-Praxis Ebersberg"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 18 Fachabteilungen):",
 """- Linksherzkatheter im Haus
- Tritt inzwischen als „Klinikum Ebersberg München Ost“ auf (ehemals Kreisklinik Ebersberg)""",
 [DKG + " Kreisklinik Ebersberg (QB 2024, Zertifikate)", "klinik-ebe.de", "privat-patienten.de – Fachabteilungsangaben"],
 "Klinikum Ebersberg, ehemals Kreisklinik, Pfarrer-Guggetzer-Straße 3. Notaufnahme über die Zentrale 08092 82 0. "
 "Regionales Traumazentrum, Chest Pain Unit, Cardiac Arrest Center, Stroke Unit.")

# ------------------------------------------------------------------ Starnberg
klinik("starnberg", "Klinikum Starnberg (Kreisklinik Starnberg)", "Starnberg",
 ["Starnberg", "Kreisklinik Starnberg", "Klinikum Starnberg", "Kreiskrankenhaus Starnberg", "Starnberger Kliniken"],
 """Oßwaldstraße 1, 82319 Starnberg
Zentrale: 08151 18-0""",
 """- **Zentrale Notaufnahme (interdisziplinär, rund um die Uhr):** Direktnummer """ + NE + """ – über Zentrale 08151 18-0
- Kreißsaal / Geburtshilfe: 08151 18-2310""",
 """- Grund- und Regelversorgung mit interdisziplinärer Notaufnahme
- Chest Pain Unit (laut KTQ-Qualitätsbericht 2025; DKG-Zertifikat dort nicht gelistet)
- Neonatologische Intensivstation Level II
- Traumazentrum / Stroke Unit: """ + NE + """
- 300 Betten (QB 2024)""",
 ["Innere Medizin incl. Neurologie und Hämato- / Onkologie" + NA, "Kardiologie" + NA, "Gastroenterologie" + NA,
  "Nephrologie" + NA, "Palliativmedizin", "Allgemein- und Viszeralchirurgie" + NA, "Endokrine Chirurgie" + NA,
  "Unfallchirurgie" + NA, "Orthopädie", "Handchirurgie", "Urologie", "Frauenheilkunde" + NA, "Geburtshilfe" + NA,
  "Pädiatrie" + NA, "Neonatologie" + NA, "Anästhesiologie und operative Intensivmedizin",
  "Belegabteilung Gastroenterologie", "Belegabteilung Hals-, Nasen-, Ohrenheilkunde"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 18 Fachabteilungen):",
 """- KVB-Bereitschaftspraxis im Klinikum zur Entlastung der Notaufnahme
- Kinderklinik mit Notfallambulanz; Neonatologie im Haus
- Teil der Starnberger Kliniken (weitere Häuser: Seefeld, Herrsching, Penzberg)""",
 [DKG + " Klinikum Starnberg (QB 2024)", "KTQ-Qualitätsbericht Starnberger Kliniken 2025", "krankenhaus.de / Stellenausschreibungen Starnberger Kliniken"],
 "Klinikum Starnberg, Oßwaldstraße 1. Interdisziplinäre Notaufnahme rund um die Uhr, über die Zentrale 08151 18 0. "
 "Chest Pain Unit, Kinderklinik und Neonatologie im Haus.")

# ------------------------------------------------------------------ Erding
klinik("erding", "Klinikum Landkreis Erding", "Erding",
 ["Erding", "Klinikum Erding", "Kreisklinik Erding", "Krankenhaus Erding", "Bajuwarenstraße"],
 """Bajuwarenstraße 5, 85435 Erding
Zentrale: 08122 59-0""",
 """- **Zentrale Notaufnahme (24/7):** Direktnummer """ + NE + """ – über Zentrale 08122 59-0
- Unfallchirurgie und Orthopädie: 08122 59-5700""",
 """- Regionales Traumazentrum (DGU, zertifiziert bis 03.2027), TraumaNetzwerk
- Chest Pain Unit (DKG, zertifiziert bis 10.2027; Betrieb seit August 2023)
- Stroke Unit (DSG, zertifiziert bis 03.2028)
- 288 Betten (QB 2024)""",
 ["Innere Medizin – Kardiologie und Pneumologie", "Innere Medizin – Gastroenterologie und Stoffwechsel",
  "Unfallchirurgie und Orthopädie", "Visceral- und Thoraxchirurgie, Plastische Chirurgie", "Gefäßchirurgie", "Urologie",
  "Gynäkologie und Geburtshilfe", "Intensivmedizin", "Radiologie und Nuklearmedizin", "Interdisziplinäre Schmerztherapie",
  "Hals-, Nasen-, Ohrenheilkunde (Belegabteilung)", "Orthopädie (Belegabteilung)", "Urologie (Belegabteilung)"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 13 Fachabteilungen; Notfallambulanzen dort nicht einzeln ausgewiesen):",
 """- Akutgeriatrie seit Februar 2025 von Dorfen nach Erding verlagert
- Stroke Unit: Thrombektomien werden bei Bedarf vor Ort durchgeführt, das Team wird dafür eingeflogen (Pressemitteilung Oktober 2025 – Ablauf über IVENA / Klinik klären)
- Außenstelle Klinik Dorfen (Erdinger Straße 17, 84405 Dorfen) ist ein eigener kleiner Standort""",
 [DKG + " Klinikum Landkreis Erding (QB 2024, Zertifikate)", "Landkreis Erding – Pressemitteilungen 2024 und 2025", "kliniken.de"],
 "Klinikum Landkreis Erding, Bajuwarenstraße 5. Notaufnahme rund um die Uhr, über die Zentrale 08122 59 0. "
 "Regionales Traumazentrum, Chest Pain Unit, Stroke Unit.")

# ------------------------------------------------------------------ Agatharied
klinik("agatharied", "Krankenhaus Agatharied", "Agatharied",
 ["Agatharied", "Krankenhaus Agatharied", "Klinik Agatharied", "Hausham", "Miesbach", "Kreisklinik Miesbach"],
 """Norbert-Kerkel-Platz 1, 83734 Hausham
Zentrale: 08026 393-0""",
 """- **Notaufnahme (Integriertes Notfall- und Behandlungszentrum, INBZ):** Direktnummer """ + NE + """ – über Zentrale 08026 393-0
- Allgemein-, Viszeral-, Gefäß- und Endokrine Chirurgie: 08026 393-2444
- Innere Medizin: 08026 393-2222""",
 """- Stroke Unit (zertifiziert bis 03.2028)
- EndoProthetikZentrum der Maximalversorgung, Schulter- und Ellenbogenklinik
- Traumazentrum / Chest Pain Unit: """ + NE + """
- 350 Betten (QB 2024)""",
 ["Innere Medizin – Schwerpunkt Kardiologie" + NA,
  "Innere Medizin – Schwerpunkt Gastroenterologie, Diabetologie, Hämato-/Onkologie" + NA,
  "Innere Medizin – Schwerpunkt Geriatrie" + NA, "Neurologie" + NA,
  "Allgemein-, Viszeral-, Gefäß- und Endokrine Chirurgie" + NA, "Unfallchirurgie und Orthopädie" + NA,
  "Gynäkologie und Geburtshilfe" + NA, "Kinder- und Jugendmedizin" + NA, "Hals-, Nasen-, Ohrenheilkunde",
  "Anästhesie und Intensivmedizin", "Palliativmedizin", "Radiologie"],
 "Laut Qualitätsbericht 2024 (DKG-Kurzprofil, 12 Fachabteilungen):",
 """- Kinder- und Jugendmedizin mit Notfallambulanz im Haus
- Auf dem Gelände: kbo-Lech-Mangfall-Klinik Agatharied (Psychiatrie, Psychosomatik), St.-Agatha-Straße 1a, 08026 393-7000""",
 [DKG + " Krankenhaus Agatharied (QB 2024, Zertifikate)", DKG + " kbo-Lech-Mangfall-Klinik Agatharied"],
 "Krankenhaus Agatharied in Hausham, Norbert-Kerkel-Platz 1. Notaufnahme über die Zentrale 08026 393 0. "
 "Stroke Unit, Neurologie und Kinderklinik im Haus.")

# ------------------------------------------------------------------ kbo Haar
klinik("kbo-haar", "kbo-Isar-Amper-Klinikum Haar (Neurologie / Psychiatrie)", "kbo Haar",
 ["Haar", "kbo Haar", "kbo", "Isar-Amper-Klinikum", "IAK", "Klinikum München-Ost", "Psychiatrie Haar", "Neurologie Haar",
  "Stroke Haar", "Psych", "Psychiatrie"],
 """Vockestraße 72, 85540 Haar
Klinik für Neurologie: Ringstraße 56/A (auf dem Klinikgelände)
Anfahrt über A94: Ausfahrt Feldkirchen-Ost, B 471 Richtung Haar durch Ottendichl, in Haar an der Ampel links ins Klinikum
Zentrale: 089 4562-0""",
 """- **Psychiatrie – Zentrale Aufnahme / Leitstelle (rund um die Uhr):** 089 4562-0
- **Stroke Unit / Neurologische Intensivstation:** 089 4562-3441
- Neurologie Sekretariat (Mo–Fr 8–16 Uhr): 089 4562-3884""",
 """- Stroke Unit (zertifiziert bis 12.2026)
- Klinik für Neurologie mit Zentrum für Neurologische Intensivmedizin
- Psychiatrische Vollversorgung nach Sektorisierung der Stadt München und umliegender Landkreise
- 750 Betten (QB 2024)""",
 ["Allgemeine Psychiatrie" + NA, "Neurologie",
  "Klinik für Neurologie: Stroke Unit, Neurologische Intensivstation, Frühreha Phase B, Multimodale Schmerztherapie, Palliativmedizin",
  "Klinik für Psychiatrie und Psychotherapie", "Klinik für Suchtmedizin und Psychotherapie",
  "Klinik für Psychosomatik, Psychotherapie und Psychiatrie",
  "Zentrum für Altersmedizin und Entwicklungsstörungen (Gerontopsychiatrie)",
  "Forensische Psychiatrie und Psychotherapie"],
 "Laut Qualitätsbericht 2024 nur zwei Fachabteilungen (die ersten beiden Einträge); die Kliniken darunter sind die Gliederung laut kbo-Internetseite:",
 """- Unterbringungen nach BayPsychKHG aus dem Landkreis München gehen in der Regel ins kbo-Isar-Amper-Klinikum
- Klinik Nord (Psychiatrie) in Schwabing, Kölner Platz 1, Haus 7 – Anmeldung ebenfalls über 089 4562-0
- Krisenzentrum Atriumhaus: Bavariastraße 11, 80336 München, 089 7678-0
- Kinder- und Jugendpsychiatrie: kbo-Heckscher-Klinikum, Standort Haar, Max-Isserlin-Straße 23, 089 4132539-0
- Krisendienste Bayern (24 h): 0800 655 3000
- Psychiatrische Notfallambulanz auch im LMU Klinikum Campus Innenstadt (Klinik und Poliklinik für Psychiatrie und Psychotherapie, laut QB 2024)""",
 [DKG + " kbo-Isar-Amper-Klinikum Haar (QB 2024, Zertifikate)", "kbo-iak.de – Telefonkontakte Neurologie, Flyer Klinik Nord und Suchtmedizin",
  "Landratsamt München – Unterbringung psychisch kranker Menschen", DKG + " kbo-Heckscher-Klinikum Haar", MUC],
 "kbo Isar-Amper-Klinikum Haar, Vockestraße 72. Psychiatrische Aufnahme rund um die Uhr 089 4562 0. "
 "Stroke Unit und neurologische Intensivstation 089 4562 3441.")

# ================================================================== ÜBERSICHTEN NACH VERSORGUNGSMÖGLICHKEIT
# Nur Häuser, für die das Merkmal in den Quellen der Einzeleinträge belegt ist. Nicht abschließend.
UMLAND = {"ebersberg", "starnberg", "erding", "agatharied", "kbo-haar"}
UE_HINWEIS = ("Nur Häuser, für die das Merkmal in den recherchierten Quellen belegt ist – die Liste ist NICHT abschließend. "
              "Zielklinik und Aufnahmebereitschaft immer über ILS / IVENA. Details im jeweiligen Klinik-Eintrag.")

def _k(id):
    for e in E:
        if e["id"] == "klinik-" + id:
            return e
    raise KeyError(id)

def uebersicht(id, titel, kurz, such, einleitung, zeilen, zusatz="", siehe=()):
    """zeilen: Liste (klinik_id, merkmal, telefon)"""
    muc, uml, sprech = [], [], []
    for kid, merkmal, tel in zeilen:
        k = _k(kid)
        z = f"- **{k['kurz']}** – {merkmal}" + (f" – {tel}" if tel else "")
        (uml if kid in UMLAND else muc).append(z)
        sprech.append(k["kurz"] + (", " + tel.replace("-", " ") if tel else ""))
    ab = [("Überblick", einleitung)]
    if muc: ab.append(("München", "\n".join(muc)))
    if uml: ab.append(("Umland", "\n".join(uml)))
    if zusatz: ab.append(("Ergänzend", zusatz))
    ab.append(("Hinweis", UE_HINWEIS))
    quellen = sorted({q for kid, _, _ in zeilen for q in _k(kid)["quelle"].split(" · ")})
    E.append({"id": "klinik-uebersicht-" + id, "bereich": "klinik", "titel": titel, "kurz": kurz,
              "suchbegriffe": list(such), "siehe": [_k(kid)["titel"] for kid, _, _ in zeilen] + list(siehe),
              "abschnitte": [{"titel": t, "text": x.strip()} for t, x in ab],
              "sprechtext": f"{titel}. " + ". ".join(sprech) + ". Nicht abschließend, Zuweisung über IVENA.",
              "quelle": "Zusammenstellung aus den Klinik-Einträgen: " + " · ".join(quellen), "stand": STAND})

uebersicht("stroke", "Übersicht Stroke Units", "Stroke Units",
 ["Stroke", "Stroke Unit", "Stroke Units", "Stroke Klinik", "Stroke Kliniken", "Schlaganfall Klinik", "Schlaganfallklinik", "Lyse Klinik"],
 "Kliniken mit belegter Stroke Unit bzw. Stroke-Telefon / neurologischer Schlaganfallversorgung.",
 [("lmu-grosshadern", "Stroke-Telefon", "0174 3489381"),
  ("rechts-der-isar", "Stroke Unit (Neurologie, Station L1b), ZNA", "089 4140-2222"),
  ("mk-bogenhausen", "Stroke Unit (Neurologische Klinik), Notaufnahme", "089 9270-2151"),
  ("mk-harlaching", "Neurologie mit TEMPiS, ZNA", "089 6210-6666"),
  ("helios-west", "überregionale Stroke Unit (DSG), Neurologie", "089 8892-2630"),
  ("kbo-haar", "Stroke Unit (zertifiziert bis 12.2026)", "089 4562-3441"),
  ("ebersberg", "Stroke Unit (zertifiziert bis 07.2027), Zentrale", "08092 82-0"),
  ("erding", "Stroke Unit (DSG, zertifiziert bis 03.2028), Zentrale", "08122 59-0"),
  ("agatharied", "Stroke Unit (zertifiziert bis 03.2028), Zentrale", "08026 393-0")],
 "Erding: Thrombektomien bei Bedarf vor Ort durch eingeflogenes Team (Pressemitteilung Oktober 2025).")

uebersicht("cpu", "Übersicht Chest Pain Units", "Chest Pain Units",
 ["Chest Pain", "Chest Pain Unit", "Chest Pain Units", "CPU", "Herzkatheter", "Herzkatheter Klinik", "Brustschmerz Klinik", "Brustschmerzeinheit"],
 "Kliniken mit belegter Chest Pain Unit bzw. Chest-Pain-Telefon. Laut Gesundheitsreferat (2023) gibt es in München 12 Chest Pain Units – hier sind nur die belegten aufgeführt.",
 [("lmu-grosshadern", "Chest-Pain-Telefon", "089 4400-75227"),
  ("dhz", "Chest Pain Unit (24 h)", "089 1218-4552"),
  ("dritter-orden", "Chest Pain Unit (zertifiziert)", "089 1795-1449"),
  ("barmherzige-brueder", "Chest Pain Unit (DGK, Flyer 2016), Zentrale", "089 1797-0"),
  ("helios-west", "Chest Pain Unit (zertifiziert), Kardiologie", "089 8892-2307"),
  ("ebersberg", "Chest Pain Unit (zertifiziert bis 01.2027), Zentrale", "08092 82-0"),
  ("erding", "Chest Pain Unit (DKG, zertifiziert bis 10.2027), Zentrale", "08122 59-0"),
  ("starnberg", "Chest Pain Unit (laut KTQ-Bericht 2025), Zentrale", "08151 18-0")],
 siehe=["Akutes Koronarsyndrom"])

uebersicht("trauma", "Übersicht Traumazentren", "Traumazentren",
 ["Traumazentren", "Trauma Klinik", "Traumaklinik", "Traumakliniken", "Überregionales Traumazentrum", "Regionales Traumazentrum",
  "Lokales Traumazentrum", "Polytrauma Klinik", "Schockraum Klinik"],
 "Traumazentren nach belegter Stufe (DGU / TraumaNetzwerk). Schockraum-Kriterien: siehe Eintrag Schockraum-Indikation.",
 [("lmu-grosshadern", "überregional, SAV – Schockraum / Polytrauma", "089 4400-44878"),
  ("rechts-der-isar", "überregional – ZNA", "089 4140-2222"),
  ("helios-west", "regional (DGU) – Unfallchirurgie", "089 8892-2314"),
  ("ebersberg", "regional (bis 02.2028), Neurochirurgie in Kooperation mit Rechts der Isar – Zentrale", "08092 82-0"),
  ("erding", "regional (bis 03.2027) – Zentrale", "08122 59-0"),
  ("rotkreuzklinikum", "lokal – ZNA", "089 1303-2502"),
  ("barmherzige-brueder", "lokal (Flyer 2016) – Zentrale", "089 1797-0"),
  ("helios-perlach", "lokal, Alterstraumazentrum – Zentrale", "089 67802-1"),
  ("dritter-orden", "Traumazentrum (Stufe in der Quelle nicht genannt) – Traumatelefon", "089 1795-1122"),
  ("lmu-innenstadt", "MUM, Notfallversorgung inkl. Polytrauma (Stufe nicht genannt) – ZNA", "089 4400-31100")],
 siehe=["Schockraum-Indikation (Bayerische Traumanetzwerke)"])

uebersicht("kinder", "Übersicht Kinderkliniken / Kindernotaufnahmen", "Kinderkliniken",
 ["Kinderklinik", "Kinderkliniken", "Kindernotaufnahme", "Kinder Notaufnahme", "Kinderchirurgie", "Kinderchirurgische Klinik",
  "Pädiatrie Klinik", "Kinder Klinik"],
 "Kliniken mit Kinder- und Jugendmedizin bzw. Kinderchirurgie mit Notfallambulanz (laut Qualitätsbericht) oder Kindernotaufnahme.",
 [("lmu-innenstadt", "Dr. von Haunersches Kinderspital, Lindwurmstraße 4 – Kinderklinik und Kinderchirurgie", ""),
  ("mk-schwabing", "Kinderklinik und Kinderchirurgie, Neonatologie – Parzivalstraße 16", ""),
  ("mk-harlaching", "Kinderklinik, Neonatologie", "089 6210-2717"),
  ("dritter-orden", "Notaufnahme Kinder, Kinderchirurgie, Neonatologie", "089 1795-1187"),
  ("starnberg", "Pädiatrie und Neonatologie (Level II) – Zentrale", "08151 18-0"),
  ("agatharied", "Kinder- und Jugendmedizin – Zentrale", "08026 393-0")],
 """- Münchner Kindernotarzt: wöchentlicher Wechsel zwischen Hauner, Schwabing, Harlaching und Dritter Orden
- Kinderkardiologie / angeborene Herzfehler: Deutsches Herzzentrum (089 1218-0); LMU Großhadern Kinderkardiologie – Notfälle, ECMO, Intensivtransport 089 4400-72494
- Kinder- und Jugendpsychiatrie: kbo-Heckscher-Klinikum Haar, 089 4132539-0
- TUM Rechts der Isar hat Kinder- und Jugendmedizin im Haus (Notfallambulanz dort nicht ausgewiesen)""")

uebersicht("cac", "Übersicht Cardiac Arrest Center", "Cardiac Arrest Center",
 ["Cardiac Arrest Center", "Cardiac Arrest Zentrum", "CAC", "Reanimationszentrum", "Post ROSC Klinik", "ROSC Klinik"],
 "Kliniken mit belegtem Cardiac Arrest Center (Versorgung nach Kreislaufstillstand / ROSC).",
 [("rechts-der-isar", "Cardiac Arrest Center – ZNA", "089 4140-2222"),
  ("ebersberg", "Cardiac Arrest Center (zertifiziert bis 04.2027) – Zentrale", "08092 82-0")],
 siehe=["Kreislaufstillstand / Reanimation"])

uebersicht("neurochirurgie", "Übersicht Neurochirurgie", "Neurochirurgie",
 ["Neurochirurgie", "Neurochirurgie Klinik", "Neurochirurgische Klinik", "Neurochirurgien", "SHT Klinik"],
 "Kliniken mit eigener Neurochirurgie (laut Qualitätsbericht).",
 [("lmu-grosshadern", "Neurochirurgische Klinik – ZNA", "089 4400-44800"),
  ("rechts-der-isar", "Neurochirurgie – ZNA", "089 4140-2222"),
  ("mk-bogenhausen", "Klinik für Neurochirurgie – Notaufnahme", "089 9270-2151"),
  ("mk-schwabing", "Klinik für Neurochirurgie (mit Notfallambulanz) – ZNA Chirurgie", "089 3068-2600"),
  ("helios-west", "Neurochirurgie (gemeinsam mit Allgemein- und Viszeralchirurgie) – Zentrale", "089 8892-0")],
 "Ebersberg: regionales Traumazentrum mit Neurochirurgie in Kooperation mit dem TUM Klinikum Rechts der Isar (keine eigene Neurochirurgie).")

uebersicht("geburt", "Übersicht Geburtshilfe / Kreißsaal", "Geburtskliniken",
 ["Kreißsaal", "Kreisssaal", "Geburtsklinik", "Geburtskliniken", "Geburtshilfe", "Entbindung Klinik", "Entbindungsklinik"],
 "Kliniken mit Geburtshilfe bzw. Frauenklinik. Neonatologie im Haus ist jeweils vermerkt (Perinatalzentrum-Level nur, wo belegt).",
 [("lmu-grosshadern", "Notfall-Entbindung, Neonatologie Großhadern – ZNA", "089 4400-44800"),
  ("lmu-innenstadt", "Frauenheilkunde und Geburtshilfe – ZNA", "089 4400-31100"),
  ("rechts-der-isar", "Kreißsaal (24 h), Neonatologie", "089 4140-2400"),
  ("rotkreuzklinikum", "Geburtshilfe (geburtenstärkste Klinik Bayerns), Neonatologie – ZNA", "089 1303-2502"),
  ("dritter-orden", "Gynäkologie und Geburtshilfe, Neonatologie und päd. Intensiv – Notaufnahme", "089 1795-1450"),
  ("mk-harlaching", "Frauenklinik, Neonatologie – ZNA", "089 6210-6666"),
  ("mk-schwabing", "Frauenklinik, Neonatologie – ZNA Innere", "089 3068-2210"),
  ("mk-neuperlach", "Frauenklinik – Zentrale", "089 6794-0"),
  ("helios-west", "Gynäkologie und Geburtshilfe – Zentrale", "089 8892-0"),
  ("ebersberg", "Geburtshilfe – Zentrale", "08092 82-0"),
  ("starnberg", "Kreißsaal / Geburtshilfe, Neonatologie Level II", "08151 18-2310"),
  ("erding", "Gynäkologie und Geburtshilfe – Zentrale", "08122 59-0"),
  ("agatharied", "Gynäkologie und Geburtshilfe, Kinder- und Jugendmedizin – Zentrale", "08026 393-0")])

if __name__ == "__main__":
    ids = [e["id"] for e in E]
    assert len(ids) == len(set(ids)), "doppelte IDs"
    out = {"app": "Wissen RD", "titel": "Import Kliniken München und Umland (Notaufnahme)",
           "hinweis": ("Krankenhäuser mit Notaufnahme in München sowie Ebersberg, Starnberg, Erding, Agatharied und kbo Haar. Quellen: DKG Deutsches Krankenhausverzeichnis "
                       "(Qualitätsberichte), muenchen.de Notdienste, Klinikseiten. Recherche 15.11.2026 – Telefonnummern vor dem Einsatz prüfen."),
           "eintraege": E}
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(E), "Kliniken")

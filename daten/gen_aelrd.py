"""Erzeugt daten/aelrd-bayern-import.json – ausschließlich aus den gültigen Dokumenten der ÄLRD Bayern."""
import json, sys

# ---------------- Quellen ----------------
Q = {
 "med2a": ("ÄLRD Bayern: Medikamente zur Anwendung nach § 2a NotSanG, Version 1.5, freigegeben 22.10.2025, gültig bis 31.10.2027", "2025-10-22"),
 "med2c": ("ÄLRD Bayern: Medikamente nach § 4 Abs. 2 Nr. 2c NotSanG, Version 2.0, gültig ab 01.11.2025", "2025-11-01"),
 "algo":  ("ÄLRD Bayern: Delegationsalgorithmen 2c (Stand 01.11.2025)", "2025-11-01"),
 "erl":   ("ÄLRD Bayern: Medizinische Erläuterungen zu den 2c-Delegationsalgorithmen, gültig ab 01.11.2025", "2025-11-01"),
 "matrix":("Kompetenzmatrix NotSan Bayern zu § 2a und § 4 Abs. 2 Nr. 1c NotSanG, Version 2.0 vom 04.04.2025", "2025-04-04"),
 "check": ("ÄLRD Bayern: Checklisten zu § 2a NotSanG, Stand 25.07.2024", "2024-07-25"),
 "kat":   ("ÄLRD Bayern: Maßnahmenkatalog zu § 2a NotSanG, Stand 30.03.2023", "2023-03-30"),
 "tod":   ("StMI/ÄLRD Bayern: Handlungsempfehlung Erkennen sicherer Todeszeichen durch NotSan, vom 31.03.2025", "2025-03-31"),
 "hyper": ("ÄBRD Bayern: Stellungnahme gegen 2c-Algorithmus arterielle Hypertension, 08.01.2026", "2026-01-08"),
 "umset": ("StMI Bayern: Umsetzungshinweise NotSan-Delegation, Stand 05.05.2022", "2022-05-05"),
}
def quelle(*keys):
    return " · ".join(Q[k][0] for k in keys), Q[keys[0]][1][:7]

E = []
def eintrag(id, bereich, titel, kurz, such, abschnitte, quellen, siehe=()):
    q, st = quelle(*quellen)
    E.append({"id": id, "bereich": bereich, "titel": titel, "kurz": kurz, "suchbegriffe": list(such),
              "siehe": list(siehe), "abschnitte": [{"titel": t, "text": x.strip()} for t, x in abschnitte if x and x.strip()],
              "sprechtext": "", "quelle": q, "stand": st})

KAT1 = "Kategorie 1 (grün) der Kompetenzmatrix: Kompetenzniveau soll von jedem Notfallsanitäter erreicht werden."
KAT2 = ("Kategorie 2 (gelb) der Kompetenzmatrix: Kompetenzniveau kann grundsätzlich durch zusätzliche Aus- / Fortbildung erreicht werden "
        "(Berufserfahrung sowie deutlich über den regulären Umfang hinausgehende Bildungsmaßnahmen erforderlich).")
KEINE_DOSIS = ("In den gültigen Dokumenten der ÄLRD Bayern ist für dieses Medikament keine Dosierungsempfehlung enthalten "
               "(nicht in der Medikamentenliste nach § 2a NotSanG).")
BTM = ("Opiatgabe: § 2a NotSanG gibt eine eigenständige Befugnis zu heilkundlichem Handeln. § 13 Abs. 1b BtMG ermöglicht in diesem Rahmen "
       "auch die Gabe von Betäubungsmitteln entsprechend der Empfehlungen der Medikamentenliste zu Indikation, Art und Weise der Verabreichung und Dosierung.")

# ======================= MEDIKAMENTE § 2a (Kategorie 1) =======================
def med(id, titel, such, form, indik, dosis, extra=(), quellen=("med2a", "matrix"), siehe=(), kurz=""):
    ab = [("Darreichungsform / Zusammensetzung", form), ("Indikation nach § 2a NotSanG", indik),
          ("Dosierung / Hinweise (§ 2a)", dosis)] + list(extra) + [("Einordnung Kompetenzmatrix", KAT1)]
    eintrag(id, "medikament", titel, kurz, such, ab, quellen, siehe)

med("amiodaron", "Amiodaron", ["Antiarrhythmikum"], "Ampulle, 150 mg / 3 ml",
    "Kammerflimmern / pulslose ventrikuläre Tachykardie",
    """- **Erwachsene:** nach 3. Defibrillation 300 mg i.v. (i.o.); nach 5. Defibrillation 150 mg i.v. (i.o.)
- **Kinder** (siehe DIVI-Kindernotfallkarte): nach 3. Defibrillation 5 mg/kg KG (max. 300 mg) i.v. (i.o.); nach 5. Defibrillation 5 mg/kg KG (max. 150 mg) i.v. (i.o.)""",
    siehe=["Kreislaufstillstand", "Manuelle Defibrillation"])

med("atropin", "Atropinsulfat", ["Atropin"], "Ampulle, 0,5 mg / 1 ml", "lebensbedrohliche Bradykardie",
    """- **Erwachsene:** initial 0,5 mg i.v. (i.o.); ggf. Wiederholung alle 3–5 Minuten bis maximal 3 mg
- **Kinder:** 0,01 mg/kg KG i.v. (i.o.), max. 0,5 mg""", siehe=["Bradykardie", "Transthorakaler Schrittmacher"])

med("cafedrin-theodrenalin", "Cafedrin / Theodrenalin", ["Cafedrin", "Theodrenalin"], "Ampulle, 200/10 mg / 2 ml",
    "kritische Hypotension trotz adäquater bzw. mit Kontraindikation für i.v.-Flüssigkeitsgabe",
    """- **Erwachsene:** initial 0,5 ml i.v. (i.o.); ggf. Repetition alle 5 Minuten bis max. 4 ml (2 Ampullen)
- **Kinder:** keine Zulassung
- **CAVE:** Konzept der permissiven Hypotension bei aktiver Blutung!""", siehe=["Kritische Hypotension"])

med("diazepam", "Diazepam (Rectiole)", ["Diazepam", "Diazepam rektal"], "Rectiole, 5 mg",
    "prolongierter kindlicher Krampfanfall (> 3 min)",
    """- **Kinder < 15 kg KG:** 5 mg rektal
- **Kinder ≥ 15 kg KG:** 10 mg rektal, bzw. siehe Midazolam
- keine Repetition (siehe Midazolam)""", siehe=["Krampfanfall", "Midazolam"])

med("epinephrin", "Epinephrin (Adrenalin)", ["Adrenalin", "Epinephrin", "Suprarenin"],
    "- Stechampulle 25 mg / 25 ml (Kreislaufstillstand, Inhalation)\n- Ampulle 1 mg / 1 ml (anaphylaktischer Schock)",
    "- Kreislaufstillstand\n- anaphylaktischer Schock\n- kritische akute stenosierende Laryngotracheitis (Pseudokrupp), kritische Schwellung / Ödem der oberen Atemwege – zur Inhalation",
    """**Kreislaufstillstand**
- Erwachsene: nicht defibrillierbar 1 mg i.v. (i.o.) sobald möglich; defibrillierbar 1 mg i.v. (i.o.) nach 3. Defibrillation; Repetition alle 3–5 Minuten unter ALS
- Kinder (siehe DIVI-Kindernotfallkarte): nicht defibrillierbar 0,01 mg/kg KG i.v. (i.o.) sobald möglich; defibrillierbar 0,01 mg/kg KG i.v. (i.o.) nach 3. Defibrillation; Repetition i.v. (i.o.) alle 3–5 Minuten unter ALS
**Anaphylaktischer Schock**
- Erwachsene: 0,5 mg i.m.; Repetition (i.m.) nach 5 Minuten bei ausbleibender Wirkung
- Kinder (siehe DIVI-Kindernotfallkarte): 0,01 mg/kg KG i.m.; Repetition (i.m.) nach 5–10 Minuten bei ausbleibender Wirkung
**Inhalation (Pseudokrupp / Schwellung obere Atemwege)**
- Erwachsene: 5 mg (5 ml) zur Inhalation; Repetition bei Symptompersistenz und (kardiovaskulärer) Verträglichkeit
- Kinder (siehe DIVI-Kindernotfallkarte): 5 mg (5 ml) zur Inhalation; Repetition bei Symptompersistenz und (kardiovaskulärer) Verträglichkeit""",
    siehe=["Kreislaufstillstand", "Anaphylaxie", "Pseudokrupp"])

med("esketamin", "Esketamin (intranasal, Kinder)", ["Esketamin", "Ketamin"], "Ampulle, 50 mg / 2 ml",
    "kritischer Schmerzzustand **Kinder bis 11 Jahre** – intranasale Applikation",
    """- siehe DIVI-Kindernotfallkarte
- 2 mg/kg KG intranasal
- ggf. Repetition der Hälfte der Initialdosis nach 10 Minuten""", siehe=["Kritischer Schmerzzustand"])

med("fentanyl", "Fentanyl", ["Fentanyl"], "Ampulle, 0,5 mg / 10 ml",
    "- kritischer Schmerzzustand Kinder ab 12 Jahre – intranasale Applikation\n- kritischer Schmerzzustand (außer bei akutem Koronarsyndrom) – i.v.",
    """**Intranasal (Kinder ab 12 Jahre)**
- siehe DIVI-Kindernotfallkarte
- 0,002 mg/kg KG intranasal
- ggf. Repetition der Hälfte der Initialdosis nach 10 Minuten
**Intravenös**
- nur Erwachsene und Kinder ab 12 Jahre
- unverdünnte Einzeldosis von 0,05 mg i.v. (i.o.)
- ggf. Repetition nach 5 Minuten bis maximal 0,2 mg
- **nicht bei akutem Koronarsyndrom**""", extra=[("Betäubungsmittel", BTM)], siehe=["Kritischer Schmerzzustand"])

med("flumazenil", "Flumazenil", ["Flumazenil", "Benzodiazepin-Antagonist"], "Ampulle, 0,5 mg / 5 ml",
    "kritische Benzodiazepin-Überdosierung / -Intoxikation",
    """- **Erwachsene:** 0,2 mg i.v. (i.o.); ggf. Repetition nach 1 Minute bis maximal 1 mg
- **Kinder ab 1 Jahr:** 0,01 mg/kg KG (max. 0,2 mg) langsam i.v. (i.o.); ggf. Repetition nach 1 Min. bis Gesamtdosis von 0,05 mg/kg KG (max. 1 mg)""",
    siehe=["Benzodiazepin-Intoxikation"])

med("glucose-40", "Glucose 40 %", ["Glucose", "Glukose", "Glukose 40", "G40", "Traubenzucker i.v."], "Ampulle, 4,0 g / 10 ml",
    "kritische Hypoglykämie",
    """- **Erwachsene:** initial 20 g langsam i.v. (i.o.) zu maximal laufender Infusion; ggf. weitere 20 g i.v. (i.o.) nach Blutzuckerwert
- **Kinder** (siehe DIVI-Kindernotfallkarte): 200 mg/kg KG i.v. (i.o.)""",
    extra=[("2c-Delegation (Algorithmus Hypoglykämie)",
            """- 20 g (50 ml) intravenös zu schnelllaufender Infusion
- ggf. einmalige Repetition
- nur Erwachsene / Adoleszente
- Zuspritzung langsam zu einer möglichst schnell laufenden Infusion zur Verdünnung; große Sorgfalt, damit kein Paravasat dieser hochosmolaren Lösung entsteht""")],
    quellen=("med2a", "med2c", "erl", "matrix"), siehe=["Hypoglykämie", "2c Hypoglykämie", "Glucose-Gel", "Thiamin"])

eintrag("glucose-gel", "medikament", "Glucose-Gel (oral)", "", ["Glucose-Gel", "Glukose Gel", "Zuckergel", "Glucose oral"],
    [("Darreichungsform", "Tube / Beutel o. ä."),
     ("2c-Delegation (Algorithmus Hypoglykämie)", """- 30 g Glucose per os
- ggf. einmalige Repetition (nach 15 Minuten, wenn BZ weiter < 70 mg/dl)
- nur Erwachsene / Adoleszente
- nur bei erhaltener Schluckfähigkeit"""),
     ("Hinweis (Erläuterungen)", "Die orale Glukosegabe ist bei erhaltener Schluckfähigkeit zu bevorzugen. Falls keine geeigneten oralen Glukosequellen verfügbar sind (z. B. Zucker-Gels), kann im Ausnahmefall Glukose-Injektionslösung in entsprechender Dosis oral verabreicht werden.")],
    ("med2c", "erl"), ["Hypoglykämie", "2c Hypoglykämie"])

med("ipratropiumbromid", "Ipratropiumbromid", ["Ipratropium", "Atrovent"], "Inhalationslösung, 0,5 mg / 2 ml",
    "kritische Bronchospastik – zur Inhalation",
    """- Restmenge der verwendeten Verneblungsmaske beachten!
- **Erwachsene:** 0,5 mg (2,0 ml) zur Inhalation; Repetition bei Symptompersistenz und (kardiovaskulärer) Verträglichkeit
- **Kinder:** 0,25 mg (1,0 ml) zur Inhalation; Repetition bei Symptompersistenz und (kardiovaskulärer) Verträglichkeit""",
    siehe=["Bronchospastik", "Salbutamol"])

med("midazolam", "Midazolam", ["Midazolam", "Dormicum"],
    "- Ampulle 5 mg / 5 ml (intravenös)\n- Ampulle 15 mg / 3 ml (intranasal)",
    "generalisierter Status epilepticus – intravenöse bzw. intranasale Applikation",
    """**Intravenös** (in der Regel nur indiziert, wenn i.v.-Zugang bei Krampfbeginn bereits etabliert)
- Erwachsene: initial 5 mg; einmalige Repetition bei Krampfpersistenz
- Kinder (siehe DIVI-Kindernotfallkarte): 0,1 mg/kg KG i.v. (i.o.)
**Intranasal**
- Erwachsene: 10 mg intranasal; einmalige Repetition bei Krampfpersistenz nach frühestens 5 Minuten
- Kinder (siehe DIVI-Kindernotfallkarte): 0,3 mg/kg KG intranasal""", siehe=["Status epilepticus", "Diazepam"])

med("morphin", "Morphin", ["Morphin", "Morphium"], "Ampulle, 10 mg / 1 ml",
    "kritischer Schmerzzustand **bei akutem Koronarsyndrom**",
    """- nur Erwachsene
- 1–2 mg i.v. (i.o.)
- Repetition nach frühestens 5 Minuten bis maximal 5 mg""", extra=[("Betäubungsmittel", BTM)],
    siehe=["ACS", "Kritischer Schmerzzustand"])

med("naloxon", "Naloxon (nasal)", ["Naloxon", "Opiat-Antagonist"], "Einzeldosis nasal, 2 x 1,8 mg",
    "kritische Opiat-Überdosierung / -Intoxikation",
    """- Anwendung zugelassen ab 14. Lebensjahr
- 1,8 mg intranasal
- Repetition nach 2–3 Minuten oder bei Symptomrückkehr""", siehe=["Opiat-Intoxikation"])

med("oxymetazolin", "Oxymetazolin 0,05 %", ["Oxymetazolin", "Nasenspray"], "Nasenspray, 0,5 mg / ml", "kritische Epistaxis",
    """- nur Erwachsene / Adoleszente > 50 kg KG
- 2–6 Sprühstöße in jedes betroffene Nasenloch
- keine Repetition""", siehe=["Epistaxis"])

med("oxytocin", "Oxytocin", ["Oxytocin", "Syntocinon"], "Ampulle, 3 IE / 1 ml", "kritische postpartale Blutung",
    """- 3 IE langsam i.v. (i.o.)
- einmalige Repetition nach frühestens 5 Minuten""", siehe=["Postpartale Blutung"])

med("piritramid", "Piritramid", ["Piritramid", "Dipidolor"], "Ampulle, 7,5 mg / 1 ml",
    "kritischer Schmerzzustand (außer bei akutem Koronarsyndrom)",
    """- nur Erwachsene / Adoleszente > 50 kg KG
- 7,5 mg als Kurzinfusion in 100 ml NaCl 0,9 % i.v. (i.o.) über mind. 5 Minuten
- ggf. Repetition nach 10 Minuten
- **nicht bei akutem Koronarsyndrom**""",
    extra=[("2c-Delegation (Algorithmen Traumatisch bedingter Schmerz / Akuter Abdominalschmerz)",
            """- Indikation: nicht tolerable traumatisch bedingte Schmerzen bzw. nicht tolerable akute abdominelle Schmerzen bei vital stabilen Patienten
- 7,5 mg intravenös in 100 ml NaCl 0,9 % als Kurzinfusion über mindestens 5 Minuten
- **keine Repetitionsgabe**
- nur Erwachsene / Adoleszente > 50 kg KG; nicht bei Schwangeren
- Patienten unter 50 kg, Schwangere sowie schwer gebrechliche und vital instabile Patienten dürfen kein Piritramid erhalten
- Infusion abbrechen, wenn der gewünschte Effekt vorzeitig erreicht ist oder bei gravierenden Nebenwirkungen / Komplikationen
- Gabe möglichst in stabiler liegender Position unter vollständigem Basismonitoring
- Schmerzniveau vor und nach Analgesie mit NRS erheben und dokumentieren"""),
           ("Betäubungsmittel", BTM)],
    quellen=("med2a", "med2c", "erl", "matrix"), siehe=["2c Trauma-Schmerz", "2c Abdominalschmerz", "Kritischer Schmerzzustand"])

med("prednison", "Prednison (Suppositorium)", ["Prednison", "Rectodelt", "Kortison Zäpfchen"], "Suppositorium, 100 mg",
    "- kritische akute stenosierende Laryngotracheitis (Pseudokrupp)\n- kritische spastische Bronchitis",
    """- nur Kinder (siehe DIVI-Kindernotfallkarte)
- 100 mg rektal (alters- / gewichtsunabhängig)""", siehe=["Pseudokrupp"])

med("salbutamol", "Salbutamol", ["Salbutamol", "Sultanol"], "Inhalationslösung, 1,25 mg / 2,5 ml",
    "kritische Bronchospastik – zur Inhalation",
    """- Restmenge der verwendeten Verneblungsmaske beachten!
- **Erwachsene:** 2,5 mg (5 ml) initial zur Inhalation; Repetition bei Symptompersistenz und (kardiovaskulärer) Verträglichkeit
- **Kinder** (siehe DIVI-Kindernotfallkarte): 2,5 mg (5 ml) zur Inhalation; Repetition bei Symptompersistenz und (kardiovaskulärer) Verträglichkeit""",
    siehe=["Bronchospastik", "Ipratropiumbromid"])

med("sauerstoff", "Sauerstoff", ["Sauerstoff", "O2", "Sauerstoffgabe"], "inhalativ", "kritische Hypoxie",
    """- 15 l/min über Maske
- CPR: höchstmögliche inspiratorische Sauerstoffkonzentration""",
    extra=[("2c-Delegation (Algorithmus Moderate Hypoxämie)",
            """- nur Erwachsene / Adoleszente; Applikation über Nasenbrille; Dosierung nach SpO2-Zielbereich
- ohne Risiko für hyperkapnisches Atemversagen: bis 6 l/min, Ziel SpO2 94–98 %
- mit Risiko für hyperkapnisches Atemversagen: bis 2 l/min (+ LTOT-Dosis), Ziel SpO2 88–92 %
- maximaler O2-Fluss zur Prä- und Post-Oxygenierung vor trachealer Absaugung""")],
    quellen=("med2a", "med2c", "matrix"), siehe=["Hypoxämie", "2c Sauerstoff"])

med("thiamin", "Thiamin (Vitamin B1)", ["Thiamin", "Vitamin B1"], "Ampulle, 100 mg / 2 ml",
    "- V. a. alkoholinduzierter, generalisierter Status epilepticus\n- kritische Hypoglykämie bei V. a. chron. Alkoholabusus\n- kritische Hypoglykämie mit Hinweis auf schwere Mangelernährung (Kachexie / Marasmus, Anamnese)",
    """- nur Adoleszente und Erwachsene
- bei V. a. chronischen Alkoholabusus bzw. Hinweisen auf eine schwere Mangelernährung zur Prophylaxe von gravierenden Folgeschäden: Thiamin-Gabe unmittelbar nach Krampfdurchbrechung; Thiamin-Gabe **vor** i.v./i.o.-Hypoglykämie-Ausgleich!
- 100 mg langsam (über eine Minute) i.v. (i.o.)""",
    extra=[("2c-Delegation (Algorithmus Hypoglykämie)",
            """- Indikation: Hypoglykämie verbunden mit schwerer Mangelernährung
- 100 mg langsam (über eine Minute) intravenös, möglichst vor Glucosegabe
- nur bei intravenöser Glucosegabe; nur Erwachsene / Adoleszente
- Alkoholabusus ohne körperliche Folgeerscheinungen oder eine gut kontrollierte Darmerkrankung sind keine Indikation; bei oraler Glukosegabe nicht empfohlen""")],
    quellen=("med2a", "med2c", "erl", "matrix"), siehe=["Hypoglykämie", "Status epilepticus"])

med("urapidil", "Urapidil", ["Urapidil", "Ebrantil"], "Ampulle, 50 mg / 10 ml", "hypertensiver Notfall",
    """- nur Erwachsene
- initial 5 mg i.v. (i.o.)
- Repetition frühestens nach 5 Minuten
- Senkung nach Symptomatik, max. um 25 % des Ausgangswerts RR syst.""", siehe=["Hypertensiver Notfall"])

med("elektrolytloesung", "Balancierte Elektrolytlösung (Acetat/Malat)", ["Vollelektrolytlösung", "Infusion", "Kristalloide", "Ringer", "Elektrolytlösung"],
    "Infusionslösung, 500 ml",
    "- Träger-Infusionslösung zur i.v.-Medikamentenapplikation\n- Flüssigkeitsersatz bei kritischem Volumenmangel",
    """- nach Bedarf
- **CAVE:** Konzept der permissiven Hypotension bei aktiver Blutung!""",
    extra=[("2c-Delegation", """- nur Erwachsene / Adoleszente; intravenös als Infusion nach jeweiligem Delegationsalgorithmus
- V. a. Sepsis: max. 500 ml zur Einleitung der Infusionstherapie, danach weitere langsame Infusion zum Offenhalten des Zugangs
- sonstige Algorithmen: langsame Infusion (Offenhalten, Richtwert 1 Tropfen pro Sekunde)""")],
    quellen=("med2a", "med2c", "erl", "matrix"), siehe=["2c Sepsis"])

# ---- Kategorie 2 (gelb): keine Dosierung in den Dokumenten ----
for id, titel, such, zusatz in [
    ("ass", "Acetylsalicylsäure (ASS)", ["ASS", "Aspirin", "Acetylsalicylsäure"], ""),
    ("dimetinden", "Dimetinden", ["Dimetinden", "Fenistil"], ""),
    ("furosemid", "Furosemid", ["Furosemid", "Lasix"], "Laut ÄBRD-Stellungnahme vom 08.01.2026 im bayerischen Rettungsdienst intravenös zur Blutdrucksenkung verfügbar."),
    ("glyceroltrinitrat", "Glyceroltrinitrat sublingual", ["Nitro", "Nitroglycerin", "Glyceroltrinitrat", "Nitrospray"], "Laut ÄBRD-Stellungnahme vom 08.01.2026 im bayerischen Rettungsdienst sublingual zur Blutdrucksenkung verfügbar."),
    ("heparin", "Heparin", ["Heparin"], ""),
    ("lidocain", "Lidocain", ["Lidocain", "Xylocain"], "Nicht länger zur intraossären Lokalanästhesie in der grünen Kategorie (Empfehlung RDA Bayern vom 10.07.2024 – nicht mehr empfohlen). Kann als alternatives Antiarrhythmikum im Rahmen der Reanimation Verwendung finden; zunächst als Reanimationsmedikament in Kategorie gelb geführt."),
    ("magnesiumsulfat", "Magnesiumsulfat", ["Magnesium", "Magnesiumsulfat"], "Kategorie 2 (gelb) nur für Torsade de Pointes und Asthma / COPD (Erweiterung um Asthma / COPD aufgrund neuer Leitlinienempfehlungen). Magnesiumsulfat für sonstige Indikationen: Kategorie 3 (rot)."),
    ("metamizol", "Metamizol", ["Metamizol", "Novalgin"], ""),
    ("butylscopolamin", "N-Butylscopolamin", ["Butylscopolamin", "Buscopan"], ""),
    ("prednisolon", "Prednisolon", ["Prednisolon", "Solu-Decortin"], ""),
    ("tranexamsaeure", "Tranexamsäure", ["Tranexamsäure", "TXA"], ""),
]:
    ab = [("Einordnung Kompetenzmatrix", KAT2), ("Dosierung", KEINE_DOSIS)]
    if zusatz: ab.append(("Hinweis", zusatz))
    eintrag(id, "medikament", titel, "", such, ab,
            ("matrix", "hyper") if "Stellungnahme" in zusatz else ("matrix",), ["Kompetenzmatrix"])

# ======================= 2c-ALGORITHMEN =======================
NOTARZT_STANDARD = """- Kritischer Patient (symptombezogener Zustand) → **Notarzt-Nachforderung**
- Initiale Beurteilung: kritisches (x)ABCDE-Problem → **Notarzt-Nachforderung**
- Danach: Ist eine Wartezeit auf den Notarzt medizinisch vertretbar? Nein → Maßnahmen nach § 2a NotSanG → ggf. Rendezvous mit Notarzt / Transport ohne Notarzt mit Schockraumanmeldung; Ja → Versorgung / Transport mit Notarzt"""
IV_FUSS = "IV-Zugang: max. 2 Versuche – kein IO-Zugang. Medikamente nach Medikamentenliste Delegation."

eintrag("2c-hypoxaemie", "algorithmus", "Moderate Hypoxämie: Delegation von Sauerstoffgabe", "2c Sauerstoff",
    ["2c Hypoxämie", "Algorithmus Sauerstoff", "Algorithmus Hypoxämie", "moderate Hypoxämie"],
    [("Gültigkeit", "Stand 01.08.2022"),
     ("Einstieg", "Notfallpatient mit SpO2 kleiner 94 %"),
     ("Notarzt", NOTARZT_STANDARD + "\n- SpO2 < 85 % gilt als kritische Hypoxämie → regelhaft kritisch, Notarzt nachfordern, Behandlung nach § 2a NotSanG"),
     ("Ohne Risiko für hyperkapnisches Atemversagen", """- Patientenaufklärung über Sauerstoffgabe
- **2c: Sauerstoffgabe 4 l/min über Nasenbrille, Ziel SpO2 94–98 %**
- SpO2 mindestens 94 % → Transport in geeignete Behandlungseinrichtung; sonst Notarzt-Nachforderung"""),
     ("Mit Risiko für hyperkapnisches Atemversagen", """- SpO2 kleiner 88 % (ggf. unter LTOT)? Nein → Vorgehen nach Befund
- Patientenaufklärung über Sauerstoffgabe
- **2c: Sauerstoffgabe 2 l/min + LTOT, Ziel SpO2 88–92 %**
- SpO2 mindestens 88 % → Transport in geeignete Behandlungseinrichtung; sonst Notarzt-Nachforderung"""),
     ("Checkbox Risiko für hyperkapnisches Atemversagen", """- Bekannte COPD oder Bronchiektasen
- Morbide Adipositas (BMI größer 40 kg/m²)
- Bekannte zystische Fibrose / Mukoviszidose
- Bekannte neuromuskuläre Erkrankung oder Brustwanddeformitäten mit chronischer Beeinträchtigung der Atmung"""),
     ("Titrieren", """- Bei Verlassen des Zielbereichs Sauerstoff literweise reduzieren bzw. erhöhen (max. 6 l/min ohne bzw. 2 l/min + LTOT mit Risiko für hyperkapnisches Atemversagen)
- Nach einer Äquilibrationszeit von 5 Minuten kann die nächste Anpassung erfolgen
- Kurzfristige Sättigungsausschläge (bis zu einer Minute) bleiben ohne Konsequenz
- Die delegierte Dosis kann um eine bestehende LTOT-Dosis erhöht werden"""),
     ("Erläuterungen", "Die Delegation bezieht sich explizit auf Notfallpatienten. Eine SpO2 unter 94 % bei ansonsten gesunden bzw. stabilen Patienten ohne notfallmedizinischen Versorgungsbedarf (z. B. Heimfahrt im KTW) bedingt keine Indikation zur O2-Therapie.")],
    ("algo", "erl"), ["Sauerstoff", "Hypoxämie"])

eintrag("2c-trachealkanuele", "algorithmus", "Sekret in Trachealkanüle beim spontanatmenden Patienten: Delegation von Absaugen", "2c Absaugen",
    ["Trachealkanüle", "Absaugen Trachealkanüle", "Tracheostoma Absaugen", "Algorithmus Absaugen"],
    [("Gültigkeit", "Stand 01.03.2022"),
     ("Einstieg", "Sekret in Trachealkanüle bei stabilem Tracheostoma"),
     ("Checkbox stabiles Tracheostoma", "- Anlage vor mindestens 14 Tagen\n- Kanülenwechsel bereits problemlos ohne Hilfsmittel erfolgt (keine Verlegungsstrukturen oder Kollapsneigung)"),
     ("Notarzt", NOTARZT_STANDARD),
     ("Ablauf 2c", """- Atembehinderung? Nein → Vorgehen nach Befund
- Patientenaufklärung über Absaugen
- **2c: Präoxygenieren über Trachealkanüle** (max. O2-Fluss über 1 Minute)
- **2c: Absaugen der Trachealkanüle**, Fortführen der Oxygenierung für 1 Minute (max. 2 Versuche à 15 Sek. innerhalb von 5 Minuten)
- Nach 5 Minuten Reevaluation: Atembehinderung gelöst? Ja → Vorgehen nach Befund; Nein → Notarzt-Nachforderung"""),
     ("Checkbox Atembehinderung (mindestens 1 erfüllt)", """- Anhaltender Hustenreiz
- SpO2-Abfall um mindestens 5 Prozentpunkte unter den Ausgangswert oder SpO2 unter 90 %
- (Teil-)Verlegung des Atemwegs durch Sekret
- V. a. geringfügige Aspiration von Flüssigkeiten
- Unbehagen / Wunsch des Patienten"""),
     ("Technik (Erläuterungen)", """- Eigenen Infektionsschutz beachten! Auf sichere Fixierung der Trachealkanüle achten!
- Durchmesser des Absaugkatheters maximal die Hälfte des Trachealkanülendurchmessers
- Sog auf max. −0,25 bar begrenzen, falls technisch möglich
- Eingeführter Teil des Absaugkatheters muss steril bleiben
- Katheter ohne Sog bis maximal zur Kanülenspitze einführen, dann unter Sog langsam zurückziehen
- Absaugvorgang dauert maximal 15 Sekunden"""),
     ("Besonderheiten", """- Delegation gilt für (zäh-)flüssiges Sekret, nicht für die Entfernung von Verborkungen; sichere Spontanatmung ist Voraussetzung
- Dislokation der Kanüle: ABC-Check; atmet der Patient unbehindert ohne Kanüle → keine Replatzierung durch NotSan, Transport in eine Einrichtung mit Kompetenz zur Replatzierung; ABC-Problem → unverzüglich Notarzt
- Nach der Absaugung ist nicht zwingend ein Transport in eine Behandlungseinrichtung erforderlich; ggf. ursprüngliches Transportziel""")],
    ("algo", "erl"), ["Freimachen des Tracheostomas"])

HYPO_ABLAUF = """- BZ < 70 mg/dl **und** klinische Manifestation der Hypoglykämie? Nein → Vorgehen nach Befund
- **Patient kann sicher schlucken:** Patientenaufklärung → **2c: Glukose 30 g per os** → nach 15 Min.: BZ < 70 mg/dl? → ggf. **erneut 30 g per os** → nach 15 Min. Reevaluation
- **Patient kann nicht sicher schlucken:** Patientenaufklärung → **2c: IV-Zugang** → V. a. schwere Mangelernährung? → **2c: Thiamin 100 mg langsam IV** → **2c: Glukose 40 % 50 ml IV zu schnelllaufender Infusion** → nach 5 Min.: BZ < 70 mg/dl? → ggf. **erneut Glukose 40 % 50 ml IV** → nach 5 Min. Reevaluation
- Symptome verschwunden oder eindeutige Besserung **und** BZ ≥ 70 mg/dl → Transport in geeignete Behandlungseinrichtung (bei Transportverweigerung Vorgehen laut Umsetzungshinweisen); sonst **Notarzt-Nachforderung**"""
HYPO_SYMPT = """Identifikation durch Patient oder Dritte · Schwitzen · Zittern · Heißhunger · Herzklopfen · Gedankenflucht · Logorrhoe · Wortfindungsstörungen · Reizbarkeit · Sehstörungen · Kopfschmerzen · Verwirrtheit · Ängstlichkeit · Schläfrigkeit · Koordinationsdefizite · Bewusstseinsstörung · Verhaltensauffälligkeiten · Krampfanfall · Fokale Neurologie · Übelkeit"""
HYPO_MANGEL = """- Kachexie
- Schwerer chronischer Alkoholabusus
- Chronische Gastritis, Magenkarzinom
- Chronisch entzündliche Darmerkrankung mit regelmäßigen Symptomen (M. Crohn, Colitis ulcerosa)
- Langanhaltendes Erbrechen (täglich länger 1 Woche), z. B. während Krebserkrankung, Schwangerschaft, Magersucht
- Z. n. Adipositas-Chirurgie"""
HYPO_ERL = """- Liegt bei einem bewusstseinsgestörten, aber nicht kritischen Patienten eine Hypoglykämie als alleinige Ursache nahe, kann die Notarzt-Alarmierung zunächst zurückgestellt werden – auch bei Patienten ohne Insulin
- Repetition ausgeschlossen, wenn der BZ wieder im Normbereich ist, auch bei fortbestehenden Symptomen → an andere Ursache denken
- Wartezeiten bei oraler Gabe für Vorbereitung bzw. Beginn des Transports nutzen
- Schwere Hypoglykämien gehen häufig mit Hypothermie einher → Temperaturmessung
- Besondere Vorsicht bei oraler Sulfonylharnstoff-Therapie (z. B. Glibenclamid, Glimepirid, Gliclazid, Gliquidon): ausgeprägte, langanhaltende Hypoglykämien mit schweren Rückfällen – vom Verzicht auf Krankenhauseinweisung dringend abraten; ebenso bei Problemen mit Nahrungsaufnahme oder sehr hoher Dosis Insulin / oraler Antidiabetika
- Bei Verdacht auf suizidale Verabreichung ist ein Kliniktransport obligat
- Transportverweigerung: Einwilligungsfähigkeit korrekt feststellen, über Folgen aufklären, schriftlich dokumentieren"""
eintrag("2c-hypoglykaemie", "algorithmus", "Hypoglykämie: Delegation von IV-Zugang, Infusion, Thiamin- und Glukosegabe", "2c Hypoglykämie",
    ["Algorithmus Hypoglykämie", "2c Unterzucker"],
    [("Gültigkeit", "gültig ab 01.11.2025"), ("Einstieg", "V. a. Hypoglykämie"), ("Notarzt", NOTARZT_STANDARD.replace("(x)ABCDE", "ABC")),
     ("Ablauf 2c", HYPO_ABLAUF), ("Checkbox typische klinische Manifestationen (mindestens 1 erfüllt)", HYPO_SYMPT),
     ("Checkbox V. a. schwere Mangelernährung (mindestens 1 erfüllt)", HYPO_MANGEL), ("Erläuterungen", HYPO_ERL),
     ("Hinweise", IV_FUSS + " BZ-Umrechnung: 70 mg/dl = 3,9 mmol/l.")],
    ("algo", "erl"), ["Hypoglykämie", "Glucose 40 %", "Glucose-Gel", "Thiamin"])

SCHOCKRAUM_A = """- **Präklinische Intervention** (z. B. Tourniquet, Atemwegssicherung, Thoraxentlastung, Katecholamingabe)
- **Gestörte Vitalparameter** (Atemstörungen (SpO2 < 90 %), AF < 10 oder > 29 /min, RRsyst < 90 mmHg, Puls > 120 /min, Schockindex > 0,9, GCS < 13, Hypothermie < 35,0 °C)
- **Kritische Verletzung** (penetrierende Verletzungen Rumpf/Hals, instabiler Thorax, mechanisch instabile Beckenverletzung, Amputationsverletzung proximal der Hände/Füße, Frakturen von 2 oder mehr proximalen langen Röhrenknochen (Oberarm, Oberschenkel), sensomotorisches Defizit nach Wirbelsäulenverletzung, Verbrennungen > 20 % und Grad ≥ 2)"""
eintrag("2c-trauma-schmerz", "algorithmus", "Traumatisch bedingter Schmerz: Delegation von IV-Zugang, Infusion, IV-Analgesie BtM und achsengerechter Lagerung", "2c Trauma-Schmerz",
    ["Algorithmus Schmerz", "Trauma Schmerz", "2c Analgesie Trauma", "Algorithmus Trauma"],
    [("Gültigkeit", "gültig ab 01.04.2024"), ("Einstieg", "Akutes Trauma oder thermische Verletzung"),
     ("Notarzt", "- Offensichtlich schwerverletzt (auf den ersten Blick auf den Schadensort) → **Notarzt-Nachforderung**\n" + NOTARZT_STANDARD.replace("kritisches (x)ABCDE-Problem", "xABCDE-Problem oder Schockraum-A-Indikation")),
     ("Ablauf 2c", """- Ausschlusskriterium? Ja → **Notarzt-Nachforderung**
- Für den Patienten tolerabler Schmerz? Ja → 2c: bei Frakturverdacht achsengerechte Lagerung → Transport
- Patientenaufklärung über IV-Zugang / Medikamente
- **2c: IV-Zugang + 7,5 mg Piritramid in 100 ml NaCl 0,9 % als Kurzinfusion über mind. 5 Min.**
- Danach tolerabler Schmerz? Ja → 2c: bei Frakturverdacht achsengerechte Lagerung → Transport in geeignete Behandlungseinrichtung; Nein → **Notarzt-Nachforderung**"""),
     ("Checkbox Schockraum-A-Indikation", SCHOCKRAUM_A),
     ("Checkbox Ausschlusskriterien", """- Grob dislozierte Fraktur
- Beckenverletzung
- Defizit Durchblutung / Motorik / Sensibilität
- Beeinträchtigung Weichteilmantel / Haut
- Verbrennung / Verbrühung > 10 % Körperoberfläche 2° / 3° und/oder Beteiligung Kopf / Hals
- Hinweis auf Inhalationstrauma
- Lange Rettungszeit"""),
     ("Erläuterungen", """- Versorgung von Verletzungen an mehr als einer Körperregion möglich, sofern kein (vorhersehbares) xABCDE-Problem – bei Mehrfachverletzungen Notarztindikation großzügig stellen
- Als Traumafolge gelten auch Verletzungen durch besondere Kraftanstrengung (z. B. Achillessehnenruptur, Muskel(faser)riss, Verhebetrauma); ausdrücklich **nicht** die Verschlechterung chronischer Rückenschmerzen
- Luxationen sind eingeschlossen; junge Patienten (bis 40 Jahre) mit isolierter, habitueller Schulter- oder Patellaluxation ohne relevantes Trauma: Verzicht auf 2c-Analgesie und Notarzt-Nachforderung erwägen
- Überdehnung / gravierende Druckbelastung des Weichteilmantels → präklinische Reposition oft angezeigt → Notarzt; Luxationsfrakturen des Sprunggelenks stets Indikation zur zeitnahen Reposition → Notarzt
- Hinweis auf Inhalationstrauma: Person war Feuer, Rauch oder Explosion ausgesetzt UND Rußablagerungen im Mund-/Rachenraum und/oder Auswurf mit Ruß, schwerer Husten, Heiserkeit und/oder Verbrennungen des Gesichts / Halses oder versengte Augenbrauen / Nasenhaare
- Lange Rettungszeit ist immer anzunehmen bei technischer oder besonderer Rettung (Einklemmung / Verschüttung, Drehleiterrettung, unwegsames Gelände etc.)"""),
     ("Hinweise", IV_FUSS)],
    ("algo", "erl"), ["Piritramid", "Schockraum-Indikation"])

eintrag("2c-abdominalschmerz", "algorithmus", "Akuter Abdominalschmerz: Delegation von IV-Zugang, Infusion, IV-Analgesie BtM", "2c Abdominalschmerz",
    ["Algorithmus Bauchschmerz", "Algorithmus Abdomen", "2c Bauchschmerz"],
    [("Gültigkeit", "gültig ab 01.04.2024"), ("Einstieg", "Akuter Bauchschmerz"), ("Notarzt", NOTARZT_STANDARD),
     ("Ablauf 2c", """- Für den Patienten tolerabler Schmerz? Ja → Transport in geeignete Behandlungseinrichtung
- Ausschlusskriterium? Ja → **Notarzt-Nachforderung**
- Patientenaufklärung über IV-Zugang / Medikamente
- **2c: IV-Zugang + 7,5 mg Piritramid in 100 ml NaCl 0,9 % als Kurzinfusion über mind. 5 Min.**
- Danach tolerabler Schmerz? Ja → Transport; Nein → **Notarzt-Nachforderung**"""),
     ("Checkbox Ausschlusskriterien", """- Blutiger Stuhl / Teerstuhl oder blutiges / kaffeesatzartiges Erbrechen
- Bekanntes Aortenaneurysma
- Schwangerschaft
- (zusätzlicher) Thoraxschmerz
- Bei Oberbauchschmerz: ST-Strecken-Veränderungen im 12-Kanal-EKG"""),
     ("Erläuterungen", """- Vor der 2c-Analgesie Hinweise auf lebensbedrohliche Erkrankungen ausschließen, insbesondere gastrointestinale Blutung, akutes Aortensyndrom und akutes Koronarsyndrom
- Bei Oberbauchschmerz 12-Kanal-EKG: nur wenn die ST-Strecke in allen Ableitungen isoelektrisch ist, darf die Delegation angewendet werden; ST-Hebungen oder -Senkungen in mindestens einer Ableitung → Ausschluss und Notarzt-Nachalarmierung
- Akutes Abdomen / bretthartes Bauch / Peritonismus: mit hoher Dringlichkeit in Klinik mit chirurgischer Sofortbehandlungsmöglichkeit voranmelden; schon bei geringsten Zeichen respiratorischer oder kardiozirkulatorischer Instabilität Notarzt obligat
- Gilt auch für Flankenschmerzen und akutes Skrotum (Zielklinik mit operativer urologischer Versorgungsmöglichkeit)"""),
     ("Hinweise", IV_FUSS)],
    ("algo", "erl"), ["Piritramid", "ACS"])

NEWS2 = """| Parameter | 3 | 2 | 1 | 0 | 1 | 2 | 3 |
- **Atemfrequenz (/min):** 3 = ≤ 8 · 1 = 9–11 · 0 = 12–20 · 2 = 21–24 · 3 = ≥ 25
- **SpO2 (%):** 3 = ≤ 91 · 2 = 92–93 · 1 = 94–95 · 0 = ≥ 96
- **Raumluft oder O2:** 2 = O2 · 0 = Raumluft
- **Syst. Blutdruck (mmHg):** 3 = ≤ 90 · 2 = 91–100 · 1 = 101–110 · 0 = 111–219 · 3 = ≥ 220
- **Pulsfrequenz (/min):** 3 = ≤ 40 · 1 = 41–50 · 0 = 51–90 · 1 = 91–110 · 2 = 111–130 · 3 = ≥ 131
- **Bewusstsein:** 0 = wach · 3 = verwirrt, getrübt, bewusstlos (nur falls neu aufgetreten oder verschlechtert)
- **Temperatur (°C):** 3 = ≤ 35,0 · 1 = 35,1–36,0 · 0 = 36,1–38,0 · 1 = 38,1–39,0 · 2 = ≥ 39,1
- NEWS-2 nicht anwendbar bei Schwangeren und Patienten jünger als 16 Jahre""".split("\n", 1)[1]
INFEKT = """- **Allgemeine Hinweise:** Temperatur ≤ 36,0 °C (Hypothermie) oder ≥ 38,0 °C (Fieber), Schüttelfrost, Blutzucker > 140 mg/dl ohne Diabetes
- **Risikofaktoren:** Immunsuppression, Krankenhausaufenthalt in den letzten 30 Tagen
- **Atemwegsinfekt:** Husten und Auswurf, Dyspnoe, atemabhängiger Brustschmerz
- **Harnwegsinfekt:** Brennen beim Wasserlassen, auffälliger Geruch, Verfärbung des Urins
- **Intraabdominale Infektion:** Durchfall, Bauchschmerzen, Voroperationen
- **Weichteil- und Knocheninfektion:** chronische Wunden, Gelenk- und Wirbelsäulenschmerzen, Rötung, Bewegungseinschränkung
- **Fremdkörper-assoziierte Infekte:** Portkatheter, Blasendauerkatheter, medizinische Implantate (z. B. Endoprothesen, Herzklappenersatz, Herzschrittmacher), Körperschmuck (z. B. Piercing), sonstige Fremdkörper
- **Endokarditis:** Herzrhythmusstörungen, Herzklappenersatz
- **Meningitis:** veränderte Bewusstseinslage, Kopfschmerz, Nackensteifigkeit"""
eintrag("2c-sepsis", "algorithmus", "V. a. Sepsis: Delegation von IV-Zugang und Infusion", "2c Sepsis",
    ["Algorithmus Sepsis", "2c Infusion Sepsis"],
    [("Gültigkeit", "gültig ab 01.11.2025"), ("Einstieg", "Akut reduzierter Allgemeinzustand"),
     ("Notarzt", NOTARZT_STANDARD + "\n- **Meningismus** → Notarzt-Nachforderung (unabhängig von einem kritischen ABCDE-Problem)"),
     ("Ablauf 2c", """- Vereinfachter NEWS-2: Summe mindestens 5 Punkte **plus** Hinweis auf Infektion? Nein → Vorgehen nach Befund
- Patientenaufklärung über IV-Zugang / Infusion
- **2c: IV-Zugang, Einleitung Infusionstherapie mit 500 ml Vollelektrolytlösung, Voranmeldung „V. a. Sepsis“**
- Transport in geeignete Behandlungseinrichtung"""),
     ("Vereinfachter NEWS-2 (Punkte)", NEWS2 + "\n- Ein alleiniger roter Warnwert hat in diesem Algorithmus keine Wirkung"),
     ("Checkliste „Hinweise auf Infektion“", INFEKT),
     ("Erläuterungen", """- Die Diagnose „Sepsis“ ist präklinisch nicht möglich; ≥ 5 Punkte NEWS2 plus Infektionshinweis ergeben den Verdacht mit akzeptabler Sensitivität und Spezifität
- Anwendbar erst ab 16 Jahren und nicht bei Schwangeren; NEWS2-Elemente vollständig dokumentieren
- Voranmeldung als „roter“ Patient mit Tracerdiagnose Sepsis; bei entsprechenden Kriterien nicht-traumatologischer Schockraum; bei chirurgischem Fokus Zielklinik mit aufnahmebereiter Chirurgie
- Blutzucker bestimmen (Infektionshinweis bzw. Hypoglykämie als Differenzialdiagnose)
- Keine forcierte Volumengabe: rasche Gabe von 500 ml, danach langsame Infusion zum Offenhalten; erster Volumenbolus soll leitliniengemäß erst innerhalb der ersten drei Stunden komplett verabreicht sein
- Kontraindikationen zur Infusionstherapie (z. B. Dialysepflichtigkeit, dekompensierte Herzinsuffizienz) beachten – dann ABCDE-Problem als „kritisch“ einstufen → Notarzt"""),
     ("Hinweise", IV_FUSS)],
    ("algo", "erl"), ["Sepsis", "NEWS2"])

eintrag("2c-zustandsverschlechterung", "algorithmus", "Risiko für relevante Zustandsverschlechterung: Delegation von IV-Zugang und Infusion", "2c NEWS",
    ["Algorithmus NEWS", "prophylaktischer Zugang", "Zustandsverschlechterung", "2c Zugang"],
    [("Gültigkeit", "Stand 01.10.2023"), ("Einstieg", "Notfallpatient"), ("Notarzt", NOTARZT_STANDARD),
     ("Ablauf 2c", """- Vereinfachter NEWS-2: Summe mindestens 5 Punkte **oder** 3 Punkte bei einem einzelnen Vitalparameter (roter Warnwert)? Nein → Vorgehen nach Befund
- Patientenaufklärung über IV-Zugang / Infusion
- **2c: IV-Zugang, langsame Infusion Vollelektrolytlösung**
- Transport in geeignete Behandlungseinrichtung"""),
     ("Vereinfachter NEWS-2 (Punkte)", NEWS2),
     ("Erläuterungen", """- Nur bei Notfallpatienten im engeren Sinne; nicht, wenn ein trivialer Zustand die Auffälligkeiten erklärt oder sich der Zustand durch nicht-invasive Basismaßnahmen suffizient bessern lässt
- Nur valide, gleichzeitig erhobene Messwerte verwenden (Artefakte ausschließen)
- Bewusstsein: 3 Punkte nur bei neu aufgetretener oder akut verschlechterter Bewusstseinsminderung / Verwirrtheit
- SpO2-Skala 2 (hyperkapnisches Atemversagen) wird nicht verwendet
- Schwangere und Jugendliche unter 16 Jahren ausgeschlossen; NEWS2 bei Zustandsänderungen ggf. wiederholt erheben
- Misslingt der prophylaktische Zugang: ohne weiteren Versuch Transport ins Krankenhaus"""),
     ("Hinweise", IV_FUSS)],
    ("algo", "erl"), ["NEWS2"])

eintrag("2c-verletzte-person", "algorithmus", "Verletzte Person: Delegation von IV-Zugang und Infusion", "2c Verletzte Person",
    ["Algorithmus verletzte Person", "geriatrisches SHT", "2c Trauma Zugang"],
    [("Gültigkeit", "gültig ab 01.04.2024"), ("Einstieg", "Relevantes Trauma"),
     ("Notarzt", "- Offensichtlich schwerverletzt → **Notarzt-Nachforderung**\n" + NOTARZT_STANDARD.replace("kritisches (x)ABCDE-Problem", "xABCDE-Problem oder Schockraum-A-Indikation").replace("Schockraumanmeldung", "Schockraumanmeldung TraumaZentrum")),
     ("Ablauf 2c", """- Schockraum-Indikation nach Unfallmechanismus? **Ja** → Patientenaufklärung → **2c: IV-Zugang + langsame Infusion Vollelektrolytlösung + Voranmeldung TraumaZentrum „Schockraum B“** → Transport in TraumaZentrum
- **Nein** → Geriatrischer Patient? Nein → Vorgehen nach Befund
- Geriatrisch: mindestens zwei Körperregionen mehr als nur oberflächlich verletzt? **Ja** → wie oben, Voranmeldung „Schockraum B“
- Geriatrisch, nicht zwei Regionen: bekanntes oder vermutetes SHT mit GCS 13–15? **Ja** → Patientenaufklärung → **2c: IV-Zugang + langsame Infusion Vollelektrolytlösung + Voranmeldung TraumaZentrum „geriatrisches leichtes SHT“**; Nein → Vorgehen nach Befund"""),
     ("Checkbox Schockraum-A-Indikation", SCHOCKRAUM_A),
     ("Checkbox Schockraumindikation nach Unfallmechanismus (S3-Leitlinie Polytrauma, Konsens der Bayer. Traumanetzwerke)", """- (Ab)Sturz aus über 3 Metern Höhe oder
- Großtierunfall (z. B. Rind, Pferd) oder
- Kraftfahrzeugunfall mit Ejektion aus dem Fahrzeug und/oder sicheren Frakturzeichen an mindestens einem langen Röhrenknochen (Oberarm, Unterarm, Oberschenkel, Unterschenkel)"""),
     ("Checkbox geriatrischer Patient", "- 80 Jahre oder älter\n- 70 Jahre oder älter mit geriatrietypischer Multimorbidität (definiert als Vorliegen von mindestens 3 chronischen Erkrankungen)"),
     ("Checkbox Körperregionen", "- Kopf (inkl. SHT), Mittelgesicht, Hals (ohne HWS)\n- Brustkorb\n- Abdomen / Becken\n- Wirbelsäule (inkl. HWS)\n- Extremitäten"),
     ("Erläuterungen", """- Potenziell schwerverletzt im 2c-Kontext: Schockraumindikation nach Unfallmechanismus, geriatrischer Patient mit mindestens zwei relevant verletzten Körperregionen oder geriatrischer Patient mit bekanntem/vermutetem leichtem SHT – nicht jedoch bei Schockraum-A-Indikation oder beim geriatrischen Patienten mit RR syst. < 100 mmHg (C-Problem)
- Kraftfahrzeugunfall: Straßenverkehr mit mindestens einem motorisierten Verkehrsmittel (auch E-Bike); Kollisionen eines Radfahrers mit einem Hindernis aus großer Geschwindigkeit eingeschlossen
- Großtierunfall: Tritt, Kopfstoß oder Einklemmung im Bereich Körperstamm, Hals oder Kopf durch ein Großtier sowie Sturz vom Großtier in Bewegung
- Kann der Patient keine verwertbaren Angaben zu Vorerkrankungen machen, gilt dies als Beleg für Multimorbidität
- Geriatrisches leichtes SHT (GCS 13–15 ohne Verschlechterungstendenz) trotz D-Problem nach diesem Algorithmus; Voranmeldung analog Schockraumalarmierung (IVENA: PZC 222, Behandlungsdringlichkeit Notfallversorgung / rot); Voranmeldung dokumentieren"""),
     ("Hinweise", IV_FUSS + " SHT = Schädel-Hirn-Trauma, GCS = Glasgow-Coma-Scale, HWS = Halswirbelsäule.")],
    ("algo", "erl"), ["Schockraum-Indikation"])

# ======================= CHECKLISTEN § 2a (Maßnahmen) =======================
def check(id, titel, such, punkte, siehe=()):
    eintrag(id, "massnahme", titel, "", such, punkte, ("check", "matrix"), siehe)

check("xabcde", "Ersteinschätzung und initiale Beurteilung xABCDE", ["xABCDE", "ABCDE", "Ersteinschätzung", "Primary Survey"], [
 ("Grundsatz", "Bei jedem x-, A-, B-, C-, D- oder E-Problem: Notarzt alarmiert? Invasive Maßnahmen NotSan nur, sofern nach Checkliste indiziert."),
 ("x – Exsanguination", "Katastrophale Blutung? → Stillen lebensbedrohlicher Blutungen"),
 ("A – Airway", "Atemwege? → Supraglottische Atemwegshilfe · Freimachen des Tracheostomas · Endobronchiales Absaugen · Laryngoskopie / Fremdkörperentfernung mit Magill-Zange"),
 ("B – Breathing", "Adäquate Atmung? → Beutel-Masken-Beatmung ± Naso-/Oropharyngealtubus · Thoraxentlastungspunktion · Magenentlastung"),
 ("C – Circulation", "Kreislauffunktion? → Applikationstechniken für Medikamente und Infusionen · Kardioversion / Defibrillation · Transthorakaler Schrittmacher · Beckenschlinge · Reposition in achsengerechte Lage · Stillen lebensbedrohlicher Blutungen"),
 ("D – Disability", "Neurologischer Status? → Applikationstechniken für Medikamente und Infusionen · Reposition in achsengerechte Lage"),
 ("E – Exposure und Environment", "Weiteres A-, B-, C- oder D-Problem auch im Verlauf (secondary survey) erkannt, das eine invasive Maßnahme erfordert? → Geburtsbegleitung (ohne Checkliste)")])

check("blutung", "Stillen lebensbedrohlicher Blutungen", ["Tourniquet", "Blutung", "Wundtamponade", "Blutstillung", "Hämostyptikum"], [
 ("Indikation", "- Lebensgefährliche Blutungen, die mit anderen Maßnahmen nicht zeitgerecht gestoppt werden können\n- Erstversorgung bei unzugänglichem Blutungsort (z. B. eingeklemmte Person)"),
 ("Weniger invasiv zuerst", "- Manuelle Kompression, Druckverband\n- Hochlagerung der verletzten Extremität"),
 ("Maßnahmen", "- Wundtamponade mit hämostyptischen Verbandsstoffen\n- Tourniquet"),
 ("Voraussetzung", "Die Anlage eines Tourniquets ist sehr schmerzhaft und erfordert frühestmöglich eine adäquate Analgesie."),
 ("Folgemaßnahmen", "- Bei nicht sistierender Blutung zweites Tourniquet proximal des ersten\n- i.v./i.o.-Zugang und ausreichende Analgesie (entfällt bei bewusstlosen Patienten)\n- Volumentherapie\n- Nach technischer Rettung prüfen, ob Verfahrenswechsel auf Druckverband oder Wundtamponade möglich ist")])

check("sga", "Supraglottische Atemwegssicherung", ["Larynxtubus", "Larynxmaske", "SGA", "Supraglottische Atemwegshilfe", "i-gel"], [
 ("Indikation", "- Bewusstloser Patient mit beatmungspflichtiger respiratorischer Insuffizienz ohne Schutzreflexe\n- Atemwegssicherung ist gemäß CPR-Leitlinien im Verlauf der Reanimation indiziert"),
 ("Voraussetzung", "Ggf. Laryngoskopie und Fremdkörperentfernung"),
 ("Folgemaßnahmen", "- Beutelbeatmung\n- Fortführung CPR entsprechend der gültigen Leitlinien\n- Magenentlastung über Absaugkanal mittels Sonde\n- i.v./i.o.-Zugang")])

check("tracheostoma", "Freimachen des Tracheostomas", ["Tracheostoma", "Trachealkanüle frei", "Kanüle disloziert"], [
 ("Indikation", "- Tracheostoma-Träger mit respiratorischer Insuffizienz aufgrund Atemwegsverlegung und/oder Aspiration (z. B. Körpersekrete, Nahrungsmittel, Blut)\n- Dislokation der Trachealkanüle mit respiratorischer Insuffizienz"),
 ("Mögliche Maßnahmen", "- Blockung der Trachealkanüle\n- Entfernung / Wiedereinsetzen der Innenkanüle (Seele)\n- Absaugen / endobronchiales Absaugen\n- Entfernung der Außenkanüle mit / ohne Führungshilfe\n- Neuplatzierung einer dislozierten Kanüle\n- Intubation des Tracheostomas mit Endotrachealtubus"),
 ("Folgemaßnahmen", "- Sauerstoffgabe\n- Beutel-Masken-Beatmung über Mund/Nase oder Tracheostoma\n- Beutelbeatmung über geblockte Trachealkanüle oder Tubus")],
 ["2c Absaugen"])

check("endobronchial", "Endobronchiales Absaugen", ["Endobronchiales Absaugen", "Absaugen Tubus"], [
 ("Indikation", "Patient mit vorhandenem Tracheostoma oder liegendem Endotrachealtubus und kritischer Atembehinderung durch flüssige und/oder feste Substanzen in den Atemwegen"),
 ("Weniger invasiv zuerst", "Eigenständiges Abhusten (tracheotomierter Patient)"),
 ("Voraussetzung", "Ggf. Sauerstoffgabe (Präoxygenierung)"),
 ("Folgemaßnahmen", "- Laryngoskopie und Fremdkörperentfernung mit Magill-Zange\n- Beutel-Masken-Beatmung bzw. Beutelbeatmung über Tracheostoma / Tubus\n- Supraglottische Atemwegssicherung\n- Freimachen des Tracheostomas\n- i.v./i.o.-Zugang")])

check("magill", "Laryngoskopie und Fremdkörperentfernung mit Magill-Zange", ["Magill", "Magillzange", "Laryngoskopie", "Fremdkörper", "Bolus"], [
 ("Indikation", "Bewusstloser Patient ohne suffiziente Eigenatmung aufgrund einer Atemwegsverlegung"),
 ("Weniger invasiv zuerst", "- ggf. Seitenlage zum Sekretabfluss\n- Maßnahmen bei Atemwegsverlegung durch Fremdkörper laut CPR-Leitlinie"),
 ("Folgemaßnahmen", "- Beutel-Masken-Beatmung\n- Supraglottische Atemwegssicherung\n- CPR entsprechend der gültigen Leitlinien")])

check("bmv", "Beutel-Masken-Beatmung", ["Beutel-Masken-Beatmung", "BMV", "Beatmung", "Guedel", "Wendl"], [
 ("Indikation", "Patient mit beatmungspflichtiger respiratorischer Insuffizienz ohne Atemwegsverlegung"),
 ("Weniger invasiv zuerst", "- Kommandoatmung bei Wirkung atemdepressiver Substanzen\n- Sauerstoffgabe"),
 ("Voraussetzung", "- ggf. Einlage eines Oro- oder Nasopharyngealtubus\n- Laryngoskopie und Fremdkörperentfernung"),
 ("Folgemaßnahmen", "- Supraglottische Atemwegssicherung\n- Magenentlastung mittels Sonde\n- Antagonisierung atemdepressiver Substanzen\n- Sauerstoffgabe\n- i.v./i.o.-Zugang")])

check("thoraxentlastung", "Thoraxentlastungspunktion", ["Entlastungspunktion", "Pneumothorax", "Thoraxpunktion"], [
 ("Indikation", "Patient mit vital bedrohlicher hämodynamischer und/oder respiratorischer Störung **und** Zeichen eines Spannungspneumothorax"),
 ("Weniger invasiv zuerst", "- Sauerstoffgabe\n- Beutel-Masken-Beatmung"),
 ("Folgemaßnahmen", "- Sauerstoffgabe\n- Beutel-Masken-Beatmung\n- CPR entsprechend der gültigen Leitlinien\n- Supraglottische Atemwegssicherung\n- i.v./i.o.-Zugang\n- Analgesie")])

check("magenentlastung", "Magenentlastung", ["Magensonde", "Magenentlastung", "Magenüberblähung"], [
 ("Indikation", "Bewusstloser und beatmungspflichtiger Patient mit erfolgter supraglottischer Atemwegssicherung oder Magenüberblähung mit Beatmungsproblemen (insbesondere beim Säugling / Kleinkind)"),
 ("Voraussetzung", "- ggf. Beutel-Masken-Beatmung\n- ggf. supraglottische Atemwegssicherung")])

check("applikation", "Applikationstechniken für Medikamente und Infusionen", ["i.v.-Zugang", "Zugang", "intraossär", "i.o.-Zugang", "Applikation", "Venenzugang"], [
 ("Indikation", "- Zwingende Notwendigkeit einer Medikamentengabe oder Infusionstherapie unter den Voraussetzungen von § 2a NotSanG oder\n- ausreichend hohe Wahrscheinlichkeit einer Medikamentengabe oder Infusionstherapie durch den anfahrenden Notarzt oder\n- ausreichend hohe Wahrscheinlichkeit einer Zustandsverschlechterung mit Eintritt einer der o. g. Situationen bei anfahrendem Notarzt"),
 ("Maßnahmen eskalierend", "Je invasiver die Maßnahme, umso strenger ist die Indikation zu stellen!\n- Inhalation\n- i.m.-Injektion\n- i.v.-Zugang\n- nasale Medikamentengabe\n- i.o.-Zugang"),
 ("Folgemaßnahmen", "Medikamentengabe, Infusion")])

check("kardioversion", "Elektrische Kardioversion", ["Kardioversion", "Tachykardie instabil"], [
 ("Indikation", "Patient mit tachykarder Rhythmusstörung **und** hämodynamisch instabil **und** bewusstlos\n(Kurznarkose oder Analgosedierung bei nicht bewusstlosen Patienten ist nur vom Notarzt durchzuführen)"),
 ("Folgemaßnahmen", "- Erneute Kardioversion entsprechend der gültigen Leitlinien\n- i.v./i.o.-Zugang\n- Analgesie")])

check("defibrillation", "Manuelle Defibrillation", ["Defibrillation", "Defi", "Kammerflimmern", "pulslose VT"], [
 ("Indikation", "- Kammerflimmern\n- Pulslose ventrikuläre Tachykardie mit Bewusstlosigkeit"),
 ("Hinweis", "Die manuelle Defibrillation soll nur durchgeführt werden, wenn die Defibrillation im AED-Modus nicht möglich / nicht verfügbar ist."),
 ("Voraussetzung", "CPR entsprechend der gültigen Leitlinien und Beutel-Masken-Beatmung bis zur Defibrillationsbereitschaft"),
 ("Folgemaßnahmen", "- Erneute Defibrillation entsprechend der gültigen CPR-Leitlinien\n- i.v./i.o.-Zugang\n- CPR entsprechend der gültigen Leitlinien\n- Beutel-Masken-Beatmung\n- Supraglottische Atemwegssicherung")],
 ["Amiodaron", "Epinephrin"])

check("schrittmacher", "Transthorakaler Schrittmacher", ["Schrittmacher", "Pacing", "externer Schrittmacher"], [
 ("Indikation", "- Patient mit P-Wellen, jedoch ohne QRS-Komplexe im EKG\noder\n- bradykarde Rhythmusstörung **und** hämodynamisch instabil **und** schwer bewusstseinsgemindert **und** keine suffiziente Reaktion auf medikamentöse Therapie"),
 ("Weniger invasiv zuerst", "Medikamentöse antibradykarde Therapie"),
 ("Voraussetzung", "- CPR entsprechend der gültigen Leitlinien bis zur Schrittmacherbereitschaft\n- i.v./i.o.-Zugang\n- medikamentöse antibradykarde Therapie"),
 ("Folgemaßnahmen", "- CPR entsprechend der gültigen Leitlinien\n- i.v./i.o.-Zugang\n- Analgesie\n- Sauerstoffgabe")],
 ["Atropinsulfat"])

check("beckenschlinge", "Beckenschlinge (Trochanterschlinge)", ["Beckenschlinge", "Trochanterschlinge", "Beckenverletzung", "Beckenfraktur"], [
 ("Indikation", "Klinische Anhaltspunkte für eine Beckenringverletzung oder instabile Beckenringverletzung **und** hämodynamisch instabil"),
 ("Voraussetzung", "- ggf. i.v./i.o.-Zugang (entfällt bei bewusstlosen Patienten)\n- ggf. Analgesie (entfällt bei bewusstlosen Patienten)"),
 ("Folgemaßnahmen", "- i.v./i.o.-Zugang\n- Volumentherapie\n- Analgesie")])

check("reposition", "Reposition in achsengerechte Lage", ["Reposition", "Luxation", "Fehlstellung"], [
 ("Indikation", "Patient mit fehlstehender Extremität mit Störung von Durchblutung, Motorik und/oder Sensibilität"),
 ("Voraussetzung", "- i.v./i.o.-Zugang (entfällt bei bewusstlosen Patienten)\n- Analgesie (entfällt bei bewusstlosen Patienten)"),
 ("Folgemaßnahmen", "- Retention / Immobilisation\n- i.v./i.o.-Zugang\n- Analgesie (entfällt bei bewusstlosen Patienten)\n- Volumentherapie")])

# ======================= VERDACHTSDIAGNOSEN (nur Inhalte der Dokumente) =======================
FEHLT = "Symptome, Diagnostik und weiterführende Therapie sind in den gültigen Dokumenten der ÄLRD Bayern hierzu nicht beschrieben."
def diag(id, titel, kurz, such, abschnitte, quellen, siehe=(), fehlt=True):
    ab = list(abschnitte) + ([("Hinweis", FEHLT)] if fehlt else [])
    eintrag(id, "diagnose", titel, kurz, such, ab, quellen, siehe)

diag("acs", "Akutes Koronarsyndrom", "ACS", ["Herzinfarkt", "Myokardinfarkt", "Koronarsyndrom", "Brustschmerz", "Thoraxschmerz"], [
 ("Medikamente nach § 2a (Kategorie 1)", "**Morphin** – kritischer Schmerzzustand bei akutem Koronarsyndrom:\n- nur Erwachsene\n- 1–2 mg i.v. (i.o.)\n- Repetition nach frühestens 5 Minuten bis maximal 5 mg"),
 ("Nicht beim ACS", "Fentanyl i.v. und Piritramid sind laut § 2a-Liste ausdrücklich **nicht** beim akuten Koronarsyndrom vorgesehen."),
 ("Kategorie 2 (gelb) – keine Dosierungsempfehlung", "Acetylsalicylsäure, Heparin und Glyceroltrinitrat sublingual sind Kategorie 2: Kompetenz nur durch zusätzliche Aus-/Fortbildung; in den ÄLRD-Dokumenten ist keine Dosierung enthalten."),
 ("Bezug in den 2c-Algorithmen", "- Akuter Abdominalschmerz: das ACS ist vor einer 2c-Analgesie auszuschließen; bei Oberbauchschmerz 12-Kanal-EKG – ST-Hebungen oder -Senkungen in mindestens einer Ableitung → Ausschluss, Notarzt-Nachalarmierung\n- (zusätzlicher) Thoraxschmerz ist Ausschlusskriterium für die 2c-Analgesie beim Abdominalschmerz"),
 ("Hypertensiver Notfall", "Laut ÄBRD-Stellungnahme kann ein ACS Begleitsymptom eines hypertensiven Notfalls sein.")],
 ("med2a", "matrix", "erl", "hyper"), ["Morphin", "ASS", "Heparin", "Glyceroltrinitrat", "2c Abdominalschmerz"])

diag("hypoglykaemie", "Hypoglykämie", "", ["Unterzucker", "Unterzuckerung", "Hypo", "niedriger Blutzucker"], [
 ("Typische klinische Manifestationen (Checkbox 2c)", HYPO_SYMPT),
 ("§ 2a – kritische Hypoglykämie", "**Glucose 40 %:** Erwachsene initial 20 g langsam i.v. (i.o.) zu maximal laufender Infusion, ggf. weitere 20 g nach BZ; Kinder 200 mg/kg KG i.v. (i.o.) (DIVI-Kindernotfallkarte)\n**Thiamin** 100 mg langsam i.v. (i.o.) **vor** dem Hypoglykämie-Ausgleich bei V. a. chronischen Alkoholabusus bzw. schwere Mangelernährung (nur Adoleszente und Erwachsene)"),
 ("2c-Algorithmus (Kurzfassung)", HYPO_ABLAUF),
 ("V. a. schwere Mangelernährung (Checkbox 2c)", HYPO_MANGEL),
 ("Wichtig", "- Zielwert BZ ≥ 70 mg/dl (= 3,9 mmol/l)\n- Sulfonylharnstoffe (z. B. Glibenclamid, Glimepirid, Gliclazid, Gliquidon): Gefahr langanhaltender Hypoglykämie mit Rückfällen – von Verzicht auf Klinik dringend abraten\n- Bei Verdacht auf suizidale Verabreichung Kliniktransport obligat\n- Hypothermie häufig – Temperatur messen")],
 ("med2a", "algo", "erl"), ["2c Hypoglykämie", "Glucose 40 %", "Glucose-Gel", "Thiamin"], fehlt=False)

diag("sepsis", "Sepsis (Verdacht)", "", ["Sepsis", "Blutvergiftung", "septisch"], [
 ("Erkennen (2c-Algorithmus)", "Vereinfachter NEWS-2 mit mindestens 5 Punkten **plus** Hinweis auf Infektion → Verdacht auf Sepsis (ab 16 Jahren, nicht bei Schwangeren)"),
 ("Hinweise auf Infektion", INFEKT),
 ("Vorgehen 2c", "IV-Zugang, Einleitung Infusionstherapie mit 500 ml Vollelektrolytlösung, Voranmeldung „V. a. Sepsis“, Transport in geeignete Behandlungseinrichtung. Meningismus oder kritisches ABCDE-Problem → Notarzt."),
 ("Vereinfachter NEWS-2", NEWS2)],
 ("algo", "erl"), ["2c Sepsis", "NEWS2"])

diag("anaphylaxie", "Anaphylaktischer Schock", "", ["Anaphylaxie", "allergischer Schock", "Allergie"], [
 ("§ 2a – Epinephrin (Adrenalin) i.m.", "- Erwachsene: 0,5 mg i.m.; Repetition (i.m.) nach 5 Minuten bei ausbleibender Wirkung\n- Kinder (siehe DIVI-Kindernotfallkarte): 0,01 mg/kg KG i.m.; Repetition (i.m.) nach 5–10 Minuten bei ausbleibender Wirkung\n- Ampulle 1 mg / 1 ml"),
 ("Kategorie 2 (gelb)", "Dimetinden und Prednisolon: keine Dosierungsempfehlung in den ÄLRD-Dokumenten.")],
 ("med2a", "matrix"), ["Epinephrin", "Dimetinden", "Prednisolon"])

diag("kreislaufstillstand", "Kreislaufstillstand / Reanimation", "CPR", ["Reanimation", "Herzstillstand", "Kreislaufstillstand", "ALS", "Herz-Kreislauf-Stillstand"], [
 ("Epinephrin (Adrenalin) § 2a", "- Erwachsene: nicht defibrillierbar 1 mg i.v. (i.o.) sobald möglich; defibrillierbar 1 mg i.v. (i.o.) nach 3. Defibrillation; Repetition alle 3–5 Minuten unter ALS\n- Kinder (DIVI-Kindernotfallkarte): 0,01 mg/kg KG i.v. (i.o.) – nicht defibrillierbar sobald möglich, defibrillierbar nach 3. Defibrillation; Repetition alle 3–5 Minuten"),
 ("Amiodaron § 2a (Kammerflimmern / pulslose VT)", "- Erwachsene: nach 3. Defibrillation 300 mg i.v. (i.o.), nach 5. Defibrillation 150 mg i.v. (i.o.)\n- Kinder: 5 mg/kg KG (max. 300 mg bzw. 150 mg) nach 3. bzw. 5. Defibrillation"),
 ("Sauerstoff", "CPR: höchstmögliche inspiratorische Sauerstoffkonzentration"),
 ("Maßnahmen (Checklisten § 2a)", "Manuelle Defibrillation (nur wenn AED-Modus nicht möglich), Beutel-Masken-Beatmung, supraglottische Atemwegssicherung, i.v./i.o.-Zugang – CPR jeweils entsprechend der gültigen Leitlinien"),
 ("Lidocain", "Kann als alternatives Antiarrhythmikum in der Reanimation verwendet werden – Kategorie 2 (gelb)."),
 ("Sichere Todeszeichen", "Siehe Eintrag „Sichere Todeszeichen“: Liegen die Kriterien nicht vor, ist in jedem Fall mit Wiederbelebung zu beginnen.")],
 ("med2a", "check", "matrix", "tod"), ["Manuelle Defibrillation", "Epinephrin", "Amiodaron", "Sichere Todeszeichen"], fehlt=False)

diag("bradykardie", "Lebensbedrohliche Bradykardie", "", ["Bradykardie", "langsamer Puls", "AV-Block"], [
 ("§ 2a – Atropinsulfat", "- Erwachsene: initial 0,5 mg i.v. (i.o.); ggf. Wiederholung alle 3–5 Minuten bis maximal 3 mg\n- Kinder: 0,01 mg/kg KG i.v. (i.o.), max. 0,5 mg"),
 ("Transthorakaler Schrittmacher (Checkliste)", "P-Wellen ohne QRS-Komplexe **oder** bradykarde Rhythmusstörung + hämodynamisch instabil + schwer bewusstseinsgemindert + keine suffiziente Reaktion auf medikamentöse Therapie")],
 ("med2a", "check"), ["Atropinsulfat", "Transthorakaler Schrittmacher"])

diag("tachykardie", "Instabile tachykarde Rhythmusstörung", "", ["Tachykardie", "Herzrasen"], [
 ("Elektrische Kardioversion (Checkliste § 2a)", "Tachykarde Rhythmusstörung **und** hämodynamisch instabil **und** bewusstlos. Kurznarkose oder Analgosedierung bei nicht bewusstlosen Patienten ist nur vom Notarzt durchzuführen."),
 ("Medikamente", "Adenosin und Metoprolol sind Kategorie 3 (rot) der Kompetenzmatrix.")],
 ("check", "matrix"), ["Elektrische Kardioversion"])

diag("status-epilepticus", "Status epilepticus / Krampfanfall", "", ["Krampfanfall", "Epilepsie", "Krampf", "Status epilepticus", "Fieberkrampf"], [
 ("Generalisierter Status epilepticus – Midazolam § 2a", "**Intranasal** (Ampulle 15 mg / 3 ml): Erwachsene 10 mg, einmalige Repetition bei Krampfpersistenz nach frühestens 5 Minuten; Kinder 0,3 mg/kg KG (DIVI-Kindernotfallkarte)\n**Intravenös** (Ampulle 5 mg / 5 ml, in der Regel nur, wenn i.v.-Zugang bei Krampfbeginn bereits etabliert): Erwachsene initial 5 mg, einmalige Repetition; Kinder 0,1 mg/kg KG i.v. (i.o.)"),
 ("Prolongierter kindlicher Krampfanfall (> 3 min) – Diazepam rektal", "Kinder < 15 kg KG: 5 mg rektal · Kinder ≥ 15 kg KG: 10 mg rektal bzw. siehe Midazolam · keine Repetition"),
 ("V. a. alkoholinduzierten Status", "Thiamin 100 mg langsam (über eine Minute) i.v. (i.o.) unmittelbar nach Krampfdurchbrechung (nur Adoleszente und Erwachsene)"),
 ("Kompetenzmatrix", "Levetiracetam und Lorazepam: Kategorie 3 (rot).")],
 ("med2a", "matrix"), ["Midazolam", "Diazepam (Rectiole)", "Thiamin"])

diag("pseudokrupp", "Pseudokrupp / Schwellung obere Atemwege", "", ["Pseudokrupp", "Krupp", "Laryngotracheitis", "Atemwegsschwellung", "Larynxödem"], [
 ("§ 2a – Epinephrin zur Inhalation", "Kritische akute stenosierende Laryngotracheitis (Pseudokrupp), kritische Schwellung / Ödem der oberen Atemwege:\n- Erwachsene und Kinder: 5 mg (5 ml) zur Inhalation (Kinder siehe DIVI-Kindernotfallkarte)\n- Repetition bei Symptompersistenz und (kardiovaskulärer) Verträglichkeit"),
 ("§ 2a – Prednison rektal (nur Kinder)", "Pseudokrupp und kritische spastische Bronchitis: 100 mg rektal (alters-/gewichtsunabhängig)")],
 ("med2a",), ["Epinephrin", "Prednison"])

diag("bronchospastik", "Kritische Bronchospastik (Asthma / COPD)", "", ["Bronchospastik", "Asthma", "COPD", "Bronchospasmus", "Atemnot", "spastische Bronchitis", "Asthmaanfall"], [
 ("§ 2a – Salbutamol (Inhalation)", "- Erwachsene: 2,5 mg (5 ml) initial; Repetition bei Symptompersistenz und Verträglichkeit\n- Kinder (DIVI-Kindernotfallkarte): 2,5 mg (5 ml); Repetition entsprechend\n- Restmenge der Verneblungsmaske beachten!"),
 ("§ 2a – Ipratropiumbromid (Inhalation)", "- Erwachsene: 0,5 mg (2,0 ml)\n- Kinder: 0,25 mg (1,0 ml)\n- Repetition bei Symptompersistenz und (kardiovaskulärer) Verträglichkeit"),
 ("Kinder: kritische spastische Bronchitis", "Prednison 100 mg rektal (alters-/gewichtsunabhängig)"),
 ("Kategorie 2 (gelb)", "Magnesiumsulfat bei Asthma / COPD sowie Prednisolon – keine Dosierungsempfehlung in den ÄLRD-Dokumenten."),
 ("Sauerstoff 2c", "Bei Risiko für hyperkapnisches Atemversagen (z. B. bekannte COPD): Ziel-SpO2 88–92 % (siehe 2c Sauerstoff).")],
 ("med2a", "matrix", "med2c"), ["Salbutamol", "Ipratropiumbromid", "2c Sauerstoff"])

diag("hypertensiver-notfall", "Hypertensiver Notfall / hypertensive Entgleisung", "", ["Hypertensiver Notfall", "Bluthochdruck", "Hypertonie", "hypertensive Krise", "hypertensive Entgleisung", "hoher Blutdruck"], [
 ("Definition hypertensive Entgleisung", "Blutdruck > 180 / 110 mmHg **ohne** akute Manifestation einer Endorganschädigung."),
 ("Definition hypertensiver Notfall", "Akuter starker Blutdruckanstieg auf > 180 / 110 mmHg **mit** akuten Begleitsymptomen (z. B. Ruhedyspnoe, V. a. Schlaganfall, ACS, Aortendissektion, Lungenödem, rasch progrediente oder neu aufgetretene Nierenkrankheit, akute schwere Blutung o. ä.)."),
 ("Vorgehen laut ÄBRD", "- **Kein 2c-Algorithmus** für hypertensive Entgleisung oder hypertensiven Notfall (Stellungnahme 08.01.2026)\n- Entgleisung: für die meisten Fälle vorteilhaft, den Patienten ohne präklinische Intervention in eine (bereitschafts)ärztliche Versorgung zu verweisen\n- Notfall: möglichst rasche ärztliche Beurteilung durch Notarzt bzw. künftig Telenotarzt; ggf. kann es angezeigt sein, von einer präklinischen Senkung abzusehen (z. B. bei V. a. Schlaganfall)"),
 ("§ 2a – Urapidil (zur Überbrückung in akut lebensbedrohlichen Situationen)", "- nur Erwachsene\n- initial 5 mg i.v. (i.o.)\n- Repetition frühestens nach 5 Minuten\n- Senkung nach Symptomatik, max. um 25 % des Ausgangswerts RR syst."),
 ("Verfügbar im bayerischen Rettungsdienst", "Orales Captopril, sublinguales Glyceroltrinitrat, intravenös Urapidil, Metoprolol und Furosemid (Auswahl erfordert ärztliche Expertise).")],
 ("hyper", "med2a"), ["Urapidil"], fehlt=False)

diag("hypotension", "Kritische Hypotension / Volumenmangel", "", ["Kritische Hypotension", "Hypotonie", "niedriger Blutdruck", "Schock", "Volumenmangel"], [
 ("§ 2a – Cafedrin / Theodrenalin", "Kritische Hypotension trotz adäquater bzw. mit Kontraindikation für i.v.-Flüssigkeitsgabe:\n- Erwachsene: initial 0,5 ml i.v. (i.o.); ggf. Repetition alle 5 Minuten bis max. 4 ml (2 Ampullen)\n- Kinder: keine Zulassung"),
 ("§ 2a – Balancierte Elektrolytlösung", "Flüssigkeitsersatz bei kritischem Volumenmangel – nach Bedarf"),
 ("CAVE", "Konzept der permissiven Hypotension bei aktiver Blutung!")],
 ("med2a",), ["Cafedrin / Theodrenalin", "Balancierte Elektrolytlösung (Acetat/Malat)"])

diag("opiat-intox", "Opiat-Überdosierung / -Intoxikation", "", ["Opiat-Intoxikation", "Opiat", "Opioid", "Heroin", "Überdosis", "Opiatvergiftung"], [
 ("§ 2a – Naloxon nasal", "- Anwendung zugelassen ab 14. Lebensjahr\n- 1,8 mg intranasal\n- Repetition nach 2–3 Minuten oder bei Symptomrückkehr"),
 ("Beatmung", "Checkliste Beutel-Masken-Beatmung: Kommandoatmung bei Wirkung atemdepressiver Substanzen; Folgemaßnahme Antagonisierung atemdepressiver Substanzen.")],
 ("med2a", "check"), ["Naloxon (nasal)"])

diag("benzo-intox", "Benzodiazepin-Überdosierung / -Intoxikation", "", ["Benzodiazepin-Intoxikation", "Benzodiazepin", "Benzo", "Tablettenvergiftung Benzodiazepin"], [
 ("§ 2a – Flumazenil", "- Erwachsene: 0,2 mg i.v. (i.o.); ggf. Repetition nach 1 Minute bis maximal 1 mg\n- Kinder ab 1 Jahr: 0,01 mg/kg KG (max. 0,2 mg) langsam i.v. (i.o.); ggf. Repetition nach 1 Min. bis Gesamtdosis 0,05 mg/kg KG (max. 1 mg)")],
 ("med2a",), ["Flumazenil"])

diag("epistaxis", "Kritische Epistaxis (Nasenbluten)", "", ["Nasenbluten", "Epistaxis"], [
 ("§ 2a – Oxymetazolin 0,05 %", "- nur Erwachsene / Adoleszente > 50 kg KG\n- 2–6 Sprühstöße in jedes betroffene Nasenloch\n- keine Repetition"),
 ("Kompetenzmatrix", "Mechanische Nasentamponade bei Epistaxis: Kategorie 3 (rot).")],
 ("med2a", "matrix"), ["Oxymetazolin 0,05 %"])

diag("postpartale-blutung", "Kritische postpartale Blutung", "", ["postpartale Blutung", "Nachblutung Geburt", "PPH"], [
 ("§ 2a – Oxytocin", "- 3 IE langsam i.v. (i.o.)\n- einmalige Repetition nach frühestens 5 Minuten"),
 ("Geburtsbegleitung", "Die Beherrschung der Geburtsbegleitung bis zum Eintreffen des Notarztes ist eine wichtige Kompetenz (Kategorie 1, ohne Checkliste).")],
 ("med2a", "matrix"), ["Oxytocin"])

diag("schmerz", "Kritischer Schmerzzustand (Analgesie-Übersicht)", "", ["Kritischer Schmerzzustand", "Schmerz", "Analgesie", "Schmerztherapie", "Schmerzmittel"], [
 ("Kinder bis 11 Jahre", "**Esketamin** intranasal 2 mg/kg KG; ggf. Repetition der Hälfte der Initialdosis nach 10 Minuten (DIVI-Kindernotfallkarte)"),
 ("Kinder ab 12 Jahre", "**Fentanyl** intranasal 0,002 mg/kg KG; ggf. Repetition der Hälfte nach 10 Minuten (DIVI-Kindernotfallkarte)"),
 ("Erwachsene (außer ACS)", "**Fentanyl** i.v. (auch Kinder ab 12 J.): Einzeldosis 0,05 mg unverdünnt, ggf. Repetition nach 5 Minuten bis max. 0,2 mg\n**Piritramid** (> 50 kg KG): 7,5 mg als Kurzinfusion in 100 ml NaCl 0,9 % über mind. 5 Minuten, ggf. Repetition nach 10 Minuten"),
 ("Akutes Koronarsyndrom", "**Morphin** (nur Erwachsene): 1–2 mg i.v. (i.o.), Repetition nach frühestens 5 Minuten bis max. 5 mg"),
 ("2c-Delegation", "Traumatisch bedingter Schmerz und akuter Abdominalschmerz: Piritramid 7,5 mg als Kurzinfusion, **keine Repetition**, nicht bei Schwangeren, > 50 kg KG (siehe 2c-Algorithmen)"),
 ("Kategorie 2 (gelb)", "Metamizol und N-Butylscopolamin – keine Dosierungsempfehlung in den ÄLRD-Dokumenten. Paracetamol: Kategorie 3b (keine Indikation laut § 2a)."),
 ("Betäubungsmittel", BTM)],
 ("med2a", "med2c", "matrix"), ["Esketamin (intranasal, Kinder)", "Fentanyl", "Piritramid", "Morphin", "2c Trauma-Schmerz", "2c Abdominalschmerz"], fehlt=False)

diag("hypoxie", "Hypoxie / Hypoxämie", "", ["Hypoxie", "Hypoxämie", "Sauerstoffmangel", "niedrige Sättigung"], [
 ("§ 2a – kritische Hypoxie", "Sauerstoff 15 l/min über Maske; CPR: höchstmögliche inspiratorische Sauerstoffkonzentration"),
 ("2c – moderate Hypoxämie (SpO2 < 94 %)", "- ohne Hyperkapnierisiko: 4 l/min über Nasenbrille, Ziel 94–98 %, max. 6 l/min\n- mit Hyperkapnierisiko: 2 l/min + LTOT, Ziel 88–92 %\n- SpO2 < 85 % = kritische Hypoxämie → Notarzt, § 2a")],
 ("med2a", "algo", "erl"), ["Sauerstoff", "2c Sauerstoff"])

diag("abdominalschmerz", "Akuter Abdominalschmerz", "", ["Bauchschmerz", "Bauchschmerzen", "akutes Abdomen", "Flankenschmerz", "Kolik"], [
 ("2c-Algorithmus (Kurzfassung)", "Nicht tolerabler Schmerz, kein kritisches xABCDE-Problem, kein Ausschlusskriterium → IV-Zugang + 7,5 mg Piritramid als Kurzinfusion über mind. 5 Min.; danach nicht tolerabel → Notarzt"),
 ("Ausschlusskriterien", "- Blutiger Stuhl / Teerstuhl oder blutiges / kaffeesatzartiges Erbrechen\n- Bekanntes Aortenaneurysma\n- Schwangerschaft\n- (zusätzlicher) Thoraxschmerz\n- Bei Oberbauchschmerz: ST-Strecken-Veränderungen im 12-Kanal-EKG"),
 ("Wichtig", "Gastrointestinale Blutung, akutes Aortensyndrom und akutes Koronarsyndrom ausschließen. Akutes Abdomen / Peritonismus: dringliche Voranmeldung in Klinik mit chirurgischer Sofortbehandlungsmöglichkeit. Akutes Skrotum: Zielklinik mit operativer Urologie.")],
 ("algo", "erl"), ["2c Abdominalschmerz", "Piritramid"])

diag("spannungspneu", "Spannungspneumothorax", "", ["Spannungspneumothorax", "Spannungspneu"], [
 ("Thoraxentlastungspunktion (Checkliste § 2a)", "Patient mit vital bedrohlicher hämodynamischer und/oder respiratorischer Störung und Zeichen eines Spannungspneumothorax. Vorher Sauerstoffgabe / Beutel-Masken-Beatmung, falls ausreichend."),
 ("Schockraum-A", "Thoraxentlastung ist eine präklinische Intervention mit Schockraum-A-Indikation.")],
 ("check", "algo"), ["Thoraxentlastungspunktion"])

# ======================= SONSTIGES =======================
eintrag("todeszeichen", "sonstiges", "Sichere Todeszeichen – Vorgehen NotSan", "", ["Sichere Todeszeichen", "Todeszeichen", "verstorben", "Leichenschau", "Totenflecken", "Totenstarre", "Tod"], [
 ("Grundsätze", "- Unterlassen von Wiederbelebung allein auf Basis einer Patientenverfügung oder eines mutmaßlichen Willens ist für nichtärztliches Personal grundsätzlich nicht möglich\n- Jegliche Verzögerung indizierter Wiederbelebungsmaßnahmen ist inakzeptabel\n- Bei sicher verstorbenen Patienten besteht keine Notarztindikation; die Leichenschau ist keine Aufgabe des Notarztdienstes"),
 ("Ausreichend Zugang schaffen", "Der Patient muss in vollem Umfang beurteilt werden können; Umstände, die die Untersuchung beeinträchtigen, entfernen. Bei „Erhängten“ ist der Zeitpunkt unklar – Wiederbelebung kann grundsätzlich noch erfolgreich sein. Auffindesituation einprägen und formlos dokumentieren."),
 ("Ohne weitere Maßnahmen", "Großflächige, fortgeschrittene Fäulnis oder sicher nicht mit dem Leben vereinbare Verletzungen (z. B. Dekapitation) → keine weiteren medizinischen Maßnahmen, keine Notarzt-Nachforderung"),
 ("Sonst immer", "Komplette ABCDE-Beurteilung, ggf. Maßnahmen und EKG (3-Kanal) – auch bei vermeintlich anderen „sicheren“ Todeszeichen.\nKeine weitere Behandlungsindikation nur bei **gemeinsamem** Vorliegen von **Totenstarre, Totenflecken und Asystolie**. Asystolie bis zum Einsatzende ableiten (mindestens 3 min). An Intoxikationen mit Hautveränderungen, Unterkühlung, Kontrakturen, Kältestarre u. v. m. denken."),
 ("Kriterien nicht erfüllt", "In jedem Fall mit Wiederbelebung beginnen und fortführen, bis der Notarzt eintrifft; ist noch kein Notarzt auf Anfahrt, unverzüglich nachfordern."),
 ("Kriterien erfüllt", "- Rückmeldung an die ILS: „Patient verstorben“ (den Begriff „Todesfeststellung“ vermeiden)\n- ILS beendet den Einsatz für anfahrenden / anfliegenden Notarzt\n- Dokumentation im Rettungsdienstprotokoll, Ausdruck am Einsatzort belassen\n- Keine (vorläufige) Todesbescheinigung durch NotSan"),
 ("a) Identifizierter Verstorbener bei Angehörigen mit Zugangsrecht bzw. in Pflegeeinrichtung, kein Anhalt für nicht-natürlichen Tod", "Weder Notarzt noch Polizei alarmieren. Angehörige/Pflegekräfte an Hausarzt bzw. ärztlichen Bereitschaftsdienst **116 117** verweisen. Eintreffen eines Arztes nicht abwarten. Bei Überforderung der Angehörigen Unterstützung organisieren (Angehörige, Nachbarn, Seelsorger, Hausarzt, Notfallseelsorge über ILS); nur wenn niemand erreichbar ist, Polizei."),
 ("b) Polizei alarmieren und Eintreffen grundsätzlich abwarten", "- fortgeschrittene Fäulnis / Verwesung\n- Verstorbene allein, bei „Dritten“ (außer Pflegeeinrichtungen), bei Angehörigen ohne Zugangsrecht, nicht sicher identifiziert oder im öffentlichen Raum\n- offensichtlicher Anhalt für nicht-natürlichen Tod\nKeine Pflicht, aktiv nach Anhaltspunkten zu suchen. Für einen weiteren Notfalleinsatz darf die Einsatzstelle in Rechtsgüterabwägung verlassen werden.")],
 ("tod",), ["Kreislaufstillstand"])

eintrag("kompetenzmatrix", "sonstiges", "Kompetenzmatrix NotSan Bayern (§ 2a)", "", ["Kompetenzmatrix", "Kategorie grün", "Kategorie gelb", "Kategorie rot",
    "Adenosin", "Ceftriaxon", "Fenoterol", "Haloperidol", "Levetiracetam", "Lorazepam", "Metoprolol", "Norepinephrin", "Promethazin",
    "Propofol", "Reproterol", "Rocuronium", "Tenecteplase", "Thiopental", "Captopril", "Dimenhydrinat", "Ondansetron", "Paracetamol", "Intubation", "CPAP", "NIV"], [
 ("Kategorien", "- **Kategorie 1 (grün):** Kompetenzniveau soll von jedem Notfallsanitäter erreicht werden\n- **Kategorie 2 (gelb):** kann grundsätzlich durch zusätzliche Aus-/Fortbildung erreicht werden\n- **Kategorie 3 (rot):** Anwendungsbereich des § 2a NotSanG im Allgemeinen nicht gegeben (Kenntnis für Assistenz trotzdem essenziell)"),
 ("Medikamente Kategorie 1 (grün)", "Adrenalin/Epinephrin · Amiodaron · Atropin · Cafedrin/Theodrenalin · Diazepam · Esketamin · Fentanyl · Flumazenil · Glucose · Ipratropiumbromid · Kristalloide Infusionslösung · Midazolam · Morphin · Naloxon · Oxymetazolin · Oxytocin · Piritramid · Prednison · Salbutamol · Sauerstoff · Thiamin · Urapidil"),
 ("Medikamente Kategorie 2 (gelb)", "Acetylsalicylsäure · Dimetinden · Furosemid · Glyceroltrinitrat sublingual · Heparin · Lidocain · Magnesiumsulfat für Torsade de Pointes, Asthma / COPD · Metamizol · N-Butylscopolamin · Prednisolon · Tranexamsäure"),
 ("Medikamente Kategorie 3a (rot): nicht ausbildbar", "Adenosin · Ceftriaxon · Fenoterol i.v. · Haloperidol · Kolloidale Infusionslösung · Levetiracetam · Lorazepam · Magnesiumsulfat (sonstige Indikationen) · Metoprolol · Norepinephrin · Promethazin · Propofol · Reproterol · Rocuronium · Tenecteplase · Thiopental"),
 ("Medikamente Kategorie 3b (rot): keine Indikation lt. § 2a", "Captopril · Dimenhydrinat · Ondansetron · Paracetamol spp."),
 ("Maßnahmen Kategorie 1 (grün)", "Applikationstechniken Medikamente (i.v., i.o., i.m., nasal, inhalativ, bukkal, rektal, oral) · Beutel-Masken-Beatmung (alle Altersgruppen) · Direkte Laryngoskopie · Endobronchiales Absaugen · Freimachen des Tracheostomas · Fremdkörperentfernung mit Magillzange · Geburtsbegleitung · Magenentlastung · Manuelle Defibrillation · Naso- und Oropharyngealtubus · Kardioversion · Reposition · Supraglottische Atemwegshilfe (alle Altersgruppen) · Thoraxentlastungspunktion · Tourniquet · Transthorakaler Schrittmacher · Trochanterschlinge (Beckenschlinge) · Wundtamponade mit hämostatischen Verbandstoffen"),
 ("Maßnahmen Kategorie 2 (gelb)", "Endotracheale Intubation (Erwachsene und Adoleszente ab Beginn der Pubertät) · NIV-Therapie (Erwachsene und Adoleszente)"),
 ("Maßnahmen Kategorie 3 (rot)", "Allgemein- und Regionalanästhesie · CPAP-Therapie Kinder · Endotracheale Intubation (Kinder) · Nabelvenenkatheter · Mechanische Nasentamponade bei Epistaxis · Operative Eingriffe · Perkutane transtracheale Ventilation · Thoraxdrainage · Zentraler Venenkatheter"),
 ("Wichtig", "Bei der Versorgung nach § 2a sind das NotSanG, die Umsetzungshinweise des StMI sowie die Checklisten und die Medikamentenliste zu § 2a der ÄLRD zu beachten. Grundsätzlich sind die am wenigsten invasiven Maßnahmen anzuwenden.")],
 ("matrix", "kat"))

eintrag("delegation-2c", "sonstiges", "2c-Delegation – Grundsätze", "2c", ["Delegation", "2c Delegation", "Paragraph 2c", "Umsetzungshinweise", "Dokumentation 2c"], [
 ("Grundlage", "Delegation durch den ÄLRD nach Art. 12 Abs. 1 Satz 2 Nr. 6 BayRDG. Nur die von allen bayerischen ÄLRD konsentierten, bayernweit einheitlichen Maßnahmen sind für in Bayern tätige NotSan bindend – Vorgaben anderer Bundesländer oder Berufsverbände sind nicht delegiert."),
 ("Altersgruppen", "Vorgaben gelten, sofern nicht anders festgelegt, für Erwachsene und Adoleszente (ab Beginn der Pubertät)."),
 ("Ausschluss", "Ausschlusskriterien der Algorithmen führen automatisch zur Notarztnachforderung und Versorgung nach § 2a NotSanG. Nur kritische ABCDE-Probleme (mittelbare / unmittelbare Lebensbedrohung oder Gefahr von Folgeschäden) erfordern beim nicht-traumatologischen Patienten grundsätzlich den Notarzt; beim Trauma führt jedes xABCDE-Problem zur Notarzt-Nachforderung."),
 ("Monitoring", "Basismonitoring (EKG, SpO2, Blutdruck) vor Behandlungsbeginn, vollständige Dokumentation im elektronischen Einsatzprotokoll; Körpertemperatur mindestens einmal erheben."),
 ("IV-Zugang", "In der Regel nach zwei erfolglosen Punktionsversuchen misslungen. Kein invasiveres Vorgehen (z. B. kein IO-Zugang) nach Misslingen. Bei dringender Behandlungsindikation Notarzt; bei rein vorsorglichem Zugang Transport ohne weiteren Versuch. Offenhalten mit langsam tropfender balancierter Elektrolytlösung (Richtwert 1 Tropfen pro Sekunde)."),
 ("Medikamente", "Medikamentengabe in Delegation ist an Präparat und Dosis der Algorithmen gebunden; andere vorgehaltene Medikamente (insbesondere Analgetika) sind nicht möglich."),
 ("Transport", "Nach 2c-Maßnahmen immer Transport in geeignete Behandlungseinrichtung, sofern nicht anders vorgegeben (Ausnahme z. B. Absaugen Trachealkanüle). Verbleib vor Ort nur bei Transportverweigerung."),
 ("Aufklärung / Verweigerung", "Einwilligung nach Aufklärung (gleiche Anforderungen wie beim Notarzt) bzw. mutmaßliche Einwilligung; im Protokoll dokumentieren. Verweigerung schriftlich mit Zeugen. Einwilligungsunfähiger Patient verweigert erforderliche Behandlung → Polizei zur Durchsetzung."),
 ("Betäubungsmittel", "2c (Piritramid): Eintrag ins BtM-Buch mit Einsatznummer und Personalnummer, als behandelnder Arzt der delegierende ÄLRD; Unterschrift NotSan nicht erforderlich. § 2a: Eintrag unter Verweis auf § 2a NotSanG, kein Arzt anzugeben."),
 ("Dokumentation (mindestens)", "- Klinisches Zustandsbild zu allen im Algorithmus abgefragten Aspekten\n- Einverständnis bzw. mutmaßliches Einverständnis\n- Maßnahme, Medikament mit Dosis, Überwachung\n- Zustandsveränderung nach Behandlung\n- Kennzeichnung als „2c-Behandlung“\nDelegation grundsätzlich nur mit elektronischer Dokumentation (NIDAPad)."),
 ("Geltungsbereich", "Gilt auch bei Einsätzen bayerischer Rettungsmittel in anderen Bundesländern und in Tschechien (Umfang nach bayerischen Vorgaben); in Österreich kann von der Delegation kein Gebrauch gemacht werden. Maßnahmen nach § 2a sind in Österreich und Tschechien möglich.")],
 ("umset", "erl"), ["Kompetenzmatrix"])

eintrag("paragraph-2a", "sonstiges", "§ 2a NotSanG – eigenverantwortliche Heilkunde", "2a", ["Paragraph 2a", "2a NotSanG", "eigenverantwortlich", "Notkompetenz"], [
 ("Voraussetzungen", "Heilkundliche Maßnahmen nur, wenn sie zur Abwendung von Lebensgefahr oder drohenden wesentlichen Folgeschäden intendiert und geeignet sind – nur bis zum Eintreffen des Notarztes oder dem Beginn einer sonstigen (tele)ärztlichen Behandlung."),
 ("Notarzt", "Ist der Zustand lebensbedrohlich oder lässt er ohne Behandlung wesentliche Folgeschäden erwarten, ist sofort der Notarzt zu alarmieren – ebenso bei entsprechender Zustandsänderung im Verlauf. Ob wegen eines Zeitvorteils durch sofortigen Klinik-Transport auf den Notarzt verzichtet werden kann, kann nur die ILS beurteilen."),
 ("Umfang", "Kompetenzniveau beachten (Kompetenzmatrix); grundsätzlich die am wenigsten invasiven Maßnahmen (Checklisten). Darüber hinaus nur im rechtfertigenden Notstand (§ 34 StGB), z. B. Intubation nach Versagen aller sonstigen Maßnahmen. Behandlung von allgemeinem „Unwohlsein“ ist kein Maßstab für „wesentliche Folgeschäden“."),
 ("Gültige Dokumente", "Nur auf www.aelrd-bayern.de: Medikamentenliste § 2a, Maßnahmenkatalog, Checklisten, Kompetenzmatrix.")],
 ("umset", "kat", "matrix"), ["Kompetenzmatrix", "Ersteinschätzung und initiale Beurteilung xABCDE"])

eintrag("news2", "sonstiges", "Vereinfachter NEWS-2 (Bayern 2c)", "NEWS2", ["NEWS", "NEWS 2", "Early Warning Score", "Warnscore"], [
 ("Punkte", NEWS2),
 ("Verwendung", "- 2c V. a. Sepsis: ≥ 5 Punkte **plus** Hinweis auf Infektion (roter Warnwert allein ohne Wirkung)\n- 2c Risiko für relevante Zustandsverschlechterung: ≥ 5 Punkte **oder** 3 Punkte bei einem einzelnen Parameter (roter Warnwert)\n- SpO2-Skala 2 wird nicht verwendet; nur valide, zeitgleiche Werte")],
 ("algo", "erl"), ["2c Sepsis", "2c NEWS"])

eintrag("schockraum", "sonstiges", "Schockraum-Indikation (Bayerische Traumanetzwerke)", "", ["Schockraum-Indikation", "Schockraum", "Schockraum A", "Schockraum B", "Traumazentrum", "Polytrauma", "Unfallmechanismus"], [
 ("Schockraum-A-Indikation", SCHOCKRAUM_A),
 ("Schockraumindikation nach Unfallmechanismus", "- (Ab)Sturz aus über 3 Metern Höhe\n- Großtierunfall (z. B. Rind, Pferd)\n- Kraftfahrzeugunfall mit Ejektion aus dem Fahrzeug und/oder sicheren Frakturzeichen an mindestens einem langen Röhrenknochen (Oberarm, Unterarm, Oberschenkel, Unterschenkel)"),
 ("Geriatrischer Patient", "80 Jahre oder älter, oder 70 Jahre oder älter mit geriatrietypischer Multimorbidität (mindestens 3 chronische Erkrankungen)"),
 ("Voranmeldung", "Dreistufig: Schockraum A / Schockraum B / „geriatrisches leichtes SHT“ (IVENA: PZC 222, Behandlungsdringlichkeit Notfallversorgung / rot)")],
 ("algo", "erl"), ["2c Verletzte Person", "2c Trauma-Schmerz"])

if __name__ == "__main__":
    ids = [e["id"] for e in E]
    assert len(ids) == len(set(ids)), "doppelte IDs"
    out = {"app": "Wissen RD", "titel": "Import ÄLRD Bayern",
           "hinweis": "Ausschließlich aus den gültigen Dokumenten der ÄLRD Bayern (www.aelrd-bayern.de, NotSan-Seite), Stand der Prüfung 15.11.2026. Vor Nutzung mit den Originaldokumenten abgleichen.",
           "eintraege": E}
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(E), "Einträge", Counter(e["bereich"] for e in E))

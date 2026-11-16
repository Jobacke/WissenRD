"""Erzeugt daten/abkuerzungen-import.json – Abkürzungen und Merkhilfen im Rettungsdienst (Bereich „abkuerzung“).
Bedeutung = allgemeine notfallmedizinische Fachsprache; Bayern-Bezug nur, wo ein ÄLRD-Bayern-Dokument ihn belegt.
Keine Dosierungen oder Grenzwerte außerhalb der ÄLRD-Dokumente. Recherche 16.11.2026."""
import json, re, sys, unicodedata

STAND = "2026-11"
Q_ALLG = "Allgemeine notfallmedizinische Fachsprache"
Q_2A_APP = "ÄLRD Bayern: 2a-Checklisten (Stand 25.07.2024), Applikationstechniken für Medikamente und Infusionen"
Q_2A_X = "ÄLRD Bayern: 2a-Checklisten (Stand 25.07.2024), Ersteinschätzung und initiale Beurteilung Patient xABCDE"
Q_2C = "ÄLRD Bayern: Delegationsalgorithmen 2c (gültig ab 01.11.2025)"
Q_MED = "ÄLRD Bayern: Medikamente zur Anwendung nach § 2a NotSanG, Version 1.5 (22.10.2025)"
Q_RDA = "ÄLRD Bayern: Empfehlungen (RDA-Dokumente)"
Q_DOC = "DocCheck Flexikon"

E = []
def ab(kurz, bedeutung, erklaerung="", bayern="", siehe=(), such=(), quellen=(Q_ALLG,)):
    E.append({"kurz": kurz, "bedeutung": bedeutung, "erklaerung": erklaerung.strip(), "bayern": bayern.strip(),
              "siehe": list(siehe), "such": list(such), "quellen": list(quellen)})

APP = "Eskalierende Reihenfolge der Applikationswege (2a-Checkliste „Applikationstechniken“): Inhalation → i.m.-Injektion → i.v.-Zugang → nasale Medikamentengabe → i.o.-Zugang. Je invasiver die Maßnahme, umso strenger die Indikation."

# ------------------------------------------------------------------ gewünschte Abkürzungen
ab("STEMI", "ST-Elevation Myocardial Infarction – ST-Hebungsinfarkt",
   "- Form des akuten Koronarsyndroms mit ST-Strecken-Hebungen im 12-Kanal-EKG\n- Abgrenzung: **NSTEMI** (Infarkt ohne ST-Hebung) und instabile Angina pectoris",
   siehe=["Akutes Koronarsyndrom", "NSTEMI", "ACS"], such=["ST-Hebungsinfarkt", "ST Hebungsinfarkt"])
ab("KRIMP", "Merkhilfe zur Pupillenbeurteilung",
   "- **K**onsensuell – beide Pupillen reagieren gleichsinnig, auch wenn nur in ein Auge geleuchtet wird\n"
   "- **R**und – Pupillen rund und gleichmäßig geformt\n- **I**sokor – beide Pupillen gleich groß (Gegenteil: anisokor)\n"
   "- **M**ydriasis / **M**iosis – weite bzw. enge Pupillen\n- **P**rompt – prompte (zügige) Lichtreaktion\n"
   "- Gehört zum D (Disability) der Untersuchung nach xABCDE",
   siehe=["PERLA", "xABCDE", "GCS"], such=["KRIMP-Schema", "Krimp Pupillen", "Pupillenbeurteilung"],
   quellen=["Notfallmedizinische Lehrinhalte zur Pupillenbeurteilung (u. a. SMEDEX-Lerneinheit „Strukturierte Untersuchung von Notfallpatienten“)"])
ab("PERLA", "Pupils Equal, (Round,) reactive to Light and Accommodation – Pupillen gleich (rund), licht- und akkommodationsreagibel",
   "- Englische Merkhilfe zur Pupillenbeurteilung, Varianten: **PERL** (ohne Akkommodation), **PERRLA** (mit „Round“)\n"
   "- **P**upils – Pupillen\n- **E**qual – gleich groß (isokor)\n- **R**ound – rund\n- **R**eactive to **L**ight – lichtreagibel\n"
   "- **A**ccommodation – Engstellung beim Blick in die Nähe\n- Deutschsprachige Entsprechung im Rettungsdienst: KRIMP",
   siehe=["KRIMP"], such=["PERRLA", "PERL", "Perla Pupillen"], quellen=["Cleveland Clinic: PERRLA Eye Exam", "GPnotebook: PERLA"])
ab("ZOPS", "Orientierung zu Zeit, Ort, Person und Situation",
   "- **Z**eit – Welcher Tag, Monat, welches Jahr? Wie spät ist es?\n- **O**rt – Wo sind Sie?\n"
   "- **P**erson – Wie heißen Sie? Wie alt sind Sie?\n- **S**ituation – Was ist passiert?\n"
   "- Dokumentation z. B. „WAO zu ZOPS“ = wach, ansprechbar, zu allen vier Qualitäten orientiert\n- Synonym: ZÖPS",
   siehe=["WAO", "GCS", "AVPU"], such=["ZÖPS", "ZOPS-Schema", "Orientierung", "WAO zu ZOPS"], quellen=[Q_DOC + ": ZOPS-Schema, WAO-Schema"])
ab("i.v.", "intravenös – in die Vene",
   "- Applikationsweg über einen peripheren Venenzugang (Venenverweilkanüle)\n- Im Abkürzungsverzeichnis der ÄLRD Bayern: **IV = intravenös**",
   bayern=APP + "\n- In den 2c-Algorithmen: IV-Zugang max. 2 Versuche, **kein IO-Zugang** im Rahmen der 2c-Delegation",
   siehe=["Applikationstechniken für Medikamente und Infusionen", "i.o.", "i.m."],
   such=["iv", "intravenös", "intravenoes", "Venenzugang", "IV-Zugang"], quellen=[Q_ALLG, Q_2A_APP, Q_2C])
ab("i.m.", "intramuskulär – in den Muskel",
   "- Injektion in einen Muskel, z. B. in die Außenseite des Oberschenkels",
   bayern=APP + "\n- Beispiel ÄLRD-Medikamentenliste: Epinephrin (Adrenalin) i.m. bei Anaphylaxie – Dosierung siehe dort",
   siehe=["Applikationstechniken für Medikamente und Infusionen", "Epinephrin (Adrenalin)", "Anaphylaktischer Schock"],
   such=["im", "intramuskulär", "intramuskulaer"], quellen=[Q_ALLG, Q_2A_APP, Q_MED])
ab("i.o.", "intraossär – in den Knochen (Markraum)",
   "- Gefäßzugang über eine spezielle Nadel in den Knochenmarkraum, wenn ein i.v.-Zugang nicht (rechtzeitig) gelingt\n"
   "- In den ÄLRD-Dosierungen oft als „i.v. (i.o.)“ angegeben",
   bayern=APP + "\n- 2c-Delegation: **kein IO-Zugang** (IV-Zugang max. 2 Versuche)",
   siehe=["Applikationstechniken für Medikamente und Infusionen", "i.v."],
   such=["io", "intraossär", "intraossaer", "IO-Zugang", "intraossärer Zugang"], quellen=[Q_ALLG, Q_2A_APP, Q_2C])
ab("ACS", "Acute Coronary Syndrome – Akutes Koronarsyndrom",
   "- Oberbegriff für instabile Angina pectoris, NSTEMI und STEMI",
   bayern="Vorgehen bei V. a. ACS: siehe Eintrag „Akutes Koronarsyndrom“ (ÄLRD Bayern)",
   siehe=["Akutes Koronarsyndrom", "STEMI", "NSTEMI"])
ab("CPR", "Cardiopulmonary Resuscitation – kardiopulmonale Reanimation",
   "- Deutsche Entsprechung: **HLW** (Herz-Lungen-Wiederbelebung)\n- Thoraxkompressionen und Beatmung bei Kreislaufstillstand\n- mCPR = mechanische Thoraxkompression",
   siehe=["Kreislaufstillstand / Reanimation", "ROSC", "AED", "ALS"], such=["HLW", "Reanimation", "Herz-Lungen-Wiederbelebung"])

# ------------------------------------------------------------------ Diagnosen / Befunde
ab("NSTEMI", "Non-ST-Elevation Myocardial Infarction – Myokardinfarkt ohne ST-Hebung",
   "- Form des akuten Koronarsyndroms ohne ST-Strecken-Hebung im EKG", siehe=["ACS", "STEMI", "Akutes Koronarsyndrom"])
ab("AP", "Angina pectoris – Brustenge",
   "- Anfallsartiger Brustschmerz/Engegefühl durch Minderdurchblutung des Herzmuskels\n- Instabile AP gehört zum ACS", siehe=["ACS"])
ab("LAE", "Lungenarterienembolie", "- Verschluss einer Lungenarterie, meist durch ein Blutgerinnsel (Thrombus) aus den Beinvenen\n- Synonym: Lungenembolie (LE)",
   such=["Lungenembolie", "LE"])
ab("TVT", "Tiefe Venenthrombose", "- Blutgerinnsel in einer tiefen Vene, meist im Bein/Becken; Hauptquelle der Lungenembolie", siehe=["LAE"])
ab("SHT", "Schädel-Hirn-Trauma", "- Verletzung des Schädels mit Beteiligung des Gehirns", siehe=["GCS", "HWS"])
ab("HWS", "Halswirbelsäule", "- Ebenso: **BWS** Brustwirbelsäule, **LWS** Lendenwirbelsäule", such=["BWS", "LWS"])
ab("ICB", "Intrazerebrale Blutung – Hirnblutung", "- Blutung in das Hirngewebe; Ursache eines hämorrhagischen Schlaganfalls", siehe=["SAB", "TIA"])
ab("SAB", "Subarachnoidalblutung", "- Blutung in den Raum zwischen Spinnwebenhaut und weicher Hirnhaut, typisch: schlagartiger, stärkster Kopfschmerz",
   bayern="ÄLRD-Bayern-Empfehlung: Nutzung des PZC „Kopf-/Gesichtsschmerz“ bei Verdacht auf akute Subarachnoidalblutung (08.10.2026)",
   siehe=["ICB", "PZC"], quellen=[Q_ALLG, Q_RDA])
ab("TIA", "Transitorische ischämische Attacke", "- Vorübergehende neurologische Ausfälle durch kurzzeitige Minderdurchblutung des Gehirns; Warnzeichen für einen Schlaganfall",
   siehe=["BE-FAST", "ICB"])
ab("COPD", "Chronic Obstructive Pulmonary Disease – chronisch obstruktive Lungenerkrankung",
   siehe=["Kritische Bronchospastik (Asthma / COPD)", "LTOT", "NIV"])
ab("LTOT", "Long-Term Oxygen Therapy – Langzeit-Sauerstofftherapie",
   "- Dauerhafte Sauerstoffgabe zu Hause, z. B. bei schwerer COPD", siehe=["COPD"], quellen=[Q_ALLG, Q_2C])
ab("DD", "Differenzialdiagnose", "- Andere in Frage kommende Erkrankung mit ähnlichem Erscheinungsbild")
ab("V. a.", "Verdacht auf", "- Vor einer Diagnose, die noch nicht gesichert ist, z. B. „V. a. Sepsis“", such=["Va", "Verdacht auf"])
ab("Z. n.", "Zustand nach", "- Kennzeichnet eine frühere Erkrankung oder Operation, z. B. „Z. n. Herzinfarkt“", such=["Zn", "Zustand nach"])

# ------------------------------------------------------------------ Untersuchung / Merkhilfen
ab("xABCDE", "Strukturierte Ersteinschätzung: eXsanguination, Airway, Breathing, Circulation, Disability, Exposure/Environment",
   "- **x** – lebensbedrohliche (katastrophale) Blutung\n- **A** – Atemweg\n- **B** – Atmung\n- **C** – Kreislauf\n"
   "- **D** – neurologischer Status (z. B. GCS, Pupillen, BZ)\n- **E** – Entkleiden/Untersuchen, Umgebung, Wärmeerhalt\n"
   "- Varianten: ABCDE, cABCDE (c = critical bleeding)",
   bayern="ÄLRD Bayern: 2a-Checkliste „Ersteinschätzung und initiale Beurteilung Patient xABCDE“ – je Buchstabe: Notarzt alarmiert? invasive Maßnahmen NotSan nach Checkliste",
   siehe=["Ersteinschätzung und initiale Beurteilung xABCDE", "KRIMP", "GCS"], such=["ABCDE", "cABCDE", "ABCDE-Schema"],
   quellen=[Q_ALLG, Q_2A_X])
ab("SAMPLER", "Anamnese-Schema",
   "- **S**ymptome\n- **A**llergien\n- **M**edikamente\n- **P**atientenvorgeschichte (Vorerkrankungen)\n- **L**etzte Mahlzeit (auch letzte Ausscheidung, Menstruation)\n"
   "- **E**reignis – was ist passiert?\n- **R**isikofaktoren", siehe=["OPQRST"], such=["SAMPLE", "SAMPLER-Schema", "Anamnese"])
ab("OPQRST", "Schmerzanamnese",
   "- **O**nset – Beginn (plötzlich/allmählich)\n- **P**rovocation/Palliation – was verstärkt, was lindert?\n- **Q**uality – Art des Schmerzes\n"
   "- **R**egion/Radiation – Ort und Ausstrahlung\n- **S**everity – Stärke (z. B. NRS 0–10)\n- **T**ime – Dauer, Verlauf",
   siehe=["SAMPLER", "NRS"], such=["OPQRST-Schema", "Schmerzanamnese"])
ab("BE-FAST", "Schlaganfall-Erkennung",
   "- **B**alance – Gleichgewicht/Schwindel\n- **E**yes – Sehstörung\n- **F**ace – Gesicht (hängender Mundwinkel)\n- **A**rms – Armschwäche\n"
   "- **S**peech – Sprachstörung\n- **T**ime – Zeitpunkt des Symptombeginns / keine Zeit verlieren\n- Kurzform ohne B und E: **FAST**",
   bayern="ÄLRD-Bayern-Empfehlung „Präklinische Versorgung von Patienten mit akutem Schlaganfall“ (23.03.2021) – Inhalt hier nicht übernommen",
   siehe=["Übersicht Stroke Units", "TIA"], such=["BEFAST", "FAST", "FAST-Test"], quellen=[Q_ALLG, Q_RDA])
ab("GCS", "Glasgow Coma Scale",
   "- Bewertung der Bewusstseinslage in drei Kategorien: **Augenöffnen** 1–4, **verbale Reaktion** 1–5, **motorische Reaktion** 1–6\n"
   "- Summe 3 (tiefe Bewusstlosigkeit) bis 15 (wach, orientiert)\n- Bei Kindern: angepasste pädiatrische GCS",
   siehe=["AVPU", "WAO", "ZOPS", "SHT"], such=["Glasgow Coma Scale", "Glasgow-Koma-Skala"], quellen=[Q_ALLG, Q_2C])
ab("AVPU", "Alert, Verbal, Pain, Unresponsive – Schnellbeurteilung der Bewusstseinslage",
   "- **A** – wach\n- **V** – reagiert auf Ansprache\n- **P** – reagiert auf Schmerzreiz\n- **U** – reagiert nicht", siehe=["GCS", "WAO"])
ab("WAO", "wach, ansprechbar, orientiert",
   "- **W** – Patient ist wach\n- **A** – reagiert auf Ansprache\n- **O** – orientiert (weitere Beurteilung mit ZOPS)\n- Dokumentation z. B. „WAO zu ZOPS“",
   siehe=["ZOPS", "AVPU"], such=["WAO-Schema"], quellen=[Q_DOC + ": WAO-Schema"])
ab("NEWS2", "National Early Warning Score 2",
   "- Punktesystem aus Vitalparametern zur Einschätzung des Risikos einer Zustandsverschlechterung",
   bayern="ÄLRD Bayern verwendet einen **vereinfachten NEWS-2** in den 2c-Algorithmen „V. a. Sepsis“ und „Risiko für relevante Zustandsverschlechterung“ – Punktetabelle siehe dort",
   siehe=["2c Sepsis", "2c NEWS"], such=["NEWS", "NEWS-2", "News Score"], quellen=[Q_ALLG, Q_2C])
ab("NRS", "Numerische Rating-Skala", "- Schmerzstärke von 0 (kein Schmerz) bis 10 (stärkster vorstellbarer Schmerz)",
   siehe=["OPQRST", "Kritischer Schmerzzustand (Analgesie-Übersicht)"], such=["Schmerzskala"])

# ------------------------------------------------------------------ Vitalwerte / Messung
ab("BZ", "Blutzucker", "- Blutglukosewert, Angabe in mg/dl oder mmol/l",
   bayern="ÄLRD Bayern (2c Hypoglykämie): BZ-Umrechnung 70 mg/dl = 3,9 mmol/l", siehe=["Hypoglykämie", "Hyperglykämie"],
   such=["Blutzucker", "BZ-Messung"], quellen=[Q_ALLG, Q_2C])
ab("RR", "Blutdruck nach Riva-Rocci", "- Nicht-invasive Blutdruckmessung mit Manschette; Angabe systolisch/diastolisch in mmHg\n- Ebenso: **NIBP** (non-invasive blood pressure)",
   such=["Blutdruck", "NIBP", "Riva-Rocci"])
ab("HF", "Herzfrequenz", "- Schläge pro Minute; Puls = tastbare Herzfrequenz", such=["Herzfrequenz", "Puls"])
ab("AF", "Atemfrequenz", "- Atemzüge pro Minute\n- **Achtung:** AF steht im kardiologischen Kontext auch für **Atrial Fibrillation** = Vorhofflimmern (VHF)",
   such=["Atemfrequenz", "VHF", "Vorhofflimmern"])
ab("SpO2", "Periphere (pulsoxymetrisch gemessene) Sauerstoffsättigung", "- Anteil des mit Sauerstoff beladenen Hämoglobins in %",
   siehe=["Hypoxie / Hypoxämie", "2c Sauerstoff"], such=["SpO 2", "Sauerstoffsättigung", "Sättigung", "Pulsoxymetrie"])
ab("etCO2", "Endtidales Kohlendioxid", "- CO2-Konzentration am Ende der Ausatmung, gemessen per Kapnometrie/Kapnografie (Lage-/Beatmungskontrolle, Reanimation)",
   such=["etCO 2", "endtidales CO2", "Kapnografie", "Kapnometrie"])
ab("O2", "Sauerstoff", siehe=["2c Sauerstoff", "Hypoxie / Hypoxämie"], such=["Sauerstoffgabe"], quellen=[Q_ALLG, Q_2C])
ab("EKG", "Elektrokardiogramm", "- Ableitung der elektrischen Herzaktivität; **12-Kanal-EKG** zur Infarktdiagnostik", siehe=["STEMI", "ACS"],
   such=["12-Kanal-EKG", "Zwölf-Kanal-EKG"])
ab("ROSC", "Return of Spontaneous Circulation – Wiederkehr eines Spontankreislaufs", "- Nach erfolgreicher Reanimation",
   siehe=["CPR", "Kreislaufstillstand / Reanimation"])
ab("KG", "Körpergewicht", "- In Dosierungen: „mg/kg KG“ = Milligramm pro Kilogramm Körpergewicht", quellen=[Q_ALLG, Q_2C])

# ------------------------------------------------------------------ Applikation / Pharmakologie
ab("s.c.", "subkutan – unter die Haut", such=["sc", "subkutan"])
ab("i.n.", "intranasal – über die Nase", "- Gabe meist über einen Zerstäuber (Mucosal Atomization Device)",
   bayern=APP, siehe=["Applikationstechniken für Medikamente und Infusionen"], such=["in", "intranasal", "nasal"], quellen=[Q_ALLG, Q_2A_APP])
ab("p.o.", "per os – über den Mund (zum Schlucken)", such=["po", "per os", "oral"])
ab("s.l.", "sublingual – unter die Zunge", such=["sl", "sublingual"])
ab("KI", "Kontraindikation – Gegenanzeige", "- Umstand, bei dem ein Medikament oder eine Maßnahme nicht angewendet werden darf", such=["Kontraindikation", "Gegenanzeige"])
ab("UAW", "Unerwünschte Arzneimittelwirkung – Nebenwirkung", "- Auch: **NW** (Nebenwirkung)", such=["NW", "Nebenwirkung"])
ab("BtM", "Betäubungsmittel", "- Medikamente, die dem Betäubungsmittelgesetz unterliegen (z. B. Opioide wie Fentanyl, Morphin)",
   siehe=["2c Trauma-Schmerz", "2c Abdominalschmerz"], such=["Betäubungsmittel"], quellen=[Q_ALLG, Q_2C])
ab("VEL", "Vollelektrolytlösung", "- Kristalloide Infusionslösung mit plasmaähnlicher Elektrolytzusammensetzung",
   siehe=["Balancierte Elektrolytlösung (Acetat/Malat)"], such=["Vollelektrolytlösung"])

# ------------------------------------------------------------------ Atemweg / Beatmung / Geräte
ab("SGA", "Supraglottische Atemwegshilfe", "- Atemwegshilfe, die oberhalb der Stimmritze liegt (z. B. Larynxtubus, Larynxmaske)\n- Ebenso: **SAD** (supraglottic airway device)",
   siehe=["Supraglottische Atemwegssicherung"], such=["SAD", "Larynxtubus", "Larynxmaske", "supraglottischer Atemweg"], quellen=[Q_ALLG, Q_2A_X])
ab("ITN", "Intubationsnarkose", "- Narkose mit endotrachealer Intubation (Beatmungsschlauch in der Luftröhre); ärztliche Maßnahme",
   such=["Intubation", "Intubationsnarkose"])
ab("BMV", "Beutel-Masken-Beatmung", siehe=["Beutel-Masken-Beatmung"], such=["Maskenbeatmung"], quellen=[Q_ALLG, Q_2A_X])
ab("CPAP", "Continuous Positive Airway Pressure – kontinuierlicher positiver Atemwegsdruck",
   "- Atemunterstützung bei erhaltener Spontanatmung, z. B. bei Lungenödem", siehe=["NIV"])
ab("NIV", "Nicht-invasive Ventilation", "- Beatmung über eine dicht sitzende Maske ohne Intubation", siehe=["CPAP", "COPD"])
ab("AED", "Automatisierter externer Defibrillator", "- Analysiert den Herzrhythmus und gibt bei Bedarf nach Aufforderung einen Schock ab; auch für Laien",
   siehe=["CPR", "Manuelle Defibrillation"], such=["Defi", "Laiendefibrillator"])
ab("ALS", "Advanced Life Support – erweiterte Reanimationsmaßnahmen", "- Gegenstück: **BLS** (Basic Life Support) = Basismaßnahmen",
   siehe=["CPR", "Kreislaufstillstand / Reanimation"], such=["BLS", "Basic Life Support"])

# ------------------------------------------------------------------ Organisation / Rettungsmittel
ab("NA", "Notarzt / Notärztin", such=["Notarzt"])
ab("NEF", "Notarzteinsatzfahrzeug", "- Bringt den Notarzt zum Einsatzort (Rendezvous-System)", such=["Notarzteinsatzfahrzeug"])
ab("RTW", "Rettungswagen", "- Fahrzeug zur Notfallrettung und zum Transport von Notfallpatienten", such=["Rettungswagen"])
ab("KTW", "Krankentransportwagen", "- Fahrzeug für den qualifizierten Krankentransport", such=["Krankentransportwagen", "Krankentransport"])
ab("RTH", "Rettungshubschrauber", "- Ebenso: **ITH** Intensivtransporthubschrauber", such=["Rettungshubschrauber", "ITH", "Christoph"])
ab("ITW", "Intensivtransportwagen", "- Für Verlegungen intensivpflichtiger Patienten", such=["Intensivtransportwagen"])
ab("NotSan", "Notfallsanitäter/in", "- Höchste nichtärztliche Qualifikation im Rettungsdienst, geregelt im Notfallsanitätergesetz (NotSanG)",
   such=["Notfallsanitäter", "NFS"])
ab("RettSan", "Rettungssanitäter/in", such=["Rettungssanitäter", "RS"])
ab("NotSanG", "Notfallsanitätergesetz",
   "- **§ 2a**: eigenverantwortliche heilkundliche Maßnahmen bei Lebensgefahr oder drohenden wesentlichen Folgeschäden bis zum Eintreffen des Notarztes\n"
   "- **§ 4 Abs. 2 Nr. 2c**: Maßnahmen nach vom ÄLRD vorgegebenen Algorithmen (Delegation)",
   siehe=["2c-Delegation – Grundsätze", "Kompetenzmatrix NotSan Bayern (§ 2a)"], such=["Paragraph 2a", "2a", "2c"], quellen=[Q_ALLG, Q_MED, Q_2C])
ab("ÄLRD", "Ärztlicher Leiter Rettungsdienst",
   "- Ärztlich verantwortlich für die medizinische Qualität im Rettungsdienstbereich; gibt u. a. die 2c-Algorithmen vor",
   bayern="In den ÄLRD-Bayern-Dokumenten außerdem: **ÄLBRD** = Ärztlicher Landesbeauftragter Rettungsdienst, **ÄBRD** = Ärztlicher Bezirksbeauftragter Rettungsdienst, **StMI** = Staatsministerium des Innern",
   such=["ÄLRD Bayern", "Ärztlicher Leiter Rettungsdienst", "ÄLBRD", "ÄBRD"], quellen=[Q_ALLG, Q_2C])
ab("ILS", "Integrierte Leitstelle", "- Bearbeitet in Bayern Notrufe für Rettungsdienst und Feuerwehr gemeinsam (eine ILS je Rettungsdienstbereich)",
   siehe=["Übersicht Leitstellen"], such=["Integrierte Leitstelle"])
ab("IVENA", "Interdisziplinärer Versorgungsnachweis",
   "- Webbasiertes System, das freie Behandlungskapazitäten der Kliniken anzeigt und die Anmeldung von Patienten unterstützt",
   bayern="Bayernweite Nutzung laut ÄLRD-Empfehlungen (u. a. Patientenzuweisungscodes, Behandlungsprioritäten, MANV-Modul)",
   siehe=["PZC"], such=["Ivena"], quellen=[Q_ALLG, Q_RDA])
ab("PZC", "Patientenzuweisungscode",
   "- Code aus Fachgebiet/Diagnosegruppe, Alter und Dringlichkeit zur Anmeldung und Zuweisung über IVENA",
   bayern="Bayern: „Patientenzuweisungscodes Bayern“ auf Grundlage der bundeseinheitlichen PZC (ÄLRD-Empfehlung 17.06.2024)",
   siehe=["IVENA"], such=["Patientenzuweisungscode"], quellen=[Q_ALLG, Q_RDA])
ab("MANV", "Massenanfall von Verletzten (bzw. Erkrankten)",
   "- Lage mit mehr Betroffenen, als mit den regulären Mitteln versorgt werden können",
   bayern="Bayern: Begriff **MAN** (Massenanfall), Richtlinie zur Bewältigung von Ereignissen mit einem Massenanfall (MAN-RL, 07.01.2025)",
   siehe=["SanEL", "LNA"], such=["MAN", "Massenanfall"], quellen=[Q_ALLG, Q_RDA])
ab("SanEL", "Sanitätseinsatzleitung", "- Führung des Sanitäts- und Rettungsdienstes bei Großschadenslagen, bestehend aus LNA und OrgL",
   siehe=["LNA", "OrgL", "MANV"], such=["Sanitätseinsatzleitung"], quellen=[Q_ALLG, Q_RDA])
ab("LNA", "Leitender Notarzt", "- Medizinische Führung bei MANV/Großschadenslagen", siehe=["SanEL", "OrgL"], such=["Leitender Notarzt"])
ab("OrgL", "Organisatorischer Leiter Rettungsdienst", "- Organisatorische Führung bei MANV/Großschadenslagen", siehe=["SanEL", "LNA"],
   such=["Organisatorischer Leiter", "OLRD"])
ab("PSNV", "Psychosoziale Notfallversorgung", "- Betreuung von Betroffenen (z. B. Krisenintervention) und Einsatzkräften nach belastenden Einsätzen",
   such=["Krisenintervention", "KIT"])
ab("SOP", "Standard Operating Procedure – Standardvorgehensweise", "- Ebenso: **SAA** (Standardarbeitsanweisung), **BPR** (Behandlungspfad Rettungsdienst)",
   such=["SAA", "Standardarbeitsanweisung", "BPR"], quellen=[Q_ALLG, Q_2C])
ab("DIVI", "Deutsche Interdisziplinäre Vereinigung für Intensiv- und Notfallmedizin",
   bayern="ÄLRD Bayern verweist für Kinderdosierungen auf die **DIVI-Kindernotfallkarte**",
   such=["DIVI-Kindernotfallkarte", "Kindernotfallkarte"], quellen=[Q_ALLG, Q_MED, Q_RDA])

# ------------------------------------------------------------------ Normalisierung, Kollisionsprüfung, Ausgabe
def norm(s):
    s = (s or "").lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]", "", s)

def slug(s):
    return "abk-" + (norm(s) or "x")

# vorhandene Schlüssel der anderen Datensätze (Siri soll weiterhin eindeutig bleiben)
fremd, ziele = {}, set()
for f in ["aelrd-bayern-import.json", "kliniken-muenchen-import.json", "leitstellen-import.json", "ergaenzungen-import.json", "symptome-import.json"]:
    try:
        for e in json.load(open(f, encoding="utf-8"))["eintraege"]:
            ziele.update(x for x in [e.get("titel"), e.get("kurz")] if x)
            for k in [e.get("kurz"), e.get("titel"), *e.get("suchbegriffe", [])]:
                if norm(k): fremd.setdefault(norm(k), e["titel"])
    except FileNotFoundError:
        pass

titel_alle = ziele | {x["kurz"] for x in E}
aus, eigene, protokoll = [], {}, []
for x in E:
    k = x["kurz"]
    titel = k if norm(k) not in fremd else f"{k} (Abkürzung)"
    if titel != k: protokoll.append(f"{k}: Titel → „{titel}“ (Schlüssel belegt von „{fremd[norm(k)]}“)")
    such = [f"{k} Abkürzung", f"Abkürzung {k}"]
    for s in x["such"]:
        n = norm(s)
        if not n or n in fremd or n in eigene or n == norm(titel): 
            if n in fremd: protokoll.append(f"{k}: Suchbegriff „{s}“ weggelassen (gehört zu „{fremd[n]}“)")
            elif n in eigene: protokoll.append(f"{k}: Suchbegriff „{s}“ weggelassen (schon bei {eigene[n]})")
            continue
        such.append(s)
    for s in [titel, *such]:
        eigene.setdefault(norm(s), k)
    abschn = [{"titel": "Bedeutung", "text": x["bedeutung"]}]
    if x["erklaerung"]: abschn.append({"titel": "Erklärung", "text": x["erklaerung"]})
    if x["bayern"]: abschn.append({"titel": "Bayern-Bezug (ÄLRD)", "text": x["bayern"] if x["bayern"].startswith("-") else "- " + x["bayern"]})
    siehe = [s for s in x["siehe"] if s in titel_alle]
    fehlt = [s for s in x["siehe"] if s not in titel_alle]
    if fehlt: protokoll.append(f"{k}: Querverweis ohne Ziel – {fehlt}")
    aus.append({"id": slug(k), "bereich": "abkuerzung", "titel": titel, "kurz": "",
                "suchbegriffe": such, "siehe": siehe, "abschnitte": abschn,
                "sprechtext": "",
                "quelle": " · ".join(x["quellen"]), "stand": STAND})

# Querverweise auf Abkürzungen mit geändertem Titel nachziehen
umbenannt = {x["kurz"]: a["titel"] for x, a in zip(E, aus) if a["titel"] != x["kurz"]}
for a in aus:
    a["siehe"] = [umbenannt.get(s, s) for s in a["siehe"]]

if __name__ == "__main__":
    ids = [a["id"] for a in aus]
    assert len(ids) == len(set(ids)), "doppelte IDs"
    json.dump({"app": "Wissen RD", "titel": "Import Abkürzungen Rettungsdienst",
               "hinweis": "Abkürzungen und Merkhilfen. Bedeutung nach allgemeiner Fachsprache; Bayern-Bezug nur mit ÄLRD-Beleg. Siri: „<Abkürzung> Abkürzung“ findet immer den Abkürzungs-Eintrag.",
               "eintraege": aus}, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(aus), "Abkürzungen")
    print("\n".join(protokoll))

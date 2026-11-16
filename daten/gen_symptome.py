"""Symptome ↔ Verdachtsdiagnosen (Symptom-Check).
- Erzeugt daten/symptome-import.json: Symptom-Einträge (Bereich „symptom“) und neue Verdachtsdiagnosen ohne ÄLRD-Vorgabe.
- ergaenze(E) wird von gen_aelrd.py / gen_ergaenzungen.py aufgerufen und ergänzt die vorhandenen Diagnosen
  um das Feld `symptome` und – wo die ÄLRD Bayern keine Symptome nennen – den Abschnitt „Typische Symptome“.
Quellen: ÄLRD Bayern, wo vorhanden; sonst bundesweite/europäische Fachleitlinien bzw. Fachliteratur – je Diagnose gekennzeichnet.
Keine Inhalte aus SAA/BPR anderer Bundesländer (Ausnahme: Hyperglykämie, siehe gen_ergaenzungen.py). Recherche 16.11.2026."""
import json, re, sys

STAND = "2026-11"
NICHT_BY = "nicht ÄLRD Bayern"

# ------------------------------------------------------------------ Symptom-Katalog: (id, Bezeichnung, Kategorie, Synonyme)
KAT = ["Schmerz", "Atmung", "Kreislauf", "Bewusstsein & Neurologie", "Haut & Temperatur", "Magen-Darm & Blutung", "Situation / Anamnese"]
SYM = [
 ("brustschmerz", "Brustschmerz / Engegefühl in der Brust", "Schmerz", ["Thoraxschmerz", "Druck auf der Brust", "Engegefühl"]),
 ("ausstrahlung", "Schmerzausstrahlung in Arm, Hals, Kiefer oder Rücken", "Schmerz", ["Schmerzausstrahlung"]),
 ("reissend", "Plötzlicher, reißender Schmerz in Brust, Rücken oder Bauch", "Schmerz", ["Vernichtungsschmerz", "reißender Schmerz"]),
 ("atemabh-schmerz", "Atemabhängiger Brustschmerz", "Schmerz", ["pleuritischer Schmerz"]),
 ("oberbauch", "Oberbauchschmerz", "Schmerz", ["Oberbauchbeschwerden", "epigastrischer Schmerz"]),
 ("bauchschmerz", "Bauchschmerz", "Schmerz", ["Abdominalschmerz"]),
 ("abwehrspannung", "Harter Bauch / Abwehrspannung", "Schmerz", ["Peritonismus", "brettharter Bauch"]),
 ("rueckenschmerz", "Akuter Rücken- oder Flankenschmerz", "Schmerz", ["Rückenschmerz", "Flankenschmerz"]),
 ("kopfschmerz", "Kopfschmerz", "Schmerz", ["Kopfschmerzen"]),
 ("nackensteife", "Nackensteifigkeit (Meningismus)", "Schmerz", ["Meningismus", "Nackensteifigkeit"]),
 ("atemnot", "Atemnot", "Atmung", ["Dyspnoe", "Luftnot"]),
 ("orthopnoe", "Atemnot im Liegen, Besserung im Sitzen", "Atmung", ["Orthopnoe"]),
 ("tachypnoe", "Schnelle Atmung", "Atmung", ["Tachypnoe"]),
 ("atemdepression", "Langsame oder flache Atmung", "Atmung", ["Atemdepression", "Bradypnoe"]),
 ("keine-atmung", "Keine normale Atmung / Schnappatmung", "Atmung", ["Atemstillstand", "Schnappatmung"]),
 ("stridor", "Pfeifendes Einatemgeräusch (inspiratorischer Stridor)", "Atmung", ["Stridor"]),
 ("giemen", "Giemen / verlängerte Ausatmung", "Atmung", ["Giemen", "Pfeifen beim Ausatmen"]),
 ("bellender-husten", "Bellender Husten / Heiserkeit", "Atmung", ["Krupphusten", "bellender Husten"]),
 ("husten", "Husten", "Atmung", []),
 ("rasseln", "Brodelnde Atmung / Rasselgeräusche / schaumiger Auswurf", "Atmung", ["Rasselgeräusche", "Brodeln"]),
 ("bluthusten", "Bluthusten", "Atmung", ["Hämoptyse", "Hämoptysen"]),
 ("atemgeraeusch-einseitig", "Einseitig abgeschwächtes oder fehlendes Atemgeräusch", "Atmung", ["fehlendes Atemgeräusch"]),
 ("zyanose", "Blaue Lippen / blaue Haut (Zyanose)", "Atmung", ["Zyanose"]),
 ("spo2-niedrig", "Niedrige Sauerstoffsättigung", "Atmung", ["Entsättigung", "niedrige Sättigung"]),
 ("tachykardie", "Schneller Puls", "Kreislauf", ["schneller Puls"]),
 ("bradykardie", "Langsamer Puls", "Kreislauf", ["langsamer Puls"]),
 ("palpitationen", "Herzrasen / Herzstolpern / Herzklopfen", "Kreislauf", ["Palpitationen", "Herzstolpern", "Herzklopfen"]),
 ("schock", "Niedriger Blutdruck / Schockzeichen", "Kreislauf", ["Schock", "Schockzeichen", "niedriger Blutdruck"]),
 ("hypertonie", "Stark erhöhter Blutdruck", "Kreislauf", ["hoher Blutdruck", "Blutdruck hoch"]),
 ("kaltschweissig", "Kalter Schweiß / blasse, kühle Haut", "Kreislauf", ["Kaltschweißigkeit", "kaltschweißig", "Blässe"]),
 ("synkope", "Kurze Bewusstlosigkeit / Kollaps", "Kreislauf", ["Synkope", "Ohnmacht", "Kollaps"]),
 ("pulslos", "Kein tastbarer Puls, leblos", "Kreislauf", ["Pulslosigkeit", "kein Puls"]),
 ("pulsdifferenz", "Puls- oder Blutdruckdifferenz zwischen den Armen / fehlender Puls an einer Extremität", "Kreislauf", ["Pulsdefizit", "Blutdruckdifferenz"]),
 ("halsvenen", "Gestaute Halsvenen", "Kreislauf", ["Halsvenenstauung"]),
 ("beinschwellung", "Einseitige Beinschwellung", "Kreislauf", ["Thrombosezeichen", "geschwollenes Bein"]),
 ("oedeme", "Wassereinlagerungen (Beine, Gesicht)", "Kreislauf", ["Ödeme", "Wasser in den Beinen"]),
 ("pulsierender-bauch", "Pulsierende Schwellung im Bauch", "Kreislauf", ["pulsierender Tumor"]),
 ("bewusstseinsstoerung", "Bewusstseinsstörung bis Bewusstlosigkeit", "Bewusstsein & Neurologie", ["Bewusstlos", "Bewusstlosigkeit", "Vigilanzminderung", "Somnolenz", "Koma"]),
 ("verwirrtheit", "Verwirrtheit / Verhaltensänderung", "Bewusstsein & Neurologie", ["Verwirrtheit", "desorientiert", "Wesensänderung"]),
 ("unruhe", "Angst / Unruhe", "Bewusstsein & Neurologie", ["Angst", "Unruhe", "Agitiertheit"]),
 ("krampfanfall", "Krampfanfall", "Bewusstsein & Neurologie", ["Krampf", "Anfall"]),
 ("laehmung", "Lähmung oder Schwäche einer Körperseite (Arm, Bein)", "Bewusstsein & Neurologie", ["Halbseitenlähmung", "Hemiparese", "Armschwäche"]),
 ("gesicht", "Hängender Mundwinkel / Gesichtslähmung", "Bewusstsein & Neurologie", ["Fazialisparese", "hängender Mundwinkel"]),
 ("sprache", "Sprachstörung / Wortfindungsstörung", "Bewusstsein & Neurologie", ["Sprachstörung", "Aphasie", "verwaschene Sprache"]),
 ("sehstoerung", "Sehstörung / Doppelbilder", "Bewusstsein & Neurologie", ["Sehstörung", "Doppelbilder", "Augenflimmern"]),
 ("blickwendung", "Einseitige Blickwendung", "Bewusstsein & Neurologie", ["Blickdeviation"]),
 ("schwindel", "Schwindel / Gang- und Koordinationsstörung", "Bewusstsein & Neurologie", ["Schwindel", "Gangunsicherheit"]),
 ("taubheit", "Taubheitsgefühl / Kribbeln einer Körperseite", "Bewusstsein & Neurologie", ["Sensibilitätsstörung", "Kribbeln"]),
 ("miosis", "Enge, stecknadelkopfgroße Pupillen", "Bewusstsein & Neurologie", ["Miosis", "enge Pupillen"]),
 ("anisokorie", "Ungleich weite Pupillen / einseitig weite Pupille", "Bewusstsein & Neurologie", ["Anisokorie"]),
 ("zittern", "Zittern", "Bewusstsein & Neurologie", ["Tremor"]),
 ("heisshunger", "Heißhunger", "Bewusstsein & Neurologie", []),
 ("lichtscheu", "Lichtscheu", "Bewusstsein & Neurologie", ["Photophobie"]),
 ("fieber", "Fieber", "Haut & Temperatur", []),
 ("schuettelfrost", "Schüttelfrost", "Haut & Temperatur", []),
 ("unterkuehlt", "Niedrige Körpertemperatur / Kältezittern", "Haut & Temperatur", ["Kältezittern", "Untertemperatur"]),
 ("ueberhitzt", "Sehr hohe Körpertemperatur, heiße Haut", "Haut & Temperatur", ["Hyperthermie", "Überhitzung"]),
 ("schwitzen", "Starkes Schwitzen", "Haut & Temperatur", ["Schweißausbruch", "Schwitzen"]),
 ("quaddeln", "Quaddeln, Juckreiz, Hautrötung", "Haut & Temperatur", ["Urtikaria", "Nesselsucht", "Flush", "Juckreiz"]),
 ("schwellung", "Schwellung von Lippen, Zunge oder Gesicht", "Haut & Temperatur", ["Angioödem", "Quincke-Ödem"]),
 ("petechien", "Punktförmige Hauteinblutungen", "Haut & Temperatur", ["Petechien"]),
 ("exsikkose", "Durst, trockene Schleimhäute, viel Wasserlassen", "Haut & Temperatur", ["Exsikkose", "Polyurie", "Austrocknung"]),
 ("uebelkeit", "Übelkeit / Erbrechen", "Magen-Darm & Blutung", ["Übelkeit", "Erbrechen", "Brechreiz"]),
 ("bluterbrechen", "Bluterbrechen / kaffeesatzartiges Erbrechen", "Magen-Darm & Blutung", ["Hämatemesis", "Kaffeesatzerbrechen"]),
 ("teerstuhl", "Teerstuhl / Blut im Stuhl", "Magen-Darm & Blutung", ["Meläna", "schwarzer Stuhl", "Blut im Stuhl"]),
 ("nasenbluten", "Starkes Nasenbluten", "Magen-Darm & Blutung", []),
 ("blutung-geburt", "Starke vaginale Blutung nach der Geburt", "Magen-Darm & Blutung", ["Blutung nach Geburt"]),
 ("allergen", "Kontakt mit Allergen (Insektenstich, Nahrungsmittel, Medikament)", "Situation / Anamnese", ["Insektenstich", "Bienenstich", "Wespenstich", "Allergie"]),
 ("opioid-hinweis", "Hinweis auf Opioide (z. B. Heroin, Schmerzpflaster, Spritzen)", "Situation / Anamnese", ["Heroin", "Drogen", "Fixer"]),
 ("benzo-hinweis", "Hinweis auf Schlaf- oder Beruhigungsmittel", "Situation / Anamnese", ["Schlaftabletten", "Beruhigungsmittel"]),
 ("diabetes", "Bekannter Diabetes / Insulin", "Situation / Anamnese", ["Diabetiker", "Insulin", "Zucker"]),
 ("infekt", "Hinweis auf Infektion", "Situation / Anamnese", ["Infekt", "Infektion"]),
 ("schwanger", "Schwangerschaft / Wochenbett", "Situation / Anamnese", ["Schwangere", "Wochenbett"]),
 ("trauma", "Unfall / Verletzung", "Situation / Anamnese", ["Unfall", "Verletzung", "Sturz"]),
 ("kopfverletzung", "Kopfverletzung / Sturz auf den Kopf", "Situation / Anamnese", ["Kopfplatzwunde"]),
 ("kaelte", "Kälte- oder Nässeexposition", "Situation / Anamnese", ["Kälte", "Lawine", "Kaltwasser"]),
 ("hitze", "Hitze / Anstrengung bei Hitze", "Situation / Anamnese", ["Hitze", "Sonne"]),
 ("co-quelle", "Brand, Ofen, Heizung, Garage, Shisha – evtl. mehrere Betroffene", "Situation / Anamnese", ["CO-Warner", "Kohlenmonoxid", "Shisha"]),
 ("thromboserisiko", "Immobilisation, Operation oder Thrombose", "Situation / Anamnese", ["Immobilisation", "Thromboserisiko"]),
 ("kleinkind", "Kleinkind", "Situation / Anamnese", []),
 ("lunge-bekannt", "Bekanntes Asthma / COPD", "Situation / Anamnese", ["Asthmatiker"]),
 ("herz-bekannt", "Bekannte Herzschwäche / Herzerkrankung", "Situation / Anamnese", ["Herzschwäche"]),
 ("hypertonie-bekannt", "Bekannter Bluthochdruck", "Situation / Anamnese", []),
 ("aneurysma-bekannt", "Bekanntes Aortenaneurysma", "Situation / Anamnese", []),
 ("antikoagulation", "Einnahme von Blutverdünnern", "Situation / Anamnese", ["Blutverdünner", "Marcumar", "Antikoagulation"]),
]
SYM_ID = {s[0]: s for s in SYM}

# ------------------------------------------------------------------ Quellen
Q = {
 "acs": "ESC-Leitlinie Akutes Koronarsyndrom 2023 (DGK Pocket-Leitlinie), u. a. nach DocCheck Flexikon",
 "le": "ESC-Leitlinie Lungenembolie 2019 (DGK Pocket-Leitlinie / CardioCard 2021)",
 "aorta": "Fachliteratur Akutes Aortensyndrom (u. a. Aortentelefon DHZC, ESC-Leitlinie Aortenerkrankungen)",
 "baa": "Notfallmedizinische Fachliteratur (klassische Trias rupturiertes Bauchaortenaneurysma)",
 "hi": "ESC-Leitlinie Herzinsuffizienz 2021; MSD Manual Lungenödem",
 "men": "DGN-Leitlinie Ambulant erworbene bakterielle Meningoenzephalitis im Erwachsenenalter (2023)",
 "gib": "Notfallmedizinische Fachliteratur obere GI-Blutung (Hämatemesis, Meläna)",
 "hes": "S2k-Leitlinie Hypertensive Erkrankungen in der Schwangerschaft (DGGG), nach Fachliteratur",
 "hypo-t": "ERC-Leitlinien (GRC) / Schweizer Stadieneinteilung akzidentelle Hypothermie, nach Fachliteratur",
 "hitze": "ERC-Leitlinien 2025 (GRC-Algorithmus Hyperthermie)",
 "co": "S2k-Leitlinie Diagnostik und Therapie der Kohlenmonoxidvergiftung (AWMF 040-012)",
 "sht": "S3-Leitlinie Polytrauma/Schwerverletzten-Behandlung (Zeichen der Einklemmung), notfallmedizinische Fachliteratur",
 "ana": "S2k-Leitlinie Akuttherapie und Management der Anaphylaxie 2021 (AWMF 061-025)",
 "erc": "ERC-Leitlinien 2025 (GRC) – Reanimation / Instabilitätszeichen bei Rhythmusstörungen",
 "tox": "Notfallmedizinische Fachliteratur (Toxidrom), u. a. DocCheck Flexikon / AMBOSS",
 "pt": "S3-Leitlinie Polytrauma/Schwerverletzten-Behandlung (Spannungspneumothorax)",
 "allg": "Notfallmedizinische Fachliteratur",
 "by-stroke": "ÄLRD Bayern / RDA: Verdachtsdiagnose Schlaganfall, Version 1.0 (2021), Anhang B",
 "by-hypo": "ÄLRD Bayern: 2c-Algorithmus Hypoglykämie, Checkbox typische klinische Manifestationen (01.11.2025)",
 "by-sepsis": "ÄLRD Bayern: 2c-Algorithmus V. a. Sepsis – Hinweise auf Infektion und vereinfachter NEWS-2 (01.11.2025)",
 "by-hyp": "ÄLRD Bayern / ÄBRD-Stellungnahme: Definition hypertensiver Notfall (08.01.2026)",
 "by-acs": "ÄLRD Bayern / RDA: Verdachtsdiagnose akutes Koronarsyndrom, Version 2.0 (2025)",
}

# ------------------------------------------------------------------ Zuordnung Verdachtsdiagnose → Symptome
# abschnitt=False: Diagnose hat bereits einen Bayern-Abschnitt mit Symptomen (nur Feld `symptome` ergänzen)
Z = {
 # vorhandene Einträge (ÄLRD Bayern / Ergänzungen)
 "acs": dict(s=["brustschmerz", "ausstrahlung", "atemnot", "oberbauch", "kaltschweissig", "schwitzen", "uebelkeit", "unruhe", "palpitationen"], q="acs",
   txt="- Leitsymptom: Brustschmerz / Engegefühl, ggf. mit Ausstrahlung\n- Brustschmerz-Äquivalente: Atemnot, Übelkeit, Oberbauchbeschwerden, ausgeprägte Schwäche – häufig bei Älteren, Diabetikern und Frauen\n- Vegetativ: Angst, Unruhe, Schwitzen, Übelkeit / Erbrechen\n- Ggf. Herzrasen / Herzstolpern",
   by="- ÄLRD-Bayern-Empfehlung ACS: 12-Kanal-EKG ≤ 10 Minuten nach Erstkontakt; Unterscheidung STEMI / NSTE-ACS über das EKG\n- Hochrisikokriterien NSTE-ACS u. a.: hämodynamische Instabilität oder kardiogener Schock, therapierefraktärer infarkttypischer Thoraxschmerz, lebensbedrohliche Arrhythmien oder Herzstillstand, akute Herzinsuffizienz",
   byq="by-acs"),
 "hypoglykaemie": dict(s=["schwitzen", "zittern", "heisshunger", "palpitationen", "verwirrtheit", "sprache", "sehstoerung", "kopfschmerz", "unruhe", "schwindel", "bewusstseinsstoerung", "krampfanfall", "laehmung", "uebelkeit", "diabetes"], q="by-hypo", abschnitt=False),
 "sepsis": dict(s=["fieber", "unterkuehlt", "schuettelfrost", "infekt", "tachypnoe", "spo2-niedrig", "tachykardie", "schock", "verwirrtheit", "husten"], q="by-sepsis", abschnitt=False),
 "hypertensiver-notfall": dict(s=["hypertonie", "atemnot", "brustschmerz", "laehmung", "sprache", "hypertonie-bekannt"], q="by-hyp", abschnitt=False),
 "anaphylaxie": dict(s=["quaddeln", "schwellung", "atemnot", "stridor", "giemen", "schock", "tachykardie", "uebelkeit", "bauchschmerz", "unruhe", "bewusstseinsstoerung", "allergen"], q="ana",
   txt="- Rasches Auftreten (Minuten bis Stunden) nach Allergenkontakt\n- Haut: Juckreiz, Rötung (Flush), Quaddeln, Schwellung (Angioödem)\n- Atemwege: Atemnot, Stridor, Bronchospastik\n- Kreislauf: Tachykardie, Blutdruckabfall bis Schock und Kreislaufstillstand\n- Magen-Darm: Übelkeit, Erbrechen, Bauchschmerzen\n- ZNS: Unruhe, Bewusstseinsstörung\n- Symptome können ein oder mehrere Organsysteme betreffen; erneutes Auftreten innerhalb von 24 Stunden möglich"),
 "kreislaufstillstand": dict(s=["bewusstseinsstoerung", "keine-atmung", "pulslos"], q="erc",
   txt="- Keine Reaktion auf Ansprache und Berührung\n- Keine normale Atmung (Schnappatmung zählt als „nicht normal“)\n- Kein Lebenszeichen / kein tastbarer Puls"),
 "bradykardie": dict(s=["bradykardie", "schock", "synkope", "schwindel", "bewusstseinsstoerung", "kaltschweissig", "brustschmerz"], q="erc",
   txt="- Langsamer Puls\n- Zeichen der Instabilität: Schock / Blutdruckabfall, Synkope, Brustschmerz (Myokardischämie), Herzinsuffizienz\n- Schwindel, Bewusstseinsstörung, kalte blasse Haut"),
 "tachykardie": dict(s=["tachykardie", "palpitationen", "schock", "synkope", "brustschmerz", "atemnot", "schwindel", "bewusstseinsstoerung"], q="erc",
   txt="- Herzrasen, schneller Puls\n- Zeichen der Instabilität: Schock / Blutdruckabfall, Synkope, Brustschmerz (Myokardischämie), Herzinsuffizienz (Atemnot)\n- Schwindel, Bewusstseinsstörung"),
 "status-epilepticus": dict(s=["krampfanfall", "bewusstseinsstoerung", "zyanose"], q="allg",
   txt="- Anhaltender Krampfanfall oder Serie von Anfällen ohne Wiedererlangen des Bewusstseins dazwischen\n- Bewusstseinsstörung, ggf. Zyanose"),
 "pseudokrupp": dict(s=["bellender-husten", "stridor", "atemnot", "unruhe", "kleinkind"], q="allg",
   txt="- Bellender Husten, Heiserkeit\n- Inspiratorischer Stridor, Atemnot\n- Typisch bei Kleinkindern, oft nachts\n- Unruhe; kritisch: Erschöpfung, Zyanose, Bewusstseinsstörung"),
 "bronchospastik": dict(s=["atemnot", "giemen", "husten", "tachypnoe", "zyanose", "spo2-niedrig", "unruhe", "lunge-bekannt"], q="allg",
   txt="- Atemnot, Giemen, verlängerte Ausatmung\n- Husten, schnelle Atmung\n- Niedrige Sauerstoffsättigung, Zyanose\n- Unruhe; kritisch: Erschöpfung, „stille Lunge“, Bewusstseinsstörung\n- Häufig bekanntes Asthma / COPD"),
 "hypotension": dict(s=["schock", "tachykardie", "kaltschweissig", "synkope", "schwindel", "verwirrtheit"], q="allg",
   txt="- Niedriger Blutdruck, schneller Puls\n- Kalte, blasse, schweißige Haut\n- Schwindel, Kollaps, Verwirrtheit"),
 "opiat-intox": dict(s=["bewusstseinsstoerung", "miosis", "atemdepression", "opioid-hinweis", "zyanose"], q="tox",
   txt="- Trias: Bewusstseinsstörung, enge (stecknadelkopfgroße) Pupillen, Atemdepression\n- Die Trias muss nicht vollständig sein; bei längerer Hypoxie können die Pupillen weit werden\n- Hinweise: Spritzen, Injektionsstellen, Schmerzpflaster"),
 "benzo-intox": dict(s=["bewusstseinsstoerung", "atemdepression", "benzo-hinweis", "schwindel"], q="tox",
   txt="- Schläfrigkeit bis Bewusstlosigkeit\n- Atemdepression (v. a. bei Mischintoxikation, z. B. mit Alkohol)\n- Gang- und Koordinationsstörung\n- Hinweise: Tablettenpackungen, Anamnese"),
 "epistaxis": dict(s=["nasenbluten", "antikoagulation", "hypertonie"], q="allg",
   txt="- Starke Blutung aus der Nase, ggf. Blut im Rachen\n- Risiko: Blutverdünner, hoher Blutdruck\n- Bei starkem Blutverlust Schockzeichen"),
 "postpartale-blutung": dict(s=["blutung-geburt", "schwanger", "schock", "tachykardie", "kaltschweissig"], q="allg",
   txt="- Starke vaginale Blutung nach der Geburt\n- Schockzeichen: schneller Puls, Blutdruckabfall, kalte blasse Haut"),
 "abdominalschmerz": dict(s=["bauchschmerz", "abwehrspannung", "oberbauch", "uebelkeit", "fieber"], q="allg",
   txt="- Bauchschmerz, ggf. Abwehrspannung (harter Bauch)\n- Übelkeit, Erbrechen, ggf. Fieber\n- Warnzeichen siehe Ausschlusskriterien (Blut im Stuhl, Bluterbrechen, Aortenaneurysma, Schwangerschaft, Thoraxschmerz)"),
 "spannungspneu": dict(s=["atemnot", "atemgeraeusch-einseitig", "brustschmerz", "tachykardie", "schock", "halsvenen", "zyanose", "spo2-niedrig", "bewusstseinsstoerung", "trauma"], q="pt",
   txt="- Einseitig abgeschwächtes oder fehlendes Atemgeräusch (nach Tubuslagekontrolle) plus typische Symptome\n- Atemnot, Brustschmerz, schneller Puls\n- Gestaute Halsvenen, Blutdruckabfall (eher spät), Zyanose, Bewusstseinsstörung\n- Beim Beatmeten: stark steigende Beatmungsdrücke"),
 "hyperglykaemie": dict(s=["exsikkose", "bewusstseinsstoerung", "verwirrtheit", "diabetes", "infekt"], q="allg", abschnitt=False),
}

# neue Verdachtsdiagnosen (ohne eigene ÄLRD-Bayern-Vorgabe zu Maßnahmen)
NEU = [
 dict(id="schlaganfall", titel="Schlaganfall (Verdacht)", kurz="", such=["Schlaganfall", "Apoplex", "Hirninfarkt", "Stroke Verdacht", "TIA Verdacht"],
   s=["laehmung", "gesicht", "sprache", "sehstoerung", "blickwendung", "schwindel", "taubheit", "kopfschmerz", "bewusstseinsstoerung", "uebelkeit", "antikoagulation"], q="by-stroke", bayern=True,
   txt="- **Leitsymptome (ÄLRD Bayern):** FAST (Gesicht, Arm, Sprache, Zeit) sowie Bewusstseinsstörung, starker Kopfschmerz, akuter Schwindel, Sehstörungen und Blickwendung\n- Neu aufgetretene neurologische Symptome der letzten 24 Stunden – auch vorübergehende\n- Ergänzend: einseitiges Taubheitsgefühl / Kribbeln, einseitige Beinschwäche",
   extra=[("Anamnese (ÄLRD Bayern)", "- Genauer Zeitpunkt des Symptombeginns; plötzlich oder allmählich?\n- Nur vorübergehend? Dauer?\n- Medikamente: Antikoagulantien, Thrombozytenaggregationshemmer, Antiepileptika\n- Frühere Schlaganfälle / TIA; Vorerkrankungen (Epilepsie, Diabetes, kardiovaskulär)\n- Vorangegangene Kopfschmerzen, Übelkeit oder Fieber\n- Angehörige kontaktieren bzw. mit in die Klinik nehmen"),
          ("Untersuchung (ÄLRD Bayern)", "- Gesicht: spontan lächeln lassen, Augen zukneifen\n- Arm: Armvorhalteversuch, Kraft im Seitenvergleich\n- Sprache: Satz nachsprechen, Aufforderung befolgen, Gegenstände benennen\n- Bewusstsein: GCS\n- Schwindel: Nystagmus, unsicherer Gang, Fallneigung\n- Augen: Doppelbilder, Blindheit, Pupillen, Blickwendung, Folgebewegungen")],
   siehe=["Übersicht Stroke Units", "BE-FAST", "GCS"]),
 dict(id="lungenembolie", titel="Lungenembolie (Verdacht)", kurz="", such=["Lungenembolie", "Lungenarterienembolie"],
   s=["atemnot", "tachypnoe", "brustschmerz", "atemabh-schmerz", "synkope", "bluthusten", "husten", "tachykardie", "beinschwellung", "schock", "unruhe", "thromboserisiko"], q="le",
   txt="- Typisch: Atemnot, Brustschmerz (oft atemabhängig), (Prä-)Synkope, Bluthusten\n- Schnelle Atmung, schneller Puls, Angst / Unruhe, Husten\n- Zeichen einer Beinvenenthrombose (einseitige Beinschwellung)\n- Hämodynamische Instabilität möglich\n- CAVE: Beschwerdebild oft unspezifisch, evtl. symptomarm",
   siehe=["LAE", "TVT"]),
 dict(id="aortendissektion", titel="Aortendissektion / akutes Aortensyndrom (Verdacht)", kurz="", such=["Aortendissektion", "Aortensyndrom", "Dissektion"],
   s=["reissend", "brustschmerz", "rueckenschmerz", "bauchschmerz", "pulsdifferenz", "schock", "synkope", "laehmung", "hypertonie-bekannt"], q="aorta",
   txt="- Plötzlicher, sehr starker Schmerz in Brust, Rücken oder Bauch – reißend, stechend oder schneidend\n- Puls- oder Blutdruckdifferenz, fehlende Pulse\n- Blutdruckabfall, Schock, Synkope\n- Neurologisches Defizit zusammen mit dem Schmerzereignis\n- Risiko: Bluthochdruck, bekannte Bindegewebserkrankung"),
 dict(id="rupturiertes-baa", titel="Rupturiertes Bauchaortenaneurysma (Verdacht)", kurz="", such=["Bauchaortenaneurysma", "Aortenaneurysma Ruptur", "BAA", "AAA"],
   s=["bauchschmerz", "rueckenschmerz", "schock", "pulsierender-bauch", "kaltschweissig", "aneurysma-bekannt"], q="baa",
   txt="- Klassische Trias: plötzlicher Bauch- oder Rückenschmerz, Blutdruckabfall / Schock, pulsierende Schwellung im Bauch\n- Die Trias ist oft unvollständig\n- Bekanntes Aneurysma: siehe Ausschlusskriterium im 2c-Algorithmus Abdominalschmerz",
   siehe=["Akuter Abdominalschmerz"]),
 dict(id="lungenoedem", titel="Akute Herzinsuffizienz / Lungenödem (Verdacht)", kurz="", such=["Lungenödem", "Herzinsuffizienz", "kardiales Lungenödem", "Asthma cardiale", "Linksherzinsuffizienz"],
   s=["atemnot", "orthopnoe", "rasseln", "tachypnoe", "giemen", "husten", "zyanose", "spo2-niedrig", "kaltschweissig", "schwitzen", "unruhe", "halsvenen", "oedeme", "herz-bekannt"], q="hi",
   txt="- Schwere Atemnot, Atemnot im Liegen (Besserung im Sitzen)\n- Rasselgeräusche, brodelnde Atmung, ggf. schaumiger, blutig tingierter Auswurf; Giemen möglich („Herzasthma“)\n- Unruhe, Angst, Schwitzen, Blässe, Zyanose\n- Gestaute Halsvenen, Ödeme\n- Häufig bekannte Herzerkrankung"),
 dict(id="meningitis", titel="Meningitis / Meningokokken-Erkrankung (Verdacht)", kurz="", such=["Meningitis", "Hirnhautentzündung", "Meningokokken", "Meningoenzephalitis"],
   s=["kopfschmerz", "fieber", "nackensteife", "bewusstseinsstoerung", "verwirrtheit", "uebelkeit", "lichtscheu", "krampfanfall", "petechien"], q="men",
   txt="- Vier Leitsymptome: Kopfschmerz, Fieber, Nackensteifigkeit, Bewusstseinsstörung\n- Oft fehlen einzelne Leitsymptome – schon bei zwei der vier daran denken\n- Übelkeit, Erbrechen, Lichtscheu, Krampfanfälle\n- Punktförmige Hauteinblutungen (Petechien) als Warnzeichen, v. a. bei Meningokokken",
   by="- 2c-Algorithmus V. a. Sepsis: Meningismus → Notarzt-Nachforderung (unabhängig von einem kritischen ABCDE-Problem)", byq="by-sepsis",
   siehe=["Sepsis (Verdacht)"]),
 dict(id="gi-blutung", titel="Obere gastrointestinale Blutung (Verdacht)", kurz="", such=["GI-Blutung", "Magenblutung", "Ösophagusvarizenblutung", "Bluterbrechen Verdacht"],
   s=["bluterbrechen", "teerstuhl", "schock", "kaltschweissig", "synkope", "oberbauch", "antikoagulation"], q="gib",
   txt="- Bluterbrechen oder kaffeesatzartiges Erbrechen\n- Teerstuhl (schwarzer Stuhl) oder Blut im Stuhl\n- Schockzeichen, Kollaps\n- Risiko: Blutverdünner",
   by="- 2c-Algorithmus Akuter Abdominalschmerz: blutiger Stuhl / Teerstuhl oder blutiges / kaffeesatzartiges Erbrechen sind **Ausschlusskriterien** für die 2c-Analgesie", byq="by-sepsis",
   siehe=["Akuter Abdominalschmerz", "Kritische Hypotension / Volumenmangel"]),
 dict(id="praeeklampsie", titel="Präeklampsie / Eklampsie (Verdacht)", kurz="", such=["Präeklampsie", "Eklampsie", "HELLP", "Schwangerschaftsvergiftung", "Gestose"],
   s=["schwanger", "hypertonie", "kopfschmerz", "sehstoerung", "oberbauch", "atemnot", "oedeme", "krampfanfall", "bewusstseinsstoerung"], q="hes",
   txt="- Erhöhter Blutdruck in der Schwangerschaft (bis ins Wochenbett) mit Organbeteiligung\n- ZNS: Kopfschmerzen, Sehstörungen (Augenflimmern, Gesichtsfeldausfälle)\n- Leber: rechtsbetonte Oberbauchschmerzen\n- Lunge: Atemnot\n- Eklampsie: generalisierter Krampfanfall in Schwangerschaft, Geburt oder Wochenbett, Bewusstseinsstörung",
   siehe=["Status epilepticus / Krampfanfall", "Hypertensiver Notfall / hypertensive Entgleisung"]),
 dict(id="hypothermie", titel="Unterkühlung (akzidentelle Hypothermie)", kurz="", such=["Hypothermie", "Unterkühlung", "unterkühlt"],
   s=["unterkuehlt", "kaelte", "zittern", "verwirrtheit", "bewusstseinsstoerung", "bradykardie", "atemdepression"], q="hypo-t",
   txt="- Körperkerntemperatur unter 35 °C\n- Anfangs Kältezittern, später kein Zittern mehr\n- Zunehmende Verwirrtheit bis Bewusstlosigkeit\n- Langsamer Puls, langsame Atmung, Muskelsteife\n- Blässe, kühle Haut; paradoxes Wärmegefühl (Entkleiden) möglich"),
 dict(id="hitzschlag", titel="Hitzschlag / Hyperthermie", kurz="", such=["Hitzschlag", "Hyperthermie", "Hitzeerschöpfung", "Sonnenstich"],
   s=["ueberhitzt", "hitze", "verwirrtheit", "bewusstseinsstoerung", "krampfanfall", "tachykardie"], q="hitze",
   txt="- Sehr hohe Körpertemperatur (ERC/GRC: Kerntemperatur ≥ 40,5 °C) **und** Verwirrtheit / Desorientierung\n- Bewusstseinsstörung, Krampfanfall möglich\n- Nach Hitze oder körperlicher Anstrengung in Wärme"),
 dict(id="co-intox", titel="Kohlenmonoxid-Vergiftung (Verdacht)", kurz="", such=["Kohlenmonoxidvergiftung", "CO-Vergiftung", "CO Intoxikation", "Rauchgasvergiftung"],
   s=["kopfschmerz", "schwindel", "uebelkeit", "verwirrtheit", "sehstoerung", "bewusstseinsstoerung", "krampfanfall", "brustschmerz", "atemnot", "palpitationen", "co-quelle"], q="co",
   txt="- Erste Anzeichen: Kopfschmerzen, Schwindel, Schwächegefühl, Übelkeit, Erbrechen\n- Schwer: Orientierungs- und Bewusstseinsstörung, Krampfanfall, Brustenge, Atemnot, Herzrhythmusstörungen, Kreislaufversagen\n- Symptome unspezifisch – an CO-Quellen denken (Brand, Heizung, Ofen, Garage, Holzkohlegrill, Shisha), oft mehrere Betroffene\n- Pulsoximetrie ist bei CO-Vergiftung **nicht zuverlässig**",
   by="- ÄLRD-Bayern-Empfehlung „CO-Pulsoximetrie“ (29.11.2023) – Inhalt hier nicht übernommen", byq="by-acs"),
 dict(id="sht", titel="Schädel-Hirn-Trauma", kurz="SHT", such=["Schädel-Hirn-Trauma", "Gehirnerschütterung", "Kopfverletzung"],
   s=["kopfverletzung", "trauma", "bewusstseinsstoerung", "verwirrtheit", "kopfschmerz", "uebelkeit", "anisokorie", "krampfanfall", "laehmung", "antikoagulation"], q="sht",
   txt="- Kopfverletzung oder passender Unfallmechanismus\n- Bewusstseinsstörung (GCS), Verwirrtheit, Erinnerungslücke\n- Kopfschmerz, Übelkeit, Erbrechen\n- Warnzeichen erhöhter Hirndruck / Einklemmung: einseitig weite Pupille, Strecksynergismen, zunehmende Bewusstseinstrübung\n- Krampfanfall, Lähmungen; erhöhtes Blutungsrisiko unter Blutverdünnern",
   siehe=["Schockraum-Indikation (Bayerische Traumanetzwerke)", "GCS", "KRIMP"]),
]

HINWEIS_ALT = "Symptome, Diagnostik und weiterführende Therapie sind in den gültigen Dokumenten der ÄLRD Bayern hierzu nicht beschrieben."
HINWEIS_NEU = ("Diagnostik und weiterführende Therapie sind in den gültigen Dokumenten der ÄLRD Bayern hierzu nicht beschrieben. "
               "Die „Typischen Symptome“ stammen aus Fachleitlinien bzw. Fachliteratur (siehe Quelle) und dienen nur der Einordnung.")

def sym_ids(liste):
    for s in liste: assert s in SYM_ID, f"unbekanntes Symptom {s}"
    return ["sym-" + s for s in liste]

def ergaenze(E):
    """Ergänzt vorhandene Diagnosen (ÄLRD / Ergänzungen) um Symptome."""
    for e in E:
        z = Z.get(e["id"])
        if not z: continue
        e["symptome"] = sym_ids(z["s"])
        if z.get("abschnitt", True):
            titel = "Typische Symptome" + ("" if z["q"].startswith("by-") else f" ({NICHT_BY})")
            neu = [{"titel": titel, "text": z["txt"]}]
            if z.get("by"): neu.append({"titel": "Bayern-Bezug (ÄLRD)", "text": z["by"]})
            e["abschnitte"] = neu + [a for a in e["abschnitte"] if a["titel"] not in (titel, "Bayern-Bezug (ÄLRD)")]
            for a in e["abschnitte"]:
                if a["text"] == HINWEIS_ALT: a["text"] = HINWEIS_NEU
            zusatz = " · Symptome: " + Q[z["q"]] + (" · " + Q[z["byq"]] if z.get("byq") else "")
            if "· Symptome:" not in e.get("quelle", ""): e["quelle"] = (e.get("quelle", "") + zusatz).strip(" ·")
    return E

def norm(s):
    s = (s or "").lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]", "", s)

if __name__ == "__main__":
    # vorhandene Schlüssel und Diagnose-Titel (ohne Abkürzungen – die weichen später aus)
    fremd, diag_titel = {}, {}
    for f in ["aelrd-bayern-import.json", "kliniken-muenchen-import.json", "leitstellen-import.json", "ergaenzungen-import.json"]:
        for e in json.load(open(f, encoding="utf-8"))["eintraege"]:
            if e["bereich"] == "diagnose": diag_titel[e["id"]] = e
            for k in [e.get("kurz"), e.get("titel"), *e.get("suchbegriffe", [])]:
                if norm(k): fremd.setdefault(norm(k), e["titel"])
    for z in Z: assert z in diag_titel, f"Diagnose {z} fehlt"
    aus, protokoll, belegt = [], [], dict(fremd)

    def such_frei(liste, eigen):
        ok = []
        for s in liste:
            n = norm(s)
            if not n or n in belegt: 
                if n in belegt: protokoll.append(f"{eigen}: „{s}“ weggelassen (gehört zu „{belegt[n]}“)")
                continue
            ok.append(s); belegt[n] = eigen
        return ok

    # neue Diagnosen
    for d in NEU:
        titel = d["titel"]
        assert norm(titel) not in belegt, f"Titel belegt: {titel}"
        belegt[norm(titel)] = titel
        if d["kurz"]:
            if norm(d["kurz"]) in fremd: protokoll.append(f"{titel}: Kurzform {d['kurz']} belegt"); d["kurz"] = ""
            else: belegt[norm(d["kurz"])] = titel
        such = such_frei(d["such"], titel)
        abschn = [{"titel": "Typische Symptome" + ("" if d["q"].startswith("by-") else f" ({NICHT_BY})"), "text": d["txt"]}]
        for t, x in d.get("extra", []): abschn.append({"titel": t, "text": x})
        if d.get("by"): abschn.append({"titel": "Bayern-Bezug (ÄLRD)", "text": d["by"]})
        abschn.append({"titel": "Hinweis", "text":
            "Für dieses Krankheitsbild gibt es keine eigene Vorgabe der ÄLRD Bayern zu Maßnahmen oder Medikamenten. "
            "Vorgehen nach xABCDE, Befund und Notarzt; allgemeine § 2a-Maßnahmen und -Medikamente siehe jeweilige Einträge."})
        quellen = [Q[d["q"]]] + ([Q[d["byq"]]] if d.get("byq") and d["byq"] != d["q"] else [])
        aus.append({"id": d["id"], "bereich": "diagnose", "titel": titel, "kurz": d["kurz"], "suchbegriffe": such,
                    "siehe": d.get("siehe", []), "abschnitte": abschn, "symptome": sym_ids(d["s"]),
                    "sprechtext": "", "quelle": " · ".join(quellen), "stand": STAND})
        diag_titel[d["id"]] = aus[-1]

    # Symptom-Einträge – „Mögliche Verdachtsdiagnosen“ aus der Zuordnung berechnet
    zu = {}
    for did, e in diag_titel.items():
        for s in e.get("symptome", []) if did not in Z else sym_ids(Z[did]["s"]):
            zu.setdefault(s, []).append(e["titel"])
    for i, (sid, label, kat, syn) in enumerate(SYM):
        titel = label if norm(label) not in belegt else f"{label} (Symptom)"
        belegt.setdefault(norm(titel), titel)
        diags = sorted(zu.get("sym-" + sid, []))
        such = such_frei(syn, titel)
        aus.append({"id": "sym-" + sid, "bereich": "symptom", "titel": titel, "kurz": "", "kategorie": kat, "reihe": i,
                    "suchbegriffe": such, "siehe": diags,
                    "abschnitte": [{"titel": "Mögliche Verdachtsdiagnosen", "text": "\n".join("- " + t for t in diags) or "– keine Zuordnung –"},
                                   {"titel": "Hinweis", "text": "Hilfe zur Einordnung, keine Diagnose. Im Bereich „Symptome“ mehrere Symptome antippen, um die passenden Verdachtsdiagnosen zu sehen."}],
                    "sprechtext": "", "quelle": "Zusammenstellung aus den Verdachtsdiagnosen der App", "stand": STAND})
    ids = [a["id"] for a in aus]
    assert len(ids) == len(set(ids))
    json.dump({"app": "Wissen RD", "titel": "Import Symptome und weitere Verdachtsdiagnosen",
               "hinweis": "Symptom-Check: Symptome ↔ Verdachtsdiagnosen. Quellen je Diagnose; ÄLRD Bayern, wo vorhanden, sonst Fachleitlinien/Fachliteratur (gekennzeichnet). "
                          "Zuerst aelrd-bayern-import.json und ergaenzungen-import.json neu importieren.",
               "eintraege": aus}, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(sum(a["bereich"] == "diagnose" for a in aus), "neue Diagnosen,", sum(a["bereich"] == "symptom" for a in aus), "Symptome")
    leer = [a["titel"] for a in aus if a["bereich"] == "symptom" and not a["siehe"]]
    if leer: print("Symptome ohne Diagnose:", leer)
    print("\n".join(protokoll))

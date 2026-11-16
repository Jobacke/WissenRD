"""Erzeugt daten/ergaenzungen-import.json – Einträge OHNE Leitlinie des ÄLRD Bayern.
Nur auf ausdrücklichen Wunsch des Nutzers; Inhalt nach Vorgaben anderer Bundesländer, klar gekennzeichnet.
Recherche 16.11.2026."""
import json, sys

E = []
KEINE = "⚠️ Keine Leitlinie des ÄLRD in Bayern"

Q_SAA = ("ÄLRD Baden-Württemberg, Brandenburg, Mecklenburg-Vorpommern, Nordrhein-Westfalen, Sachsen, Sachsen-Anhalt: "
         "Standardarbeitsanweisungen und Behandlungspfade im Rettungsdienst (SAA und BPR 2025), "
         "BPR Hyperglykämie und SAA Vollelektrolytlösung, Stand 30.04.2025")

E.append({
 "id": "hyperglykaemie", "bereich": "diagnose", "titel": "Hyperglykämie", "kurz": "",
 "suchbegriffe": ["Überzuckerung", "Überzucker", "hoher Blutzucker", "Blutzucker hoch", "Coma diabeticum",
                  "Koma diabeticum", "diabetisches Koma", "Ketoazidose", "diabetische Ketoazidose", "hyperglykämisches Koma"],
 "siehe": ["Hypoglykämie", "Sepsis (Verdacht)", "Kritische Hypotension / Volumenmangel",
           "Balancierte Elektrolytlösung (Acetat/Malat)"],
 "abschnitte": [
  {"titel": KEINE, "text":
   "Für die Hyperglykämie gibt es **keine Leitlinie des ÄLRD in Bayern** (keine 2a-Checkliste, kein 2c-Algorithmus, "
   "keine Empfehlung). Der folgende Inhalt stammt aus den gemeinsamen Vorgaben (SAA/BPR 2025) der ÄLRD in "
   "Baden-Württemberg, Brandenburg, Mecklenburg-Vorpommern, Nordrhein-Westfalen, Sachsen und Sachsen-Anhalt und ist "
   "in Bayern **nicht verbindlich**. Vorgehen in Bayern nach Befund bzw. nach Rücksprache mit dem Notarzt."},
  {"titel": "Einstieg / Definition (andere Bundesländer)", "text":
   "- Kritische Blutzuckererhöhung: **Erwachsene > 250 mg/dl**, **Kinder > 200 mg/dl**\n"
   "- zusätzlich Allgemeinsymptome"},
  {"titel": "Symptome", "text":
   "- Allgemeinsymptome\n- ggf. Vigilanzminderung bis Koma diabeticum\n- ggf. Störungen weiterer Vitalfunktionen"},
  {"titel": "Erweiterte spezifische Anamnese", "text":
   "- bekannter Diabetes oder Neumanifestation\n- Infektzeichen\n- Therapieänderungen, Diätfehler\n"
   "- Steroidmedikation (z. B. Kortison)\n- Störung einer Insulinpumpe"},
  {"titel": "Maßnahmen (andere Bundesländer)", "text":
   "- Basismaßnahmen, Körpertemperatur messen\n- i.v.-Zugang\n"
   "- Volumengabe mit Vollelektrolytlösung (SAA VEL, Indikation „kritische Hyperglykämie“): "
   "Patienten über 12 Jahre 500–1.000 ml i.v., Patienten bis 12 Jahre 10 ml/kg KG i.v., Wiederholung möglich\n"
   "- 12-Kanal-EKG\n- weitere Versorgung und Transport\n"
   "- bei Bewusstseinsminderung nach anderen Ursachen suchen"},
  {"titel": "Erläuterungen (andere Bundesländer)", "text":
   "- Die Verträglichkeit einer Hyperglykämie ist individuell sehr unterschiedlich\n"
   "- Häufigste Ursache: bekannter Diabetes; weitere: Erstmanifestation, Therapiefehler, Medikamente (z. B. Kortison), Infekte\n"
   "- Die Therapie ist je nach Ursache (Säure-Basen-Haushalt, Ketoazidose) komplex; Insulin ist präklinisch schlecht praktikabel\n"
   "- Präklinisch daher in der Regel symptomatische Behandlung nach ABCDE und angepasste Volumensubstitution\n"
   "- Bei Bewusstseinseinschränkung weitere Ursachen erwägen"},
  {"titel": "Bayern-Bezug (ÄLRD Bayern, belegt)", "text":
   "- **Balancierte Elektrolytlösung nach § 2a:** Flüssigkeitsersatz bei kritischem Volumenmangel – nach Bedarf "
   "(Indikation ist der Volumenmangel, nicht die Hyperglykämie)\n"
   "- **2c-Algorithmus V. a. Sepsis:** „Blutzucker > 140 mg/dl ohne Diabetes“ zählt als allgemeiner Hinweis auf eine Infektion"},
 ],
 "sprechtext": "Hyperglykämie. Achtung: keine Leitlinie des Ä L R D in Bayern. Nach den Vorgaben anderer Bundesländer: "
               "kritisch ab 250 Milligramm pro Deziliter bei Erwachsenen und ab 200 bei Kindern, mit Allgemeinsymptomen. "
               "Anamnese: bekannter Diabetes oder Neumanifestation, Infekt, Therapieänderung, Diätfehler, Kortison, Insulinpumpe. "
               "Maßnahmen: Basismaßnahmen, Temperatur, i.v.-Zugang, Vollelektrolytlösung, bei über 12 Jahren 500 bis 1000 Milliliter, "
               "bis 12 Jahre 10 Milliliter pro Kilogramm, 12-Kanal-E K G, Transport. Bei Bewusstseinsminderung an andere Ursachen denken. "
               "Insulin ist präklinisch schlecht praktikabel.",
 "quelle": "Keine Leitlinie des ÄLRD in Bayern · Inhalt nach: " + Q_SAA +
           " · Bayern-Bezug: ÄLRD Bayern: Medikamente zur Anwendung nach § 2a NotSanG, Version 1.5 (22.10.2025); "
           "ÄLRD Bayern: Delegationsalgorithmen 2c, V. a. Sepsis (gültig ab 01.11.2025)",
 "stand": "2025-04",
})

if __name__ == "__main__":
    ids = [e["id"] for e in E]
    assert len(ids) == len(set(ids))
    json.dump({"app": "Wissen RD", "titel": "Import Ergänzungen ohne ÄLRD-Bayern-Leitlinie",
               "hinweis": "Ausnahmen auf ausdrücklichen Wunsch: Inhalte nach Vorgaben anderer Bundesländer, in jedem Eintrag als „Keine Leitlinie des ÄLRD in Bayern“ gekennzeichnet.",
               "eintraege": E}, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(E), "Ergänzungs-Einträge")

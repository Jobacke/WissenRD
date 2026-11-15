// Bereiche der Wissensdatenbank.
// Neuer Bereich = neuer Block hier (Schlüssel nur Kleinbuchstaben ohne Umlaute).
// „vorlage“ = Abschnitte, die beim Anlegen eines neuen Eintrags vorgeschlagen werden.
// „telefon: true“ macht Telefonnummern in diesem Bereich antippbar.
export const BEREICHE = {
  diagnose: {
    name: "Verdachtsdiagnosen", icon: "🩺",
    vorlage: ["Leitsymptome", "Typische Symptome", "Diagnostik", "Differenzialdiagnosen",
              "Maßnahmen", "Medikamente", "Zielklinik / Transport", "Merke / Red Flags"]
  },
  symptom: {
    name: "Symptome", icon: "🔎",
    vorlage: ["Beschreibung", "Mögliche Ursachen", "Gezielt fragen / untersuchen", "Red Flags"]
  },
  medikament: {
    name: "Medikamente", icon: "💊",
    vorlage: ["Wirkstoff / Handelsname", "Wirkgruppe", "Indikation", "Kontraindikationen",
              "Dosierung Erwachsene", "Dosierung Kinder", "Applikation", "Nebenwirkungen",
              "Freigabe (NotSan / Arzt)"]
  },
  algorithmus: {
    name: "Algorithmen & SAA", icon: "📋",
    vorlage: ["Indikation", "Ablauf", "Besonderheiten"]
  },
  leitstelle: {
    name: "Leitstellen", icon: "📡", telefon: true,
    vorlage: ["Zuständigkeitsbereich", "Telefon", "Funk / Kanäle", "Besonderheiten"]
  },
  klinik: {
    name: "Kliniken", icon: "🏥", telefon: true,
    vorlage: ["Adresse / Anfahrt", "Fachbereiche", "Zentren / Versorgungsstufe",
              "Anmeldung (Telefon)", "Besonderheiten"]
  },
  abkuerzung: {
    name: "Abkürzungen", icon: "🔤",
    vorlage: ["Bedeutung", "Erklärung"]
  },
  sonstiges: {
    name: "Sonstiges", icon: "📌",
    vorlage: ["Inhalt"]
  }
};

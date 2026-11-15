"""Erzeugt die Kurzbefehle „Wissen“ und „Wissen hören“ als (unsignierte) .shortcut-Dateien."""
import plistlib, uuid, sys

OBJ = "￼"
API_KEY = "AIzaSyD2gljUDG3_u3AThk4c021cVTlrR1EuD_c"
PROJEKT = "wissen-rd"
APP_URL = "https://wissen.vjbackhaus.de/"
KB_VERSION = "1.0"

def U(): return str(uuid.uuid4()).upper()

# ---------- Variablen-Referenzen ----------
def var(name, key=None, dict_coerce=False):
    v = {"Type": "Variable", "VariableName": name}
    agg = []
    if dict_coerce or key:
        agg.append({"Type": "WFCoercionVariableAggrandizement", "CoercionItemClass": "WFDictionaryContentItem"})
    if key:
        agg.append({"Type": "WFDictionaryValueVariableAggrandizement", "DictionaryKey": key})
    if agg: v["Aggrandizements"] = agg
    return v

def out(uid, name):
    return {"Type": "ActionOutput", "OutputUUID": uid, "OutputName": name}

def att(v):  # einzelne Variable als Parameter
    return {"Value": v, "WFSerializationType": "WFTextTokenAttachment"}

def tok(*teile):
    """Textbaustein aus Strings und Variablen. Positionen in UTF-16."""
    s, ranges = "", {}
    for t in teile:
        if isinstance(t, str):
            s += t
        else:
            pos = len(s.encode("utf-16-le")) // 2
            ranges[f"{{{pos}, 1}}"] = t
            s += OBJ
    return {"Value": {"string": s, "attachmentsByRange": ranges}, "WFSerializationType": "WFTextTokenString"}

def bedingung_input(v):
    return {"Type": "Variable", "Variable": att(v)}

A = []
def act(ident, **p):
    A.append({"WFWorkflowActionIdentifier": "is.workflow.actions." + ident, "WFWorkflowActionParameters": p})
    return p

def text(inhalt, uid=None):
    uid = uid or U()
    act("gettext", UUID=uid, WFTextActionText=inhalt if isinstance(inhalt, dict) else tok(inhalt))
    return uid

def setvar(name, v):
    act("setvariable", WFVariableName=name, WFInput=att(v))

def dict_feld(key, value):
    return {"WFItemType": 0, "WFKey": tok(key), "WFValue": value if isinstance(value, dict) else tok(value)}

def wenn_start(g, **p): act("conditional", GroupingIdentifier=g, WFControlFlowMode=0, **p)
def sonst(g): act("conditional", GroupingIdentifier=g, WFControlFlowMode=1)
def wenn_ende(g): act("conditional", GroupingIdentifier=g, WFControlFlowMode=2, UUID=U())

def bauen(vorlesen: bool):
    A.clear()
    name = "Wissen hören" if vorlesen else "Wissen"
    act("comment", WFCommentActionText=f"Wissen RD – Kurzbefehl „{name}“ v{KB_VERSION}\n"
        "Fragt per Siri nach einem Thema und zeigt den passenden Eintrag aus wissen.vjbackhaus.de"
        + (" und liest ihn vor." if vorlesen else "."))

    # --- Teil A: Einstellungen ---
    u = U()
    act("dictionary", UUID=u, WFItems={"Value": {"WFDictionaryFieldValueItems": [
        dict_feld("apiKey", API_KEY), dict_feld("projekt", PROJEKT), dict_feld("url", APP_URL),
        dict_feld("vorlesen", "ja" if vorlesen else "nein")]}, "WFSerializationType": "WFDictionaryFieldValue"})
    setvar("K", out(u, "Wörterbuch"))
    act("comment", WFCommentActionText="Zugangsdaten des Siri-LESEKONTOS (darf nur lesen). Werden beim Import abgefragt.")
    u = text("siri@wissen-rd.app"); setvar("Email", out(u, "Text"))
    u = text("PASSWORT_HIER"); setvar("Passwort", out(u, "Text"))

    # --- Teil B: Frage + Normalisierung (identisch zur App) ---
    u = U()
    act("ask", UUID=u, WFAskActionPrompt="Welches Thema?", WFInputType="Text")
    setvar("Frage", out(u, "Eingabe"))
    u = U(); act("text.changecase", UUID=u, WFCaseType="lowercase", text=tok(var("Frage")))
    vorher = u
    for suche, ersatz, regex in [("ä", "ae", False), ("ö", "oe", False), ("ü", "ue", False),
                                 ("ß", "ss", False), ("[^a-z0-9]", "", True)]:
        u = U()
        act("text.replace", UUID=u, WFInput=tok(out(vorher, "Aktualisierter Text")),
            WFReplaceTextFind=suche, WFReplaceTextReplace=ersatz,
            WFReplaceTextRegularExpression=regex, WFReplaceTextCaseSensitive=False)
        vorher = u
    setvar("Schluessel", out(vorher, "Aktualisierter Text"))

    # --- Teil C: Anmelden ---
    body = text(tok('{"email":"', var("Email"), '","password":"', var("Passwort"), '","returnSecureToken":true}'))
    u = U()
    act("downloadurl", UUID=u,
        WFURL=tok("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=", var("K", "apiKey")),
        WFHTTPMethod="POST", ShowHeaders=True,
        WFHTTPHeaders={"Value": {"WFDictionaryFieldValueItems": [dict_feld("Content-Type", "application/json")]},
                       "WFSerializationType": "WFDictionaryFieldValue"},
        WFHTTPBodyType="File", WFRequestVariable=att(out(body, "Text")))
    t = U()
    act("getvalueforkey", UUID=t, WFInput=att(out(u, "Inhalte der URL")),
        WFDictionaryKey="idToken", WFGetDictionaryValueType="Value")
    setvar("Token", out(t, "Wörterbuchwert"))

    # --- Teil D: Suchen ---
    q = text(tok('{"structuredQuery":{"from":[{"collectionId":"eintraege"}],"where":{"fieldFilter":'
                 '{"field":{"fieldPath":"schluessel"},"op":"ARRAY_CONTAINS","value":{"stringValue":"',
                 var("Schluessel"),
                 '"}}},"select":{"fields":[{"fieldPath":"titel"},{"fieldPath":"markdown"},'
                 '{"fieldPath":"vorlesen"}]},"limit":10}}'))
    u = U()
    act("downloadurl", UUID=u,
        WFURL=tok("https://firestore.googleapis.com/v1/projects/", var("K", "projekt"),
                  "/databases/(default)/documents:runQuery"),
        WFHTTPMethod="POST", ShowHeaders=True,
        WFHTTPHeaders={"Value": {"WFDictionaryFieldValueItems": [
            dict_feld("Authorization", tok("Bearer ", var("Token"))),
            dict_feld("Content-Type", "application/json")]}, "WFSerializationType": "WFDictionaryFieldValue"},
        WFHTTPBodyType="File", WFRequestVariable=att(out(q, "Text")))
    setvar("Antwort", out(u, "Inhalte der URL"))

    # --- Teil E: Titel der Treffer sammeln ---
    g = U()
    act("repeat.each", GroupingIdentifier=g, WFControlFlowMode=0, WFInput=att(var("Antwort")))
    t = U()
    act("getvalueforkey", UUID=t, WFInput=att(var("Repeat Item", dict_coerce=True)),
        WFDictionaryKey="document.fields.titel.stringValue", WFGetDictionaryValueType="Value")
    w = U(); wenn_start(w, WFCondition=100, WFInput=bedingung_input(out(t, "Wörterbuchwert")))
    act("appendvariable", WFVariableName="Titel", WFInput=att(out(t, "Wörterbuchwert")))
    wenn_ende(w)
    act("repeat.each", GroupingIdentifier=g, WFControlFlowMode=2, UUID=U())

    # --- Teil F: Kein Treffer → App-Suche ---
    w = U(); wenn_start(w, WFCondition=101, WFInput=bedingung_input(var("Titel")))
    act("speaktext", WFText=tok("Nichts zu ", var("Frage"), " gefunden. Ich öffne die Suche."), WFSpeakTextWait=True)
    e = U(); act("urlencode", UUID=e, WFInput=tok(var("Frage")), WFEncodeMode="Encode")
    l = U(); act("url", UUID=l, WFURLActionURL=tok(var("K", "url"), "?q=", out(e, "URL-codierter Text")))
    act("openurl", WFInput=att(out(l, "URL")))
    act("exit")
    wenn_ende(w)

    # --- Teil G: Auswahl bei mehreren Treffern ---
    c = U(); act("count", UUID=c, WFCountType="Items", Input=att(var("Titel")))
    w = U(); wenn_start(w, WFCondition=2, WFNumberValue="1", WFInput=bedingung_input(out(c, "Anzahl")))
    x = U(); act("choosefromlist", UUID=x, WFInput=att(var("Titel")), WFChooseFromListActionPrompt="Welcher Eintrag?")
    setvar("Gewaehlt", out(x, "Ausgewähltes Objekt"))
    sonst(w)
    x = U(); act("getitemfromlist", UUID=x, WFInput=att(var("Titel")), WFItemSpecifier="First Item")
    setvar("Gewaehlt", out(x, "Objekt aus Liste"))
    wenn_ende(w)

    # Gewählten Eintrag in der Antwort wiederfinden
    g = U()
    act("repeat.each", GroupingIdentifier=g, WFControlFlowMode=0, WFInput=att(var("Antwort")))
    t = U()
    act("getvalueforkey", UUID=t, WFInput=att(var("Repeat Item", dict_coerce=True)),
        WFDictionaryKey="document.fields.titel.stringValue", WFGetDictionaryValueType="Value")
    w = U(); wenn_start(w, WFCondition=4, WFConditionalActionString=tok(var("Gewaehlt")),
                        WFInput=bedingung_input(out(t, "Wörterbuchwert")))
    setvar("Eintrag", var("Repeat Item"))
    wenn_ende(w)
    act("repeat.each", GroupingIdentifier=g, WFControlFlowMode=2, UUID=U())

    # --- Teil H: Vorlesen (nur „Wissen hören“) und anzeigen ---
    w = U(); wenn_start(w, WFCondition=4, WFConditionalActionString=tok("ja"),
                        WFInput=bedingung_input(var("K", "vorlesen")))
    v = U()
    act("getvalueforkey", UUID=v, WFInput=att(var("Eintrag", dict_coerce=True)),
        WFDictionaryKey="document.fields.vorlesen.stringValue", WFGetDictionaryValueType="Value")
    act("speaktext", WFText=tok(out(v, "Wörterbuchwert")), WFSpeakTextWait=False)
    wenn_ende(w)
    m = U()
    act("getvalueforkey", UUID=m, WFInput=att(var("Eintrag", dict_coerce=True)),
        WFDictionaryKey="document.fields.markdown.stringValue", WFGetDictionaryValueType="Value")
    r = U(); act("getrichtextfrommarkdown", UUID=r, WFInput=att(out(m, "Wörterbuchwert")))
    act("previewdocument", WFInput=att(out(r, "Rich Text aus Markdown")))

    # Index der Text-Aktionen für Import-Fragen
    idx_mail = next(i for i, a in enumerate(A) if a["WFWorkflowActionIdentifier"].endswith("gettext")
                    and a["WFWorkflowActionParameters"]["WFTextActionText"]["Value"]["string"] == "siri@wissen-rd.app")
    idx_pw = next(i for i, a in enumerate(A) if a["WFWorkflowActionIdentifier"].endswith("gettext")
                  and a["WFWorkflowActionParameters"]["WFTextActionText"]["Value"]["string"] == "PASSWORT_HIER")

    return {
        "WFWorkflowClientVersion": "2607.0.2",
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowIcon": {"WFWorkflowIconStartColor": 463140863, "WFWorkflowIconGlyphNumber": 59511},
        "WFWorkflowTypes": [],
        "WFWorkflowInputContentItemClasses": ["WFStringContentItem"],
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowHasShortcutInputVariables": False,
        "WFQuickActionSurfaces": [],
        "WFWorkflowImportQuestions": [
            {"ActionIndex": idx_mail, "Category": "Parameter", "ParameterKey": "WFTextActionText",
             "Text": "E-Mail-Adresse des Siri-Lesekontos (Firebase)", "DefaultValue": "siri@wissen-rd.app"},
            {"ActionIndex": idx_pw, "Category": "Parameter", "ParameterKey": "WFTextActionText",
             "Text": "Passwort des Siri-Lesekontos (Firebase)", "DefaultValue": ""},
        ],
        "WFWorkflowActions": list(A),
    }

if __name__ == "__main__":
    ziel = sys.argv[1]
    for vl, datei in [(False, "Wissen.unsigned.shortcut"), (True, "Wissen hören.unsigned.shortcut")]:
        with open(f"{ziel}/{datei}", "wb") as f:
            plistlib.dump(bauen(vl), f, fmt=plistlib.FMT_BINARY)
        print("erstellt:", datei, len(A), "Aktionen")

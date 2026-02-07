"""Configurazione centrale: scenari, carte fenomeno, template prompt."""

APP_TITLE = "Scenari Futuri: Competitività e AI"
APP_ICON = "🔮"

# ── Scenari (4 tecniche di foresight) ──────────────────────────────────────

SCENARIOS = [
    {
        "id": "backcasting",
        "title": "Backcasting: Le barriere scompaiono",
        "description": (
            "Tecnica: BACKCASTING. Immaginate che tutte le barriere (WEIGHT) identificate "
            "nella mappatura del presente siano scomparse entro il 2035. Nessun ostacolo "
            "burocratico, nessuna carenza di competenze, nessun gap infrastrutturale. "
            "Partendo da questo futuro ideale, ricostruite a ritroso: quali passi sarebbero "
            "stati necessari? Che aspetto ha la competitività delle medie e grandi imprese "
            "italiane? Come hanno sfruttato AI, HPC e tecnologie abilitanti? "
            "Quali regolamentazioni sono state necessarie per raggiungere questo futuro?"
        ),
        "keywords": [
            "backcasting", "futuro ideale", "barriere rimosse",
            "competitività", "imprese italiane", "2035",
        ],
    },
    {
        "id": "trend_analysis",
        "title": "Trend Analysis: Modello EuroHPC federato",
        "description": (
            "Tecnica: TREND ANALYSIS. A livello nazionale e sovranazionale è stata "
            "applicata la seguente raccomandazione: «Occorrerebbe aprire l'EuroHPC a un "
            "modello federato di risorse infrastrutturali che favorisca la cooperazione "
            "tra infrastrutture pubbliche e private per fornire potenza di addestramento "
            "all'IA, sfruttando la capacità congiunta di risorse informatiche pubbliche "
            "e private e aumentando la scala competitiva dell'UE.» "
            "Come impatta questa policy sulla competitività delle medie e grandi imprese "
            "italiane nel 2035?"
        ),
        "keywords": [
            "trend analysis", "EuroHPC", "supercalcolo federato",
            "sovranità digitale", "risorse computazionali", "2035",
        ],
    },
    {
        "id": "scenario_planning",
        "title": "Scenario Planning: Senza regolazione cloud",
        "description": (
            "Tecnica: SCENARIO PLANNING. A livello nazionale viene ignorata la seguente "
            "raccomandazione: «Occorre favorire una regolazione pro-concorrenziale del cloud, "
            "assieme ad una politica industriale di sviluppo di un cloud europeo e di "
            "avanzamento nei modelli di Edge Computing.» "
            "L'indifferenza rispetto a questa policy come impatta la competitività delle "
            "medie e grandi imprese italiane nel 2035? Quali conseguenze può avere?"
        ),
        "keywords": [
            "scenario planning", "cloud", "regolamentazione",
            "hyperscaler", "dipendenza tecnologica", "edge computing", "2035",
        ],
    },
    {
        "id": "cross_impact",
        "title": "Cross Impact: Talenti sì, semplificazione no",
        "description": (
            "Tecnica: CROSS IMPACT ANALYSIS. A livello nazionale viene applicata la policy "
            "di formazione e attrazione dei talenti digitali (percorsi specialistici, incentivi, "
            "rientro dei cervelli). Ma al contempo viene ignorata la semplificazione normativa: "
            "si costruiscono ulteriori sovrastrutture burocratiche che appesantiscono il contesto "
            "regolatorio. L'interazione tra queste due tendenze come impatta la competitività "
            "delle medie e grandi imprese italiane nel 2035?"
        ),
        "keywords": [
            "cross impact", "talenti digitali", "formazione",
            "burocrazia", "semplificazione normativa", "brain drain", "2035",
        ],
    },
]

# ── Carte fenomeno per Mappatura del Presente ──────────────────────────────

CARD_CATEGORIES = {
    "PULL": {
        "label": "PULL (Attrattori / Driver)",
        "description": "Fenomeni che TRAINANO le imprese verso l'adozione dell'AI",
        "color": "#2ecc71",
        "icon": "🧲",
    },
    "PUSH": {
        "label": "PUSH (Facilitatori / Opportunità)",
        "description": "Fenomeni che SPINGONO e facilitano la transizione AI",
        "color": "#3498db",
        "icon": "🚀",
    },
    "WEIGHT": {
        "label": "WEIGHT (Barriere / Pesi)",
        "description": "Fenomeni che FRENANO o ostacolano la transizione AI",
        "color": "#e74c3c",
        "icon": "⚓",
    },
}

PHENOMENON_CARDS = [
    # --- PULL (Driver) ---
    {
        "id": "card_01",
        "title": "Crescita esponenziale della potenza di calcolo",
        "description": (
            "La legge di Moore e i nuovi chip specializzati (GPU, TPU) rendono "
            "l'addestramento di modelli AI sempre più accessibile e veloce, "
            "abbattendo le barriere d'ingresso per le imprese."
        ),
        "suggested_category": "PULL",
    },
    {
        "id": "card_02",
        "title": "Domanda di mercato per prodotti personalizzati",
        "description": (
            "I consumatori richiedono sempre più prodotti e servizi su misura. "
            "L'AI permette la mass customization: produzione industriale con "
            "personalizzazione individuale."
        ),
        "suggested_category": "PULL",
    },
    {
        "id": "card_03",
        "title": "Competizione globale e pressione sui margini",
        "description": (
            "Le imprese italiane competono con player globali che già usano AI "
            "massicciamente. Non adottare AI significa perdere competitività "
            "su costi, qualità e velocità."
        ),
        "suggested_category": "PULL",
    },
    {
        "id": "card_04",
        "title": "Disponibilità di Large Language Model open source",
        "description": (
            "Modelli come Llama, Mistral e altri LLM open-source permettono "
            "anche alle medie imprese di sviluppare soluzioni AI proprietarie "
            "senza dipendere interamente dai big tech."
        ),
        "suggested_category": "PULL",
    },
    {
        "id": "card_05",
        "title": "Eccellenza manifatturiera italiana nel Made in Italy",
        "description": (
            "La tradizione manifatturiera italiana (meccanica, moda, alimentare, "
            "design) rappresenta un patrimonio unico. L'AI può amplificare "
            "questa eccellenza, non sostituirla."
        ),
        "suggested_category": "PULL",
    },
    # --- PUSH (Facilitatori) ---
    {
        "id": "card_06",
        "title": "PNRR e fondi europei per la transizione digitale",
        "description": (
            "Il Piano Nazionale di Ripresa e Resilienza e i fondi Horizon Europe "
            "mettono a disposizione miliardi per la digitalizzazione e l'adozione "
            "dell'AI nelle imprese italiane."
        ),
        "suggested_category": "PUSH",
    },
    {
        "id": "card_07",
        "title": "Ecosistema EuroHPC e supercalcolo europeo",
        "description": (
            "L'infrastruttura EuroHPC (incluso Leonardo al CINECA di Bologna) "
            "offre alle imprese italiane accesso a risorse di supercalcolo "
            "per addestrare modelli AI complessi."
        ),
        "suggested_category": "PUSH",
    },
    {
        "id": "card_08",
        "title": "Cluster tecnologici e distretti dell'innovazione",
        "description": (
            "Competence Center, Digital Innovation Hub e cluster tecnologici "
            "facilitano il trasferimento tecnologico dall'università all'impresa, "
            "abbassando la soglia di adozione dell'AI."
        ),
        "suggested_category": "PUSH",
    },
    {
        "id": "card_09",
        "title": "AI Act europeo come standard globale",
        "description": (
            "La regolamentazione europea sull'AI crea un framework chiaro "
            "che può diventare standard globale, dando alle imprese europee "
            "un vantaggio di compliance first."
        ),
        "suggested_category": "PUSH",
    },
    {
        "id": "card_10",
        "title": "Partnership pubblico-private per la ricerca AI",
        "description": (
            "Programmi come il Partenariato Esteso FAIR (Future AI Research) "
            "collegano università, centri di ricerca e imprese per sviluppare "
            "AI applicata ai bisogni del tessuto produttivo italiano."
        ),
        "suggested_category": "PUSH",
    },
    # --- WEIGHT (Barriere) ---
    {
        "id": "card_11",
        "title": "Carenza di competenze digitali e AI nelle imprese",
        "description": (
            "L'Italia è tra gli ultimi in Europa per competenze digitali della "
            "forza lavoro (DESI Index). Le imprese faticano a trovare data scientist, "
            "ML engineer e AI specialist."
        ),
        "suggested_category": "WEIGHT",
    },
    {
        "id": "card_12",
        "title": "Complessità burocratica e normativa",
        "description": (
            "La burocrazia italiana rallenta l'adozione di nuove tecnologie: "
            "tempi lunghi per autorizzazioni, complessità fiscale, incertezza "
            "normativa sull'uso dei dati e dell'AI."
        ),
        "suggested_category": "WEIGHT",
    },
    {
        "id": "card_13",
        "title": "Tessuto produttivo frammentato (PMI)",
        "description": (
            "Il 95% delle imprese italiane sono micro o piccole. Investire in AI "
            "richiede risorse, competenze e scala che molte PMI non hanno, "
            "creando un divario digitale interno."
        ),
        "suggested_category": "WEIGHT",
    },
    {
        "id": "card_14",
        "title": "Dipendenza da infrastrutture cloud extra-europee",
        "description": (
            "La maggior parte delle imprese italiane usa cloud di provider USA "
            "(AWS, Azure, Google). Questo crea dipendenza tecnologica, rischi "
            "di sovranità dei dati e vulnerabilità geopolitica."
        ),
        "suggested_category": "WEIGHT",
    },
    {
        "id": "card_15",
        "title": "Brain drain: fuga dei talenti digitali italiani",
        "description": (
            "Molti laureati STEM e ricercatori AI italiani emigrano verso "
            "paesi con stipendi più alti e ecosistemi più dinamici. L'Italia "
            "forma talenti che poi vanno a rafforzare la competitività altrui."
        ),
        "suggested_category": "WEIGHT",
    },
]

# ── System Prompt per il Brainstorming Scenari ─────────────────────────────

BRAINSTORMING_SYSTEM_PROMPT = """Sei un facilitatore esperto di strategic foresight e politiche \
dell'innovazione. Stai guidando un gruppo di partecipanti in un workshop sulla competitività \
delle medie e grandi imprese italiane grazie all'AI e alle tecnologie abilitanti.

Il gruppo sta lavorando con la tecnica: "{scenario_title}"
Contesto dello scenario: {scenario_description}

Il tuo compito:
1. Aiutali ad applicare correttamente la tecnica di foresight assegnata
2. Stimola il pensiero critico con domande provocatorie sul futuro al 2035
3. Cita esempi reali di politiche, tecnologie e imprese (EuroHPC, CINECA Leonardo, PNRR, AI Act, GAIA-X, ecc.)
4. Guidali a costruire uno scenario coerente e argomentato
5. Spingi a considerare sia le opportunità che i rischi per il sistema-Italia

Regole:
- Rispondi SEMPRE in italiano
- Sii stimolante e provocatorio ma rigoroso
- Fai domande aperte, non dare risposte pronte
- Mantieni le risposte brevi (max 150 parole) per favorire il dialogo
- Se il gruppo propone un'idea, costruisci su quella invece di cambiarla
- Ricorda loro di collegare l'analisi alla mappatura PULL/PUSH/WEIGHT fatta in precedenza"""

# ── System Prompt per il Feedback sulla Scenario Card ──────────────────────

FEEDBACK_SYSTEM_PROMPT = """Sei un esperto di strategic foresight e competitività industriale. \
Analizza questa Scenario Card creata da un gruppo di partecipanti e fornisci un feedback costruttivo.

Scenario Card:
- Tecnica utilizzata: {technique_name}
- Titolo dello scenario: {scenario_title_custom}
- Descrizione del futuro al 2035: {future_description}
- Impatto sulle imprese italiane: {impact_on_enterprises}
- Fattori chiave identificati: {key_factors}
- Raccomandazioni strategiche: {strategic_recommendations}

Fornisci un feedback strutturato in italiano:
1. PUNTI DI FORZA: cosa hanno colto bene nell'analisi (2-3 punti)
2. DOMANDE APERTE: aspetti da approfondire o angoli non considerati (2-3 domande)
3. SUGGERIMENTI: come rendere lo scenario più rigoroso e le raccomandazioni più concrete (2-3 suggerimenti)

Sii incoraggiante ma rigoroso. Massimo 200 parole totali."""

# ── Template per il Policy Advisor AI (AI Lab) ─────────────────────────────

COACH_SYSTEM_PROMPT_TEMPLATE = """Sei {coach_role}.

CONTESTO:
Stai conducendo una sessione di analisi strategica sullo scenario "{career_role}" \
con un gruppo che sta esplorando la competitività delle imprese italiane nell'era dell'AI.

LA TUA PERSONALITÀ:
- Tono: {tone}
- Stile: {style}

LE TUE CONOSCENZE SPECIFICHE:
{knowledge}

COME CONDUCI LA SESSIONE:
- Fai domande di tipo: {question_types}
- Valuti le proposte del gruppo su: {evaluation_criteria}
- Inizi sempre presentandoti brevemente e spiegando il tuo approccio
- Fai una domanda alla volta
- Dopo ogni risposta del gruppo, reagisci brevemente e approfondisci
- Dopo 4-5 scambi, dai un breve giudizio complessivo sulla qualità dell'analisi

REGOLE:
- Rispondi SEMPRE in italiano
- Mantieni le risposte brevi e incisive (max 100 parole)
- Sii coerente col tuo ruolo e personalità
- Se il gruppo divaga, riportalo al tema dello scenario"""

COACH_ROLES = [
    "il/la Chief Strategy Officer di una media impresa manifatturiera italiana",
    "il/la Direttore/Direttrice di un Competence Center per l'AI e il digitale",
    "un/una Policy Advisor del Ministero delle Imprese e del Made in Italy",
    "il/la CEO di una startup deep-tech italiana che lavora con il supercalcolo",
]

COACH_TONES = [
    ("Formale e professionale", "formale"),
    ("Informale e amichevole", "informale"),
    ("Diretto e sfidante", "sfidante"),
    ("Curioso e incoraggiante", "curioso"),
]

COACH_QUESTION_TYPES = [
    "Di analisi (valutazione critica di trend, dati, evidenze)",
    "Di policy (quali politiche pubbliche servirebbero, quali effetti)",
    "Di strategia aziendale (come un'impresa dovrebbe posizionarsi)",
    "Di scenario (cosa succederebbe se..., quali rischi, quali opportunità)",
]

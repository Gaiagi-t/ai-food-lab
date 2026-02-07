"""Configurazione centrale: scenari, carte fenomeno, template prompt."""

APP_TITLE = "Scenari Futuri: Competitività e AI"
APP_ICON = "🔮"

# ── Scenari (4 tecniche di foresight) ──────────────────────────────────────

SCENARIOS = [
    {
        "id": "backcasting",
        "title": "Backcasting: Il food italiano del futuro",
        "description": (
            "Immaginate che nel 2035 ogni azienda alimentare e ristorante in Italia "
            "usi l'AI senza problemi: menu personalizzati in base alle allergie e "
            "ai gusti di ogni cliente, zero sprechi perche' l'AI prevede esattamente "
            "quanto cibo servira', tracciabilita' totale dal campo alla tavola. "
            "Partendo da questo futuro perfetto, ragionate all'indietro: "
            "cosa e' successo per arrivarci? Quali scelte sono state fatte? "
            "Come funzionano ristoranti e aziende food in questo mondo ideale?"
        ),
        "keywords": [
            "futuro ideale", "zero sprechi", "menu personalizzati",
            "tracciabilita'", "ristoranti", "food italiano", "2035",
        ],
    },
    {
        "id": "trend_analysis",
        "title": "Trend Analysis: AI per creare nuovi cibi",
        "description": (
            "Oggi i supercomputer piu' potenti vengono usati soprattutto "
            "per la ricerca scientifica. Immaginate che nel 2035 le aziende "
            "alimentari li usino per creare nuovi alimenti: simulare ricette, "
            "inventare combinazioni di sapori mai provate, sviluppare proteine "
            "alternative, prevedere quali prodotti piaceranno ai consumatori. "
            "Come cambierebbe il settore food italiano? Chi ne beneficerebbe? "
            "Che fine farebbero le ricette tradizionali?"
        ),
        "keywords": [
            "nuovi alimenti", "ricette AI", "proteine alternative",
            "food design", "sapori", "innovazione alimentare", "2035",
        ],
    },
    {
        "id": "scenario_planning",
        "title": "Scenario Planning: Le nostre ricette su server stranieri",
        "description": (
            "Oggi le aziende food italiane usano piattaforme americane per "
            "tutto: gestire ordini, salvare ricette, analizzare i clienti. "
            "Immaginate che nel 2035 tutti i dati del food italiano "
            "(ricette, fornitori, preferenze dei clienti, segreti industriali) "
            "siano nelle mani di Amazon, Google e Microsoft. "
            "Che conseguenze ha? Un concorrente straniero potrebbe copiare "
            "il Made in Italy alimentare? Quali rischi corrono le aziende?"
        ),
        "keywords": [
            "dati", "ricette", "segreti industriali",
            "Made in Italy", "piattaforme straniere", "food", "2035",
        ],
    },
    {
        "id": "cross_impact",
        "title": "Cross Impact: Chef tecnologici ma troppa burocrazia",
        "description": (
            "Immaginate due cose che succedono insieme nel 2035: "
            "da un lato l'Italia forma tantissimi food technologist che sanno "
            "usare l'AI (corsi ITS, universita', borse di studio). "
            "Dall'altro, la burocrazia peggiora: servono piu' certificazioni, "
            "piu' controlli, piu' tempo per lanciare un nuovo prodotto alimentare. "
            "Cosa succede? I nuovi esperti riescono a innovare o la burocrazia "
            "li blocca? Le aziende food italiane restano competitive?"
        ),
        "keywords": [
            "food technologist", "formazione ITS", "burocrazia",
            "certificazioni", "innovazione alimentare", "2035",
        ],
    },
]

# ── Carte fenomeno per Mappatura del Presente ──────────────────────────────

CARD_CATEGORIES = {
    "PULL": {
        "label": "PULL (Attrae)",
        "description": "Cose che ATTRAGGONO le aziende verso l'AI",
        "color": "#2ecc71",
        "icon": "🧲",
    },
    "PUSH": {
        "label": "PUSH (Spinge)",
        "description": "Cose che AIUTANO le aziende ad adottare l'AI",
        "color": "#3498db",
        "icon": "🚀",
    },
    "WEIGHT": {
        "label": "WEIGHT (Frena)",
        "description": "Cose che FRENANO le aziende nell'adottare l'AI",
        "color": "#e74c3c",
        "icon": "⚓",
    },
}

PHENOMENON_CARDS = [
    # --- PULL (Attrae) ---
    {
        "id": "card_01",
        "title": "Computer e chip sempre piu' potenti",
        "description": (
            "I computer diventano sempre piu' potenti e costano meno. "
            "Oggi anche un'azienda media puo' usare AI che prima "
            "era riservata solo ai giganti della tecnologia."
        ),
        "suggested_category": "PULL",
    },
    {
        "id": "card_02",
        "title": "I clienti vogliono prodotti su misura",
        "description": (
            "Le persone vogliono prodotti personalizzati, non tutti uguali. "
            "L'AI permette alle aziende di offrire personalizzazione "
            "anche producendo grandi quantita'."
        ),
        "suggested_category": "PULL",
    },
    {
        "id": "card_03",
        "title": "La concorrenza mondiale usa gia' l'AI",
        "description": (
            "Le aziende cinesi, americane e tedesche usano gia' l'AI "
            "per produrre meglio e piu' velocemente. Se le aziende "
            "italiane non si adeguano, restano indietro."
        ),
        "suggested_category": "PULL",
    },
    {
        "id": "card_04",
        "title": "AI gratis e open source per tutti",
        "description": (
            "Esistono modelli AI gratuiti e aperti (come Llama o Mistral) "
            "che chiunque puo' scaricare e usare. Non serve piu' "
            "pagare milioni per avere un'AI potente."
        ),
        "suggested_category": "PULL",
    },
    {
        "id": "card_05",
        "title": "Il Made in Italy e' un punto di forza",
        "description": (
            "L'Italia e' famosa per moda, cibo, design e meccanica. "
            "L'AI puo' rendere queste eccellenze ancora piu' competitive, "
            "senza sostituire la creativita' italiana."
        ),
        "suggested_category": "PULL",
    },
    # --- PUSH (Aiuta) ---
    {
        "id": "card_06",
        "title": "Fondi pubblici per il digitale (PNRR)",
        "description": (
            "L'Italia e l'Europa mettono a disposizione miliardi di euro "
            "per aiutare le aziende ad adottare tecnologie digitali e AI. "
            "Ci sono bandi e finanziamenti dedicati."
        ),
        "suggested_category": "PUSH",
    },
    {
        "id": "card_07",
        "title": "Supercomputer europei (come Leonardo a Bologna)",
        "description": (
            "In Europa ci sono supercomputer potentissimi, come Leonardo "
            "a Bologna. Le aziende italiane possono usarli per "
            "addestrare modelli AI che richiedono enorme potenza di calcolo."
        ),
        "suggested_category": "PUSH",
    },
    {
        "id": "card_08",
        "title": "Centri che aiutano le aziende a innovare",
        "description": (
            "Esistono centri specializzati (Competence Center, hub digitali) "
            "che aiutano le aziende a capire come usare l'AI, "
            "collegandole con universita' e ricercatori."
        ),
        "suggested_category": "PUSH",
    },
    {
        "id": "card_09",
        "title": "Regole europee chiare sull'AI (AI Act)",
        "description": (
            "L'Europa ha creato regole chiare su come usare l'AI "
            "in modo sicuro e responsabile. Questo da' certezza "
            "alle aziende e ai consumatori."
        ),
        "suggested_category": "PUSH",
    },
    {
        "id": "card_10",
        "title": "Universita' e aziende che lavorano insieme",
        "description": (
            "Sempre piu' universita' e aziende collaborano su progetti AI. "
            "I risultati della ricerca arrivano piu' velocemente "
            "nelle fabbriche e negli uffici."
        ),
        "suggested_category": "PUSH",
    },
    # --- WEIGHT (Frena) ---
    {
        "id": "card_11",
        "title": "Mancano le persone che sanno usare l'AI",
        "description": (
            "In Italia ci sono pochi esperti di AI e dati. "
            "Le aziende vorrebbero assumerne, ma non li trovano. "
            "Siamo tra gli ultimi in Europa per competenze digitali."
        ),
        "suggested_category": "WEIGHT",
    },
    {
        "id": "card_12",
        "title": "Troppa burocrazia e regole complicate",
        "description": (
            "In Italia servono troppi permessi e documenti per fare "
            "qualsiasi cosa. Questo rallenta le aziende che vogliono "
            "innovare e adottare nuove tecnologie."
        ),
        "suggested_category": "WEIGHT",
    },
    {
        "id": "card_13",
        "title": "Le aziende italiane sono troppo piccole",
        "description": (
            "Il 95% delle aziende italiane e' piccolo o piccolissimo. "
            "Per usare l'AI servono soldi e competenze che le piccole "
            "aziende spesso non hanno."
        ),
        "suggested_category": "WEIGHT",
    },
    {
        "id": "card_14",
        "title": "I nostri dati sono tutti su server americani",
        "description": (
            "Quasi tutte le aziende italiane usano servizi cloud "
            "di Amazon, Google o Microsoft. I nostri dati sono "
            "su server stranieri: e se un giorno li spegnessero?"
        ),
        "suggested_category": "WEIGHT",
    },
    {
        "id": "card_15",
        "title": "I talenti italiani vanno all'estero",
        "description": (
            "Tanti giovani italiani bravi con la tecnologia e l'AI "
            "se ne vanno a lavorare all'estero, dove guadagnano di piu'. "
            "L'Italia li forma ma poi li perde."
        ),
        "suggested_category": "WEIGHT",
    },
]

# ── System Prompt per il Brainstorming Scenari ─────────────────────────────

BRAINSTORMING_SYSTEM_PROMPT = """Sei un facilitatore che guida studenti delle superiori \
in un workshop sull'AI e il futuro delle aziende italiane.

Il gruppo sta lavorando su: "{scenario_title}"
Contesto: {scenario_description}

Il tuo compito:
1. Aiutali a ragionare sullo scenario assegnato con domande semplici e concrete
2. Fai esempi pratici che uno studente puo' capire (aziende note, app che usano, tecnologie quotidiane)
3. Guidali a costruire uno scenario credibile per il 2035
4. Stimolali a pensare sia ai lati positivi che ai rischi
5. Collegati alla mappatura PULL/PUSH/WEIGHT fatta prima

Regole:
- Rispondi SEMPRE in italiano
- Usa un linguaggio semplice e diretto, come parleresti a dei ragazzi di quinta
- Fai domande aperte, non dare risposte pronte
- Risposte brevi (max 120 parole)
- Se propongono un'idea, costruisci su quella"""

# ── System Prompt per il Feedback sulla Scenario Card ──────────────────────

FEEDBACK_SYSTEM_PROMPT = """Sei un insegnante che da' feedback a studenti delle superiori \
sulla loro Scenario Card. Sii incoraggiante ma aiutali a migliorare.

Scenario Card del gruppo:
- Tecnica usata: {technique_name}
- Titolo: {scenario_title_custom}
- Come sara' il futuro nel 2035: {future_description}
- Cosa cambia per le aziende: {impact_on_enterprises}
- Fattori importanti: {key_factors}
- Cosa dovrebbero fare le aziende: {strategic_recommendations}

Dai un feedback in italiano con questo schema:
1. BRAVI! Cosa hanno fatto bene (2-3 punti)
2. CI AVETE PENSATO? Domande per farli riflettere su cose che mancano (2-3 domande)
3. CONSIGLI: come migliorare il lavoro (2-3 suggerimenti concreti)

Usa un linguaggio semplice, adatto a studenti di quinta superiore. Max 200 parole."""

# ── Template per il Policy Advisor AI (AI Lab) ─────────────────────────────

COACH_SYSTEM_PROMPT_TEMPLATE = """Sei {coach_role}.

CONTESTO:
Stai parlando con un gruppo di studenti delle superiori che ha creato lo scenario "{career_role}" \
sul futuro delle aziende italiane e l'AI.

LA TUA PERSONALITA':
- Tono: {tone}
- Stile: {style}

LE TUE CONOSCENZE:
{knowledge}

COME TI COMPORTI:
- Fai domande di tipo: {question_types}
- Valuti le idee del gruppo su: {evaluation_criteria}
- Ti presenti brevemente all'inizio
- Fai una domanda alla volta, semplice e diretta
- Dopo ogni risposta, reagisci e approfondisci
- Dopo 4-5 scambi, dai un giudizio complessivo

REGOLE:
- Rispondi SEMPRE in italiano
- Usa un linguaggio semplice, adatto a studenti
- Risposte brevi (max 100 parole)
- Resta nel tuo ruolo
- Se divagano, riportali sul tema"""

COACH_ROLES = [
    "il/la manager di un'azienda italiana che sta decidendo se investire nell'AI",
    "un/una esperto/a di tecnologia che aiuta le aziende a innovare",
    "un/una imprenditore/imprenditrice che ha fondato una startup di AI in Italia",
    "un/una giornalista esperto/a di tecnologia e innovazione",
]

COACH_TONES = [
    ("Formale e professionale", "formale"),
    ("Informale e amichevole", "informale"),
    ("Diretto e sfidante", "sfidante"),
    ("Curioso e incoraggiante", "curioso"),
]

COACH_QUESTION_TYPES = [
    "Pratiche (come funzionerebbe nella realta'?)",
    "Critiche (siete sicuri? quali prove avete?)",
    "Di scenario (cosa succederebbe se...?)",
    "Creative (avete pensato anche a...?)",
]

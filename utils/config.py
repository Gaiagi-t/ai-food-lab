"""Configurazione centrale: scenari, domande quiz, template prompt."""

APP_TITLE = "🍕 AI Food Innovation Lab"
APP_ICON = "🍕"

# ── Scenari per il Career Designer ──────────────────────────────────────────

SCENARIOS = [
    {
        "id": "precision_agriculture",
        "title": "Agricoltura di Precisione e Sostenibilità",
        "description": (
            "L'agricoltura sta vivendo una rivoluzione tecnologica: droni, sensori IoT, "
            "immagini satellitari e modelli predittivi permettono di ottimizzare irrigazione, "
            "fertilizzazione e raccolti. L'AI analizza dati meteo, suolo e colture per "
            "suggerire interventi mirati, riducendo sprechi e impatto ambientale."
        ),
        "keywords": ["precision farming", "IoT", "droni", "sostenibilità", "dati satellitari"],
    },
    {
        "id": "food_safety",
        "title": "Sicurezza Alimentare e Controllo Qualità con AI",
        "description": (
            "Garantire la sicurezza degli alimenti è una sfida globale. L'AI può analizzare "
            "immagini per rilevare contaminazioni, predire shelf-life, monitorare la catena "
            "del freddo in tempo reale e identificare anomalie nei processi produttivi. "
            "Computer vision e sensori intelligenti stanno trasformando il controllo qualità."
        ),
        "keywords": ["HACCP", "computer vision", "shelf-life", "tracciabilità", "sensori"],
    },
    {
        "id": "personalized_nutrition",
        "title": "Nutrizione Personalizzata e Salute",
        "description": (
            "Ogni persona ha esigenze nutrizionali diverse. L'AI può analizzare dati "
            "genetici, microbioma, stile di vita e preferenze per creare piani alimentari "
            "personalizzati. App intelligenti tracciano l'alimentazione e suggeriscono "
            "modifiche. La nutrogenomica sta aprendo frontiere impensabili."
        ),
        "keywords": ["nutrigenomica", "microbioma", "app salute", "diete personalizzate", "wearable"],
    },
    {
        "id": "smart_supply_chain",
        "title": "Supply Chain Intelligente e Riduzione Spreco Alimentare",
        "description": (
            "Un terzo del cibo prodotto nel mondo viene sprecato. L'AI può prevedere "
            "la domanda, ottimizzare logistica e magazzino, gestire date di scadenza "
            "e suggerire redistribuzione del cibo in eccesso. Blockchain e IoT "
            "garantiscono trasparenza lungo tutta la filiera."
        ),
        "keywords": ["food waste", "logistica", "blockchain", "previsione domanda", "last-mile"],
    },
    {
        "id": "food_innovation",
        "title": "Innovazione di Prodotto Alimentare con AI",
        "description": (
            "L'AI sta rivoluzionando la R&D alimentare: può generare nuove ricette, "
            "prevedere combinazioni di sapori, ottimizzare formulazioni e persino "
            "progettare proteine alternative. Aziende come NotCo usano AI per creare "
            "sostituti vegetali che imitano perfettamente il gusto degli originali."
        ),
        "keywords": ["food design", "proteine alternative", "R&D", "flavour pairing", "novel food"],
    },
]

# ── Domande Quiz "Il Polso della Classe" ────────────────────────────────────

QUIZ_QUESTIONS = [
    {
        "id": "q1",
        "text": "L'AI potrà mai inventare un nuovo piatto stellato Michelin?",
        "myth_bust": (
            "🔍 Nel 2023, il sistema Chef Watson di IBM ha creato ricette "
            "apprezzate da chef professionisti. Però nessun piatto AI ha ancora "
            "ottenuto una stella Michelin: la creatività culinaria richiede "
            "cultura, emozione e contesto che l'AI non possiede... per ora."
        ),
    },
    {
        "id": "q2",
        "text": "Fra 10 anni un agronomo userà più AI o intuito nel suo lavoro?",
        "myth_bust": (
            "🔍 Già oggi il 30% delle grandi aziende agricole usa AI per le decisioni "
            "di campo. Ma l'agronomo resta insostituibile: l'AI fornisce dati, "
            "l'agronomo interpreta il contesto locale, il clima anomalo, "
            "la storia del terreno. È un lavoro di squadra umano-AI."
        ),
    },
    {
        "id": "q3",
        "text": "L'AI può sostituire completamente un tecnologo alimentare?",
        "myth_bust": (
            "🔍 L'AI può ottimizzare formulazioni e predire shelf-life, ma un "
            "tecnologo alimentare fa molto di più: gestisce normative, valuta "
            "rischi, innova con creatività, comunica con fornitori e clienti. "
            "L'AI è uno strumento potentissimo, non un sostituto."
        ),
    },
    {
        "id": "q4",
        "text": "Un algoritmo può davvero capire se un vino è buono?",
        "myth_bust": (
            "🔍 Esistono AI che analizzano composizione chimica e prevedono "
            "punteggi dei critici con l'80% di accuratezza. Ma il gusto è "
            "soggettivo, culturale, emotivo. Un sommelier racconta storie, "
            "crea esperienze, adatta la scelta al momento. L'AI può assistere, "
            "non sostituire il palato umano."
        ),
    },
    {
        "id": "q5",
        "text": "Affideresti a un'AI il controllo qualità di un salumificio?",
        "myth_bust": (
            "🔍 Computer vision e sensori AI già controllano linee di produzione "
            "alimentare in tempo reale, individuando difetti invisibili all'occhio umano. "
            "Ma le decisioni critiche (richiami, blocco produzione) richiedono "
            "giudizio umano, responsabilità legale e buon senso."
        ),
    },
    {
        "id": "q6",
        "text": "L'AI può risolvere il problema dello spreco alimentare globale?",
        "myth_bust": (
            "🔍 App come Too Good To Go e piattaforme AI di previsione domanda "
            "hanno ridotto lo spreco del 30% dove implementate. Ma il problema "
            "è anche politico, culturale e infrastrutturale. L'AI è una parte "
            "della soluzione, non LA soluzione."
        ),
    },
]

# ── System Prompt per il Brainstorming AI ────────────────────────────────────

BRAINSTORMING_SYSTEM_PROMPT = """Sei un facilitatore esperto di innovazione nel settore food-tech. \
Stai guidando un gruppo di studenti di un istituto tecnico informatico in un workshop \
sulle carriere del futuro all'intersezione tra AI e industria alimentare.

Il gruppo sta esplorando lo scenario: "{scenario_title}"
Descrizione dello scenario: {scenario_description}

Il tuo compito:
1. Aiutali a esplorare lo scenario con domande stimolanti e provocatorie
2. Suggerisci trend reali e concreti del settore (cita esempi veri di aziende e tecnologie)
3. Provocali: "Ma un'AI non potrebbe fare anche questo?" per farli riflettere
4. Guidali verso l'ideazione di un ruolo professionale NUOVO che non esiste ancora
5. Sottolinea sempre il valore insostituibile delle competenze umane

Regole:
- Rispondi SEMPRE in italiano
- Sii entusiasta ma realistico
- Fai domande aperte, non dare risposte pronte
- Mantieni le risposte brevi (max 150 parole) per favorire il dialogo
- Se il gruppo propone un'idea, costruisci su quella invece di cambiarla"""

# ── System Prompt per il Feedback sulla Career Card ──────────────────────────

FEEDBACK_SYSTEM_PROMPT = """Sei un esperto di futuro del lavoro e innovazione food-tech. \
Analizza questa career card creata da un gruppo di studenti e fornisci un feedback costruttivo.

Career Card:
- Ruolo: {role_name}
- Descrizione: {description}
- Hard Skills: {hard_skills}
- Soft Skills: {soft_skills}
- AI come alleata: {ai_ally}
- Tocco umano: {human_touch}

Fornisci un feedback strutturato in italiano:
1. 💪 PUNTI DI FORZA: cosa hanno colto bene (2-3 punti)
2. 🤔 DOMANDE APERTE: aspetti da approfondire (2-3 domande)
3. 💡 SUGGERIMENTI: come rendere il profilo ancora più realistico e innovativo (2-3 suggerimenti)

Sii incoraggiante ma onesto. Massimo 200 parole totali."""

# ── Template per il Career Coach (AI Lab) ────────────────────────────────────

COACH_SYSTEM_PROMPT_TEMPLATE = """Sei {coach_role}.

CONTESTO:
Stai conducendo un colloquio per il ruolo di "{career_role}" in un'azienda food-tech del futuro.

LA TUA PERSONALITÀ:
- Tono: {tone}
- Stile: {style}

LE TUE CONOSCENZE SPECIFICHE:
{knowledge}

COME CONDUCI IL COLLOQUIO:
- Fai domande di tipo: {question_types}
- Valuti il candidato su: {evaluation_criteria}
- Inizi sempre presentandoti brevemente e spiegando il ruolo
- Fai una domanda alla volta
- Dopo ogni risposta del candidato, reagisci brevemente e fai la domanda successiva
- Dopo 4-5 domande, dai un breve feedback complessivo al candidato

REGOLE:
- Rispondi SEMPRE in italiano
- Mantieni le risposte brevi e naturali (max 100 parole)
- Sii coerente col tuo ruolo e personalità
- Se il candidato divaga, riportalo gentilmente al tema"""

COACH_ROLES = [
    "il/la Responsabile HR di un'azienda food-tech del 2035",
    "il/la CEO di una startup innovativa nel settore alimentare",
    "il/la Direttore/Direttrice tecnico/a di un laboratorio di R&D alimentare",
    "il/la Head of AI di un grande gruppo della GDO (Grande Distribuzione Organizzata)",
]

COACH_TONES = [
    ("Formale e professionale", "formale"),
    ("Informale e amichevole", "informale"),
    ("Diretto e sfidante", "sfidante"),
    ("Curioso e incoraggiante", "curioso"),
]

COACH_QUESTION_TYPES = [
    "Tecniche (competenze specifiche, strumenti, metodologie)",
    "Motivazionali (perché questo ruolo, passioni, obiettivi)",
    "Situazionali (come gestiresti questa situazione...)",
    "Creative (proponi una soluzione innovativa per...)",
]

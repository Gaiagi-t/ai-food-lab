"""Configurazione centrale: scenari, carte fenomeno, template prompt."""

APP_TITLE = "Food Futures: AI e il Futuro del Cibo"
APP_ICON = "\U0001f355"  # pizza emoji

# ── Scenari (4 tecniche di foresight sul food) ────────────────────────────

SCENARIOS = [
    {
        "id": "backcasting",
        "title": "Backcasting: Zero Waste 2035",
        "description": (
            "E' il 2035. Ogni ristorante, mensa e supermercato in Italia ha raggiunto "
            "lo zero spreco alimentare grazie all'AI. I frigo smart a casa ordinano "
            "da soli prima che il cibo scada. Le app di food delivery prevedono "
            "esattamente quanti piatti servire ogni sera. I menu cambiano in tempo reale "
            "in base a cosa sta per scadere in magazzino. Nessun cibo finisce nella spazzatura. "
            "Partendo da questo futuro perfetto, ragionate all'indietro: "
            "com'e' successo? Quali app, leggi e abitudini hanno reso possibile tutto questo? "
            "Chi ha guadagnato e chi ha perso in questo cambiamento?"
        ),
        "keywords": [
            "zero spreco", "frigo smart", "food delivery",
            "menu dinamici", "sostenibilita'", "Too Good To Go", "2035",
        ],
    },
    {
        "id": "trend_analysis",
        "title": "Trend Analysis: L'invasione delle dark kitchen",
        "description": (
            "Oggi le dark kitchen (ristoranti fantasma, solo delivery) sono gia' centinaia "
            "in Italia. Proiettate questo trend al 2035: e se il 70% dei ristoranti non avesse "
            "piu' una sala? L'AI chef decide i menu analizzando i trend di TikTok. "
            "Robot preparano i piatti. I rider consegnano (o forse droni?). "
            "Mangiare fuori significa solo ordinare da un'app. "
            "Che fine fanno gli chef veri? I camerieri? L'esperienza di andare al ristorante? "
            "In questo mondo, quali nuovi lavori nascerebbero nel food tech?"
        ),
        "keywords": [
            "dark kitchen", "ghost restaurant", "AI chef", "robot cucina",
            "delivery", "automazione", "TikTok food", "2035",
        ],
    },
    {
        "id": "scenario_planning",
        "title": "Scenario Planning: BigTech controlla il cibo italiano",
        "description": (
            "E' il 2035. Amazon, Google e le big tech controllano il food italiano. "
            "Amazon Fresh e' il supermercato numero uno, Google ha comprato le ricette "
            "di migliaia di ristoranti, un'AI americana decide i menu delle mense scolastiche. "
            "Il Made in Italy alimentare esiste ancora, ma i dati, le ricette, i gusti "
            "dei clienti sono tutti su server stranieri. Un algoritmo di San Francisco "
            "decide cosa mangerete a pranzo. "
            "Come si e' arrivati a questo punto? Si poteva evitare? "
            "Cosa puo' fare l'Italia per proteggere il proprio food senza bloccare l'innovazione?"
        ),
        "keywords": [
            "big tech", "Amazon Fresh", "dati alimentari",
            "Made in Italy", "ricette italiane", "privacy", "2035",
        ],
    },
    {
        "id": "cross_impact",
        "title": "Cross Impact: Sostenibilita' + Automazione = ?",
        "description": (
            "Due mega-trend si scontrano nel 2035. Da un lato, la Gen Z "
            "chiede cibo sostenibile, km zero, packaging biodegradabile, zero emissioni. "
            "Dall'altro, l'automazione avanza: robot in cucina, AI che gestisce le scorte, "
            "droni che consegnano, vertical farm automatiche in citta'. "
            "Queste due forze si aiutano o si ostacolano? L'automazione rende il food "
            "piu' sostenibile (meno sprechi, piu' efficienza) o lo peggiora "
            "(piu' energia, piu' plastica per il delivery, meno contatto con la terra)? "
            "Costruite uno scenario dove questi due trend si incontrano. Chi vince?"
        ),
        "keywords": [
            "sostenibilita'", "Gen Z", "km zero", "automazione",
            "vertical farm", "delivery droni", "packaging", "2035",
        ],
    },
]

# ── Carte fenomeno per Mappatura del Presente ──────────────────────────────

CARD_CATEGORIES = {
    "MI_PIACE": {
        "label": "Mi piace",
        "description": "Questo fenomeno mi piace, lo trovo positivo",
        "color": "#2ecc71",
        "icon": "\U0001f44d",
    },
    "NON_MI_PIACE": {
        "label": "Non mi piace",
        "description": "Questo fenomeno non mi piace, mi preoccupa",
        "color": "#e74c3c",
        "icon": "\U0001f44e",
    },
}

PHENOMENON_CARDS = [
    # --- MI_PIACE ---
    {
        "id": "card_01",
        "emoji": "\U0001f3af",
        "title": "L'algoritmo sa cosa vuoi mangiare",
        "short_description": "Glovo e JustEat ti suggeriscono piatti scelti dall'AI",
        "description": (
            "Apri Glovo o JustEat e i primi piatti che vedi sono scelti dall'AI "
            "in base a quello che hai ordinato prima. Funziona: il 40% degli ordini "
            "arriva dai suggerimenti. Se l'AI ti conosce, il ristorante vende di piu'."
        ),
        "suggested_category": "MI_PIACE",
    },
    {
        "id": "card_02",
        "emoji": "\U0001f4f1",
        "title": "TikTok decide cosa mangiamo",
        "short_description": "Un video virale puo' far esplodere le vendite di un prodotto",
        "description": (
            "L'algoritmo di TikTok ha reso virali il Dubai chocolate, la baked feta pasta "
            "e i pancake giapponesi. Un video da 10 milioni di views puo' far esplodere "
            "le vendite di un prodotto in tutto il mondo, da un giorno all'altro."
        ),
        "suggested_category": "MI_PIACE",
    },
    {
        "id": "card_03",
        "emoji": "\U0001f9ea",
        "title": "Ricette create dall'intelligenza artificiale",
        "short_description": "L'AI inventa nuovi cibi analizzando migliaia di combinazioni",
        "description": (
            "Aziende come NotCo usano l'AI per inventare nuovi cibi analizzando "
            "migliaia di combinazioni di ingredienti. L'AI puo' creare una maionese "
            "vegetale che ha lo stesso sapore di quella classica. Addio trial and error."
        ),
        "suggested_category": "MI_PIACE",
    },
    {
        "id": "card_04",
        "emoji": "\U0001f957",
        "title": "Nutrizione personalizzata con l'AI",
        "short_description": "App che analizzano il TUO corpo e ti dicono cosa mangiare",
        "description": (
            "App come Zoe e Noom analizzano il tuo microbioma e il tuo metabolismo "
            "per dirti cosa dovresti mangiare TU, non una dieta generica uguale per tutti. "
            "Il cibo diventa una cosa personale come la playlist di Spotify."
        ),
        "suggested_category": "MI_PIACE",
    },
    {
        "id": "card_05",
        "emoji": "\U0001f52c",
        "title": "La carne che non viene dagli animali",
        "short_description": "Beyond Meat, Impossible Foods e la carne coltivata in lab",
        "description": (
            "Beyond Meat, Impossible Foods e la carne coltivata in laboratorio. "
            "L'AI accelera lo sviluppo di proteine alternative che hanno il gusto "
            "della carne ma senza allevamenti. Un mercato che vale gia' 8 miliardi."
        ),
        "suggested_category": "MI_PIACE",
    },
    # --- MI_PIACE (continua) ---
    {
        "id": "card_06",
        "emoji": "\U0001f916",
        "title": "ChatGPT in cucina: l'AI e' gratis per tutti",
        "short_description": "Qualsiasi ristorante puo' usare l'AI per menu, food cost, recensioni",
        "description": (
            "Oggi qualsiasi ristorante o piccola azienda food puo' usare ChatGPT "
            "per scrivere menu, tradurre in 10 lingue, calcolare food cost, gestire "
            "le recensioni. Strumenti AI potenti e gratuiti che prima non esistevano."
        ),
        "suggested_category": "MI_PIACE",
    },
    {
        "id": "card_07",
        "emoji": "\U0001f331",
        "title": "Vertical farm e agricoltura di precisione",
        "short_description": "Serre in citta' gestite dall'AI: -80% acqua, +produzione",
        "description": (
            "Sensori, droni e AI controllano campi e serre verticali in citta'. "
            "Si usa fino all'80% di acqua in meno. Aziende come Planeta Farms "
            "a Milano coltivano insalata in capannoni con l'AI che regola tutto."
        ),
        "suggested_category": "MI_PIACE",
    },
    {
        "id": "card_08",
        "emoji": "\U0001f4f2",
        "title": "QR code e blockchain: sai cosa mangi davvero",
        "short_description": "Scansioni e vedi tutto: dal campo alla tavola, senza trucchi",
        "description": (
            "Scansioni il QR sulla confezione e vedi tutto: da quale campo viene "
            "il pomodoro, chi l'ha raccolto, come e' stato trasportato. La blockchain "
            "rende impossibile barare. Il Made in Italy diventa verificabile al 100%."
        ),
        "suggested_category": "MI_PIACE",
    },
    {
        "id": "card_09",
        "emoji": "\U0001f47b",
        "title": "Dark kitchen e ghost restaurant",
        "short_description": "Ristoranti senza sala, solo delivery: costano poco e l'AI gestisce tutto",
        "description": (
            "Ristoranti che esistono solo su Deliveroo, senza sala, senza camerieri. "
            "L'AI gestisce gli ordini, ottimizza i tempi di cottura e prevede la domanda. "
            "Costano poco da aprire. In Italia sono gia' centinaia."
        ),
        "suggested_category": "MI_PIACE",
    },
    {
        "id": "card_10",
        "emoji": "\U0001f393",
        "title": "Nuovi lavori: il food technologist",
        "short_description": "Una professione che non esisteva 10 anni fa, oggi richiestissima",
        "description": (
            "Il food technologist unisce competenze di cibo e tecnologia: "
            "una figura che non esisteva 10 anni fa e che oggi le aziende cercano "
            "disperatamente. Sa di AI, dati, e capisce il settore alimentare."
        ),
        "suggested_category": "MI_PIACE",
    },
    # --- NON_MI_PIACE ---
    {
        "id": "card_11",
        "emoji": "\U0001f441\ufe0f",
        "title": "Le app sanno tutto di quello che mangi",
        "short_description": "Ogni ordine, ogni ricerca, ogni allergia: i tuoi dati alimentari in mano ad altri",
        "description": (
            "Ogni volta che ordini su Glovo, usi Yuka o cerchi ricette online, "
            "le aziende tech raccolgono dati su di te. Sanno le tue allergie, "
            "le tue abitudini, i tuoi orari. Chi controlla questi dati ha un potere enorme."
        ),
        "suggested_category": "NON_MI_PIACE",
    },
    {
        "id": "card_12",
        "emoji": "\U0001f6f5",
        "title": "I rider e il lato oscuro del delivery",
        "short_description": "L'algoritmo decide tutto, i rider hanno poche tutele",
        "description": (
            "L'AI ottimizza le consegne ma chi fa le consegne? Rider pagati "
            "a cottimo, senza tutele, guidati da un algoritmo che decide tutto. "
            "Piu' la tecnologia avanza, piu' il lavoro umano rischia di valere meno."
        ),
        "suggested_category": "NON_MI_PIACE",
    },
    {
        "id": "card_13",
        "emoji": "\U0001f3ea",
        "title": "Piccoli ristoranti schiacciati dalle piattaforme",
        "short_description": "Commissioni del 20-35%: o ci stai o sei fuori",
        "description": (
            "Le piattaforme di delivery prendono commissioni del 20-35% su ogni ordine. "
            "Un piccolo ristorante o non ci sta, o perde soldi. Il potere si sposta "
            "verso chi controlla la tecnologia e i dati, non verso chi cucina."
        ),
        "suggested_category": "NON_MI_PIACE",
    },
    {
        "id": "card_14",
        "emoji": "\U0001f5d1\ufe0f",
        "title": "Sprechiamo ancora un terzo del cibo",
        "short_description": "Nonostante la tech, buttiamo ancora il 30% del cibo prodotto",
        "description": (
            "Nonostante la tecnologia, buttiamo ancora il 30% del cibo prodotto. "
            "App come Too Good To Go aiutano, ma il problema e' strutturale. "
            "Servira' davvero l'AI per risolverlo, o servono scelte diverse?"
        ),
        "suggested_category": "NON_MI_PIACE",
    },
    {
        "id": "card_15",
        "emoji": "\U0001f475",
        "title": "La nonna non si fida dell'AI",
        "short_description": "In Italia il cibo e' tradizione: molti non vogliono che l'AI ci metta le mani",
        "description": (
            "In Italia il cibo e' tradizione, famiglia, territorio. Molti pensano "
            "che l'AI rovini l'autenticita' del food italiano. 'La carbonara la fa "
            "la nonna, non un robot.' Questa resistenza culturale frena l'innovazione."
        ),
        "suggested_category": "NON_MI_PIACE",
    },
]

# ── System Prompt per il Brainstorming Scenari ─────────────────────────────

BRAINSTORMING_SYSTEM_PROMPT = """Sei un facilitatore che guida studenti delle superiori \
in un workshop di orientamento al mondo del food tech e dell'AI.

Il gruppo sta lavorando su: "{scenario_title}"
Contesto: {scenario_description}

Il tuo compito:
1. Aiutali a ragionare sullo scenario con domande semplici e concrete
2. Fai esempi che conoscono: app di delivery, TikTok food, brand come Beyond Meat, Too Good To Go
3. Guidali a costruire uno scenario credibile per il 2035
4. Stimolali a pensare sia ai lati positivi che ai rischi
5. Ogni tanto collega il food al quadro piu' ampio: "Questo succede nel food, ma l'AI sta facendo la stessa cosa in medicina, gaming, musica... Quali competenze servirebbero?"
6. Collegati alla mappatura "mi piace / non mi piace" fatta prima

Regole:
- Rispondi SEMPRE in italiano
- Linguaggio diretto e concreto, come parleresti a ragazzi di quinta superiore
- Fai domande aperte, non dare risposte pronte
- Risposte brevi (max 120 parole)
- Se propongono un'idea, costruisci su quella"""

# ── System Prompt per il Feedback sulla Scenario Card ──────────────────────

FEEDBACK_SYSTEM_PROMPT = """Sei un facilitatore che da' feedback a studenti delle superiori \
sulla loro Scenario Card in un workshop di orientamento al food tech. \
Sii incoraggiante ma aiutali a migliorare.

Scenario Card del gruppo:
- Tecnica usata: {technique_name}
- Titolo: {scenario_title_custom}
- Come sara' il mondo del cibo nel 2035: {future_description}
- Cosa cambia per chi lavora nel food: {impact_on_enterprises}
- Fattori importanti: {key_factors}
- Cosa dovrebbe fare chi lavora nel food: {strategic_recommendations}
- Nuovi lavori e competenze che nascono: {new_jobs_and_skills}
- Cosa c'entra con il loro futuro: {career_reflection}

Dai un feedback in italiano con questo schema:
1. BRAVI! Cosa hanno fatto bene (2-3 punti)
2. CI AVETE PENSATO? Domande per farli riflettere su cose che mancano (2-3 domande)
3. CONSIGLI: come migliorare il lavoro (2-3 suggerimenti concreti)
4. E VOI? Collega il loro scenario alle competenze del futuro: quali abilita' sarebbero utili? Cosa dovrebbero imparare? (2 spunti)

Linguaggio semplice, adatto a ragazzi di quinta superiore. Max 250 parole."""

# ── Template per l'Assistente AI (AI Lab) ─────────────────────────────────

COACH_SYSTEM_PROMPT_TEMPLATE = """Sei {coach_role}.

CONTESTO:
Stai parlando con un gruppo di studenti delle superiori che ha creato lo scenario "{career_role}" \
sul futuro del cibo e dell'AI, in un workshop di orientamento al food tech.

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
- Se divagano, riportali sul tema
- Dopo 2-3 scambi, chiedi: "E voi? Quali competenze di quelle che avete visto vi sembrano piu' utili per il vostro futuro, anche fuori dal food?\""""

COACH_ROLES = [
    {
        "emoji": "\U0001f4f1",
        "label": "Food influencer",
        "full": (
            "un food influencer da 2 milioni di follower che recensisce ristoranti "
            "AI-powered e robot chef su TikTok e Instagram. Parli come un creator: "
            "diretto, entusiasta, con qualche termine inglese, e sai tutto di trend food virali"
        ),
    },
    {
        "emoji": "\U0001f469\u200d\U0001f373",
        "label": "Chef stellata AI-curious",
        "full": (
            "una chef stellata che ha iniziato a usare l'AI per creare piatti innovativi "
            "nel suo ristorante. Sei scettica ma curiosa: credi nella creativita' umana "
            "ma riconosci che l'AI ti ha aiutata a scoprire combinazioni di sapori impossibili"
        ),
    },
    {
        "emoji": "\u267b\ufe0f",
        "label": "Attivista anti-spreco",
        "full": (
            "un attivista per la sostenibilita' alimentare che usa la tecnologia per combattere "
            "lo spreco di cibo. Hai fondato un'app tipo Too Good To Go e usi l'AI per prevedere "
            "gli sprechi. Sei appassionato e a volte un po' polemico contro le big tech"
        ),
    },
    {
        "emoji": "\U0001f680",
        "label": "Startup founder food tech",
        "full": (
            "una startup founder ventiseienne che ha creato un'app di food tech in Italia. "
            "Hai raccolto fondi, assunto un team, e sai cosa significa fare innovazione nel food "
            "partendo da zero. Parli ai ragazzi come una che ci e' passata da poco"
        ),
    },
]

COACH_TONES = [
    ("\U0001f3a9 Formale e professionale", "formale"),
    ("\U0001f60e Informale e amichevole", "informale"),
    ("\u26a1 Diretto e sfidante", "sfidante"),
    ("\U0001f50d Curioso e incoraggiante", "curioso"),
]

COACH_QUESTION_TYPES = [
    "Pratiche (come funzionerebbe nella realta'?)",
    "Critiche (siete sicuri? quali prove avete?)",
    "Di scenario (cosa succederebbe se...?)",
    "Creative (avete pensato anche a...?)",
]

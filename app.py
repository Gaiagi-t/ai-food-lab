"""Food Futures: AI e il Futuro del Cibo - Home Page.

Pagina principale dell'app: selezione del gruppo, istruzioni e pannello admin.
"""

import streamlit as st
from utils.shared_state import get_shared_state
from utils.styles import inject_custom_css, render_phase_bar
from utils.config import APP_TITLE, APP_ICON, SCENARIOS
import random

st.set_page_config(
    page_title="Food Futures: AI e il Futuro del Cibo",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
state = get_shared_state()

# ── Sidebar: selezione gruppo ────────────────────────────────────────────────

with st.sidebar:
    st.header("Il tuo gruppo")

    if "group_name" not in st.session_state:
        st.session_state.group_name = None

    if st.session_state.group_name:
        st.success(f"**Gruppo:** {st.session_state.group_name}")
        group_data = state.get_group(st.session_state.group_name)
        if group_data:
            st.info(f"**Scenario:** {group_data['scenario']['title']}")
        if st.button("Cambia gruppo", use_container_width=True):
            st.session_state.group_name = None
            st.rerun()
    else:
        st.info("Registra il tuo gruppo per iniziare il workshop.")

        existing = state.get_group_names()
        if existing:
            st.caption(f"Gruppi gia' registrati: {', '.join(existing)}")

        with st.form("register_group"):
            group_name = st.text_input(
                "Nome del gruppo",
                placeholder="Es: Team Sushi, I Futuristi, Pizza Crew...",
            )
            join_existing = st.selectbox(
                "...oppure unisciti a un gruppo esistente",
                options=["— Crea nuovo —"] + existing,
            )
            submitted = st.form_submit_button(
                "Entra nel workshop", use_container_width=True
            )

            if submitted:
                if join_existing != "— Crea nuovo —":
                    st.session_state.group_name = join_existing
                    st.rerun()
                elif group_name.strip():
                    used_scenarios = {
                        g["scenario"]["id"]
                        for g in state.get_all_groups().values()
                    }
                    available = [
                        s for s in SCENARIOS if s["id"] not in used_scenarios
                    ]
                    if not available:
                        available = SCENARIOS
                    scenario = random.choice(available)

                    if state.register_group(group_name.strip(), scenario):
                        st.session_state.group_name = group_name.strip()
                        st.rerun()
                    else:
                        st.error("Questo nome e' gia' stato preso!")
                else:
                    st.warning("Inserisci un nome per il gruppo.")

    st.divider()
    st.caption("Food Futures v2.0")

# ── Hero section ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-section">
    <span class="hero-emoji">🍕🤖🔬</span>
    <h1>Food Futures: AI e il Futuro del Cibo</h1>
    <p class="hero-subtitle">
        Scopri come l'AI sta cambiando il mondo del lavoro — partendo dal cibo
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
> **L'AI sta cambiando tutto: il cibo, il lavoro, la scienza, la creativita'.**

In questo workshop userete il **mondo del food** come caso studio per capire
come funziona l'AI, cosa sa fare davvero e cosa no, e come sta cambiando
le professioni e il modo di lavorare. Immaginerete scenari futuri
e costruirete il vostro assistente AI.
""")

# Phase bar
render_phase_bar(0)

# Step cards visive
STEPS = [
    ("1", "🗺️", "Mappatura", "45 min", "Cosa attrae, aiuta o frena il food nell'usare l'AI?"),
    ("2", "🔮", "Scenari 2035", "50 min", "Immagina il mondo del cibo tra 10 anni"),
    ("3", "🤖", "AI Lab", "40 min", "Crea il tuo assistente AI e mettilo alla prova"),
    ("4", "🏆", "Showcase", "20 min", "Presenta, vota e rifletti su AI e futuro"),
]

cols = st.columns(4)
for col, (num, emoji, title, time, desc) in zip(cols, STEPS):
    with col:
        st.markdown(f"""
        <div class="step-card">
            <span class="step-num">{num}</span>
            <span class="step-emoji">{emoji}</span>
            <h4>{title}</h4>
            <span class="step-time">{time}</span>
            <p class="step-desc">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Status dei gruppi
st.divider()
groups = state.get_all_groups()
if groups:
    st.subheader(f"Gruppi registrati: {len(groups)}")
    cols = st.columns(min(len(groups), 5))
    for i, (name, data) in enumerate(groups.items()):
        with cols[i % len(cols)]:
            has_card = data.get("scenario_card") is not None
            has_advisor = data.get("coach_system_prompt") is not None
            status = ""
            if has_advisor:
                status = "Assistente AI pronto"
            elif has_card:
                status = "Scenario card completata"
            else:
                status = "In mappatura..."
            st.metric(name, data["scenario"]["title"], status)
else:
    st.info("Nessun gruppo registrato ancora. Usa la sidebar per creare il tuo gruppo!")

# ── Pannello Admin (nascosto) ────────────────────────────────────────────────

with st.expander("Pannello Facilitatore", expanded=False):
    pwd = st.text_input("Password", type="password", key="admin_pwd")
    if pwd == st.secrets.get("ADMIN_PASSWORD", "workshop2025"):
        st.success("Accesso facilitatore attivo")

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Gruppi", len(groups))
            st.metric("Risposte mappatura", len(state.get_quiz_responses()))
        with col_b:
            st.metric("Voti ricevuti", len(state.get_all_votes()))

        if st.button("RESET COMPLETO", type="primary"):
            state.reset_all()
            st.success("Tutti i dati sono stati cancellati.")
            st.rerun()
    elif pwd:
        st.error("Password errata.")

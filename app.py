"""AI Food Innovation Lab - Home Page.

Pagina principale dell'app: selezione del gruppo, istruzioni e pannello admin.
"""

import streamlit as st
from utils.shared_state import get_shared_state
from utils.config import APP_TITLE, APP_ICON, SCENARIOS
import random

st.set_page_config(
    page_title="AI Food Innovation Lab",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

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
            st.caption(f"Gruppi già registrati: {', '.join(existing)}")

        with st.form("register_group"):
            group_name = st.text_input(
                "Nome del gruppo",
                placeholder="Es: Team Rocket, I Carbonara...",
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
                    # Assegna uno scenario casuale tra quelli non ancora assegnati
                    used_scenarios = {
                        g["scenario"]["id"]
                        for g in state.get_all_groups().values()
                    }
                    available = [
                        s for s in SCENARIOS if s["id"] not in used_scenarios
                    ]
                    if not available:
                        available = SCENARIOS  # fallback: riusa gli scenari
                    scenario = random.choice(available)

                    if state.register_group(group_name.strip(), scenario):
                        st.session_state.group_name = group_name.strip()
                        st.rerun()
                    else:
                        st.error("Questo nome è già stato preso!")
                else:
                    st.warning("Inserisci un nome per il gruppo.")

    st.divider()
    st.caption("AI Food Innovation Lab v1.0")

# ── Pagina principale ────────────────────────────────────────────────────────

st.title(APP_TITLE)
st.markdown("### Workshop Modulo 3 — ITS Tech & Food")

st.markdown("""
> **Che cos'è davvero l'Intelligenza Artificiale e qual è l'impatto possibile sulle carriere future?**

Benvenuti nel laboratorio interattivo! In questo workshop esplorerete come l'AI sta
trasformando il mondo del food e immaginerete le **carriere del futuro**.
""")

# Istruzioni
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    #### 1. Il Polso della Classe
    *20 minuti*

    Rispondi alle domande sull'AI
    nel food. Individuale!
    """)

with col2:
    st.markdown("""
    #### 2. Career Designer
    *50 minuti*

    Progetta la carriera del futuro
    con il tuo gruppo, assistiti dall'AI.
    """)

with col3:
    st.markdown("""
    #### 3. AI Lab
    *40 minuti*

    Costruisci il tuo Career Coach AI:
    un agente che fa colloqui!
    """)

with col4:
    st.markdown("""
    #### 4. Showcase & Voto
    *20 minuti*

    Presenta il tuo lavoro e vota
    i migliori progetti!
    """)

# Status dei gruppi
st.divider()
groups = state.get_all_groups()
if groups:
    st.subheader(f"Gruppi registrati: {len(groups)}")
    cols = st.columns(min(len(groups), 5))
    for i, (name, data) in enumerate(groups.items()):
        with cols[i % len(cols)]:
            has_card = data.get("career_card") is not None
            has_coach = data.get("coach_system_prompt") is not None
            status = ""
            if has_coach:
                status = "Coach pronto"
            elif has_card:
                status = "Career card completata"
            else:
                status = "In esplorazione..."
            st.metric(name, data["scenario"]["title"][:30] + "...", status)
else:
    st.info("Nessun gruppo registrato ancora. Usa la sidebar per creare il tuo gruppo!")

# ── Pannello Admin (nascosto) ────────────────────────────────────────────────

with st.expander("Pannello Docente", expanded=False):
    pwd = st.text_input("Password", type="password", key="admin_pwd")
    if pwd == st.secrets.get("ADMIN_PASSWORD", "workshop2025"):
        st.success("Accesso docente attivo")

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Gruppi", len(groups))
            st.metric("Risposte quiz", len(state.get_quiz_responses()))
        with col_b:
            st.metric("Voti ricevuti", len(state.get_all_votes()))

        if st.button("RESET COMPLETO", type="primary"):
            state.reset_all()
            st.success("Tutti i dati sono stati cancellati.")
            st.rerun()
    elif pwd:
        st.error("Password errata.")

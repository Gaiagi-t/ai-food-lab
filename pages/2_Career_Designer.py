"""Pagina 2: Career Designer - Progetta la carriera del futuro con AI."""

import streamlit as st
from utils.shared_state import get_shared_state
from utils.ai_client import chat_stream
from utils.config import (
    BRAINSTORMING_SYSTEM_PROMPT,
    FEEDBACK_SYSTEM_PROMPT,
    APP_ICON,
)

st.set_page_config(page_title="Career Designer", page_icon=APP_ICON, layout="wide")

state = get_shared_state()

# ── Verifica gruppo ──────────────────────────────────────────────────────────

if not st.session_state.get("group_name"):
    st.warning("Devi prima registrare il tuo gruppo dalla **Home page** (sidebar).")
    st.stop()

group_name = st.session_state.group_name
group_data = state.get_group(group_name)

if not group_data:
    st.error("Gruppo non trovato. Torna alla Home e registrati di nuovo.")
    st.stop()

scenario = group_data["scenario"]

st.title("Career Designer")
st.markdown(f"**Gruppo:** {group_name} | **Scenario:** {scenario['title']}")

# ── Navigazione via radio (no tabs → chat_input rimane in fondo) ─────────

section = st.radio(
    "Fase",
    options=["1. Brainstorming con AI", "2. Design Career Card", "3. Feedback AI"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 1: BRAINSTORMING
# ══════════════════════════════════════════════════════════════════════════════

if section == "1. Brainstorming con AI":
    st.markdown(f"""
    ### Esplora lo scenario con l'AI

    **Il vostro scenario:** {scenario['title']}

    {scenario['description']}

    **Keywords:** {', '.join(scenario['keywords'])}

    ---
    Chattate con l'AI per esplorare il vostro scenario. Fatevi ispirare,
    fatevi provocare, e trovate l'idea per un **ruolo professionale del futuro**!
    """)

    # Mostra la chat history
    history = state.get_brainstorm_history(group_name)
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 2: CAREER CARD
# ══════════════════════════════════════════════════════════════════════════════

elif section == "2. Design Career Card":
    st.markdown("""
    ### Progetta la Career Card

    Compilate la scheda della **carriera del futuro** che avete immaginato.
    Pensate a un ruolo che **non esiste ancora** all'intersezione tra AI e food!
    """)

    existing = group_data.get("career_card") or {}

    with st.form("career_card_form"):
        role_name = st.text_input(
            "Nome del ruolo",
            value=existing.get("role_name", ""),
            placeholder="Es: Food Data Strategist, AI Sommelier Trainer...",
        )

        description = st.text_area(
            "Descrizione: cosa fa questa persona ogni giorno?",
            value=existing.get("description", ""),
            height=120,
            placeholder="Descrivi una giornata tipo di questa persona...",
        )

        col1, col2 = st.columns(2)
        with col1:
            hard_skills = st.text_area(
                "Hard Skills (competenze tecniche)",
                value=existing.get("hard_skills", ""),
                height=100,
                placeholder="Es: analisi dati, machine learning, Python, conoscenza HACCP...",
            )
        with col2:
            soft_skills = st.text_area(
                "Soft Skills (competenze umane)",
                value=existing.get("soft_skills", ""),
                height=100,
                placeholder="Es: pensiero critico, comunicazione, creatività, empatia...",
            )

        ai_ally = st.text_area(
            "AI come alleata: come l'AI supporta (non sostituisce) questo ruolo?",
            value=existing.get("ai_ally", ""),
            height=100,
            placeholder="Es: l'AI analizza i dati in tempo reale, il professionista interpreta e decide...",
        )

        human_touch = st.text_area(
            "Il tocco umano: perché un umano è ancora indispensabile?",
            value=existing.get("human_touch", ""),
            height=100,
            placeholder="Es: serve creatività, contesto culturale, gestione delle relazioni...",
        )

        submitted = st.form_submit_button(
            "Salva la Career Card", use_container_width=True, type="primary"
        )

        if submitted:
            if not role_name.strip():
                st.error("Il nome del ruolo è obbligatorio!")
            else:
                card = {
                    "role_name": role_name.strip(),
                    "description": description.strip(),
                    "hard_skills": hard_skills.strip(),
                    "soft_skills": soft_skills.strip(),
                    "ai_ally": ai_ally.strip(),
                    "human_touch": human_touch.strip(),
                }
                state.update_group(group_name, career_card=card)
                st.success("Career Card salvata! Ora potete chiedere il **Feedback AI**.")
                st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 3: FEEDBACK AI
# ══════════════════════════════════════════════════════════════════════════════

elif section == "3. Feedback AI":
    st.markdown("### Feedback AI sulla vostra Career Card")

    group_data = state.get_group(group_name)
    card = group_data.get("career_card") if group_data else None

    if not card:
        st.info("Prima compilate e salvate la **Career Card** nella sezione 2!")
    else:
        st.markdown(f"""
        **Ruolo:** {card['role_name']}
        **Scenario:** {scenario['title']}
        """)

        if st.button("Chiedi feedback all'AI", type="primary", use_container_width=True):
            sys_prompt = FEEDBACK_SYSTEM_PROMPT.format(
                role_name=card["role_name"],
                description=card["description"],
                hard_skills=card["hard_skills"],
                soft_skills=card["soft_skills"],
                ai_ally=card["ai_ally"],
                human_touch=card["human_touch"],
            )

            with st.spinner("L'AI sta analizzando la vostra career card..."):
                messages = [{"role": "user", "content": "Analizza questa career card e dammi il tuo feedback."}]
                with st.chat_message("assistant"):
                    st.write_stream(chat_stream(sys_prompt, messages))

        # Anteprima della card
        st.divider()
        st.markdown("#### Anteprima della vostra Career Card")

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f"**{card['role_name']}**")
            st.markdown(f"*{scenario['title']}*")
            st.markdown(f"**Descrizione:** {card['description']}")
            st.markdown(f"**Hard Skills:** {card['hard_skills']}")
        with col_right:
            st.markdown(f"**Soft Skills:** {card['soft_skills']}")
            st.markdown(f"**AI come alleata:** {card['ai_ally']}")
            st.markdown(f"**Tocco umano:** {card['human_touch']}")

# ══════════════════════════════════════════════════════════════════════════════
# CHAT INPUT GLOBALE (sempre in fondo alla pagina, solo per brainstorming)
# ══════════════════════════════════════════════════════════════════════════════

if section == "1. Brainstorming con AI":
    sys_prompt = BRAINSTORMING_SYSTEM_PROMPT.format(
        scenario_title=scenario["title"],
        scenario_description=scenario["description"],
    )

    if prompt := st.chat_input("Scrivi al facilitatore AI..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        state.add_brainstorm_message(group_name, "user", prompt)

        messages = state.get_brainstorm_history(group_name)
        with st.chat_message("assistant"):
            response = st.write_stream(chat_stream(sys_prompt, messages))
        state.add_brainstorm_message(group_name, "assistant", response)

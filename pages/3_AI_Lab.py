"""Pagina 3: AI Lab - Crea il tuo Career Coach AI."""

import streamlit as st
from utils.shared_state import get_shared_state
from utils.ai_client import chat_stream
from utils.config import (
    COACH_SYSTEM_PROMPT_TEMPLATE,
    COACH_ROLES,
    COACH_TONES,
    COACH_QUESTION_TYPES,
    APP_ICON,
)

st.set_page_config(page_title="AI Lab - Career Coach", page_icon=APP_ICON, layout="wide")

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

card = group_data.get("career_card")
if not card:
    st.warning(
        "Prima completate la **Career Card** nella pagina Career Designer! "
        "Il coach farà colloqui per il ruolo che avete progettato."
    )
    st.stop()

st.title("AI Lab: Crea il tuo Career Coach")
st.markdown(
    f"**Gruppo:** {group_name} | **Ruolo:** {card['role_name']}\n\n"
    "Costruite un agente AI che conduce colloqui di lavoro per il ruolo "
    "che avete progettato. Scegliete la personalità, il tono e lo stile "
    "del vostro coach, poi testatelo!"
)

# ── Tre step in tab ──────────────────────────────────────────────────────────

tab_design, tab_test, tab_cross = st.tabs([
    "1. Progetta il Coach",
    "2. Testa il Coach",
    "3. Prova i Coach degli altri",
])

# ── Tab 1: Design del Coach ──────────────────────────────────────────────────

with tab_design:
    st.markdown("""
    ### Progetta il tuo Career Coach AI

    Configurate la personalità e il comportamento del vostro agente AI.
    L'app assemblerà automaticamente il **system prompt** dalle vostre scelte.
    """)

    existing_config = group_data.get("coach_config") or {}

    with st.form("coach_config_form"):
        coach_role = st.selectbox(
            "Chi è il coach?",
            options=COACH_ROLES,
            index=COACH_ROLES.index(existing_config["coach_role"]) if existing_config.get("coach_role") in COACH_ROLES else 0,
        )

        tone_labels = [t[0] for t in COACH_TONES]
        selected_tone_label = st.selectbox(
            "Tono e personalità",
            options=tone_labels,
            index=tone_labels.index(existing_config["tone_label"]) if existing_config.get("tone_label") in tone_labels else 0,
        )
        tone_value = dict(COACH_TONES)[selected_tone_label]

        question_types = st.multiselect(
            "Tipo di domande che il coach deve fare",
            options=COACH_QUESTION_TYPES,
            default=existing_config.get("question_types", COACH_QUESTION_TYPES[:2]),
        )

        knowledge = st.text_area(
            "Conoscenze specifiche del coach",
            value=existing_config.get("knowledge", ""),
            height=80,
            placeholder="Es: Esperto di machine learning applicato alla filiera agroalimentare, "
                        "conosce le normative EU sul novel food...",
        )

        evaluation = st.text_area(
            "Criteri di valutazione del candidato",
            value=existing_config.get("evaluation", ""),
            height=80,
            placeholder="Es: Capacità di problem solving, conoscenza delle tecnologie AI, "
                        "visione innovativa, capacità di lavorare in team...",
        )

        custom_instructions = st.text_area(
            "Istruzioni aggiuntive (opzionale - per personalizzare ancora di più!)",
            value=existing_config.get("custom_instructions", ""),
            height=80,
            placeholder="Es: Fai una domanda trabocchetto sull'etica dell'AI, "
                        "chiedi sempre un esempio concreto...",
        )

        submitted = st.form_submit_button(
            "Genera il System Prompt", use_container_width=True, type="primary"
        )

        if submitted:
            # Salva la configurazione
            config = {
                "coach_role": coach_role,
                "tone_label": selected_tone_label,
                "tone_value": tone_value,
                "question_types": question_types,
                "knowledge": knowledge.strip(),
                "evaluation": evaluation.strip(),
                "custom_instructions": custom_instructions.strip(),
            }

            # Assembla il system prompt
            sys_prompt = COACH_SYSTEM_PROMPT_TEMPLATE.format(
                coach_role=coach_role,
                career_role=card["role_name"],
                tone=selected_tone_label,
                style=tone_value,
                knowledge=knowledge.strip() or "Conoscenze generali sul settore food-tech e AI",
                question_types=", ".join(question_types) if question_types else "Miste",
                evaluation_criteria=evaluation.strip() or "Competenze tecniche, soft skills, visione innovativa",
            )

            # Aggiungi istruzioni custom
            if custom_instructions.strip():
                sys_prompt += f"\n\nISTRUZIONI AGGIUNTIVE DEL GRUPPO:\n{custom_instructions.strip()}"

            # Aggiungi contesto dalla career card
            sys_prompt += (
                f"\n\nDESCRIZIONE DEL RUOLO (dal gruppo):\n{card['description']}"
                f"\n\nHARD SKILLS RICHIESTE:\n{card['hard_skills']}"
                f"\n\nSOFT SKILLS RICHIESTE:\n{card['soft_skills']}"
            )

            state.update_group(
                group_name,
                coach_config=config,
                coach_system_prompt=sys_prompt,
                coach_chat_history=[],
            )
            st.success("System prompt generato! Andate al tab **Testa il Coach** per provarlo.")

    # Mostra il system prompt generato
    current_prompt = group_data.get("coach_system_prompt")
    if current_prompt:
        with st.expander("Visualizza il System Prompt generato"):
            st.code(current_prompt, language=None)

# ── Tab 2: Testa il Coach ────────────────────────────────────────────────────

with tab_test:
    # Ricarica dati aggiornati
    group_data = state.get_group(group_name)
    coach_prompt = group_data.get("coach_system_prompt") if group_data else None

    if not coach_prompt:
        st.info("Prima **progettate il coach** nel tab precedente!")
        st.stop()

    st.markdown(f"""
    ### Testa il tuo Career Coach

    Il vostro coach è pronto! Provate a "candidarvi" per il ruolo di **{card['role_name']}**.
    Il coach vi farà un vero colloquio di lavoro.

    *Potete tornare al tab precedente per modificare il system prompt e vedere come cambia il comportamento!*
    """)

    col_chat, col_info = st.columns([3, 1])

    with col_info:
        st.markdown("**Suggerimenti:**")
        st.markdown(
            "- Presentatevi al coach\n"
            "- Rispondete alle domande\n"
            "- Provate a dare risposte vaghe: come reagisce?\n"
            "- Provate a cambiare argomento: vi riporta al tema?\n"
            "- Notate dove il coach 'alucina' o dice cose sbagliate"
        )
        if st.button("Ricomincia il colloquio", use_container_width=True):
            state.set_coach_chat_history(group_name, [])
            st.rerun()

    with col_chat:
        # Mostra history
        history = state.get_coach_chat_history(group_name)
        for msg in history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Se la chat è vuota, il coach si presenta
        if not history:
            with st.chat_message("assistant"):
                intro = st.write_stream(
                    chat_stream(
                        coach_prompt,
                        [{"role": "user", "content": "Buongiorno, sono qui per il colloquio."}],
                    )
                )
            state.add_coach_message(group_name, "user", "Buongiorno, sono qui per il colloquio.")
            state.add_coach_message(group_name, "assistant", intro)

        # Input candidato
        if user_input := st.chat_input("Rispondi al coach...", key="coach_test_input"):
            with st.chat_message("user"):
                st.markdown(user_input)
            state.add_coach_message(group_name, "user", user_input)

            messages = state.get_coach_chat_history(group_name)
            with st.chat_message("assistant"):
                response = st.write_stream(
                    chat_stream(coach_prompt, messages)
                )
            state.add_coach_message(group_name, "assistant", response)

# ── Tab 3: Cross-test ────────────────────────────────────────────────────────

with tab_cross:
    st.markdown("""
    ### Prova i Coach degli altri gruppi

    Seleziona un altro gruppo e provate il loro career coach!
    Confrontate: quale fa le domande migliori? Quale è più realistico?
    """)

    all_groups = state.get_all_groups()
    other_groups = {
        name: data for name, data in all_groups.items()
        if name != group_name and data.get("coach_system_prompt")
    }

    if not other_groups:
        st.info("Nessun altro gruppo ha ancora creato il proprio coach. Aspettate un momento!")
    else:
        selected_group = st.selectbox(
            "Scegli un gruppo da provare",
            options=list(other_groups.keys()),
            format_func=lambda x: f"{x} — {other_groups[x]['career_card']['role_name']}" if other_groups[x].get("career_card") else x,
        )

        if selected_group:
            other_data = other_groups[selected_group]
            other_card = other_data.get("career_card", {})
            other_prompt = other_data["coach_system_prompt"]

            st.markdown(
                f"**Ruolo:** {other_card.get('role_name', 'N/D')} | "
                f"**Scenario:** {other_data['scenario']['title']}"
            )

            # Chat separata per il cross-test (usa session_state locale)
            cross_key = f"cross_chat_{selected_group}"
            if cross_key not in st.session_state:
                st.session_state[cross_key] = []

            for msg in st.session_state[cross_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            if st.button("Ricomincia", key=f"reset_{selected_group}"):
                st.session_state[cross_key] = []
                st.rerun()

            if cross_input := st.chat_input(
                f"Parla con il coach di {selected_group}...",
                key=f"cross_input_{selected_group}",
            ):
                with st.chat_message("user"):
                    st.markdown(cross_input)
                st.session_state[cross_key].append(
                    {"role": "user", "content": cross_input}
                )

                with st.chat_message("assistant"):
                    response = st.write_stream(
                        chat_stream(other_prompt, st.session_state[cross_key])
                    )
                st.session_state[cross_key].append(
                    {"role": "assistant", "content": response}
                )

"""Pagina 3: AI Lab - Crea il tuo Policy Advisor AI."""

import streamlit as st
from utils.shared_state import get_shared_state
from utils.ai_client import chat_stream, generate_image
from utils.config import (
    COACH_SYSTEM_PROMPT_TEMPLATE,
    COACH_ROLES,
    COACH_TONES,
    COACH_QUESTION_TYPES,
    APP_ICON,
)

st.set_page_config(page_title="AI Lab - Policy Advisor", page_icon=APP_ICON, layout="wide")

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

card = group_data.get("scenario_card")
if not card:
    st.warning(
        "Prima completate la **Scenario Card** nella pagina Scenari 2035! "
        "L'advisor discuterà lo scenario che avete progettato."
    )
    st.stop()

st.title("AI Lab: Crea il tuo Policy Advisor")
st.markdown(
    f"**Gruppo:** {group_name} | **Scenario:** {card['scenario_title_custom']}"
)

# ── Navigazione via radio ────────────────────────────────────────────────────

section = st.radio(
    "Sezione",
    options=["1. Progetta l'Advisor", "2. Testa l'Advisor", "3. Prova gli Advisor degli altri"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 1: PROGETTA L'ADVISOR
# ══════════════════════════════════════════════════════════════════════════════

if section == "1. Progetta l'Advisor":
    st.markdown("""
    ### Progetta il tuo Policy Advisor AI

    Configurate la personalità e il comportamento del vostro agente AI.
    L'app assemblerà automaticamente il **system prompt** dalle vostre scelte.
    """)

    existing_config = group_data.get("coach_config") or {}

    with st.form("coach_config_form"):
        coach_role = st.selectbox(
            "Chi è l'advisor?",
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
            "Tipo di domande che l'advisor deve fare",
            options=COACH_QUESTION_TYPES,
            default=existing_config.get("question_types", COACH_QUESTION_TYPES[:2]),
        )

        knowledge = st.text_area(
            "Conoscenze specifiche dell'advisor",
            value=existing_config.get("knowledge", ""),
            height=80,
            placeholder="Es: Esperto di politiche industriali europee, "
                        "conosce EuroHPC, PNRR, AI Act, ecosistema startup italiano...",
        )

        evaluation = st.text_area(
            "Criteri di valutazione delle proposte del gruppo",
            value=existing_config.get("evaluation", ""),
            height=80,
            placeholder="Es: Coerenza dell'analisi, fattibilità delle raccomandazioni, "
                        "capacità di considerare rischi e opportunità...",
        )

        custom_instructions = st.text_area(
            "Istruzioni aggiuntive (opzionale - per personalizzare ancora di più!)",
            value=existing_config.get("custom_instructions", ""),
            height=80,
            placeholder="Es: Sfida sempre le assunzioni del gruppo, "
                        "chiedi esempi concreti di imprese italiane...",
        )

        submitted = st.form_submit_button(
            "Genera il System Prompt", use_container_width=True, type="primary"
        )

        if submitted:
            config = {
                "coach_role": coach_role,
                "tone_label": selected_tone_label,
                "tone_value": tone_value,
                "question_types": question_types,
                "knowledge": knowledge.strip(),
                "evaluation": evaluation.strip(),
                "custom_instructions": custom_instructions.strip(),
            }

            sys_prompt = COACH_SYSTEM_PROMPT_TEMPLATE.format(
                coach_role=coach_role,
                career_role=card["scenario_title_custom"],
                tone=selected_tone_label,
                style=tone_value,
                knowledge=knowledge.strip() or "Conoscenze generali su politiche industriali, AI, supercalcolo e competitività",
                question_types=", ".join(question_types) if question_types else "Miste",
                evaluation_criteria=evaluation.strip() or "Coerenza dell'analisi, fattibilità, visione strategica",
            )

            if custom_instructions.strip():
                sys_prompt += f"\n\nISTRUZIONI AGGIUNTIVE DEL GRUPPO:\n{custom_instructions.strip()}"

            sys_prompt += (
                f"\n\nSCENARIO DEL GRUPPO:\n{card['future_description']}"
                f"\n\nIMPATTO SULLE IMPRESE:\n{card['impact_on_enterprises']}"
                f"\n\nFATTORI CHIAVE:\n{card['key_factors']}"
                f"\n\nRACCOMANDAZIONI STRATEGICHE:\n{card['strategic_recommendations']}"
            )

            state.update_group(
                group_name,
                coach_config=config,
                coach_system_prompt=sys_prompt,
                coach_chat_history=[],
            )
            st.success("System prompt generato! Andate a **2. Testa l'Advisor** per provarlo.")

    # Mostra il system prompt generato
    current_prompt = group_data.get("coach_system_prompt")
    if current_prompt:
        with st.expander("Visualizza il System Prompt generato"):
            st.code(current_prompt, language=None)

    # ── Generazione foto dell'Advisor ────────────────────────────────────
    st.divider()
    st.subheader("Genera l'avatar del tuo Advisor")

    # Mostra immagine esistente
    coach_image_url = group_data.get("coach_image_url")
    if coach_image_url:
        st.image(coach_image_url, width=300, caption="Il vostro Policy Advisor AI")

    coach_config = group_data.get("coach_config") or {}
    if coach_config:
        st.markdown(
            f"L'advisor è: **{coach_config.get('coach_role', '')}**, "
            f"tono **{coach_config.get('tone_label', '')}**"
        )

        if st.button("Genera foto dell'Advisor", type="primary", use_container_width=True):
            image_prompt = (
                f"Professional portrait photo of {coach_config.get('coach_role', 'a policy advisor')}, "
                f"working in Italian industrial policy and AI strategy in the year 2035. "
                f"They have a {coach_config.get('tone_value', 'professional')} demeanor. "
                f"Modern office with a view of an Italian city, high-tech environment. "
                f"Photorealistic style, warm lighting, confident expression. "
                f"The person is leading a strategic analysis session."
            )
            with st.spinner("L'AI sta generando l'avatar del vostro advisor..."):
                try:
                    url = generate_image(image_prompt)
                    state.update_group(group_name, coach_image_url=url)
                    st.image(url, width=300, caption="Il vostro Policy Advisor AI")
                    st.success("Avatar generato!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore nella generazione dell'immagine: {e}")
    else:
        st.info("Prima genera il system prompt dell'advisor, poi potrai generare il suo avatar!")

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 2: TESTA L'ADVISOR
# ══════════════════════════════════════════════════════════════════════════════

elif section == "2. Testa l'Advisor":
    group_data = state.get_group(group_name)
    coach_prompt = group_data.get("coach_system_prompt") if group_data else None

    if not coach_prompt:
        st.info("Prima **progettate l'advisor** nella sezione 1!")
        st.stop()

    # Mostra avatar se disponibile
    coach_image_url = group_data.get("coach_image_url")

    col_header, col_avatar = st.columns([3, 1])
    with col_header:
        st.markdown(f"""
        ### Testa il tuo Policy Advisor

        Presentate il vostro scenario **"{card['scenario_title_custom']}"**
        all'advisor. Difendete le vostre analisi e raccomandazioni!
        """)
        st.markdown(
            "**Suggerimenti:** Presentate lo scenario -- Difendete le raccomandazioni -- "
            "Rispondete alle domande critiche -- Notate le 'allucinazioni'"
        )
    with col_avatar:
        if coach_image_url:
            st.image(coach_image_url, width=150)

    if st.button("Ricomincia la sessione", use_container_width=True):
        state.set_coach_chat_history(group_name, [])
        st.rerun()

    st.divider()

    # Mostra chat history
    history = state.get_coach_chat_history(group_name)
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Se la chat è vuota, l'advisor si presenta
    if not history:
        with st.chat_message("assistant"):
            intro = st.write_stream(
                chat_stream(
                    coach_prompt,
                    [{"role": "user", "content": "Buongiorno, siamo pronti per la sessione di analisi strategica."}],
                )
            )
        state.add_coach_message(group_name, "user", "Buongiorno, siamo pronti per la sessione di analisi strategica.")
        state.add_coach_message(group_name, "assistant", intro)

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 3: CROSS-TEST
# ══════════════════════════════════════════════════════════════════════════════

elif section == "3. Prova gli Advisor degli altri":
    st.markdown("""
    ### Prova gli Advisor degli altri gruppi

    Seleziona un altro gruppo e provate il loro policy advisor!
    Confrontate: quale fa le domande migliori? Quale è più incisivo?
    """)

    all_groups = state.get_all_groups()
    other_groups = {
        name: data for name, data in all_groups.items()
        if name != group_name and data.get("coach_system_prompt")
    }

    if not other_groups:
        st.info("Nessun altro gruppo ha ancora creato il proprio advisor. Aspettate un momento!")
        st.stop()

    selected_group = st.selectbox(
        "Scegli un gruppo da provare",
        options=list(other_groups.keys()),
        format_func=lambda x: f"{x} — {other_groups[x]['scenario_card']['scenario_title_custom']}" if other_groups[x].get("scenario_card") else x,
    )

    if selected_group:
        other_data = other_groups[selected_group]
        other_card = other_data.get("scenario_card", {})

        col_info, col_avatar = st.columns([3, 1])
        with col_info:
            st.markdown(
                f"**Scenario:** {other_card.get('scenario_title_custom', 'N/D')} | "
                f"**Tecnica:** {other_data['scenario']['title']}"
            )
        with col_avatar:
            other_image = other_data.get("coach_image_url")
            if other_image:
                st.image(other_image, width=100)

        cross_key = f"cross_chat_{selected_group}"
        if cross_key not in st.session_state:
            st.session_state[cross_key] = []

        if st.button("Ricomincia", key=f"reset_{selected_group}"):
            st.session_state[cross_key] = []
            st.rerun()

        st.divider()

        for msg in st.session_state[cross_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

# ══════════════════════════════════════════════════════════════════════════════
# CHAT INPUT GLOBALE (sempre in fondo alla pagina)
# ══════════════════════════════════════════════════════════════════════════════

if section == "2. Testa l'Advisor":
    group_data = state.get_group(group_name)
    coach_prompt = group_data.get("coach_system_prompt") if group_data else None

    if coach_prompt:
        if user_input := st.chat_input("Rispondi all'advisor..."):
            with st.chat_message("user"):
                st.markdown(user_input)
            state.add_coach_message(group_name, "user", user_input)

            messages = state.get_coach_chat_history(group_name)
            with st.chat_message("assistant"):
                response = st.write_stream(chat_stream(coach_prompt, messages))
            state.add_coach_message(group_name, "assistant", response)

elif section == "3. Prova gli Advisor degli altri":
    all_groups = state.get_all_groups()
    other_groups = {
        name: data for name, data in all_groups.items()
        if name != group_name and data.get("coach_system_prompt")
    }

    if other_groups and selected_group:
        other_prompt = other_groups[selected_group]["coach_system_prompt"]
        cross_key = f"cross_chat_{selected_group}"

        if cross_input := st.chat_input(f"Parla con l'advisor di {selected_group}..."):
            with st.chat_message("user"):
                st.markdown(cross_input)
            st.session_state[cross_key].append({"role": "user", "content": cross_input})

            with st.chat_message("assistant"):
                response = st.write_stream(
                    chat_stream(other_prompt, st.session_state[cross_key])
                )
            st.session_state[cross_key].append({"role": "assistant", "content": response})

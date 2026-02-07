"""Pagina 3: AI Lab - Crea il tuo Career Coach AI."""

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
    f"**Gruppo:** {group_name} | **Ruolo:** {card['role_name']}"
)

# ── Navigazione via radio (no tabs → chat_input rimane in fondo) ─────────

section = st.radio(
    "Sezione",
    options=["1. Progetta il Coach", "2. Testa il Coach", "3. Prova i Coach degli altri"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 1: PROGETTA IL COACH
# ══════════════════════════════════════════════════════════════════════════════

if section == "1. Progetta il Coach":
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
                career_role=card["role_name"],
                tone=selected_tone_label,
                style=tone_value,
                knowledge=knowledge.strip() or "Conoscenze generali sul settore food-tech e AI",
                question_types=", ".join(question_types) if question_types else "Miste",
                evaluation_criteria=evaluation.strip() or "Competenze tecniche, soft skills, visione innovativa",
            )

            if custom_instructions.strip():
                sys_prompt += f"\n\nISTRUZIONI AGGIUNTIVE DEL GRUPPO:\n{custom_instructions.strip()}"

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
            st.success("System prompt generato! Andate a **2. Testa il Coach** per provarlo.")

    # Mostra il system prompt generato
    current_prompt = group_data.get("coach_system_prompt")
    if current_prompt:
        with st.expander("Visualizza il System Prompt generato"):
            st.code(current_prompt, language=None)

    # ── Generazione foto del Coach ───────────────────────────────────────
    st.divider()
    st.subheader("Genera l'avatar del tuo Coach")

    # Mostra immagine esistente
    coach_image_url = group_data.get("coach_image_url")
    if coach_image_url:
        st.image(coach_image_url, width=300, caption="Il vostro Career Coach AI")

    coach_config = group_data.get("coach_config") or {}
    if coach_config:
        st.markdown(
            f"Il coach è: **{coach_config.get('coach_role', '')}**, "
            f"tono **{coach_config.get('tone_label', '')}**"
        )

        if st.button("Genera foto del Coach", type="primary", use_container_width=True):
            image_prompt = (
                f"Professional portrait photo of {coach_config.get('coach_role', 'a food tech executive')}, "
                f"working in the food technology and AI industry in the year 2035. "
                f"They have a {coach_config.get('tone_value', 'professional')} demeanor. "
                f"Modern office with food tech equipment in the background. "
                f"Photorealistic style, warm lighting, confident expression. "
                f"The person is conducting a job interview."
            )
            with st.spinner("L'AI sta generando l'avatar del vostro coach..."):
                try:
                    url = generate_image(image_prompt)
                    state.update_group(group_name, coach_image_url=url)
                    st.image(url, width=300, caption="Il vostro Career Coach AI")
                    st.success("Avatar generato!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore nella generazione dell'immagine: {e}")
    else:
        st.info("Prima genera il system prompt del coach, poi potrai generare il suo avatar!")

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 2: TESTA IL COACH
# ══════════════════════════════════════════════════════════════════════════════

elif section == "2. Testa il Coach":
    group_data = state.get_group(group_name)
    coach_prompt = group_data.get("coach_system_prompt") if group_data else None

    if not coach_prompt:
        st.info("Prima **progettate il coach** nella sezione 1!")
        st.stop()

    # Mostra avatar se disponibile
    coach_image_url = group_data.get("coach_image_url")

    col_header, col_avatar = st.columns([3, 1])
    with col_header:
        st.markdown(f"""
        ### Testa il tuo Career Coach

        Provate a "candidarvi" per il ruolo di **{card['role_name']}**.
        Il coach vi farà un vero colloquio di lavoro.
        """)
        st.markdown(
            "**Suggerimenti:** Presentatevi • Rispondete alle domande • "
            "Provate risposte vaghe • Cambiate argomento • Notate le 'allucinazioni'"
        )
    with col_avatar:
        if coach_image_url:
            st.image(coach_image_url, width=150)

    if st.button("Ricomincia il colloquio", use_container_width=True):
        state.set_coach_chat_history(group_name, [])
        st.rerun()

    st.divider()

    # Mostra chat history
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

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 3: CROSS-TEST
# ══════════════════════════════════════════════════════════════════════════════

elif section == "3. Prova i Coach degli altri":
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
        st.stop()

    selected_group = st.selectbox(
        "Scegli un gruppo da provare",
        options=list(other_groups.keys()),
        format_func=lambda x: f"{x} — {other_groups[x]['career_card']['role_name']}" if other_groups[x].get("career_card") else x,
    )

    if selected_group:
        other_data = other_groups[selected_group]
        other_card = other_data.get("career_card", {})

        col_info, col_avatar = st.columns([3, 1])
        with col_info:
            st.markdown(
                f"**Ruolo:** {other_card.get('role_name', 'N/D')} | "
                f"**Scenario:** {other_data['scenario']['title']}"
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

if section == "2. Testa il Coach":
    group_data = state.get_group(group_name)
    coach_prompt = group_data.get("coach_system_prompt") if group_data else None

    if coach_prompt:
        if user_input := st.chat_input("Rispondi al coach..."):
            with st.chat_message("user"):
                st.markdown(user_input)
            state.add_coach_message(group_name, "user", user_input)

            messages = state.get_coach_chat_history(group_name)
            with st.chat_message("assistant"):
                response = st.write_stream(chat_stream(coach_prompt, messages))
            state.add_coach_message(group_name, "assistant", response)

elif section == "3. Prova i Coach degli altri":
    all_groups = state.get_all_groups()
    other_groups = {
        name: data for name, data in all_groups.items()
        if name != group_name and data.get("coach_system_prompt")
    }

    if other_groups and selected_group:
        other_prompt = other_groups[selected_group]["coach_system_prompt"]
        cross_key = f"cross_chat_{selected_group}"

        if cross_input := st.chat_input(f"Parla con il coach di {selected_group}..."):
            with st.chat_message("user"):
                st.markdown(cross_input)
            st.session_state[cross_key].append({"role": "user", "content": cross_input})

            with st.chat_message("assistant"):
                response = st.write_stream(
                    chat_stream(other_prompt, st.session_state[cross_key])
                )
            st.session_state[cross_key].append({"role": "assistant", "content": response})

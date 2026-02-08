"""Pagina 3: AI Lab - Crea il tuo Assistente AI."""

import streamlit as st
from utils.shared_state import get_shared_state
from utils.ai_client import chat_stream, generate_image
from utils.styles import inject_custom_css, render_phase_bar
from utils.config import (
    COACH_SYSTEM_PROMPT_TEMPLATE,
    COACH_ROLES,
    COACH_TONES,
    COACH_QUESTION_TYPES,
    APP_ICON,
)

st.set_page_config(page_title="AI Lab", page_icon=APP_ICON, layout="wide")

inject_custom_css()
state = get_shared_state()

render_phase_bar(3)

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
        "L'assistente discutera' lo scenario che avete creato."
    )
    st.stop()

st.title("🤖 AI Lab: Crea il tuo Assistente AI")
st.markdown(
    f"**Gruppo:** {group_name} | **Scenario:** {card['scenario_title_custom']}"
)

# ── Navigazione via radio ────────────────────────────────────────────────────

section = st.radio(
    "Sezione",
    options=["🛠️ Crea l'Assistente", "💬 Provalo", "🔄 Prova quelli degli altri"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# Helper: label per i ruoli
role_labels = [f"{r['emoji']} {r['label']}" for r in COACH_ROLES]
role_by_label = {f"{r['emoji']} {r['label']}": r for r in COACH_ROLES}

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 1: PROGETTA L'ADVISOR
# ══════════════════════════════════════════════════════════════════════════════

if section == "🛠️ Crea l'Assistente":
    st.markdown("""
    ### Crea il tuo Assistente AI

    Scegliete chi sara' il vostro assistente AI e come si comportera'.
    L'app creera' il **system prompt** dalle vostre scelte.
    """)

    # Card ruoli
    st.markdown("**Scegli il personaggio:**")
    role_cols = st.columns(len(COACH_ROLES))
    for col, role in zip(role_cols, COACH_ROLES):
        with col:
            with st.container(border=True):
                st.markdown(f"### {role['emoji']}")
                st.markdown(f"**{role['label']}**")
                st.caption(role["full"][:80] + "...")

    existing_config = group_data.get("coach_config") or {}

    # Trova indice del ruolo salvato
    saved_role_label = existing_config.get("coach_role_label", "")
    default_role_idx = 0
    for idx, rl in enumerate(role_labels):
        if rl == saved_role_label:
            default_role_idx = idx
            break

    with st.form("coach_config_form"):
        selected_role_label = st.radio(
            "Chi sara' il vostro assistente?",
            options=role_labels,
            index=default_role_idx,
            horizontal=True,
        )
        selected_role = role_by_label[selected_role_label]

        tone_labels = [t[0] for t in COACH_TONES]
        selected_tone_label = st.selectbox(
            "Come parla?",
            options=tone_labels,
            index=tone_labels.index(existing_config["tone_label"]) if existing_config.get("tone_label") in tone_labels else 0,
        )
        tone_value = dict(COACH_TONES)[selected_tone_label]

        question_types = st.multiselect(
            "Che tipo di domande deve fare?",
            options=COACH_QUESTION_TYPES,
            default=existing_config.get("question_types", COACH_QUESTION_TYPES[:2]),
        )

        knowledge = st.text_area(
            "Di cosa e' esperto il vostro assistente?",
            value=existing_config.get("knowledge", ""),
            height=80,
            placeholder="Es: Esperto di food tech, conosce le startup del food, "
                        "sa tutto di delivery e social media...",
        )

        evaluation = st.text_area(
            "Come giudica le vostre idee?",
            value=existing_config.get("evaluation", ""),
            height=80,
            placeholder="Es: Guarda se le idee sono realistiche, "
                        "se avete pensato ai rischi e alle opportunita'...",
        )

        custom_instructions = st.text_area(
            "Istruzioni extra (opzionale - per personalizzarlo ancora di piu'!)",
            value=existing_config.get("custom_instructions", ""),
            height=80,
            placeholder="Es: Fai sempre l'avvocato del diavolo, "
                        "chiedi esempi concreti, parla di TikTok...",
        )

        submitted = st.form_submit_button(
            "Genera il System Prompt", use_container_width=True, type="primary"
        )

        if submitted:
            config = {
                "coach_role_label": selected_role_label,
                "coach_role_full": selected_role["full"],
                "tone_label": selected_tone_label,
                "tone_value": tone_value,
                "question_types": question_types,
                "knowledge": knowledge.strip(),
                "evaluation": evaluation.strip(),
                "custom_instructions": custom_instructions.strip(),
            }

            sys_prompt = COACH_SYSTEM_PROMPT_TEMPLATE.format(
                coach_role=selected_role["full"],
                career_role=card["scenario_title_custom"],
                tone=selected_tone_label,
                style=tone_value,
                knowledge=knowledge.strip() or "Conoscenze generali su food tech, AI e tendenze del mondo del cibo",
                question_types=", ".join(question_types) if question_types else "Miste",
                evaluation_criteria=evaluation.strip() or "Se le idee sono realistiche e ben ragionate",
            )

            if custom_instructions.strip():
                sys_prompt += f"\n\nISTRUZIONI AGGIUNTIVE DEL GRUPPO:\n{custom_instructions.strip()}"

            sys_prompt += (
                f"\n\nSCENARIO DEL GRUPPO:\n{card['future_description']}"
                f"\n\nCOSA CAMBIA NEL FOOD:\n{card['impact_on_enterprises']}"
                f"\n\nFATTORI CHIAVE:\n{card['key_factors']}"
                f"\n\nRACCOMANDAZIONI:\n{card['strategic_recommendations']}"
            )

            state.update_group(
                group_name,
                coach_config=config,
                coach_system_prompt=sys_prompt,
                coach_chat_history=[],
            )
            st.success("System prompt generato! Andate a **💬 Provalo** per provarlo.")

    # Mostra il system prompt generato
    current_prompt = group_data.get("coach_system_prompt")
    if current_prompt:
        with st.expander("Visualizza il System Prompt generato"):
            st.code(current_prompt, language=None)

    # ── Generazione foto dell'Assistente ──────────────────────────────────
    st.divider()
    st.subheader("Genera l'avatar del tuo Assistente")

    # Mostra immagine esistente
    coach_image_url = group_data.get("coach_image_url")
    if coach_image_url:
        st.image(coach_image_url, width=300, caption="Il vostro Assistente AI")

    image_prompt = st.text_area(
        "Descrivi come vuoi che appaia il tuo assistente AI",
        height=100,
        placeholder=(
            "Es: Una chef futuristica in un laboratorio di cucina high-tech, "
            "con un tablet in mano e ingredienti che fluttuano intorno a lei..."
        ),
    )

    if st.button("Genera foto dell'Assistente", type="primary", use_container_width=True):
        if not image_prompt.strip():
            st.warning("Scrivi una descrizione prima di generare l'immagine!")
        else:
            with st.spinner("L'AI sta generando l'avatar..."):
                try:
                    url = generate_image(image_prompt.strip())
                    state.update_group(group_name, coach_image_url=url)
                    st.image(url, width=300, caption="Il vostro Assistente AI")
                    st.success("Avatar generato!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore nella generazione dell'immagine: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 2: TESTA L'ADVISOR
# ══════════════════════════════════════════════════════════════════════════════

elif section == "💬 Provalo":
    group_data = state.get_group(group_name)
    coach_prompt = group_data.get("coach_system_prompt") if group_data else None

    if not coach_prompt:
        st.info("Prima **create l'assistente** nella sezione 1!")
        st.stop()

    # Mostra avatar se disponibile
    coach_image_url = group_data.get("coach_image_url")

    col_header, col_avatar = st.columns([3, 1])
    with col_header:
        st.markdown(f"""
        ### Prova il tuo Assistente AI

        Presentate il vostro scenario **"{card['scenario_title_custom']}"**
        all'assistente. Rispondete alle sue domande e difendete le vostre idee!
        """)
        st.markdown(
            "**Suggerimenti:** Presentate lo scenario -- Difendete le vostre idee -- "
            "Rispondete alle domande -- Notate se l'AI dice cose sbagliate"
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

    # Se la chat e' vuota, l'assistente si presenta
    if not history:
        with st.chat_message("assistant"):
            intro = st.write_stream(
                chat_stream(
                    coach_prompt,
                    [{"role": "user", "content": "Ciao! Siamo pronti, presentati e facci le tue domande."}],
                )
            )
        state.add_coach_message(group_name, "user", "Ciao! Siamo pronti, presentati e facci le tue domande.")
        state.add_coach_message(group_name, "assistant", intro)

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 3: CROSS-TEST
# ══════════════════════════════════════════════════════════════════════════════

elif section == "🔄 Prova quelli degli altri":
    st.markdown("""
    ### Prova gli assistenti degli altri gruppi

    Scegliete un altro gruppo e provate il loro assistente AI!
    Quale fa le domande migliori? Quale e' piu' interessante?
    """)

    all_groups = state.get_all_groups()
    other_groups = {
        name: data for name, data in all_groups.items()
        if name != group_name and data.get("coach_system_prompt")
    }

    if not other_groups:
        st.info("Nessun altro gruppo ha ancora creato il proprio assistente. Aspettate un momento!")
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

if section == "💬 Provalo":
    group_data = state.get_group(group_name)
    coach_prompt = group_data.get("coach_system_prompt") if group_data else None

    if coach_prompt:
        if user_input := st.chat_input("Scrivi la tua risposta..."):
            with st.chat_message("user"):
                st.markdown(user_input)
            state.add_coach_message(group_name, "user", user_input)

            messages = state.get_coach_chat_history(group_name)
            with st.chat_message("assistant"):
                response = st.write_stream(chat_stream(coach_prompt, messages))
            state.add_coach_message(group_name, "assistant", response)

elif section == "🔄 Prova quelli degli altri":
    all_groups = state.get_all_groups()
    other_groups = {
        name: data for name, data in all_groups.items()
        if name != group_name and data.get("coach_system_prompt")
    }

    if other_groups and selected_group:
        other_prompt = other_groups[selected_group]["coach_system_prompt"]
        cross_key = f"cross_chat_{selected_group}"

        if cross_input := st.chat_input(f"Parla con l'assistente di {selected_group}..."):
            with st.chat_message("user"):
                st.markdown(cross_input)
            st.session_state[cross_key].append({"role": "user", "content": cross_input})

            with st.chat_message("assistant"):
                response = st.write_stream(
                    chat_stream(other_prompt, st.session_state[cross_key])
                )
            st.session_state[cross_key].append({"role": "assistant", "content": response})

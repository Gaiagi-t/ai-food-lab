"""Pagina 2: Scenari 2035 - Esplora scenari futuri con AI e progetta la Scenario Card."""

import streamlit as st
from utils.shared_state import get_shared_state
from utils.ai_client import chat_stream
from utils.styles import inject_custom_css, render_phase_bar
from utils.config import (
    BRAINSTORMING_SYSTEM_PROMPT,
    FEEDBACK_SYSTEM_PROMPT,
    APP_ICON,
)

st.set_page_config(page_title="Scenari 2035", page_icon=APP_ICON, layout="wide")

inject_custom_css()
state = get_shared_state()

render_phase_bar(2)

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

st.title("🔮 Scenari 2035")
st.markdown(f"**Gruppo:** {group_name} | **Tecnica:** {scenario['title']}")

# ── Navigazione via radio ────────────────────────────────────────────────────

section = st.radio(
    "Fase",
    options=["💬 Esplorazione con AI", "📝 Scenario Card", "🤖 Feedback AI"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 1: ESPLORAZIONE CON AI
# ══════════════════════════════════════════════════════════════════════════════

if section == "💬 Esplorazione con AI":
    # Mission card con gradient
    keywords_html = " ".join(
        f'<span class="mission-kw">{kw}</span>' for kw in scenario["keywords"]
    )
    st.markdown(f"""
    <div class="mission-card">
        <h3>La vostra missione</h3>
        <p><strong>{scenario['title']}</strong></p>
        <p>{scenario['description'][:300]}{'...' if len(scenario['description']) > 300 else ''}</p>
        <div>{keywords_html}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "Chattate con l'AI per esplorare il vostro scenario. "
        "Pensate a cosa avete classificato come PULL, PUSH e WEIGHT!"
    )

    # Mostra la chat history
    history = state.get_brainstorm_history(group_name)
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 2: SCENARIO CARD
# ══════════════════════════════════════════════════════════════════════════════

elif section == "📝 Scenario Card":
    st.markdown("""
    ### Compila la Scenario Card

    Riempite la scheda con lo **scenario futuro** che avete immaginato.
    Come sara' il mondo del cibo nel 2035?
    """)

    existing = group_data.get("scenario_card") or {}

    with st.form("scenario_card_form"):
        scenario_title_custom = st.text_input(
            "Date un titolo al vostro scenario",
            value=existing.get("scenario_title_custom", ""),
            placeholder="Es: 'Italia 2035: il cibo diventa smart'...",
        )

        future_description = st.text_area(
            "Come sara' il mondo del cibo nel 2035? Descrivete il vostro scenario",
            value=existing.get("future_description", ""),
            height=120,
            placeholder="Descrivete cosa e' cambiato nel 2035 rispetto a oggi...",
        )

        impact_on_enterprises = st.text_area(
            "Cosa cambia per chi lavora nel food?",
            value=existing.get("impact_on_enterprises", ""),
            height=100,
            placeholder="Ristoranti, startup, agricoltori... chi ci guadagna e chi ci perde?",
        )

        key_factors = st.text_area(
            "Quali sono i 3-5 fattori piu' importanti nel vostro scenario?",
            value=existing.get("key_factors", ""),
            height=100,
            placeholder="Es: tecnologia accessibile, nuove abitudini alimentari, sostenibilita'...",
        )

        strategic_recommendations = st.text_area(
            "Cosa dovrebbe fare chi lavora nel food per prepararsi?",
            value=existing.get("strategic_recommendations", ""),
            height=100,
            placeholder="Es: investire in tecnologia, collaborare con startup, formarsi...",
        )

        submitted = st.form_submit_button(
            "Salva la Scenario Card", use_container_width=True, type="primary"
        )

        if submitted:
            if not scenario_title_custom.strip():
                st.error("Il titolo dello scenario e' obbligatorio!")
            else:
                card = {
                    "scenario_title_custom": scenario_title_custom.strip(),
                    "future_description": future_description.strip(),
                    "impact_on_enterprises": impact_on_enterprises.strip(),
                    "key_factors": key_factors.strip(),
                    "strategic_recommendations": strategic_recommendations.strip(),
                    "technique_name": scenario["title"],
                }
                state.update_group(group_name, scenario_card=card)
                st.success(
                    "Scenario Card salvata! Ora potete chiedere il **Feedback AI**."
                )
                st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 3: FEEDBACK AI
# ══════════════════════════════════════════════════════════════════════════════

elif section == "🤖 Feedback AI":
    st.markdown("### Feedback AI sulla vostra Scenario Card")

    group_data = state.get_group(group_name)
    card = group_data.get("scenario_card") if group_data else None

    if not card:
        st.info("Prima compilate e salvate la **Scenario Card** nella sezione 2!")
    else:
        st.markdown(f"""
        **Scenario:** {card['scenario_title_custom']}
        **Tecnica:** {scenario['title']}
        """)

        if st.button(
            "Chiedi feedback all'AI",
            type="primary",
            use_container_width=True,
        ):
            sys_prompt = FEEDBACK_SYSTEM_PROMPT.format(
                technique_name=card.get("technique_name", scenario["title"]),
                scenario_title_custom=card["scenario_title_custom"],
                future_description=card["future_description"],
                impact_on_enterprises=card["impact_on_enterprises"],
                key_factors=card["key_factors"],
                strategic_recommendations=card["strategic_recommendations"],
            )

            with st.spinner("L'AI sta analizzando la vostra scenario card..."):
                messages = [
                    {
                        "role": "user",
                        "content": "Analizza questa scenario card e dammi il tuo feedback.",
                    }
                ]
                with st.chat_message("assistant"):
                    st.write_stream(chat_stream(sys_prompt, messages))

        # Anteprima stilizzata della card
        st.divider()
        st.markdown("#### Anteprima della vostra Scenario Card")

        st.markdown(f"""
        <div class="scenario-preview">
            <h3>{card['scenario_title_custom']}</h3>
            <p><em>Tecnica: {card.get('technique_name', scenario['title'])}</em></p>
            <hr>
            <p><strong>🔮 Futuro 2035:</strong> {card['future_description']}</p>
            <p><strong>💼 Cosa cambia nel food:</strong> {card['impact_on_enterprises']}</p>
            <p><strong>🔑 Fattori chiave:</strong> {card['key_factors']}</p>
            <p><strong>💡 Raccomandazioni:</strong> {card['strategic_recommendations']}</p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CHAT INPUT GLOBALE (sempre in fondo alla pagina, solo per esplorazione)
# ══════════════════════════════════════════════════════════════════════════════

if section == "💬 Esplorazione con AI":
    sys_prompt = BRAINSTORMING_SYSTEM_PROMPT.format(
        scenario_title=scenario["title"],
        scenario_description=scenario["description"],
    )

    if prompt := st.chat_input("Discuti con il facilitatore dello scenario..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        state.add_brainstorm_message(group_name, "user", prompt)

        messages = state.get_brainstorm_history(group_name)
        with st.chat_message("assistant"):
            response = st.write_stream(chat_stream(sys_prompt, messages))
        state.add_brainstorm_message(group_name, "assistant", response)

"""Pagina 4: Showcase & Voto - Dashboard docente e sistema di voto."""

import streamlit as st
import plotly.graph_objects as go
import uuid
from collections import Counter

from utils.shared_state import get_shared_state
from utils.config import APP_ICON

st.set_page_config(page_title="Showcase & Voto", page_icon=APP_ICON, layout="wide")

state = get_shared_state()

st.title("Showcase & Voto")

# ── Selezione vista ──────────────────────────────────────────────────────────

view = st.radio(
    "Seleziona la vista",
    options=["Vista Docente (da proiettare)", "Vista Studente (vota)"],
    horizontal=True,
)

all_groups = state.get_all_groups()
groups_with_cards = {
    name: data for name, data in all_groups.items()
    if data.get("career_card")
}

# ── VISTA DOCENTE ────────────────────────────────────────────────────────────

if view == "Vista Docente (da proiettare)":
    if st.button("Aggiorna dashboard", use_container_width=True):
        st.rerun()

    if not groups_with_cards:
        st.info("Nessun gruppo ha ancora completato la career card.")
        st.stop()

    # ── Career Card Grid ──
    st.subheader(f"Le Carriere del Futuro ({len(groups_with_cards)} gruppi)")

    cols = st.columns(min(len(groups_with_cards), 3))
    for i, (name, data) in enumerate(groups_with_cards.items()):
        card = data["career_card"]
        scenario = data["scenario"]
        has_coach = data.get("coach_system_prompt") is not None

        with cols[i % len(cols)]:
            with st.container(border=True):
                st.markdown(f"### {card['role_name']}")
                st.caption(f"Gruppo: **{name}** | Scenario: *{scenario['title']}*")
                st.markdown(f"**Descrizione:** {card['description'][:200]}{'...' if len(card['description']) > 200 else ''}")

                col_hs, col_ss = st.columns(2)
                with col_hs:
                    st.markdown(f"**Hard Skills:**\n{card['hard_skills'][:150]}")
                with col_ss:
                    st.markdown(f"**Soft Skills:**\n{card['soft_skills'][:150]}")

                st.markdown(f"**AI come alleata:** {card['ai_ally'][:150]}")
                st.markdown(f"**Tocco umano:** {card['human_touch'][:150]}")

                if has_coach:
                    st.success("Career Coach AI creato")
                else:
                    st.warning("Coach non ancora creato")

    # ── Word Cloud ──
    st.divider()
    st.subheader("Word Cloud delle Competenze")

    all_text = ""
    for data in groups_with_cards.values():
        card = data["career_card"]
        all_text += f" {card['hard_skills']} {card['soft_skills']} {card['role_name']} "

    if all_text.strip():
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt

            # Stopwords italiane comuni
            stopwords = {
                "di", "a", "da", "in", "con", "su", "per", "tra", "fra",
                "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
                "e", "o", "ma", "che", "del", "della", "dei", "delle",
                "al", "alla", "ai", "alle", "dal", "dalla", "nel", "nella",
                "non", "come", "anche", "più", "molto", "tutti", "questo",
                "essere", "avere", "fare", "dire", "andare", "potere",
                "es", "ed", "ad",
            }

            wc = WordCloud(
                width=1200,
                height=400,
                background_color="white",
                colormap="viridis",
                max_words=80,
                stopwords=stopwords,
            ).generate(all_text)

            fig_wc, ax = plt.subplots(figsize=(12, 4))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig_wc)
        except ImportError:
            st.caption("(Installa `wordcloud` e `matplotlib` per la word cloud)")

    # ── Statistiche quiz ──
    st.divider()
    quiz_responses = state.get_quiz_responses()
    st.subheader(f"Risultati Quiz ({len(quiz_responses)} risposte)")

    if quiz_responses:
        from utils.config import QUIZ_QUESTIONS

        avgs = {}
        for q in QUIZ_QUESTIONS:
            vals = [r["answers"].get(q["id"], 3) for r in quiz_responses]
            avgs[q["id"]] = sum(vals) / len(vals) if vals else 0

        labels = [q["text"][:50] + "..." for q in QUIZ_QUESTIONS]
        values = [avgs[q["id"]] for q in QUIZ_QUESTIONS]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name="Media classe",
            fillcolor="rgba(46, 204, 113, 0.3)",
            line=dict(color="rgba(46, 204, 113, 1)"),
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            height=500,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── Classifica voti ──
    st.divider()
    votes = state.get_all_votes()
    if votes:
        st.subheader(f"Classifica ({len(votes)} votanti)")

        categories = ["Carriera più innovativa", "Carriera più realistica", "Coach AI migliore"]
        for cat in categories:
            cat_votes = [v.get(cat) for v in votes.values() if v.get(cat)]
            if cat_votes:
                counts = Counter(cat_votes)
                winner = counts.most_common(1)[0]

                st.markdown(f"**{cat}:** {winner[0]} ({winner[1]} voti)")

                fig_v = go.Figure(data=[
                    go.Bar(
                        x=list(counts.keys()),
                        y=list(counts.values()),
                        marker_color=["#f1c40f" if k == winner[0] else "#3498db" for k in counts.keys()],
                    )
                ])
                fig_v.update_layout(height=200, margin=dict(l=0, r=0, t=10, b=0))
                st.plotly_chart(fig_v, use_container_width=True)

# ── VISTA STUDENTE ───────────────────────────────────────────────────────────

else:
    if not groups_with_cards:
        st.info("Nessun gruppo ha ancora completato la career card.")
        st.stop()

    # ID votante
    if "voter_id" not in st.session_state:
        st.session_state.voter_id = str(uuid.uuid4())[:8]

    my_group = st.session_state.get("group_name", "")

    st.markdown("""
    ### Vota i progetti degli altri gruppi!

    Dopo le presentazioni, esprimi il tuo voto per ogni categoria.
    **Non puoi votare il tuo gruppo.**
    """)

    votable = [name for name in groups_with_cards.keys() if name != my_group]

    if not votable:
        st.warning("Non ci sono altri gruppi da votare (o il tuo gruppo è l'unico con una career card).")
        st.stop()

    # Mostra le career card in sintesi
    st.subheader("Riepilogo Career Card")
    for name in votable:
        data = groups_with_cards[name]
        card = data["career_card"]
        with st.expander(f"**{name}** — {card['role_name']}"):
            st.markdown(f"*Scenario: {data['scenario']['title']}*")
            st.markdown(f"**Descrizione:** {card['description']}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Hard Skills:** {card['hard_skills']}")
            with col2:
                st.markdown(f"**Soft Skills:** {card['soft_skills']}")
            st.markdown(f"**AI alleata:** {card['ai_ally']}")
            st.markdown(f"**Tocco umano:** {card['human_touch']}")

    # Form voto
    st.divider()
    st.subheader("Esprimi il tuo voto")

    with st.form("vote_form"):
        v_innovative = st.selectbox(
            "Carriera più INNOVATIVA",
            options=votable,
            format_func=lambda x: f"{x} — {groups_with_cards[x]['career_card']['role_name']}",
        )
        v_realistic = st.selectbox(
            "Carriera più REALISTICA",
            options=votable,
            format_func=lambda x: f"{x} — {groups_with_cards[x]['career_card']['role_name']}",
        )
        v_coach = st.selectbox(
            "Coach AI MIGLIORE",
            options=votable,
            format_func=lambda x: f"{x} — {groups_with_cards[x]['career_card']['role_name']}",
        )

        submitted = st.form_submit_button(
            "Invia il mio voto", use_container_width=True, type="primary"
        )

        if submitted:
            state.cast_vote(
                st.session_state.voter_id,
                {
                    "Carriera più innovativa": v_innovative,
                    "Carriera più realistica": v_realistic,
                    "Coach AI migliore": v_coach,
                },
            )
            st.success("Voto registrato! Il docente vedrà i risultati in tempo reale nella sua dashboard.")
            st.balloons()

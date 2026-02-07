"""Pagina 4: Showcase & Voto - Dashboard facilitatore e sistema di voto."""

import streamlit as st
import plotly.graph_objects as go
import uuid
from collections import Counter

from utils.shared_state import get_shared_state
from utils.config import APP_ICON, PHENOMENON_CARDS, CARD_CATEGORIES

st.set_page_config(page_title="Showcase & Voto", page_icon=APP_ICON, layout="wide")

state = get_shared_state()

st.title("Showcase & Voto")

# ── Selezione vista ──────────────────────────────────────────────────────────

view = st.radio(
    "Seleziona la vista",
    options=["Vista Facilitatore (da proiettare)", "Vista Partecipante (vota)"],
    horizontal=True,
)

all_groups = state.get_all_groups()
groups_with_cards = {
    name: data for name, data in all_groups.items()
    if data.get("scenario_card")
}

# ── VISTA FACILITATORE ──────────────────────────────────────────────────────

if view == "Vista Facilitatore (da proiettare)":
    if st.button("Aggiorna dashboard", use_container_width=True):
        st.rerun()

    if not groups_with_cards:
        st.info("Nessun gruppo ha ancora completato la scenario card.")
        st.stop()

    # ── Scenario Card Grid ──
    st.subheader(f"Gli Scenari del 2035 ({len(groups_with_cards)} gruppi)")

    cols = st.columns(min(len(groups_with_cards), 3))
    for i, (name, data) in enumerate(groups_with_cards.items()):
        card = data["scenario_card"]
        scenario = data["scenario"]
        has_advisor = data.get("coach_system_prompt") is not None

        with cols[i % len(cols)]:
            with st.container(border=True):
                # Avatar dell'advisor
                advisor_image = data.get("coach_image_url")
                if advisor_image:
                    st.image(advisor_image, width=200)

                st.markdown(f"### {card['scenario_title_custom']}")
                st.caption(f"Gruppo: **{name}** | Tecnica: *{scenario['title']}*")
                st.markdown(
                    f"**Futuro 2035:** {card['future_description'][:200]}"
                    f"{'...' if len(card['future_description']) > 200 else ''}"
                )

                col_hs, col_ss = st.columns(2)
                with col_hs:
                    st.markdown(
                        f"**Impatto imprese:**\n{card['impact_on_enterprises'][:150]}"
                    )
                with col_ss:
                    st.markdown(
                        f"**Fattori chiave:**\n{card['key_factors'][:150]}"
                    )

                st.markdown(
                    f"**Raccomandazioni:** {card['strategic_recommendations'][:150]}"
                )

                if has_advisor:
                    st.success("Policy Advisor AI creato")
                else:
                    st.warning("Advisor non ancora creato")

    # ── Word Cloud ──
    st.divider()
    st.subheader("Word Cloud dei Temi Chiave")

    all_text = ""
    for data in groups_with_cards.values():
        card = data["scenario_card"]
        all_text += (
            f" {card['key_factors']} {card['impact_on_enterprises']} "
            f"{card['strategic_recommendations']} {card['scenario_title_custom']} "
        )

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
                "es", "ed", "ad", "sono", "delle", "degli", "nei", "nelle",
                "sul", "sulla", "sulle", "dai", "dagli", "dalle",
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

    # ── Risultati mappatura ──
    st.divider()
    quiz_responses = state.get_quiz_responses()
    st.subheader(f"Risultati Mappatura ({len(quiz_responses)} risposte)")

    if quiz_responses:
        # Per ogni carta, mostra la classificazione prevalente
        card_results = []
        for card in PHENOMENON_CARDS:
            votes = [r["answers"].get(card["id"], "") for r in quiz_responses]
            n_pull = votes.count("PULL")
            n_push = votes.count("PUSH")
            n_weight = votes.count("WEIGHT")
            total = n_pull + n_push + n_weight
            if total > 0:
                max_cat = max(
                    [("PULL", n_pull), ("PUSH", n_push), ("WEIGHT", n_weight)],
                    key=lambda x: x[1],
                )
                card_results.append({
                    "title": card["title"][:40],
                    "category": max_cat[0],
                    "count": max_cat[1],
                    "total": total,
                    "pct": max_cat[1] / total * 100,
                })

        if card_results:
            # Grafico riepilogativo
            labels = [r["title"] for r in card_results]
            colors = [CARD_CATEGORIES[r["category"]]["color"] for r in card_results]
            pcts = [r["pct"] for r in card_results]

            fig_map = go.Figure(
                data=[
                    go.Bar(
                        y=labels,
                        x=pcts,
                        orientation="h",
                        marker_color=colors,
                        text=[
                            f"{r['category']} ({r['pct']:.0f}%)"
                            for r in card_results
                        ],
                        textposition="outside",
                    )
                ]
            )
            fig_map.update_layout(
                xaxis=dict(range=[0, 110], title="Consenso (%)"),
                height=50 * len(card_results),
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig_map, use_container_width=True)

    # ── Classifica voti ──
    st.divider()
    votes = state.get_all_votes()
    if votes:
        st.subheader(f"Classifica ({len(votes)} votanti)")

        categories = [
            "Scenario più convincente",
            "Scenario più originale",
            "Advisor AI migliore",
        ]
        for cat in categories:
            cat_votes = [v.get(cat) for v in votes.values() if v.get(cat)]
            if cat_votes:
                counts = Counter(cat_votes)
                winner = counts.most_common(1)[0]

                st.markdown(f"**{cat}:** {winner[0]} ({winner[1]} voti)")

                fig_v = go.Figure(
                    data=[
                        go.Bar(
                            x=list(counts.keys()),
                            y=list(counts.values()),
                            marker_color=[
                                "#f1c40f" if k == winner[0] else "#3498db"
                                for k in counts.keys()
                            ],
                        )
                    ]
                )
                fig_v.update_layout(
                    height=200, margin=dict(l=0, r=0, t=10, b=0)
                )
                st.plotly_chart(fig_v, use_container_width=True)

# ── VISTA PARTECIPANTE ──────────────────────────────────────────────────────

else:
    if not groups_with_cards:
        st.info("Nessun gruppo ha ancora completato la scenario card.")
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
        st.warning(
            "Non ci sono altri gruppi da votare "
            "(o il tuo gruppo è l'unico con una scenario card)."
        )
        st.stop()

    # Mostra le scenario card in sintesi
    st.subheader("Riepilogo Scenari")
    for name in votable:
        data = groups_with_cards[name]
        card = data["scenario_card"]
        with st.expander(f"**{name}** — {card['scenario_title_custom']}"):
            st.markdown(f"*Tecnica: {data['scenario']['title']}*")
            st.markdown(f"**Futuro 2035:** {card['future_description']}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"**Impatto imprese:** {card['impact_on_enterprises']}"
                )
            with col2:
                st.markdown(f"**Fattori chiave:** {card['key_factors']}")
            st.markdown(
                f"**Raccomandazioni:** {card['strategic_recommendations']}"
            )

    # Form voto
    st.divider()
    st.subheader("Esprimi il tuo voto")

    with st.form("vote_form"):
        v_convincente = st.selectbox(
            "Scenario più CONVINCENTE",
            options=votable,
            format_func=lambda x: f"{x} — {groups_with_cards[x]['scenario_card']['scenario_title_custom']}",
        )
        v_originale = st.selectbox(
            "Scenario più ORIGINALE",
            options=votable,
            format_func=lambda x: f"{x} — {groups_with_cards[x]['scenario_card']['scenario_title_custom']}",
        )
        v_advisor = st.selectbox(
            "Advisor AI MIGLIORE",
            options=votable,
            format_func=lambda x: f"{x} — {groups_with_cards[x]['scenario_card']['scenario_title_custom']}",
        )

        submitted = st.form_submit_button(
            "Invia il mio voto", use_container_width=True, type="primary"
        )

        if submitted:
            state.cast_vote(
                st.session_state.voter_id,
                {
                    "Scenario più convincente": v_convincente,
                    "Scenario più originale": v_originale,
                    "Advisor AI migliore": v_advisor,
                },
            )
            st.success(
                "Voto registrato! Il facilitatore vedrà i risultati "
                "in tempo reale nella dashboard."
            )
            st.balloons()

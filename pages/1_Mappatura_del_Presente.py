"""Pagina 1: Mappatura del Presente - Mi piace / Non mi piace."""

import streamlit as st
import plotly.graph_objects as go
import uuid

from utils.shared_state import get_shared_state
from utils.config import PHENOMENON_CARDS, CARD_CATEGORIES, APP_ICON
from utils.styles import inject_custom_css, render_phase_bar

st.set_page_config(
    page_title="Mappatura del Presente", page_icon=APP_ICON, layout="wide"
)

inject_custom_css()
state = get_shared_state()

render_phase_bar(1)

st.title("🗺️ Mappatura del Presente")

st.markdown("""
<div class="info-banner">
    <p>Per ogni fenomeno legato all'AI nel mondo del cibo,
    decidi: ti <strong>piace</strong> o <strong>non ti piace</strong>?</p>
</div>
""", unsafe_allow_html=True)

# Legenda
st.markdown("""
<div style="display:flex; gap:12px; flex-wrap:wrap; margin:0.8rem 0 1rem;">
    <span class="cat-pill cat-pill-mi_piace">👍 Mi piace</span>
    <span class="cat-pill cat-pill-non_mi_piace">👎 Non mi piace</span>
</div>
""", unsafe_allow_html=True)

st.divider()

if "student_id" not in st.session_state:
    st.session_state.student_id = str(uuid.uuid4())[:8]

# ── Classificazione ──────────────────────────────────────────────────────────

tab_classify, tab_results = st.tabs(
    ["Classifica le carte", "Risultati del gruppo"]
)

with tab_classify:
    st.markdown(
        "**Per ogni fenomeno, esprimi la tua opinione: ti piace o non ti piace?**"
    )

    with st.form("card_sorting_form"):
        classifications = {}

        for row_start in range(0, len(PHENOMENON_CARDS), 2):
            cols = st.columns(2)
            for col_idx, card_idx in enumerate(range(row_start, min(row_start + 2, len(PHENOMENON_CARDS)))):
                card = PHENOMENON_CARDS[card_idx]
                hint_cls = card.get("suggested_category", "").lower() + "-hint"
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="phenom-card {hint_cls}">
                        <span class="phenom-emoji">{card['emoji']}</span>
                        <p class="phenom-title">{card['title']}</p>
                        <p class="phenom-desc">{card['short_description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("Approfondisci"):
                        st.markdown(card["description"])
                    classifications[card["id"]] = st.radio(
                        f"Classifica: {card['title'][:40]}",
                        options=["MI_PIACE", "NON_MI_PIACE"],
                        horizontal=True,
                        key=f"classify_{card['id']}",
                        format_func=lambda x: f"{CARD_CATEGORIES[x]['icon']} {CARD_CATEGORIES[x]['label']}",
                        label_visibility="collapsed",
                    )

        submitted = st.form_submit_button(
            "Invia la mia mappatura",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            state.add_quiz_response(
                st.session_state.student_id, classifications
            )
            st.success(
                "Mappatura inviata! Vai al tab **Risultati del gruppo** "
                "per vedere la distribuzione."
            )

# ── Risultati ────────────────────────────────────────────────────────────────

with tab_results:
    responses = state.get_quiz_responses()

    if not responses:
        st.info("Nessuna risposta ancora. Aspetta che i partecipanti completino la mappatura!")
    else:
        st.metric("Risposte ricevute", len(responses))

        if st.button("Aggiorna risultati", use_container_width=True):
            st.rerun()

        # Riepilogo aggregato
        st.subheader("Distribuzione complessiva")

        total_like = 0
        total_dislike = 0
        for r in responses:
            for card_id, cat in r["answers"].items():
                if cat == "MI_PIACE":
                    total_like += 1
                elif cat == "NON_MI_PIACE":
                    total_dislike += 1

        fig_summary = go.Figure(
            data=[
                go.Bar(
                    x=["👍 Mi piace", "👎 Non mi piace"],
                    y=[total_like, total_dislike],
                    marker_color=[
                        CARD_CATEGORIES["MI_PIACE"]["color"],
                        CARD_CATEGORIES["NON_MI_PIACE"]["color"],
                    ],
                    text=[total_like, total_dislike],
                    textposition="outside",
                )
            ]
        )
        fig_summary.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(title="Voti totali"),
        )
        st.plotly_chart(fig_summary, use_container_width=True)

        # Distribuzione per carta
        st.subheader("Distribuzione per fenomeno")

        for card in PHENOMENON_CARDS:
            votes = [r["answers"].get(card["id"], "") for r in responses]
            n_like = votes.count("MI_PIACE")
            n_dislike = votes.count("NON_MI_PIACE")
            total = n_like + n_dislike

            if total == 0:
                continue

            pct_like = n_like / total * 100
            pct_dislike = n_dislike / total * 100

            col_info, col_chart = st.columns([1, 2])
            with col_info:
                st.markdown(f"**{card['emoji']} {card['title']}**")
                if pct_like >= 70:
                    st.caption(f"👍 **Piace** ({pct_like:.0f}%)")
                elif pct_dislike >= 70:
                    st.caption(f"👎 **Non piace** ({pct_dislike:.0f}%)")
                else:
                    st.caption(f"Opinioni divise ({pct_like:.0f}% / {pct_dislike:.0f}%)")
            with col_chart:
                fig_card = go.Figure()
                fig_card.add_trace(
                    go.Bar(
                        y=[""], x=[pct_like], orientation="h",
                        name="Mi piace",
                        marker_color=CARD_CATEGORIES["MI_PIACE"]["color"],
                        text=f"{n_like}" if n_like else "",
                        textposition="inside",
                    )
                )
                fig_card.add_trace(
                    go.Bar(
                        y=[""], x=[pct_dislike], orientation="h",
                        name="Non mi piace",
                        marker_color=CARD_CATEGORIES["NON_MI_PIACE"]["color"],
                        text=f"{n_dislike}" if n_dislike else "",
                        textposition="inside",
                    )
                )
                fig_card.update_layout(
                    barmode="stack",
                    height=60,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(range=[0, 100], showticklabels=False),
                    yaxis=dict(showticklabels=False),
                    showlegend=False,
                )
                st.plotly_chart(
                    fig_card, use_container_width=True,
                    key=f"dist_{card['id']}",
                )

        # Nota facilitatore
        st.divider()
        st.subheader("Spunti di discussione")
        st.markdown(
            "*Clicca su ogni fenomeno per approfondire e discuterne insieme.*"
        )

        for card in PHENOMENON_CARDS:
            suggested = card["suggested_category"]
            icon = CARD_CATEGORIES[suggested]["icon"]
            with st.expander(f"{card['emoji']} {card['title']}"):
                st.markdown(f"**Opinione degli esperti:** {icon} **{CARD_CATEGORIES[suggested]['label']}**")
                st.markdown(card["description"])

                votes = [r["answers"].get(card["id"], "") for r in responses]
                n_match = votes.count(suggested)
                total = len(votes)
                if total > 0:
                    pct = n_match / total * 100
                    if pct >= 70:
                        st.success(
                            f"Il {pct:.0f}% dei partecipanti la pensa come gli esperti."
                        )
                    elif pct >= 40:
                        st.warning(
                            f"Solo il {pct:.0f}% concorda con gli esperti. Opinioni divise: discutiamone!"
                        )
                    else:
                        st.error(
                            f"Solo il {pct:.0f}% concorda. La maggioranza ha una visione diversa!"
                        )

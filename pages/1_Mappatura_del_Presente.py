"""Pagina 1: Mappatura del Presente - Classificazione carte PULL/PUSH/WEIGHT."""

import streamlit as st
import plotly.graph_objects as go
import uuid

from utils.shared_state import get_shared_state
from utils.config import PHENOMENON_CARDS, CARD_CATEGORIES, APP_ICON

st.set_page_config(
    page_title="Mappatura del Presente", page_icon=APP_ICON, layout="wide"
)

state = get_shared_state()

st.title("Mappatura del Presente")
st.markdown(
    "Per ogni fenomeno, decidi: **attrae** le aziende verso l'AI (PULL), "
    "le **aiuta** ad adottarla (PUSH), o le **frena** (WEIGHT)?"
)

# Legenda categorie
col_l1, col_l2, col_l3 = st.columns(3)
for col, (key, cat) in zip([col_l1, col_l2, col_l3], CARD_CATEGORIES.items()):
    with col:
        st.markdown(
            f"{cat['icon']} **{key}**: {cat['description']}"
        )

st.divider()

# Genera un ID partecipante per questa sessione browser
if "student_id" not in st.session_state:
    st.session_state.student_id = str(uuid.uuid4())[:8]

# ── Sezione Classificazione ──────────────────────────────────────────────────

tab_classify, tab_results = st.tabs(
    ["Classifica le carte", "Risultati del gruppo"]
)

with tab_classify:
    st.markdown(
        "**Per ogni fenomeno, seleziona la categoria che ritieni più appropriata.**"
    )

    with st.form("card_sorting_form"):
        classifications = {}

        for i, card in enumerate(PHENOMENON_CARDS):
            with st.container(border=True):
                st.markdown(f"**{card['title']}**")
                st.caption(card["description"])
                classifications[card["id"]] = st.radio(
                    f"Classifica: {card['title'][:40]}",
                    options=["PULL", "PUSH", "WEIGHT"],
                    horizontal=True,
                    key=f"classify_{card['id']}",
                    format_func=lambda x: f"{CARD_CATEGORIES[x]['icon']} {x}",
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

# ── Sezione Risultati ────────────────────────────────────────────────────────

with tab_results:
    responses = state.get_quiz_responses()

    if not responses:
        st.info("Nessuna risposta ancora. Aspetta che i partecipanti completino la mappatura!")
    else:
        st.metric("Risposte ricevute", len(responses))

        if st.button("Aggiorna risultati", use_container_width=True):
            st.rerun()

        # ── Riepilogo aggregato: quante carte per categoria ──
        st.subheader("Distribuzione complessiva")

        total_pull = 0
        total_push = 0
        total_weight = 0
        for r in responses:
            for card_id, cat in r["answers"].items():
                if cat == "PULL":
                    total_pull += 1
                elif cat == "PUSH":
                    total_push += 1
                elif cat == "WEIGHT":
                    total_weight += 1

        fig_summary = go.Figure(
            data=[
                go.Bar(
                    x=["PULL", "PUSH", "WEIGHT"],
                    y=[total_pull, total_push, total_weight],
                    marker_color=[
                        CARD_CATEGORIES["PULL"]["color"],
                        CARD_CATEGORIES["PUSH"]["color"],
                        CARD_CATEGORIES["WEIGHT"]["color"],
                    ],
                    text=[total_pull, total_push, total_weight],
                    textposition="outside",
                )
            ]
        )
        fig_summary.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(title="Classificazioni totali"),
        )
        st.plotly_chart(fig_summary, use_container_width=True)

        # ── Distribuzione per carta (stacked bar) ──
        st.subheader("Distribuzione per fenomeno")

        for card in PHENOMENON_CARDS:
            votes = [r["answers"].get(card["id"], "") for r in responses]
            n_pull = votes.count("PULL")
            n_push = votes.count("PUSH")
            n_weight = votes.count("WEIGHT")
            total = n_pull + n_push + n_weight

            if total == 0:
                continue

            # Calcola percentuali
            pct_pull = n_pull / total * 100
            pct_push = n_push / total * 100
            pct_weight = n_weight / total * 100

            # Categoria prevalente
            max_cat = max(
                [("PULL", n_pull), ("PUSH", n_push), ("WEIGHT", n_weight)],
                key=lambda x: x[1],
            )
            consensus = max_cat[1] / total >= 0.7

            col_info, col_chart = st.columns([1, 2])
            with col_info:
                st.markdown(f"**{card['title']}**")
                icon = CARD_CATEGORIES[max_cat[0]]["icon"]
                label = max_cat[0]
                if consensus:
                    st.caption(f"{icon} **{label}** (consenso forte)")
                else:
                    st.caption(f"{icon} {label} (opinioni divise)")
            with col_chart:
                fig_card = go.Figure()
                fig_card.add_trace(
                    go.Bar(
                        y=[""],
                        x=[pct_pull],
                        orientation="h",
                        name="PULL",
                        marker_color=CARD_CATEGORIES["PULL"]["color"],
                        text=f"{n_pull}" if n_pull else "",
                        textposition="inside",
                    )
                )
                fig_card.add_trace(
                    go.Bar(
                        y=[""],
                        x=[pct_push],
                        orientation="h",
                        name="PUSH",
                        marker_color=CARD_CATEGORIES["PUSH"]["color"],
                        text=f"{n_push}" if n_push else "",
                        textposition="inside",
                    )
                )
                fig_card.add_trace(
                    go.Bar(
                        y=[""],
                        x=[pct_weight],
                        orientation="h",
                        name="WEIGHT",
                        marker_color=CARD_CATEGORIES["WEIGHT"]["color"],
                        text=f"{n_weight}" if n_weight else "",
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
                    fig_card,
                    use_container_width=True,
                    key=f"dist_{card['id']}",
                )

        # ── Nota del facilitatore ──
        st.divider()
        st.subheader("Nota del facilitatore")
        st.markdown(
            "*Clicca su ogni fenomeno per vedere la classificazione suggerita dagli esperti.*"
        )

        for card in PHENOMENON_CARDS:
            suggested = card["suggested_category"]
            icon = CARD_CATEGORIES[suggested]["icon"]
            with st.expander(f"{card['title']}"):
                st.markdown(f"**Classificazione suggerita:** {icon} **{suggested}**")
                st.markdown(card["description"])

                # Confronto con le risposte
                votes = [r["answers"].get(card["id"], "") for r in responses]
                n_match = votes.count(suggested)
                total = len(votes)
                if total > 0:
                    pct = n_match / total * 100
                    if pct >= 70:
                        st.success(
                            f"Il {pct:.0f}% dei partecipanti concorda con la classificazione suggerita."
                        )
                    elif pct >= 40:
                        st.warning(
                            f"Solo il {pct:.0f}% concorda. Opinioni divise: ottimo spunto di discussione!"
                        )
                    else:
                        st.error(
                            f"Solo il {pct:.0f}% concorda. La maggioranza ha una visione diversa: discutiamone!"
                        )

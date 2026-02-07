"""Pagina 1: Il Polso della Classe - Quiz interattivo sull'AI nel food."""

import streamlit as st
import plotly.graph_objects as go
import uuid

from utils.shared_state import get_shared_state
from utils.config import QUIZ_QUESTIONS, APP_ICON

st.set_page_config(page_title="Il Polso della Classe", page_icon=APP_ICON, layout="wide")

state = get_shared_state()

st.title("Il Polso della Classe")
st.markdown(
    "Quanto ne sai (o credi di sapere) sull'AI nel mondo del food? "
    "Rispondi **individualmente** — i risultati appariranno in tempo reale!"
)

# Genera un ID studente per questa sessione browser
if "student_id" not in st.session_state:
    st.session_state.student_id = str(uuid.uuid4())[:8]

# ── Sezione Quiz ─────────────────────────────────────────────────────────────

tab_quiz, tab_results = st.tabs(["Rispondi al quiz", "Risultati della classe"])

with tab_quiz:
    st.markdown("**Per ogni affermazione, indica quanto sei d'accordo** (1 = per niente, 5 = totalmente)")

    with st.form("quiz_form"):
        answers = {}
        for q in QUIZ_QUESTIONS:
            answers[q["id"]] = st.slider(
                q["text"],
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Per niente d'accordo, 5 = Totalmente d'accordo",
            )

        submitted = st.form_submit_button(
            "Invia le mie risposte", use_container_width=True, type="primary"
        )

        if submitted:
            state.add_quiz_response(st.session_state.student_id, answers)
            st.success("Risposte inviate! Vai al tab **Risultati della classe** per vedere i grafici.")

# ── Sezione Risultati ────────────────────────────────────────────────────────

with tab_results:
    responses = state.get_quiz_responses()

    if not responses:
        st.info("Nessuna risposta ancora. Aspetta che i tuoi compagni rispondano!")
    else:
        st.metric("Risposte ricevute", len(responses))

        if st.button("Aggiorna risultati", use_container_width=True):
            st.rerun()

        # Calcola medie per domanda
        question_avgs = {}
        question_distributions = {}
        for q in QUIZ_QUESTIONS:
            vals = [r["answers"].get(q["id"], 3) for r in responses]
            question_avgs[q["id"]] = sum(vals) / len(vals) if vals else 0
            question_distributions[q["id"]] = vals

        # ── Grafico a barre: media per domanda ──
        st.subheader("Media delle risposte")

        labels = [q["text"][:60] + "..." if len(q["text"]) > 60 else q["text"] for q in QUIZ_QUESTIONS]
        avgs = [question_avgs[q["id"]] for q in QUIZ_QUESTIONS]

        colors = []
        for avg in avgs:
            if avg < 2.5:
                colors.append("#e74c3c")
            elif avg < 3.5:
                colors.append("#f39c12")
            else:
                colors.append("#2ecc71")

        fig = go.Figure(
            data=[
                go.Bar(
                    y=labels,
                    x=avgs,
                    orientation="h",
                    marker_color=colors,
                    text=[f"{a:.1f}" for a in avgs],
                    textposition="outside",
                )
            ]
        )
        fig.update_layout(
            xaxis=dict(range=[0, 5.5], title="Media (1-5)"),
            height=80 * len(QUIZ_QUESTIONS),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Distribuzione per domanda ──
        st.subheader("Distribuzione delle risposte")
        for q in QUIZ_QUESTIONS:
            vals = question_distributions[q["id"]]
            counts = [vals.count(i) for i in range(1, 6)]

            col_q, col_chart = st.columns([1, 2])
            with col_q:
                st.markdown(f"**{q['text']}**")
                avg = question_avgs[q["id"]]
                st.caption(f"Media: **{avg:.1f}** su {len(vals)} risposte")
            with col_chart:
                fig2 = go.Figure(
                    data=[
                        go.Bar(
                            x=["1", "2", "3", "4", "5"],
                            y=counts,
                            marker_color=["#e74c3c", "#e67e22", "#f1c40f", "#27ae60", "#2ecc71"],
                        )
                    ]
                )
                fig2.update_layout(
                    height=120,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(title=""),
                    yaxis=dict(title="", dtick=1),
                    showlegend=False,
                )
                st.plotly_chart(fig2, use_container_width=True)

        # ── Myth Busting ──
        st.divider()
        st.subheader("Myth Busting: la realtà dietro le opinioni")
        st.markdown("*Clicca su ogni domanda per scoprire cosa dicono i dati reali!*")

        for q in QUIZ_QUESTIONS:
            with st.expander(q["text"]):
                avg = question_avgs[q["id"]]
                if avg >= 3.5:
                    st.markdown(f"**La classe è piuttosto d'accordo** (media: {avg:.1f}/5)")
                elif avg >= 2.5:
                    st.markdown(f"**La classe è divisa** (media: {avg:.1f}/5)")
                else:
                    st.markdown(f"**La classe è piuttosto scettica** (media: {avg:.1f}/5)")
                st.markdown(q["myth_bust"])

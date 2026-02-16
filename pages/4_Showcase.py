"""Pagina 4: Showcase & Riflessione - Dashboard facilitatore e sistema di voto."""

import streamlit as st
import plotly.graph_objects as go
import uuid
from collections import Counter

from utils.shared_state import get_shared_state
from utils.config import APP_ICON, PHENOMENON_CARDS, CARD_CATEGORIES
from utils.styles import inject_custom_css, render_phase_bar

st.set_page_config(page_title="Showcase & Riflessione", page_icon=APP_ICON, layout="wide")

inject_custom_css()
state = get_shared_state()

render_phase_bar(4)

st.title("🏆 Showcase & Riflessione")

# ── Selezione vista ──────────────────────────────────────────────────────────

view = st.radio(
    "Seleziona la vista",
    options=["📊 Vista Facilitatore (da proiettare)", "🗳️ Vista Partecipante (vota)"],
    horizontal=True,
)

all_groups = state.get_all_groups()
groups_with_cards = {
    name: data for name, data in all_groups.items()
    if data.get("scenario_card")
}

# ── VISTA FACILITATORE ──────────────────────────────────────────────────────

if view == "📊 Vista Facilitatore (da proiettare)":
    if st.button("Aggiorna dashboard", use_container_width=True):
        st.rerun()

    if not groups_with_cards:
        st.info("Nessun gruppo ha ancora completato la scenario card.")
        st.stop()

    # ── Stat cards ──
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-value">{len(groups_with_cards)}</span>
            <span class="stat-label">Scenari completati</span>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        n_votes = len(state.get_all_votes())
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-value">{n_votes}</span>
            <span class="stat-label">Voti ricevuti</span>
        </div>
        """, unsafe_allow_html=True)
    with col_s3:
        n_refl = len(state.get_reflections())
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-value">{n_refl}</span>
            <span class="stat-label">Riflessioni</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Scenario Card Grid ──
    st.subheader(f"Gli Scenari del 2035 ({len(groups_with_cards)} gruppi)")

    cols = st.columns(min(len(groups_with_cards), 3))
    for i, (name, data) in enumerate(groups_with_cards.items()):
        card = data["scenario_card"]
        scenario = data["scenario"]
        has_advisor = data.get("coach_system_prompt") is not None

        with cols[i % len(cols)]:
            # Gallery card with header
            st.markdown(f"""
            <div class="gallery-card">
                <div class="gallery-header">
                    <h4>{card['scenario_title_custom']}</h4>
                    <p>Gruppo: {name} | {scenario['title']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):
                advisor_image = data.get("coach_image_url")
                if advisor_image:
                    st.image(advisor_image, width=200)

                st.markdown(
                    f"**🔮 Futuro 2035:** {card['future_description']}"
                )

                col_hs, col_ss = st.columns(2)
                with col_hs:
                    st.markdown(
                        f"**💼 Cosa cambia:**\n{card['impact_on_enterprises']}"
                    )
                with col_ss:
                    st.markdown(
                        f"**🔑 Fattori chiave:**\n{card['key_factors']}"
                    )

                st.markdown(
                    f"**💡 Raccomandazioni:** {card['strategic_recommendations']}"
                )

                if card.get("new_jobs_and_skills"):
                    st.markdown(
                        f"**🎓 Nuovi lavori/competenze:** {card['new_jobs_and_skills']}"
                    )
                if card.get("career_reflection"):
                    st.markdown(
                        f"**🚀 Il loro futuro:** {card['career_reflection']}"
                    )

                if has_advisor:
                    st.success("🤖 Assistente AI creato")
                else:
                    st.warning("Assistente non ancora creato")

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
        card_results = []
        for card in PHENOMENON_CARDS:
            votes = [r["answers"].get(card["id"], "") for r in quiz_responses]
            n_like = votes.count("MI_PIACE")
            n_dislike = votes.count("NON_MI_PIACE")
            total = n_like + n_dislike
            if total > 0:
                pct_like = n_like / total * 100
                card_results.append({
                    "title": f"{card['emoji']} {card['title'][:35]}",
                    "n_like": n_like,
                    "n_dislike": n_dislike,
                    "total": total,
                    "pct_like": pct_like,
                })

        if card_results:
            # Ordina per % mi piace (dal piu' popolare)
            card_results.sort(key=lambda x: x["pct_like"], reverse=True)
            labels = [r["title"] for r in card_results]
            colors = [
                CARD_CATEGORIES["MI_PIACE"]["color"] if r["pct_like"] >= 50
                else CARD_CATEGORIES["NON_MI_PIACE"]["color"]
                for r in card_results
            ]
            pcts = [r["pct_like"] for r in card_results]

            fig_map = go.Figure(
                data=[
                    go.Bar(
                        y=labels,
                        x=pcts,
                        orientation="h",
                        marker_color=colors,
                        text=[
                            f"👍 {r['pct_like']:.0f}%"
                            for r in card_results
                        ],
                        textposition="outside",
                    )
                ]
            )
            fig_map.update_layout(
                xaxis=dict(range=[0, 110], title="% Mi piace"),
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
            ("🎯 Scenario piu' convincente", "Scenario piu' convincente"),
            ("🏆 Scenario piu' originale", "Scenario piu' originale"),
            ("🤖 Assistente AI migliore", "Assistente AI migliore"),
        ]
        medals = ["🥇", "🥈", "🥉"]

        for cat_display, cat_key in categories:
            cat_votes = [v.get(cat_key) for v in votes.values() if v.get(cat_key)]
            if cat_votes:
                counts = Counter(cat_votes)
                ranking = counts.most_common(3)

                st.markdown(f"#### {cat_display}")
                for rank_idx, (group_name_v, count) in enumerate(ranking):
                    medal = medals[rank_idx] if rank_idx < len(medals) else ""
                    st.markdown(f"{medal} **{group_name_v}** — {count} voti")

                fig_v = go.Figure(
                    data=[
                        go.Bar(
                            x=list(counts.keys()),
                            y=list(counts.values()),
                            marker_color=[
                                "#FF6B35" if k == ranking[0][0] else "#3498db"
                                for k in counts.keys()
                            ],
                        )
                    ]
                )
                fig_v.update_layout(
                    height=200, margin=dict(l=0, r=0, t=10, b=0)
                )
                st.plotly_chart(fig_v, use_container_width=True)

    # ── Riflessioni raccolte ──
    st.divider()
    reflections = state.get_reflections()
    st.subheader(f"Riflessioni finali ({len(reflections)} risposte)")

    if reflections:
        refl_questions = [
            ("sorpresa", "Cosa vi ha sorpreso dell'AI?"),
            ("competenza", "Competenze/lavori del futuro che colpiscono"),
            ("bilancio", "Potenzialita' vs limiti dell'AI"),
        ]
        for key, label in refl_questions:
            answers = [r.get(key, "") for r in reflections.values() if r.get(key)]
            if answers:
                with st.expander(f"**{label}** ({len(answers)} risposte)"):
                    for a in answers:
                        st.markdown(f"- {a}")
    else:
        st.info("Nessuna riflessione ancora. I partecipanti possono compilarla nella vista Partecipante.")

    # ── Presentazioni caricate ──
    st.divider()
    presentations = state.get_all_presentations()
    st.subheader(f"Presentazioni caricate ({len(presentations)})")

    if presentations:
        for gname, pinfo in presentations.items():
            col_name, col_file, col_dl = st.columns([2, 2, 1])
            with col_name:
                st.markdown(f"**{gname}**")
            with col_file:
                st.caption(f"{pinfo['filename']} — {pinfo['uploaded_at'][:16]}")
            with col_dl:
                pdata = state.get_presentation(gname)
                if pdata:
                    st.download_button(
                        "Scarica",
                        data=pdata["data_bytes"],
                        file_name=pdata["filename"],
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        key=f"dl_{gname}",
                    )
    else:
        st.info("Nessuna presentazione caricata ancora.")

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
    <div class="info-banner">
        <p><strong>Vota i lavori degli altri gruppi!</strong> Dopo le presentazioni,
        vota per ogni categoria. Non puoi votare il tuo gruppo.</p>
    </div>
    """, unsafe_allow_html=True)

    votable = [name for name in groups_with_cards.keys() if name != my_group]

    if not votable:
        st.warning(
            "Non ci sono altri gruppi da votare "
            "(o il tuo gruppo e' l'unico con una scenario card)."
        )
        st.stop()

    # Mostra le scenario card in sintesi
    st.subheader("Riepilogo Scenari")
    for name in votable:
        data = groups_with_cards[name]
        card = data["scenario_card"]
        with st.expander(f"**{name}** — {card['scenario_title_custom']}"):
            st.markdown(f"*Tecnica: {data['scenario']['title']}*")
            advisor_image = data.get("coach_image_url")
            if advisor_image:
                st.image(advisor_image, width=150)
            st.markdown(f"**🔮 Futuro 2035:** {card['future_description']}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"**💼 Cosa cambia nel food:** {card['impact_on_enterprises']}"
                )
            with col2:
                st.markdown(f"**🔑 Fattori chiave:** {card['key_factors']}")
            st.markdown(
                f"**💡 Raccomandazioni:** {card['strategic_recommendations']}"
            )
            if card.get("new_jobs_and_skills"):
                st.markdown(
                    f"**🎓 Nuovi lavori/competenze:** {card['new_jobs_and_skills']}"
                )
            if card.get("career_reflection"):
                st.markdown(
                    f"**🚀 Il loro futuro:** {card['career_reflection']}"
                )

    # Form voto
    st.divider()
    st.subheader("Esprimi il tuo voto")

    with st.form("vote_form"):
        v_convincente = st.selectbox(
            "🎯 Scenario piu' CONVINCENTE",
            options=votable,
            format_func=lambda x: f"{x} — {groups_with_cards[x]['scenario_card']['scenario_title_custom']}",
        )
        v_originale = st.selectbox(
            "🏆 Scenario piu' ORIGINALE",
            options=votable,
            format_func=lambda x: f"{x} — {groups_with_cards[x]['scenario_card']['scenario_title_custom']}",
        )
        v_advisor = st.selectbox(
            "🤖 Assistente AI MIGLIORE",
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
                    "Scenario piu' convincente": v_convincente,
                    "Scenario piu' originale": v_originale,
                    "Assistente AI migliore": v_advisor,
                },
            )
            st.success(
                "Voto registrato! Il facilitatore vedra' i risultati "
                "in tempo reale nella dashboard."
            )
            st.balloons()

    # ── Riflessione finale ────────────────────────────────────────────────
    st.divider()

    st.markdown("""
    <div class="reflection-box">
        <h3>Cosa vi portate a casa?</h3>
        <p>Dopo aver esplorato il food tech, riflettete su cosa avete scoperto
        sull'AI, sulle professioni del futuro e sulle vostre competenze.</p>
    </div>
    """, unsafe_allow_html=True)

    r_sorpresa = st.text_area(
        "Qual e' la cosa piu' sorprendente che avete scoperto sull'AI?",
        key="refl_sorpresa",
        height=80,
        placeholder="Es: non sapevo che l'AI potesse creare ricette, mi ha colpito che...",
    )
    r_competenza = st.text_area(
        "Quale competenza o lavoro del futuro vi ha colpito di piu'?",
        key="refl_competenza",
        height=80,
        placeholder="Es: il food technologist, analizzare dati per i ristoranti, creare app...",
    )
    r_bilancio = st.text_area(
        "L'AI ha piu' potenzialita' o piu' limiti? Perche'?",
        key="refl_bilancio",
        height=80,
        placeholder="Es: ha tante potenzialita' ma anche rischi come la privacy, il lavoro...",
    )

    if st.button("Salva riflessione", type="primary", use_container_width=True):
        reflection = {
            "sorpresa": r_sorpresa.strip(),
            "competenza": r_competenza.strip(),
            "bilancio": r_bilancio.strip(),
        }
        if any(reflection.values()):
            state.save_reflection(st.session_state.voter_id, reflection)
            st.success("Riflessione salvata!")
        else:
            st.warning("Scrivi almeno una risposta prima di salvare.")

    # ── Upload presentazione ─────────────────────────────────────────────
    st.divider()

    st.markdown("""
    <div class="info-banner">
        <p><strong>Carica la presentazione del tuo gruppo!</strong>
        Caricate il file PowerPoint che userete per presentare
        il vostro progetto nella prossima lezione.</p>
    </div>
    """, unsafe_allow_html=True)

    if my_group:
        existing_pres = state.get_presentation(my_group)
        if existing_pres:
            st.success(
                f"Presentazione gia' caricata: **{existing_pres['filename']}** "
                f"({existing_pres['uploaded_at'][:16]})"
            )
            st.caption("Puoi caricare una nuova versione per sostituirla.")

        uploaded_file = st.file_uploader(
            "Carica la presentazione (.pptx, .ppt, .pdf)",
            type=["pptx", "ppt", "pdf"],
            key="ppt_upload",
        )

        if uploaded_file is not None:
            if st.button(
                "Conferma caricamento",
                type="primary",
                use_container_width=True,
            ):
                state.save_presentation(
                    my_group,
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                )
                st.success(f"Presentazione **{uploaded_file.name}** caricata!")
                st.rerun()
    else:
        st.warning("Registra il tuo gruppo dalla Home per caricare la presentazione.")

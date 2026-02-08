"""CSS globale e componenti HTML riusabili per il workshop."""

import streamlit as st

GLOBAL_CSS = """
<style>
/* ── Pill badge per categorie ── */
.cat-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9em;
    color: white;
    margin: 0 4px;
}
.cat-pill-pull { background: #2ecc71; }
.cat-pill-push { background: #3498db; }
.cat-pill-weight { background: #e74c3c; }

/* ── Phase bar ── */
.phase-bar {
    display: flex;
    gap: 0;
    margin-bottom: 1.5rem;
    border-radius: 8px;
    overflow: hidden;
}
.phase-step {
    flex: 1;
    text-align: center;
    padding: 10px 4px;
    font-size: 0.85em;
    font-weight: 600;
    color: #999;
    background: #e8e8e8;
    border-right: 2px solid white;
    transition: all 0.3s;
}
.phase-step:last-child { border-right: none; }
.phase-step.active {
    background: #FF6B35;
    color: white;
}
.phase-step.completed {
    background: #2ecc71;
    color: white;
}

/* ── Step card (home) ── */
.step-card {
    text-align: center;
    padding: 1.2rem 0.8rem;
    border-radius: 12px;
    background: #F0F2F6;
    border: 2px solid #e0e0e0;
    height: 100%;
}
.step-card .step-emoji { font-size: 2.5rem; }
.step-card .step-time {
    color: #FF6B35;
    font-weight: 700;
    margin: 0;
}
.step-card .step-desc {
    font-size: 0.9em;
    color: #666;
    margin-top: 0.3rem;
}

/* ── Mission card (scenario intro) ── */
.mission-card {
    background: linear-gradient(135deg, #FF6B35 0%, #FF8E53 100%);
    color: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.mission-card h3 { color: white; margin-top: 0; }
.mission-card p { font-size: 1.05em; }
.mission-kw {
    display: inline-block;
    background: rgba(255,255,255,0.25);
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.85em;
    margin: 3px 2px;
}

/* ── Scenario preview (dark card) ── */
.scenario-preview {
    background: #1A1A2E;
    color: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.scenario-preview h3 {
    color: #FF6B35;
    margin-top: 0;
}
.scenario-preview hr {
    border-color: rgba(255,255,255,0.15);
}

/* ── Gallery card header (showcase) ── */
.gallery-header {
    background: linear-gradient(135deg, #1A1A2E, #16213E);
    color: white;
    border-radius: 12px 12px 0 0;
    padding: 1rem;
    text-align: center;
}
.gallery-header h4 {
    color: #FF6B35;
    margin: 0;
}
.gallery-header p {
    margin: 0.3rem 0 0 0;
    opacity: 0.8;
    font-size: 0.9em;
}
</style>
"""

PHASE_LABELS = [
    ("1", "🗺️", "Mappatura"),
    ("2", "🔮", "Scenari 2035"),
    ("3", "🤖", "AI Lab"),
    ("4", "🏆", "Showcase"),
]


def inject_custom_css():
    """Inietta il CSS globale nella pagina. Chiamare in testa a ogni pagina."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_phase_bar(current_phase: int):
    """Mostra la barra di progresso del workshop.

    Args:
        current_phase: 1-4 (la fase corrente). Le fasi precedenti sono 'completed'.
    """
    steps_html = ""
    for num, emoji, label in PHASE_LABELS:
        phase_num = int(num)
        if phase_num < current_phase:
            cls = "completed"
        elif phase_num == current_phase:
            cls = "active"
        else:
            cls = ""
        steps_html += f'<div class="phase-step {cls}">{emoji} {label}</div>'

    st.markdown(f'<div class="phase-bar">{steps_html}</div>', unsafe_allow_html=True)

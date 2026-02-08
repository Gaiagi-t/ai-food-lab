"""CSS globale e componenti HTML riusabili per il workshop."""

import streamlit as st

GLOBAL_CSS = """
<style>
/* ── Reset e base ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FAFAFA 0%, #FFF5F0 100%);
}

/* ── Pill badge per categorie ── */
.cat-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9em;
    color: white;
    margin: 0 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}
.cat-pill-pull { background: linear-gradient(135deg, #2ecc71, #27ae60); }
.cat-pill-push { background: linear-gradient(135deg, #3498db, #2980b9); }
.cat-pill-weight { background: linear-gradient(135deg, #e74c3c, #c0392b); }

/* ── Phase bar ── */
.phase-bar {
    display: flex;
    gap: 0;
    margin-bottom: 1.5rem;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.phase-step {
    flex: 1;
    text-align: center;
    padding: 12px 4px;
    font-size: 0.85em;
    font-weight: 600;
    color: #999;
    background: #e8e8e8;
    border-right: 2px solid white;
    transition: all 0.3s;
}
.phase-step:last-child { border-right: none; }
.phase-step.active {
    background: linear-gradient(135deg, #FF6B35, #FF8E53);
    color: white;
    text-shadow: 0 1px 2px rgba(0,0,0,0.15);
}
.phase-step.completed {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
    color: white;
}

/* ── Hero section (home) ── */
.hero-section {
    background: linear-gradient(135deg, #FF6B35 0%, #FF8E53 40%, #FFB347 100%);
    color: white;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(255, 107, 53, 0.25);
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-section h1 {
    color: white;
    font-size: 2.2rem;
    margin: 0 0 0.5rem 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
.hero-section .hero-subtitle {
    font-size: 1.15rem;
    opacity: 0.95;
    max-width: 700px;
    margin: 0 auto 1rem;
    line-height: 1.5;
}
.hero-section .hero-emoji {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    display: block;
}

/* ── Step card (home) ── */
.step-card {
    text-align: center;
    padding: 1.5rem 1rem;
    border-radius: 16px;
    background: white;
    border: none;
    height: 100%;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.step-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.step-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #FF6B35, #FF8E53);
}
.step-card .step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #FF6B35, #FF8E53);
    color: white;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}
.step-card .step-emoji {
    font-size: 2.8rem;
    margin-bottom: 0.5rem;
    display: block;
}
.step-card h4 {
    margin: 0.3rem 0;
    color: #1A1A2E;
}
.step-card .step-time {
    display: inline-block;
    background: linear-gradient(135deg, #FF6B35, #FF8E53);
    color: white;
    padding: 2px 12px;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.8em;
    margin: 0.3rem 0;
}
.step-card .step-desc {
    font-size: 0.9em;
    color: #666;
    margin-top: 0.5rem;
    line-height: 1.4;
}

/* ── Phenomenon card (mappatura) ── */
.phenom-card {
    border-radius: 14px;
    padding: 1.2rem 1.2rem 0.8rem;
    margin-bottom: 0.3rem;
    background: white;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    border-left: 5px solid #ddd;
    transition: transform 0.2s, box-shadow 0.2s;
}
.phenom-card:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 18px rgba(0,0,0,0.1);
}
.phenom-card.pull-hint { border-left-color: #2ecc71; }
.phenom-card.push-hint { border-left-color: #3498db; }
.phenom-card.weight-hint { border-left-color: #e74c3c; }
.phenom-card .phenom-emoji {
    font-size: 2.2rem;
    margin-bottom: 0.3rem;
    display: block;
}
.phenom-card .phenom-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1A1A2E;
    margin: 0;
}
.phenom-card .phenom-desc {
    font-size: 0.88rem;
    color: #666;
    margin-top: 0.3rem;
    line-height: 1.4;
}

/* ── Mission card (scenario intro) ── */
.mission-card {
    background: linear-gradient(135deg, #FF6B35 0%, #FF8E53 60%, #FFB347 100%);
    color: white;
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1rem 0;
    box-shadow: 0 6px 24px rgba(255, 107, 53, 0.2);
    position: relative;
    overflow: hidden;
}
.mission-card::after {
    content: '🔮';
    position: absolute;
    top: -10px;
    right: 10px;
    font-size: 5rem;
    opacity: 0.12;
    pointer-events: none;
}
.mission-card h3 { color: white; margin-top: 0; }
.mission-card p { font-size: 1.05em; }
.mission-kw {
    display: inline-block;
    background: rgba(255,255,255,0.25);
    padding: 4px 14px;
    border-radius: 12px;
    font-size: 0.85em;
    margin: 3px 2px;
    backdrop-filter: blur(4px);
}

/* ── Role card (AI Lab) ── */
.role-card {
    text-align: center;
    padding: 1.3rem 0.8rem;
    border-radius: 16px;
    background: white;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    border: 2px solid transparent;
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    height: 100%;
}
.role-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    border-color: #FF6B35;
}
.role-card .role-emoji {
    font-size: 3rem;
    display: block;
    margin-bottom: 0.5rem;
}
.role-card .role-label {
    font-weight: 700;
    font-size: 1rem;
    color: #1A1A2E;
    margin-bottom: 0.3rem;
}
.role-card .role-desc {
    font-size: 0.85rem;
    color: #666;
    line-height: 1.4;
}

/* ── Scenario preview (dark card) ── */
.scenario-preview {
    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
    color: white;
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(26, 26, 46, 0.3);
    position: relative;
    overflow: hidden;
}
.scenario-preview::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(255,107,53,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.scenario-preview h3 {
    color: #FF6B35;
    margin-top: 0;
}
.scenario-preview hr {
    border-color: rgba(255,255,255,0.12);
}

/* ── Gallery card (showcase) ── */
.gallery-card {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.gallery-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
.gallery-header {
    background: linear-gradient(135deg, #1A1A2E, #16213E);
    color: white;
    padding: 1.2rem;
    text-align: center;
}
.gallery-header h4 {
    color: #FF6B35;
    margin: 0;
    font-size: 1.1rem;
}
.gallery-header p {
    margin: 0.3rem 0 0 0;
    opacity: 0.8;
    font-size: 0.88em;
}

/* ── Reflection section ── */
.reflection-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1rem 0;
    text-align: center;
    box-shadow: 0 6px 24px rgba(102, 126, 234, 0.25);
}
.reflection-box h3 {
    color: white;
    margin-top: 0;
}
.reflection-box p {
    opacity: 0.9;
    font-size: 1rem;
    max-width: 600px;
    margin: 0 auto;
}

/* ── Vote category card ── */
.vote-cat {
    background: white;
    border-radius: 14px;
    padding: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}
.vote-cat .vote-cat-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

/* ── Stat card ── */
.stat-card {
    text-align: center;
    padding: 1rem;
    border-radius: 14px;
    background: white;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.stat-card .stat-value {
    font-size: 2rem;
    font-weight: 800;
    color: #FF6B35;
    display: block;
}
.stat-card .stat-label {
    font-size: 0.85rem;
    color: #666;
}

/* ── Info banner ── */
.info-banner {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    border-left: 4px solid #FF6B35;
    margin: 0.5rem 0;
}
.info-banner p {
    margin: 0;
    color: #444;
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

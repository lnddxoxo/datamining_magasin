# ─────────────────────────────────────────
# utils/styles.py
# ─────────────────────────────────────────

import streamlit as st

C_DARK  = "#475E72"
C_MID   = "#73828E"
C_WARM  = "#E1CBB2"
C_LIGHT = "#DEDEDE"
C_BG    = "#EAE6E2"

PALETTE = [C_DARK, C_MID, C_WARM, C_LIGHT, C_BG]


def inject_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Crimson+Pro:wght@400;600;700&display=swap');

        /* ── Fond général ── */
        .stApp {{
            background: #F2EEE9;
            font-family: 'DM Sans', sans-serif;
        }}

        /* ══════════════════════════════════════
           TOPBAR
        ══════════════════════════════════════ */
        header[data-testid="stHeader"] {{
            background-color: {C_DARK} !important;
            box-shadow: none !important;
            border-bottom: none !important;
        }}

        /* ── Cache le texte keyboard_double ── */
        /* C'est le bouton collapse du sidebar */
        [data-testid="stSidebarCollapseButton"] {{
            background: transparent !important;
            border: none !important;
        }}
        [data-testid="stSidebarCollapseButton"] span,
        [data-testid="stSidebarCollapseButton"] p {{
            display: none !important;
        }}
        /* Icône du bouton en blanc pour qu'elle reste visible */
        [data-testid="stSidebarCollapseButton"] svg {{
            fill: {C_BG} !important;
            color: {C_BG} !important;
        }}

        /* ══════════════════════════════════════
           SIDEBAR
           padding-top: 0 pour coller au topbar
           et supprimer le gap entre les deux
        ══════════════════════════════════════ */
        [data-testid="stSidebar"] {{
            background: {C_DARK} !important;
            box-shadow: 2px 0 15px rgba(0,0,0,0.12);
            margin-top: 0 !important;
        }}
        /* Premier div enfant — supprime le padding top */
        [data-testid="stSidebar"] > div:first-child {{
            background: {C_DARK} !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        /* Tous les divs enfants */
        [data-testid="stSidebar"] > div {{
            background: {C_DARK} !important;
        }}
        /* Texte sidebar */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {{
            color: {C_BG} !important;
            font-family: 'DM Sans', sans-serif !important;
        }}
        [data-testid="stSidebar"] hr {{
            border-color: rgba(234,230,226,0.2) !important;
            margin: 0.6rem 0 !important;
        }}

        /* ── Contenu ── */
        .block-container {{
            padding: 2rem 3rem 3rem 3rem;
            max-width: 1200px;
        }}

        /* ── Titres ── */
        h1 {{
            font-family: 'Crimson Pro', serif !important;
            color: {C_DARK} !important;
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            padding-bottom: 10px;
            border-bottom: 2px solid {C_WARM};
            margin-bottom: 1.2rem !important;
        }}
        h2 {{
            font-family: 'Crimson Pro', serif !important;
            color: {C_DARK} !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin-top: 2rem !important;
            margin-bottom: 0.8rem !important;
        }}
        h2::before {{
            content: '';
            display: inline-block;
            width: 4px; height: 18px;
            background: linear-gradient(180deg, {C_WARM}, {C_MID});
            border-radius: 2px;
            margin-right: 10px;
            vertical-align: middle;
        }}
        h3 {{
            font-family: 'DM Sans', sans-serif !important;
            color: {C_MID} !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
        }}

        /* ── Métriques ── */
        [data-testid="stMetric"] {{
            background: white;
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 4px 20px rgba(71,94,114,0.12);
            border-top: 3px solid {C_WARM};
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }}
        [data-testid="stMetric"]:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 30px rgba(71,94,114,0.2);
        }}
        [data-testid="stMetricValue"] {{
            color: {C_DARK} !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            font-family: 'DM Sans', sans-serif !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {C_MID} !important;
            font-size: 0.75rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            font-weight: 500 !important;
        }}

        /* ── Tableaux ── */
        [data-testid="stDataFrame"] {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(71,94,114,0.1);
        }}

        /* ── Onglets ── */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: white;
            border-radius: 12px;
            padding: 6px 8px;
            box-shadow: 0 2px 10px rgba(71,94,114,0.1);
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            width: 100%;
            gap: 6px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            color: {C_MID};
            font-weight: 500;
            font-size: 13px;
            padding: 10px 0;
            text-align: center;
            width: 100%;
            justify-content: center;
            transition: all 0.2s ease;
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {C_DARK}, {C_MID}) !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 3px 10px rgba(71,94,114,0.3);
        }}
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {{
            display: none !important;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: {C_BG};
            color: {C_DARK} !important;
        }}

        /* ══════════════════════════════════════
           BOÎTES — st.info / success / warning
           supprimées et remplacées par nos divs
           via info_box() success_box() warning_box()
           dans utils/charts.py
           Ces règles servent de filet de sécurité
        ══════════════════════════════════════ */
        div[data-testid="stAlert"] {{
            border-radius: 10px !important;
            border: none !important;
            padding: 14px 18px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 14px !important;
        }}
        div[data-testid="stAlert"] svg {{
            display: none !important;
        }}
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span {{
            color: {C_DARK} !important;
        }}
        /* info */
        div[data-testid="stAlert"][data-baseweb="notification"] {{
            background: rgba(71,94,114,0.09) !important;
            border-left: 4px solid {C_DARK} !important;
        }}
        /* success */
        .stSuccess, div[data-testid="stAlert"].stSuccess {{
            background: rgba(225,203,178,0.3) !important;
            border-left: 4px solid {C_WARM} !important;
        }}
        /* warning */
        .stWarning, div[data-testid="stAlert"].stWarning {{
            background: rgba(115,130,142,0.12) !important;
            border-left: 4px solid {C_MID} !important;
        }}

        /* ── Boutons ── */
        .stButton > button {{
            background-color: {C_DARK};
            color: {C_BG};
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1.8rem;
            transition: all 0.25s ease;
            box-shadow: 0 3px 10px rgba(71,94,114,0.3);
        }}
        .stButton > button:hover {{
            background-color: {C_MID};
            transform: translateY(-2px);
        }}

        /* ── Séparateurs ── */
        hr {{
            border: none !important;
            border-top: 1px solid {C_LIGHT} !important;
            margin: 1.8rem 0 !important;
        }}

        /* ── Animation entrée ── */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(16px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        .block-container {{ animation: fadeInUp 0.35s ease-out; }}

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {{ width: 5px; }}
        ::-webkit-scrollbar-track {{ background: {C_BG}; }}
        ::-webkit-scrollbar-thumb {{ background: {C_MID}; border-radius: 3px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: {C_DARK}; }}

        /* ── Expander ── */
        [data-testid="stExpander"] {{
            background: white;
            border-radius: 12px;
            border: 1px solid {C_LIGHT};
            box-shadow: 0 2px 8px rgba(71,94,114,0.08);
        }}

    </style>
    """, unsafe_allow_html=True)
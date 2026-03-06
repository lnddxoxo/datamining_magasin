# ─────────────────────────────────────────
# utils/styles.py
# Gestion des couleurs et du style CSS de l'app
# ─────────────────────────────────────────

import streamlit as st

# ── Palette de couleurs ──────────────────
C_DARK  = "#475E72"   # Bleu ardoise  — fonds, titres
C_MID   = "#73828E"   # Gris bleuté   — cartes, encadrés
C_WARM  = "#E1CBB2"   # Beige chaud   — accents, highlights
C_LIGHT = "#DEDEDE"   # Gris clair    — séparateurs
C_BG    = "#EAE6E2"   # Ivoire        — fond général

# Liste ordonnée pour les graphiques matplotlib
PALETTE = [C_DARK, C_MID, C_WARM, C_LIGHT, C_BG]


def inject_css():
    st.markdown(f"""
    <style>

        /* ── Fond général ── */
        .stApp {{
            background: linear-gradient(135deg, {C_BG} 0%, #d6d0c8 100%);
            font-family: 'Segoe UI', sans-serif;
        }}

        /* ── Barre du haut (header Streamlit) ── */
        header[data-testid="stHeader"] {{
            background-color: {C_DARK};
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {C_DARK} 0%, {C_MID} 100%);
            box-shadow: 4px 0 12px rgba(0,0,0,0.15);
        }}
        [data-testid="stSidebar"] * {{
            color: {C_BG} !important;
        }}

        /* ── Zone de contenu principal ── */
        .block-container {{
            padding: 2rem 3rem 2rem 3rem;
            max-width: 1200px;
        }}

        /* ── Titres ── */
        h1 {{
            color: {C_DARK};
            font-size: 2rem;
            font-weight: 700;
            border-left: 5px solid {C_WARM};
            padding-left: 15px;
            margin-bottom: 0.5rem;
        }}
        h2 {{
            color: {C_DARK};
            font-size: 1.4rem;
            font-weight: 600;
            margin-top: 1.5rem;
        }}
        h3 {{
            color: {C_MID};
            font-size: 1.1rem;
            font-weight: 600;
        }}

        /* ── Cards avec ombres ── */
        [data-testid="stMetric"] {{
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 15px rgba(71, 94, 114, 0.15);
            border-top: 3px solid {C_WARM};
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        [data-testid="stMetric"]:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(71, 94, 114, 0.25);
        }}

        /* ── Métriques valeurs ── */
        [data-testid="stMetricValue"] {{
            color: {C_DARK} !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {C_MID} !important;
            font-size: 0.85rem !important;
        }}

        /* ── Boutons ── */
        .stButton > button {{
            background-color: {C_DARK};
            color: {C_BG};
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1.5rem;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(71,94,114,0.3);
        }}
        .stButton > button:hover {{
            background-color: {C_MID};
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(71,94,114,0.4);
        }}

        /* ── Tableaux ── */
        [data-testid="stDataFrame"] {{
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(71,94,114,0.1);
        }}

        /* ── Onglets ── */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: white;
            border-radius: 10px;
            padding: 4px;
            box-shadow: 0 2px 8px rgba(71,94,114,0.1);
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            color: {C_MID};
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {C_DARK} !important;
            color: white !important;
        }}

        /* ── Sliders ── */
        [data-testid="stSlider"] > div > div > div {{
            background-color: {C_WARM};
        }}

        /* ── Selectbox ── */
        [data-testid="stSelectbox"] > div > div {{
            border-radius: 8px;
            border-color: {C_MID};
        }}

        /* ── Encadrés info/warning ── */
        .stAlert {{
            border-radius: 10px;
            border-left: 4px solid {C_DARK};
        }}

        /* ── Animation d'entrée des pages ── */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        .block-container {{
            animation: fadeInUp 0.4s ease-out;
        }}

        /* ── Séparateurs ── */
        hr {{
            border-color: {C_LIGHT};
            margin: 1.5rem 0;
        }}

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {{
            width: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: {C_BG};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {C_MID};
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {C_DARK};
        }}

    </style>
    """, unsafe_allow_html=True)
# ─────────────────────────────────────────
# app.py
# Point d'entrée principal de l'application
# ─────────────────────────────────────────

import streamlit as st
from utils.styles import inject_css
from streamlit_option_menu import option_menu
from data.loader import load_data
from sections import (
    page1_donnees,
    page2_dashboard,
    page3_segmentation,
    page4_classification,
    page5_prediction,
    page6_recommandations
)

# ── Configuration globale ────────────────
st.set_page_config(
    page_title="Projet Marketing a partir de data mining",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

st.markdown("""
<style>
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem !important;
    }
    section[data-testid="stSidebar"] {
        top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

data_store = load_data()

# ── Liste des pages ───────────────────────
PAGES = [
    "Données",
    "Dashboard",
    "Segmentation",
    "Classification",
    "Prédiction",
    "Recommandations"
]

# ── Session state ─────────────────────────
if "page_active" not in st.session_state:
    st.session_state.page_active = "Données"

# ── Sidebar ───────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 10px 0;'>
            <h3 style='color:#EAE6E2; margin:0;'>Projet Data Mining</h3>
            <p style='color:#E1CBB2; font-size:12px; margin:0;'>
                Magasin de Département
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = option_menu(
        menu_title   = None,
        options      = PAGES,
        icons        = [
            "table",
            "bar-chart",
            "diagram-3",
            "tree",
            "graph-up",
            "lightbulb"
        ],
        default_index = PAGES.index(st.session_state.page_active),
        styles        = {
            "container"        : {"background-color": "#475E72"},
            "icon"             : {"color": "#E1CBB2", "font-size": "16px"},
            "nav-link"         : {
                "color"     : "#EAE6E2",
                "font-size" : "14px",
                "margin"    : "2px 0"
            },
            "nav-link-selected": {"background-color": "#73828E"}
        }
    )

    st.session_state.page_active = page

    st.markdown("---")
    st.markdown(
        "<p style='color:#E1CBB2; font-size:11px;'>"
        "<b>Méthodologie KDD</b><br>"
        "Logbo Axelle & Camara Massaram"
        "</p>",
        unsafe_allow_html=True
    )

# ── Routing ───────────────────────────────
if   page == "Données"        : page1_donnees.show(data_store)
elif page == "Dashboard"      : page2_dashboard.show(data_store)
elif page == "Segmentation"   : page3_segmentation.show(data_store)
elif page == "Classification" : page4_classification.show(data_store)
elif page == "Prédiction"     : page5_prediction.show(data_store)
elif page == "Recommandations": page6_recommandations.show(data_store)
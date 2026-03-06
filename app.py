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

#Configuration de l'apparence globale de l'app

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

with st.sidebar:
    st.markdown(
          f"""
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

    page=option_menu(
        menu_title=None,
         options=[
            "Données",
            "Dashboard",
            "Segmentation",
            "Classification",
            "Prédiction",
            "Recommandations"
        ],
        icons=[
            "table",           # icône pour Données
            "bar-chart",       # icône pour Dashboard
            "diagram-3",       # icône pour Segmentation
            "tree",            # icône pour Classification
            "graph-up",        # icône pour Prédiction
            "lightbulb"        # icône pour Recommandations
        ],
        default_index=0,

        styles={
            "containe" : {"background-color": "#475E72"},
              "icon"             : {"color": "#E1CBB2", "font-size": "16px"},
              "nav-link"         : {
              "color"        : "#EAE6E2",
              "font-size"    : "14px",
               "margin"       : "2px 0"   # espacement entre les liens
            },

             "nav-link-selected": {"background-color": "#73828E"}
        }
    )
            
    st.markdown("---")
    st.markdown(
        "<p style='color:#E1CBB2; font-size:11px;'>"
        "<b>Méthodologie KDD</b><br>"
        "Logbo Axelle & Camara Massaram"
        "</p>",
        unsafe_allow_html=True
    )

if   page == "Données"        : page1_donnees.show(data_store)
elif page == "Dashboard"      : page2_dashboard.show(data_store)
elif page == "Segmentation"   : page3_segmentation.show(data_store)
elif page == "Classification" : page4_classification.show(data_store)
elif page == "Prédiction"     : page5_prediction.show(data_store)
elif page == "Recommandations": page6_recommandations.show(data_store)
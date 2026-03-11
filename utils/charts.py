# ─────────────────────────────────────────
# utils/charts.py
# Fonctions graphiques réutilisables pour toutes les pages
# ─────────────────────────────────────────

import matplotlib.pyplot as plt
from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG, PALETTE

def dark_fig(figsize=(10, 4)):
    # Crée une figure avec 1 graphique au style de la palette
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(C_BG)       # Fond de la figure
    ax.set_facecolor(C_LIGHT)           # Fond du graphique
    ax.tick_params(colors=C_DARK)       # Couleur des graduations
    ax.xaxis.label.set_color(C_DARK)    # Couleur label axe X
    ax.yaxis.label.set_color(C_DARK)    # Couleur label axe Y
    ax.title.set_color(C_DARK)          # Couleur du titre
    for spine in ax.spines.values():
        spine.set_edgecolor(C_MID)      # Couleur des bordures
    return fig, ax

def dark_fig2(figsize=(14, 4)):
    # Crée une figure avec 2 graphiques côte à côte
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    fig.patch.set_facecolor(C_BG)
    for ax in axes:
        ax.set_facecolor(C_LIGHT)
        ax.tick_params(colors=C_DARK)
        ax.xaxis.label.set_color(C_DARK)
        ax.yaxis.label.set_color(C_DARK)
        ax.title.set_color(C_DARK)
        for spine in ax.spines.values():
            spine.set_edgecolor(C_MID)
    return fig, axes

def style_legend(ax):
    # Applique le style palette à la légende d'un graphique
    legend = ax.get_legend()
    if legend:
        legend.get_frame().set_facecolor(C_BG)
        legend.get_frame().set_edgecolor(C_MID)
        for text in legend.get_texts():
            text.set_color(C_DARK)

def info_box(text):
    import streamlit as st
    st.markdown(
        "<div style='background-color:#dce3ea;border-left:4px solid #475E72;"
        "border-radius:6px;padding:10px 14px;margin-bottom:8px;font-size:0.9rem;'>"
        + text + "</div>",
        unsafe_allow_html=True
    )

def success_box(text):
    import streamlit as st
    st.markdown(
        "<div style='background-color:#e8f4e8;border-left:4px solid #2d7a2d;"
        "border-radius:6px;padding:10px 14px;margin-bottom:8px;font-size:0.9rem;'>"
        + text + "</div>",
        unsafe_allow_html=True
    )

def warning_box(text):
    import streamlit as st
    st.markdown(
        "<div style='background-color:#fdf3e3;border-left:4px solid #c8860a;"
        "border-radius:6px;padding:10px 14px;margin-bottom:8px;font-size:0.9rem;'>"
        + text + "</div>",
        unsafe_allow_html=True
    )

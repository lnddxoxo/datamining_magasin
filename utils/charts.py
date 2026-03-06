# ─────────────────────────────────────────
# utils/charts.py
# Fonctions graphiques + boîtes de message
# ─────────────────────────────────────────

import streamlit as st
import matplotlib.pyplot as plt
from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG, PALETTE


# ══════════════════════════════════════════
# BOÎTES DE MESSAGE — remplacent st.info()
# st.success() st.warning() pour avoir les
# bonnes couleurs de la palette
# ══════════════════════════════════════════

def info_box(text):
    """Remplace st.info() — fond ardoise discret"""
    st.markdown(f"""
    <div style='
        background: rgba(71,94,114,0.09);
        border-left: 4px solid {C_DARK};
        border-radius: 10px;
        padding: 14px 18px;
        color: {C_DARK};
        font-family: DM Sans, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        margin: 8px 0;
    '>{text}</div>
    """, unsafe_allow_html=True)


def success_box(text):
    """Remplace st.success() — fond beige chaud"""
    st.markdown(f"""
    <div style='
        background: rgba(225,203,178,0.3);
        border-left: 4px solid {C_WARM};
        border-radius: 10px;
        padding: 14px 18px;
        color: {C_DARK};
        font-family: DM Sans, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        margin: 8px 0;
    '>✅ {text}</div>
    """, unsafe_allow_html=True)


def warning_box(text):
    """Remplace st.warning() — fond gris bleuté"""
    st.markdown(f"""
    <div style='
        background: rgba(115,130,142,0.12);
        border-left: 4px solid {C_MID};
        border-radius: 10px;
        padding: 14px 18px;
        color: {C_DARK};
        font-family: DM Sans, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        margin: 8px 0;
    '>⚠️ {text}</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# GRAPHIQUES MATPLOTLIB
# ══════════════════════════════════════════

def dark_fig(figsize=(10, 4)):
    """Figure avec 1 graphique au style palette"""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_LIGHT)
    ax.tick_params(colors=C_DARK)
    ax.xaxis.label.set_color(C_DARK)
    ax.yaxis.label.set_color(C_DARK)
    ax.title.set_color(C_DARK)
    for spine in ax.spines.values():
        spine.set_edgecolor(C_MID)
    return fig, ax


def dark_fig2(figsize=(14, 4)):
    """Figure avec 2 graphiques côte à côte"""
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
    """Applique le style palette à la légende"""
    legend = ax.get_legend()
    if legend:
        legend.get_frame().set_facecolor(C_BG)
        legend.get_frame().set_edgecolor(C_MID)
        for text in legend.get_texts():
            text.set_color(C_DARK)


def style_dataframe(df):
    """Style palette pour les DataFrames"""
    return df.style\
        .set_properties(**{
            'background-color' : 'white',
            'color'            : C_DARK,
            'border'           : f'1px solid {C_LIGHT}',
            'font-size'        : '13px',
            'padding'          : '8px 12px',
            'text-align'       : 'left',
            'font-family'      : 'DM Sans, sans-serif',
        })\
        .set_table_styles([
            {
                'selector': 'th',
                'props': [
                    ('background-color', C_DARK),
                    ('color',            'white'),
                    ('font-weight',      'bold'),
                    ('font-size',        '13px'),
                    ('padding',          '10px 12px'),
                    ('font-family',      'DM Sans, sans-serif'),
                ]
            },
            {
                'selector': 'tr:nth-child(even)',
                'props': [('background-color', C_BG)]
            },
            {
                'selector': 'tr:hover',
                'props': [
                    ('background-color', C_WARM),
                    ('transition',       'all 0.2s ease')
                ]
            }
        ])
# ─────────────────────────────────────────
# sections/page2_dashboard.py — VERSION 7
# Classements équitables (taux obj % / marge %)
# YoY supprimé — graphiques partout
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts5 import st_echarts
from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG
from utils.charts import style_dataframe, info_box, success_box, warning_box

NOMS_DEPT = {
    "Eletrônicos" : "Électronique",
    "Vestuário"   : "Vêtements",
    "Acessórios"  : "Accessoires",
    "Casa"        : "Maison",
    "Brinquedo"   : "Jouets",
    "Esportes"    : "Sports",
    "Papelaria"   : "Papeterie"
}
NOMS_MOIS = {
    1:"Jan", 2:"Fév", 3:"Mar", 4:"Avr",
    5:"Mai", 6:"Juin", 7:"Juil", 8:"Aoû",
    9:"Sep", 10:"Oct", 11:"Nov", 12:"Déc"
}
COULEURS_ANNEES = [C_DARK, C_MID, C_WARM, "#9BB1C1", "#C8BAA8", "#7A9BAD"]
COULEURS_DEPT   = [C_DARK, C_MID, C_WARM, "#9BB1C1", "#C8BAA8", "#7A9BAD", "#B8A898"]


# ══════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════

def kpi_card(label, value, sous="", color=C_DARK):
    st.markdown(f"""
    <div style='background:white;border-radius:12px;padding:16px 12px;
    box-shadow:0 2px 12px rgba(71,94,114,0.09);border-top:3px solid {color};text-align:center;'>
        <p style='font-size:9px;font-weight:700;color:{C_MID};text-transform:uppercase;
        letter-spacing:1.2px;margin:0 0 6px 0;'>{label}</p>
        <p style='font-size:22px;font-weight:900;color:{color};margin:0;line-height:1.1;'>{value}</p>
        <p style='font-size:10px;color:{C_MID};margin:5px 0 0 0;'>{sous}</p>
    </div>""", unsafe_allow_html=True)

def section_title(emoji, titre, sous_titre=""):
    st.markdown(f"""
    <div style='border-left:4px solid {C_DARK};padding:8px 14px;margin:24px 0 14px 0;'>
        <p style='font-size:16px;font-weight:700;color:{C_DARK};margin:0;'>{emoji} {titre}</p>
        {'<p style="font-size:11px;color:'+C_MID+';margin:2px 0 0 0;">'+sous_titre+'</p>' if sous_titre else ''}
    </div>""", unsafe_allow_html=True)

def graph_wrap(title, content_fn, key_suffix="", height_px=None):
    """Enveloppe un graphique dans une card blanche avec titre"""
    st.markdown(
        f"<div style='background:white;border-radius:12px;padding:12px 16px 6px;"
        f"box-shadow:0 2px 12px rgba(71,94,114,0.09);margin-bottom:10px;'>",
        unsafe_allow_html=True
    )
    if title:
        st.markdown(
            f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
            f"text-transform:uppercase;letter-spacing:1px;margin:0 0 6px;'>{title}</p>",
            unsafe_allow_html=True
        )
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)

def preparer_df(data_store, annees, dept):
    df = data_store[data_store["Year"].isin(annees)].copy()
    if dept != "Tous":
        df = df[df["Department"] == dept]
    if df.empty:
        return None
    df["Panier_Moyen"]      = df["Revenue"] / df["Customers"].replace(0, np.nan)
    df["Revenue_Par_Vente"] = df["Revenue"] / df["Sales Quantity"].replace(0, np.nan)
    df["Marge_Absolue"]     = df["Revenue"] * df["Margin"]
    df["Ecart_Rev_Goal"]    = df["Revenue"] - df["Revenue Goal"]
    df["Dept_FR"]           = df["Department"].map(lambda x: NOMS_DEPT.get(x, x))
    return df

def barres_mois(df, key, height="320px"):
    """Barres groupées : revenu TOTAL par mois, une couleur par année"""
    evol_mo   = df.groupby(["Year","Month"]).agg(Revenue_Total=("Revenue","sum")).reset_index()
    annees_mo = sorted(evol_mo["Year"].unique())
    mois_labels = [NOMS_MOIS[m] for m in range(1, 13)]
    series_mo = []
    for i, annee in enumerate(annees_mo):
        data_a = evol_mo[evol_mo["Year"] == annee]
        vals = [
            round(data_a[data_a["Month"]==m]["Revenue_Total"].values[0]/1e3, 1)
            if len(data_a[data_a["Month"]==m]) > 0 else 0
            for m in range(1, 13)
        ]
        series_mo.append({
            "name": str(annee), "type": "bar",
            "data": vals,
            "itemStyle": {"color": COULEURS_ANNEES[i % len(COULEURS_ANNEES)],
                          "borderRadius": [3, 3, 0, 0]},
        })
    opt = {
        "backgroundColor": "white",
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": [str(y) for y in annees_mo], "bottom": 0,
                   "textStyle": {"color": C_MID, "fontSize": 11}},
        "grid": {"left": "5%", "right": "5%", "bottom": "14%", "top": "8%", "containLabel": True},
        "xAxis": {"type": "category", "data": mois_labels,
                  "axisLabel": {"color": C_MID, "fontSize": 10}},
        "yAxis": {"type": "value", "name": "K€",
                  "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value} K€"},
                  "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}}},
        "series": series_mo
    }
    st_echarts(options=opt, height=height, key=key)


def courbes_mois(df, key, height="320px"):
    """Courbes revenue moy/jour par mois — utilisé dans le profil vendeur individuel"""
    evol_mo   = df.groupby(["Year","Month"]).agg(Revenue_Moy=("Revenue","mean")).reset_index()
    annees_mo = sorted(evol_mo["Year"].unique())
    mois_labels = [NOMS_MOIS[m] for m in range(1, 13)]
    series_mo = []
    for i, annee in enumerate(annees_mo):
        data_a = evol_mo[evol_mo["Year"] == annee]
        vals = [int(round(data_a[data_a["Month"]==m]["Revenue_Moy"].values[0], 0))
                if len(data_a[data_a["Month"]==m]) > 0 else None for m in range(1, 13)]
        series_mo.append({
            "name": str(annee), "type": "line", "smooth": True,
            "data": vals, "connectNulls": False, "symbolSize": 6,
            "lineStyle": {"color": COULEURS_ANNEES[i%len(COULEURS_ANNEES)], "width": 2},
            "itemStyle": {"color": COULEURS_ANNEES[i%len(COULEURS_ANNEES)]},
        })
    opt = {
        "backgroundColor": "white",
        "tooltip": {"trigger": "axis"},
        "legend": {"data": [str(y) for y in annees_mo], "bottom": 0,
                   "textStyle": {"color": C_MID, "fontSize": 11}},
        "grid": {"left": "5%", "right": "5%", "bottom": "12%", "top": "8%", "containLabel": True},
        "xAxis": {"type": "category", "data": mois_labels,
                  "axisLabel": {"color": C_MID, "fontSize": 10}},
        "yAxis": {"type": "value", "name": "€ moy/j",
                  "axisLabel": {"color": C_MID, "fontSize": 10},
                  "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}}},
        "series": series_mo
    }
    st_echarts(options=opt, height=height, key=key)


# ══════════════════════════════════════════
# FONCTION PRINCIPALE
# ══════════════════════════════════════════

def show(data_store):

    st.title("Dashboard — Vue d'ensemble")

    ALL_ANNEES = sorted(data_store["Year"].unique())
    ALL_DEPTS  = sorted(data_store["Department"].unique())

    # ── Filtres globaux ──
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        annee_sel = st.multiselect("Année(s)", ALL_ANNEES, default=ALL_ANNEES, key="g_annees")
    with col_f2:
        dept_sel = st.selectbox(
            "Département", ["Tous"] + ALL_DEPTS,
            format_func=lambda x: NOMS_DEPT.get(x,x) if x != "Tous" else "Tous les départements",
            key="g_dept"
        )

    if not annee_sel:
        warning_box("Sélectionnez au moins une année.")
        return
    df = preparer_df(data_store, annee_sel, dept_sel)
    if df is None:
        warning_box("Aucune donnée pour ces filtres.")
        return

    st.markdown("---")

    # ════════════════════════════════════════
    # 2.1 — KPIs : 5 cards + 3 graphiques
    # ════════════════════════════════════════
    section_title("📊", "KPIs", "Indicateurs clés sur la période sélectionnée")

    sum_revenue     = df["Revenue"].sum()
    sum_goal        = df["Revenue Goal"].sum()
    ecart_rev       = sum_revenue - sum_goal
    avg_revenue     = df["Revenue"].mean()
    avg_goal        = df["Revenue Goal"].mean()
    sum_margin      = df["Marge_Absolue"].sum()
    avg_margin_pct  = df["Margin"].mean() * 100
    sum_margin_vis  = (df["Revenue Goal"] * avg_margin_pct / 100).sum()
    ecart_margin    = sum_margin - sum_margin_vis
    sum_qty         = df["Sales Quantity"].sum()
    avg_qty         = df["Sales Quantity"].mean()
    count_cust      = df["Customers"].sum()
    avg_cust        = df["Customers"].mean()
    panier_moy      = df["Panier_Moyen"].mean()
    taux_obj_global = df["Goal_Reached"].mean() * 100

    # 5 cards ligne 1
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi_card("Sum Quantity",   f"{int(sum_qty):,}",    "unités vendues",  C_MID)
    with c2: kpi_card("Avg Sales Qty",  f"{avg_qty:.1f}",       "qté moy / jour",  C_MID)
    with c3: kpi_card("Count Customer", f"{int(count_cust):,}", "clients total",   C_WARM)
    with c4: kpi_card("Avg Customer",   f"{avg_cust:.1f}",      "clients moy/j",   C_WARM)
    with c5: kpi_card("Panier Moyen",   f"{panier_moy:.2f} €",  "revenue/client",  C_DARK)

    st.markdown("<div style='margin:14px 0'></div>", unsafe_allow_html=True)

    # 3 graphiques comparatifs
    cg1, cg2, cg3 = st.columns(3)

    # G1 — Revenue Réel vs Objectif par année
    with cg1:
        rev_yr = df.groupby("Year").agg(
            Reel=("Revenue","sum"), Goal=("Revenue Goal","sum")
        ).reset_index()
        annees_l = [str(y) for y in rev_yr["Year"].tolist()]
        opt_rv = {
            "backgroundColor":"white",
            "tooltip":{"trigger":"axis"},
            "legend":{"data":["Réel","Objectif"],"bottom":0,
                      "textStyle":{"color":C_MID,"fontSize":10}},
            "grid":{"left":"5%","right":"5%","bottom":"18%","top":"8%","containLabel":True},
            "xAxis":{"type":"category","data":annees_l,
                     "axisLabel":{"color":C_MID,"fontSize":10}},
            "yAxis":{"type":"value","name":"M€",
                     "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value} M€"},
                     "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
            "series":[
                {"name":"Réel","type":"bar","barWidth":"35%",
                 "data":[round(v/1e6,2) for v in rev_yr["Reel"].tolist()],
                 "itemStyle":{"color":C_DARK,"borderRadius":[4,4,0,0]}},
                {"name":"Objectif","type":"bar","barWidth":"35%",
                 "data":[round(v/1e6,2) for v in rev_yr["Goal"].tolist()],
                 "itemStyle":{"color":C_LIGHT,"borderRadius":[4,4,0,0]}},
            ]
        }
        s_r = "▲" if ecart_rev >= 0 else "▼"
        col_r = "#27AE60" if ecart_rev >= 0 else "#E74C3C"
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 4px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
                    f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                    f"Revenue — Réel vs Objectif</p>", unsafe_allow_html=True)
        st_echarts(options=opt_rv, height="220px", key="kpi_rev_vs")
        st.markdown(f"<p style='text-align:center;font-size:13px;font-weight:700;"
                    f"color:{col_r};margin:2px 0 8px;'>{s_r} {abs(ecart_rev)/1e3:.0f} K€ vs objectif</p>",
                    unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # G2 — Marge Réelle vs Visée par année
    with cg2:
        mg_yr = df.groupby("Year").agg(
            Marge_R=("Marge_Absolue","sum"), Goal=("Revenue Goal","sum")
        ).reset_index()
        mg_yr["Marge_V"] = mg_yr["Goal"] * (avg_margin_pct / 100)
        opt_mg = {
            "backgroundColor":"white",
            "tooltip":{"trigger":"axis"},
            "legend":{"data":["Réelle","Visée"],"bottom":0,
                      "textStyle":{"color":C_MID,"fontSize":10}},
            "grid":{"left":"5%","right":"5%","bottom":"18%","top":"8%","containLabel":True},
            "xAxis":{"type":"category","data":annees_l,
                     "axisLabel":{"color":C_MID,"fontSize":10}},
            "yAxis":{"type":"value","name":"M€",
                     "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value} M€"},
                     "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
            "series":[
                {"name":"Réelle","type":"bar","barWidth":"35%",
                 "data":[round(v/1e6,2) for v in mg_yr["Marge_R"].tolist()],
                 "itemStyle":{"color":C_MID,"borderRadius":[4,4,0,0]}},
                {"name":"Visée","type":"bar","barWidth":"35%",
                 "data":[round(v/1e6,2) for v in mg_yr["Marge_V"].tolist()],
                 "itemStyle":{"color":C_LIGHT,"borderRadius":[4,4,0,0]}},
            ]
        }
        s_m = "▲" if ecart_margin >= 0 else "▼"
        col_m = "#27AE60" if ecart_margin >= 0 else "#E74C3C"
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 4px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
                    f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                    f"Marge — Réelle vs Visée</p>", unsafe_allow_html=True)
        st_echarts(options=opt_mg, height="220px", key="kpi_mg_vs")
        st.markdown(f"<p style='text-align:center;font-size:13px;font-weight:700;"
                    f"color:{col_m};margin:2px 0 8px;'>{s_m} {abs(ecart_margin)/1e3:.0f} K€ "
                    f"| moy {avg_margin_pct:.1f}%</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # G3 — Jauge taux objectif global
    with cg3:
        col_jauge = "#27AE60" if taux_obj_global >= 50 else "#E74C3C"
        opt_jauge = {
            "backgroundColor":"white",
            "series":[{
                "type":"gauge","startAngle":180,"endAngle":0,
                "min":0,"max":100,"radius":"88%","center":["50%","68%"],
                "progress":{"show":True,"width":16,"itemStyle":{"color":col_jauge}},
                "axisLine":{"lineStyle":{"width":16,"color":[[1,C_LIGHT]]}},
                "axisTick":{"show":False},"splitLine":{"show":False},
                "axisLabel":{"show":False},"pointer":{"show":False},
                "detail":{"valueAnimation":True,"formatter":"{value}%",
                          "color":col_jauge,"fontSize":24,"fontWeight":"bold",
                          "offsetCenter":[0,"-10%"]},
                "title":{"offsetCenter":[0,"18%"],"fontSize":11,"color":C_MID},
                "data":[{"value":round(taux_obj_global,1),"name":"Taux Objectif Atteint"}]
            }]
        }
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 4px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
                    f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                    f"Taux Objectif Global</p>", unsafe_allow_html=True)
        st_echarts(options=opt_jauge, height="220px", key="kpi_gauge")
        st.markdown(f"<p style='text-align:center;font-size:11px;color:{C_MID};"
                    f"margin:2px 0 8px;'>Rev moy/j : <b>{avg_revenue:,.0f} €</b> | "
                    f"Obj moy : <b>{avg_goal:,.0f} €</b></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════
    # 2.2 — ÉVOLUTION TEMPORELLE
    # Tab Annuelle (barres Rev + ligne taux obj)
    # Tab Mensuelle (courbes par année)
    # Tab Trimestrielle (barres empilées)
    # NOTE : YoY retiré — peu lisible et peu utile en présentation
    # ════════════════════════════════════════
    section_title("📅", "Évolution Temporelle")

    # ── Sélecteur d'onglet via radio (évite le bug de rendu st_echarts dans st.tabs)
    onglet_evol = st.radio(
        "Vue", ["Par Année", "Par Mois", "Par Trimestre"],
        horizontal=True, key="onglet_evol",
        label_visibility="collapsed"
    )
    st.markdown("<div style='margin:6px 0'></div>", unsafe_allow_html=True)

    if onglet_evol == "Par Année":
        evol_yr = df.groupby("Year").agg(
            Revenue_Total=("Revenue","sum"),
            Taux_Objectif=("Goal_Reached","mean"),
        ).reset_index().sort_values("Year")

        opt_yr = {
            "backgroundColor":"white",
            "tooltip":{"trigger":"axis","axisPointer":{"type":"cross"}},
            "legend":{"data":["Revenu (M€)","Taux Objectif (%)"],
                      "bottom":0,"textStyle":{"color":C_MID,"fontSize":11}},
            "grid":{"left":"5%","right":"10%","bottom":"12%","top":"8%","containLabel":True},
            "xAxis":{"type":"category",
                     "data":[str(y) for y in evol_yr["Year"].tolist()],
                     "axisLabel":{"color":C_MID,"fontSize":11}},
            "yAxis":[
                {"type":"value","name":"M€",
                 "axisLabel":{"color":C_MID,"fontSize":10,"formatter":"{value} M€"},
                 "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
                {"type":"value","name":"%","min":0,"max":100,
                 "axisLabel":{"color":C_MID,"fontSize":10,"formatter":"{value}%"},
                 "splitLine":{"show":False}},
            ],
            "series":[
                {"name":"Revenu (M€)","type":"bar","yAxisIndex":0,
                 "data":[round(v/1e6,2) for v in evol_yr["Revenue_Total"].tolist()],
                 "barWidth":"40%","itemStyle":{"color":C_DARK,"borderRadius":[6,6,0,0]},
                 "label":{"show":True,"position":"top","formatter":"{c} M€",
                          "fontSize":10,"color":C_DARK}},
                {"name":"Taux Objectif (%)","type":"line","yAxisIndex":1,
                 "data":[round(v*100,1) for v in evol_yr["Taux_Objectif"].tolist()],
                 "smooth":True,"lineStyle":{"color":C_WARM,"width":3},
                 "itemStyle":{"color":C_WARM},"symbolSize":9,
                 "label":{"show":True,"position":"top","formatter":"{c}%",
                          "fontSize":10,"color":C_WARM}},
            ]
        }
        st_echarts(options=opt_yr, height="360px", key="evol_yr")
        best_yr  = evol_yr.loc[evol_yr["Revenue_Total"].idxmax(),"Year"]
        worst_yr = evol_yr.loc[evol_yr["Revenue_Total"].idxmin(),"Year"]
        info_box(
            f"<b>{best_yr}</b> est l'année record en revenu. "
            f"<b>{worst_yr}</b> est la plus faible. "
            f"Le taux objectif reste quasi constant malgré la baisse des revenus — "
            f"signe que les objectifs sont recalibrés chaque année proportionnellement."
        )

    elif onglet_evol == "Par Mois":
        barres_mois(df, key="evol_mo_tab", height="360px")
        info_box("Revenu total mensuel en K€ — barres groupées par année. "
                 "Comparez directement chaque mois d'une année à l'autre.")

    else:  # Par Trimestre
        evol_tr = df.groupby(["Year","Quarter"]).agg(
            Revenue=("Revenue","sum")
        ).reset_index()
        annees_tr = sorted(evol_tr["Year"].unique())
        # Barres groupées : x = années, une série par trimestre
        series_tr = []
        couleurs_trim = [C_DARK, C_MID, C_WARM, "#9BB1C1"]
        for i, q in enumerate([1, 2, 3, 4]):
            vals = []
            for annee in annees_tr:
                row = evol_tr[(evol_tr["Year"]==annee) & (evol_tr["Quarter"]==q)]
                vals.append(round(row["Revenue"].values[0]/1e6, 2) if len(row)>0 else 0)
            series_tr.append({
                "name": f"T{q}",
                "type": "bar",
                "data": vals,
                "itemStyle": {"color": couleurs_trim[i], "borderRadius": [3, 3, 0, 0]},
                "label": {"show": True, "position": "top", "formatter": "{c} M€",
                          "fontSize": 9, "color": couleurs_trim[i]},
            })
        opt_tr = {
            "backgroundColor": "white",
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {"data": ["T1","T2","T3","T4"], "bottom": 0,
                       "textStyle": {"color": C_MID, "fontSize": 11}},
            "grid": {"left": "5%", "right": "5%", "bottom": "12%", "top": "10%", "containLabel": True},
            "xAxis": {"type": "category",
                      "data": [str(y) for y in annees_tr],
                      "axisLabel": {"color": C_MID, "fontSize": 12, "fontWeight": "bold"}},
            "yAxis": {"type": "value", "name": "M€",
                      "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value} M€"},
                      "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}}},
            "series": series_tr
        }
        st_echarts(options=opt_tr, height="360px", key="evol_trim_tab")
        info_box("Barres groupées — chaque couleur = un trimestre. "
                 "Axe X = années : comparez l'évolution de chaque trimestre au fil du temps.")

    st.markdown("---")

    # ════════════════════════════════════════
    # 2.3 — PERFORMANCE PAR DÉPARTEMENT
    # IMPORTANT : classement par marge % et taux objectif %
    # PAS par revenu — un vendeur Électronique génère mécaniquement
    # plus de revenu qu'un vendeur Papeterie, ce n'est pas de la performance
    # ════════════════════════════════════════
    section_title("🏬", "Performance par Département",
                  "Classement par marge % et taux objectif — indicateurs équitables entre départements")

    dept_stats = df.groupby("Dept_FR").agg(
        Revenue_Total=("Revenue","sum"),
        Revenue_Moy  =("Revenue","mean"),
        Marge_Moy    =("Margin","mean"),
        Marge_Abs    =("Marge_Absolue","sum"),
        Taux_Obj     =("Goal_Reached","mean"),
        Panier_Moy   =("Panier_Moyen","mean"),
        Sum_Qty      =("Sales Quantity","sum"),
        Count_Client =("Customers","sum"),
    ).reset_index()
    dept_stats["PDM"] = dept_stats["Revenue_Total"] / dept_stats["Revenue_Total"].sum() * 100

    dg1, dg2, dg3 = st.columns(3)

    # G1 — Marge moyenne % (indicateur de rentabilité — équitable)
    with dg1:
        dept_m = dept_stats.sort_values("Marge_Moy", ascending=True)
        opt_dm = {
            "backgroundColor":"white",
            "tooltip":{"trigger":"axis","formatter":"{b} : {c}%"},
            "grid":{"left":"2%","right":"16%","top":"4%","bottom":"4%","containLabel":True},
            "xAxis":{"type":"value",
                     "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value}%"},
                     "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
            "yAxis":{"type":"category","data":dept_m["Dept_FR"].tolist(),
                     "axisLabel":{"color":C_DARK,"fontSize":10}},
            "series":[{"type":"bar","barWidth":"55%",
                       "data":[round(v*100,1) for v in dept_m["Marge_Moy"].tolist()],
                       "itemStyle":{"color":{"type":"linear","x":0,"y":0,"x2":1,"y2":0,
                           "colorStops":[{"offset":0,"color":C_MID},{"offset":1,"color":C_WARM}]},
                           "borderRadius":[0,6,6,0]},
                       "label":{"show":True,"position":"right","formatter":"{c}%",
                                "fontSize":9,"color":C_MID}}]
        }
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 4px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
                    f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                    f"① Marge Moyenne % — rentabilité</p>", unsafe_allow_html=True)
        st_echarts(options=opt_dm, height="240px", key="dept_marge")
        st.markdown("</div>", unsafe_allow_html=True)

    # G2 — Taux objectif % (indicateur de performance — équitable)
    with dg2:
        dept_t = dept_stats.sort_values("Taux_Obj", ascending=True)
        opt_dt = {
            "backgroundColor":"white",
            "tooltip":{"trigger":"axis","formatter":"{b} : {c}%"},
            "grid":{"left":"2%","right":"16%","top":"4%","bottom":"4%","containLabel":True},
            "xAxis":{"type":"value","min":0,"max":100,
                     "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value}%"},
                     "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
            "yAxis":{"type":"category","data":dept_t["Dept_FR"].tolist(),
                     "axisLabel":{"color":C_DARK,"fontSize":10}},
            "series":[{"type":"bar","barWidth":"55%",
                       "data":[round(v*100,1) for v in dept_t["Taux_Obj"].tolist()],
                       "itemStyle":{"color":C_DARK,"borderRadius":[0,6,6,0]},
                       "markLine":{"silent":True,
                           "lineStyle":{"color":"#E74C3C","type":"dashed","width":1.5},
                           "data":[{"xAxis":50}]},
                       "label":{"show":True,"position":"right","formatter":"{c}%",
                                "fontSize":9,"color":C_DARK}}]
        }
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 4px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
                    f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                    f"② Taux Objectif % — performance</p>", unsafe_allow_html=True)
        st_echarts(options=opt_dt, height="240px", key="dept_taux")
        st.markdown("</div>", unsafe_allow_html=True)

    # G3 — Panier moyen € (indicateur comportement client)
    with dg3:
        dept_p = dept_stats.sort_values("Panier_Moy", ascending=True)
        opt_dp = {
            "backgroundColor":"white",
            "tooltip":{"trigger":"axis","formatter":"{b} : {c} €"},
            "grid":{"left":"2%","right":"16%","top":"4%","bottom":"4%","containLabel":True},
            "xAxis":{"type":"value",
                     "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value} €"},
                     "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
            "yAxis":{"type":"category","data":dept_p["Dept_FR"].tolist(),
                     "axisLabel":{"color":C_DARK,"fontSize":10}},
            "series":[{"type":"bar","barWidth":"55%",
                       "data":[round(v,2) for v in dept_p["Panier_Moy"].tolist()],
                       "itemStyle":{"color":C_WARM,"borderRadius":[0,6,6,0]},
                       "label":{"show":True,"position":"right","formatter":"{c} €",
                                "fontSize":9,"color":C_MID}}]
        }
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 4px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
                    f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                    f"③ Panier Moyen € — comportement client</p>", unsafe_allow_html=True)
        st_echarts(options=opt_dp, height="240px", key="dept_panier")
        st.markdown("</div>", unsafe_allow_html=True)

    warning_box(
        "⚠️ Nous ne classons <b>pas</b> les départements par revenu total. "
        "Électronique génère mécaniquement plus de revenu qu'Accessoires — "
        "ce n'est pas de la performance, c'est le volume du marché. "
        "Les indicateurs équitables sont la <b>marge %</b> et le <b>taux objectif %</b>."
    )

    # Tableau trimestriel département
    st.markdown("<div style='margin:14px 0 6px 0'></div>", unsafe_allow_html=True)
    annee_trim = st.selectbox("Année — tableau trimestriel", sorted(df["Year"].unique()), key="trim_annee")
    df_trim = df[df["Year"]==annee_trim].copy()
    trim_dept = df_trim.groupby(["Dept_FR","Quarter"]).agg(
        Revenue=("Revenue","sum"), Taux=("Goal_Reached","mean")
    ).reset_index()
    piv_rev  = trim_dept.pivot_table(index="Dept_FR",columns="Quarter",values="Revenue",aggfunc="sum").round(0)
    piv_rev.columns  = [f"T{q} Rev" for q in piv_rev.columns]
    piv_taux = trim_dept.pivot_table(index="Dept_FR",columns="Quarter",values="Taux",aggfunc="mean").round(3)
    piv_taux.columns = [f"T{q} Obj%" for q in piv_taux.columns]
    piv = pd.concat([piv_rev, piv_taux], axis=1)
    taux_cols = [c for c in piv.columns if "Obj%" in c]
    rev_cols  = [c for c in piv.columns if "Rev" in c]
    piv["Taux Moy"]  = piv[taux_cols].mean(axis=1)
    piv["Total Rev"] = piv[rev_cols].sum(axis=1)
    # Trié par taux objectif moyen — pas par revenu
    piv = piv.sort_values("Taux Moy", ascending=False)
    piv_d = piv.copy()
    for c in piv_d.columns:
        if "Rev" in c or "Total" in c:
            piv_d[c] = piv_d[c].apply(lambda x: f"{x/1_000:,.0f} K€" if pd.notna(x) else "—")
        elif "Obj%" in c:
            piv_d[c] = piv_d[c].apply(lambda x: f"{x*100:.1f}%" if pd.notna(x) else "—")
        elif c == "Taux Moy":
            piv_d[c] = piv_d[c].apply(lambda x: f"{x*100:.1f}%")
    piv_d.index.name = "Département"
    st.dataframe(style_dataframe(piv_d.reset_index()), use_container_width=True, hide_index=True)
    info_box(f"Trié par taux objectif moyen — indicateur équitable. Revenu en K€ pour info — <b>{annee_trim}</b>.")

    st.markdown("---")

    # ════════════════════════════════════════
    # 2.4 — CLASSEMENT VENDEURS
    # Barres taux objectif + scatter Marge vs Taux
    # MÊME logique : pas de classement par revenu brut
    # ════════════════════════════════════════
    section_title("👤", "Classement des Vendeurs",
                  "Classement par taux objectif % — indépendant du département")

    seller_stats = df.groupby("Seller").agg(
        Revenue_Total=("Revenue","sum"),
        Revenue_Moy  =("Revenue","mean"),
        Marge_Moy    =("Margin","mean"),
        Taux_Obj     =("Goal_Reached","mean"),
        Sum_Qty      =("Sales Quantity","sum"),
        Avg_Qty      =("Sales Quantity","mean"),
        Count_Client =("Customers","sum"),
        Avg_Client   =("Customers","mean"),
        Panier_Moy   =("Panier_Moyen","mean"),
        Marge_Abs    =("Marge_Absolue","sum"),
    ).reset_index()
    # Classement par taux objectif — pas par revenu
    seller_stats = seller_stats.sort_values("Taux_Obj", ascending=False).reset_index(drop=True)
    seller_stats["Rang"] = seller_stats.index + 1
    seller_stats["Département"] = seller_stats["Seller"].map(df.groupby("Seller")["Dept_FR"].first())

    sv1, sv2 = st.columns([1, 1])

    # G1 — Barres taux objectif par vendeur
    with sv1:
        top_s = seller_stats.sort_values("Taux_Obj", ascending=True)
        opt_s = {
            "backgroundColor":"white",
            "tooltip":{"trigger":"axis","formatter":"{b} : {c}%"},
            "grid":{"left":"2%","right":"12%","top":"4%","bottom":"4%","containLabel":True},
            "xAxis":{"type":"value","min":0,"max":100,
                     "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value}%"},
                     "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
            "yAxis":{"type":"category","data":top_s["Seller"].tolist(),
                     "axisLabel":{"color":C_DARK,"fontSize":10}},
            "series":[{"type":"bar","barWidth":"55%",
                       "data":[round(v*100,1) for v in top_s["Taux_Obj"].tolist()],
                       "itemStyle":{"color":{"type":"linear","x":0,"y":0,"x2":1,"y2":0,
                           "colorStops":[{"offset":0,"color":C_MID},{"offset":1,"color":C_WARM}]},
                           "borderRadius":[0,6,6,0]},
                       "markLine":{"silent":True,
                           "lineStyle":{"color":"#E74C3C","type":"dashed","width":1.5},
                           "data":[{"xAxis":50,"label":{"formatter":"50%","color":"#E74C3C","fontSize":10}}]},
                       "label":{"show":True,"position":"right","formatter":"{c}%",
                                "fontSize":9,"color":C_MID}}]
        }
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 6px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
                    f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                    f"Taux Objectif par Vendeur — ligne rouge = seuil 50%</p>", unsafe_allow_html=True)
        st_echarts(options=opt_s, height="400px", key="sell_taux")
        st.markdown("</div>", unsafe_allow_html=True)

    # G2 — Scatter Marge % vs Taux Objectif
    # Chaque point = un vendeur, couleur = département
    with sv2:
        dept_list = seller_stats["Département"].unique().tolist()
        series_sc = []
        for i, dept in enumerate(dept_list):
            sub = seller_stats[seller_stats["Département"]==dept]
            pts = []
            for _, row in sub.iterrows():
                pts.append({
                    "value":[round(row["Taux_Obj"]*100,1), round(row["Marge_Moy"]*100,1)],
                    "name": row["Seller"]
                })
            series_sc.append({
                "name":dept,"type":"scatter","data":pts,"symbolSize":14,
                "itemStyle":{"color":COULEURS_DEPT[i%len(COULEURS_DEPT)]},
                "label":{"show":True,"formatter":"{b}","position":"right",
                         "fontSize":8,"color":C_MID},
            })
        opt_sc = {
            "backgroundColor":"white",
            "tooltip":{"trigger":"item",
                       "formatter":"function(p){return p.seriesName+'<br/>'+p.data.name"
                                   "+'<br/>Taux: '+p.data.value[0]+'%"
                                   " | Marge: '+p.data.value[1]+'%'}"},
            "legend":{"data":dept_list,"bottom":0,
                      "textStyle":{"color":C_MID,"fontSize":10}},
            "grid":{"left":"5%","right":"8%","bottom":"14%","top":"8%","containLabel":True},
            "xAxis":{"type":"value","name":"Taux Objectif %","min":0,"max":100,
                     "nameTextStyle":{"color":C_MID,"fontSize":10},
                     "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value}%"},
                     "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
            "yAxis":{"type":"value","name":"Marge Moyenne %",
                     "nameTextStyle":{"color":C_MID,"fontSize":10},
                     "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value}%"},
                     "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
            "series":series_sc
        }
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 6px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:10px;font-weight:700;color:{C_MID};"
                    f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                    f"Scatter — Marge % vs Taux Objectif — chaque point = un vendeur</p>",
                    unsafe_allow_html=True)
        st_echarts(options=opt_sc, height="400px", key="sell_scatter")
        st.markdown("</div>", unsafe_allow_html=True)

    info_box(
        "Le scatter permet d'identifier les <b>vrais performers</b> : "
        "en haut à droite = bonne marge ET bon taux objectif. "
        "Un vendeur avec beaucoup de revenu mais en bas à gauche n'est pas performant — "
        "il bénéficie juste d'un département à fort volume."
    )

    # Tableau classement complet
    st_t = seller_stats.copy()
    st_t["#"]            = st_t["Rang"].map(lambda x: f"#{x}")
    st_t["Taux Obj"]     = st_t["Taux_Obj"].map(lambda x: f"{x*100:.1f}%")
    st_t["Marge Moy"]    = st_t["Marge_Moy"].map(lambda x: f"{x*100:.1f}%")
    st_t["Panier Moy"]   = st_t["Panier_Moy"].map(lambda x: f"{x:.2f} €")
    st_t["Rev Moy/j"]    = st_t["Revenue_Moy"].map(lambda x: f"{x:,.0f} €")
    st_t["Qté Moy"]      = st_t["Avg_Qty"].map(lambda x: f"{x:.1f}")
    st_t["Clients Moy"]  = st_t["Avg_Client"].map(lambda x: f"{x:.1f}")
    st_t["Revenu Total"] = st_t["Revenue_Total"].map(lambda x: f"{x/1e6:.2f} M€")
    st_t["Marge Tot"]    = st_t["Marge_Abs"].map(lambda x: f"{x/1e6:.2f} M€")
    st_t["Qté Tot"]      = st_t["Sum_Qty"].map(lambda x: f"{int(x):,}")
    st_t["Clients Tot"]  = st_t["Count_Client"].map(lambda x: f"{int(x):,}")
    st.dataframe(
        style_dataframe(st_t[["#","Seller","Département",
                               "Taux Obj","Marge Moy","Panier Moy","Rev Moy/j",
                               "Qté Moy","Clients Moy",
                               "Revenu Total","Marge Tot","Qté Tot","Clients Tot"]]),
        use_container_width=True, hide_index=True
    )

    st.markdown("---")

    # ════════════════════════════════════════
    # ANALYSES DÉTAILLÉES — expanders
    # ════════════════════════════════════════
   

    # ── A. Profil d'un vendeur ──
    with st.expander("📈 Profil d'un vendeur"):
        vendeur_sel = st.selectbox("Choisir un vendeur", sorted(df["Seller"].unique()), key="vend_profil")
        df_v      = df[df["Seller"]==vendeur_sel]
        dept_v    = df_v["Dept_FR"].iloc[0]
        dept_orig = df_v["Department"].iloc[0]
        rang_v    = int(seller_stats[seller_stats["Seller"]==vendeur_sel]["Rang"].values[0])
        taux_v    = df_v["Goal_Reached"].mean()*100
        marge_v   = df_v["Margin"].mean()*100

        vp1, vp2 = st.columns([1, 2])
        with vp1:
            df_dept  = df[df["Department"]==dept_orig]
            def norm(val, ref):
                return round(min(val/ref*50, 100),1) if ref>0 else 50
            indicators = [
                {"name":"Taux Obj","max":100},
                {"name":"Marge %","max":100},
                {"name":"Panier","max":100},
                {"name":"Rev Moy","max":100},
                {"name":"Qté Moy","max":100},
            ]
            val_vend = [
                norm(taux_v, df_dept["Goal_Reached"].mean()*100),
                norm(marge_v, df_dept["Margin"].mean()*100),
                norm(df_v["Panier_Moyen"].mean(), df_dept["Panier_Moyen"].mean()),
                norm(df_v["Revenue"].mean(), df_dept["Revenue"].mean()),
                norm(df_v["Sales Quantity"].mean(), df_dept["Sales Quantity"].mean()),
            ]
            opt_radar = {
                "backgroundColor":"white",
                "legend":{"data":[vendeur_sel,f"Moy {dept_v}"],"bottom":0,
                          "textStyle":{"color":C_MID,"fontSize":10}},
                "radar":{"indicator":indicators,"shape":"circle","radius":"60%",
                         "axisName":{"color":C_MID,"fontSize":10},
                         "splitLine":{"lineStyle":{"color":C_LIGHT}},
                         "splitArea":{"show":False}},
                "series":[{"type":"radar","data":[
                    {"value":val_vend,"name":vendeur_sel,
                     "lineStyle":{"color":C_DARK,"width":2},
                     "areaStyle":{"color":C_DARK,"opacity":0.15},
                     "itemStyle":{"color":C_DARK}},
                    {"value":[50,50,50,50,50],"name":f"Moy {dept_v}",
                     "lineStyle":{"color":C_WARM,"width":2,"type":"dashed"},
                     "areaStyle":{"color":C_WARM,"opacity":0.1},
                     "itemStyle":{"color":C_WARM}},
                ]}]
            }
            st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 4px;"
                        f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
            st_echarts(options=opt_radar, height="280px", key="vend_radar")
            st.markdown("</div>", unsafe_allow_html=True)
        with vp2:
            courbes_mois(df_v, key="vend_mo", height="280px")

        moy_dept  = df[df["Department"]==dept_orig]["Revenue"].mean()
        ecart_pct = (df_v["Revenue"].mean()-moy_dept)/moy_dept*100
        s = "▲" if ecart_pct>=0 else "▼"
        msg = (f"<b>{vendeur_sel}</b> ({dept_v}) — Rang <b>#{rang_v}</b> — "
               f"Taux objectif <b>{taux_v:.1f}%</b> | Marge <b>{marge_v:.1f}%</b> | "
               f"Rev moy/j {s} <b>{abs(ecart_pct):.1f}%</b> vs moy département.")
        success_box(msg) if ecart_pct>=0 else warning_box(msg)

    # ── B. Heatmap trimestrielle par vendeur ──
    with st.expander("🌡️ Heatmap taux objectif — Vendeur × Trimestre"):
        annee_tv = st.selectbox("Année", sorted(df["Year"].unique()), key="trim_vend_an")
        df_tv = df[df["Year"]==annee_tv]
        sellers_list = sorted(df_tv["Seller"].unique())
        heat_data = []
        for qi, q in enumerate([1,2,3,4]):
            for si, seller in enumerate(sellers_list):
                sub = df_tv[(df_tv["Seller"]==seller)&(df_tv["Quarter"]==q)]
                val = round(sub["Goal_Reached"].mean()*100,1) if len(sub)>0 else 0
                heat_data.append([qi, si, val])
        opt_heat = {
            "backgroundColor":"white",
            "tooltip":{"position":"top","formatter":"function(p){return p.data[2]+'%'}"},
            "grid":{"left":"14%","right":"5%","top":"4%","bottom":"10%","containLabel":True},
            "xAxis":{"type":"category","data":["T1","T2","T3","T4"],
                     "splitArea":{"show":True},
                     "axisLabel":{"color":C_MID,"fontSize":11,"fontWeight":"bold"}},
            "yAxis":{"type":"category","data":sellers_list,
                     "splitArea":{"show":True},
                     "axisLabel":{"color":C_DARK,"fontSize":10}},
            "visualMap":{"min":0,"max":100,"calculable":True,
                         "orient":"horizontal","left":"center","bottom":"-2%",
                         "inRange":{"color":[C_LIGHT,C_MID,C_DARK]},
                         "textStyle":{"color":C_MID,"fontSize":9}},
            "series":[{"type":"heatmap","data":heat_data,
                       "label":{"show":True,
                                "formatter":"function(p){return p.data[2]+'%'}",
                                "fontSize":9,"color":"white"}}]
        }
        st.markdown(f"<div style='background:white;border-radius:12px;padding:12px 14px 4px;"
                    f"box-shadow:0 2px 12px rgba(71,94,114,0.09);margin-bottom:10px;'>",
                    unsafe_allow_html=True)
        st_echarts(options=opt_heat,
                   height=f"{max(280,len(sellers_list)*26+60)}px", key="heat_vend")
        st.markdown("</div>", unsafe_allow_html=True)
        info_box(f"Plus la case est foncée, plus le taux objectif est élevé — <b>{annee_tv}</b>.")

    # ── C. Analyse des objectifs ──
    with st.expander("🎯 Analyse des objectifs — pourquoi 47% ?"):
        ratio_med      = (df["Revenue Goal"]/df["Revenue"].replace(0,np.nan)).median()
        pct_impossible = (df["Revenue Goal"]>df["Revenue"]*2).mean()*100
        ecart_moy      = df["Ecart_Rev_Goal"].mean()

        ao1, ao2, ao3 = st.columns(3)

        with ao1:
            ratio_s = (df["Revenue Goal"]/df["Revenue"].replace(0,np.nan)).dropna().reset_index(drop=True)
            ratio_s = ratio_s[ratio_s<ratio_s.quantile(0.98)].reset_index(drop=True)
            bins_r  = pd.cut(ratio_s, bins=20)
            dist_r  = ratio_s.groupby(bins_r, observed=True).count().reset_index(name="Count")
            dist_r.columns = ["Intervalle","Count"]
            dist_r["Label"] = dist_r["Intervalle"].apply(lambda x: f"{x.mid:.2f}")
            opt_ratio = {
                "backgroundColor":"white",
                "tooltip":{"trigger":"axis"},
                "grid":{"left":"5%","right":"5%","top":"12%","bottom":"12%","containLabel":True},
                "xAxis":{"type":"category","data":dist_r["Label"].tolist(),
                         "axisLabel":{"color":C_MID,"fontSize":8,"rotate":30}},
                "yAxis":{"type":"value","name":"Nb jours",
                         "axisLabel":{"color":C_MID,"fontSize":9},
                         "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
                "series":[{"type":"bar","data":dist_r["Count"].tolist(),
                           "itemStyle":{"color":C_MID,"borderRadius":[3,3,0,0]}}]
            }
            st.markdown(f"<div style='background:white;border-radius:12px;padding:10px 12px 4px;"
                        f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:9px;font-weight:700;color:{C_MID};"
                        f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                        f"Distribution ratio Obj/Réel (médiane ×{ratio_med:.2f})</p>",
                        unsafe_allow_html=True)
            st_echarts(options=opt_ratio, height="220px", key="dist_ratio")
            st.markdown("</div>", unsafe_allow_html=True)

        with ao2:
            ecart_clean = df["Ecart_Rev_Goal"].dropna().reset_index(drop=True)
            bins_e      = pd.cut(ecart_clean, bins=20)
            ecart_dist  = ecart_clean.groupby(bins_e, observed=True).count().reset_index(name="Count")
            ecart_dist.columns = ["Intervalle","Count"]
            ecart_dist["Label"] = ecart_dist["Intervalle"].apply(lambda x: f"{x.mid:.0f}")
            colors_e = [C_DARK if float(l)<0 else "#27AE60" for l in ecart_dist["Label"]]
            opt_ec = {
                "backgroundColor":"white",
                "tooltip":{"trigger":"axis"},
                "grid":{"left":"5%","right":"5%","top":"12%","bottom":"12%","containLabel":True},
                "xAxis":{"type":"category","data":ecart_dist["Label"].tolist(),
                         "axisLabel":{"color":C_MID,"fontSize":8,"rotate":30}},
                "yAxis":{"type":"value","name":"Nb jours",
                         "axisLabel":{"color":C_MID,"fontSize":9},
                         "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
                "series":[{"type":"bar",
                           "data":[{"value":v,"itemStyle":{"color":c}}
                                   for v,c in zip(ecart_dist["Count"].tolist(),colors_e)],
                           "itemStyle":{"borderRadius":[3,3,0,0]}}]
            }
            st.markdown(f"<div style='background:white;border-radius:12px;padding:10px 12px 4px;"
                        f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:9px;font-weight:700;color:{C_MID};"
                        f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                        f"Écart Réel − Objectif (moy {ecart_moy:+,.0f} €)</p>",
                        unsafe_allow_html=True)
            st_echarts(options=opt_ec, height="220px", key="dist_ecart")
            st.markdown("</div>", unsafe_allow_html=True)

        with ao3:
            taux_yr = df.groupby("Year").agg(
                Taux=("Goal_Reached","mean"),
                Pct_Impossible=("Revenue Goal",
                    lambda x: (x > df.loc[x.index,"Revenue"]*2).mean()*100)
            ).reset_index()
            opt_taux_yr = {
                "backgroundColor":"white",
                "tooltip":{"trigger":"axis"},
                "legend":{"data":["Taux Obj %","Obj impossibles %"],"bottom":0,
                          "textStyle":{"color":C_MID,"fontSize":9}},
                "grid":{"left":"5%","right":"5%","bottom":"18%","top":"8%","containLabel":True},
                "xAxis":{"type":"category","data":[str(y) for y in taux_yr["Year"].tolist()],
                         "axisLabel":{"color":C_MID,"fontSize":10}},
                "yAxis":{"type":"value","min":0,"max":100,
                         "axisLabel":{"color":C_MID,"fontSize":9,"formatter":"{value}%"},
                         "splitLine":{"lineStyle":{"color":C_LIGHT,"type":"dashed"}}},
                "series":[
                    {"name":"Taux Obj %","type":"line","smooth":True,
                     "data":[round(v*100,1) for v in taux_yr["Taux"].tolist()],
                     "lineStyle":{"color":C_DARK,"width":2},"itemStyle":{"color":C_DARK},"symbolSize":8,
                     "markLine":{"silent":True,
                         "lineStyle":{"color":"#E74C3C","type":"dashed","width":1.5},
                         "data":[{"yAxis":50}]}},
                    {"name":"Obj impossibles %","type":"line","smooth":True,
                     "data":[round(v,1) for v in taux_yr["Pct_Impossible"].tolist()],
                     "lineStyle":{"color":"#E67E22","width":2,"type":"dashed"},
                     "itemStyle":{"color":"#E67E22"},"symbolSize":8},
                ]
            }
            st.markdown(f"<div style='background:white;border-radius:12px;padding:10px 12px 4px;"
                        f"box-shadow:0 2px 12px rgba(71,94,114,0.09);'>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:9px;font-weight:700;color:{C_MID};"
                        f"text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;'>"
                        f"Taux objectif & objectifs impossibles par année</p>",
                        unsafe_allow_html=True)
            st_echarts(options=opt_taux_yr, height="220px", key="taux_yr_obj")
            st.markdown("</div>", unsafe_allow_html=True)

        warning_box(
            f"Ratio médian <b>×{ratio_med:.2f}</b> — les objectifs sont surévalués de ~6% en médiane. "
            f"<b>{pct_impossible:.1f}%</b> des journées ont un objectif > 2× le réel. "
            f"Conséquence directe : le taux sous 50% reflète un problème de "
            f"<b>calibration des objectifs</b>, pas un problème de performance des vendeurs."
        )
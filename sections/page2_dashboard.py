# ─────────────────────────────────────────
# sections/page2_dashboard.py
# Page 2 — Dashboard KPIs
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
from streamlit_echarts5 import st_echarts
from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG
from utils.charts import style_dataframe, info_box, success_box, warning_box


def show(data_store):

    st.title("Dashboard — Vue d'ensemble")

    info_box(
        "Ce dashboard présente les <b>9 KPIs</b> définis dans le cahier des charges. "
        "Utilisez les filtres pour explorer les performances par période, "
        "département ou vendeur."
    )

    # ════════════════════════════════════════
    # FILTRES GLOBAUX
    # Affectent tous les blocs de la page
    # ════════════════════════════════════════
    st.markdown("## Filtres")

    noms_dept = {
        "Eletrônicos" : "Électronique",
        "Vestuário"   : "Vêtements",
        "Acessórios"  : "Accessoires",
        "Casa"        : "Maison",
        "Brinquedo"   : "Jouets",
        "Esportes"    : "Sports",
        "Papelaria"   : "Papeterie"
    }

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        annees    = sorted(data_store["Year"].unique())
        annee_sel = st.multiselect(
            "Année(s)",
            options  = annees,
            default  = annees
        )

    with col_f2:
        depts    = sorted(data_store["Department"].unique())
        dept_sel = st.multiselect(
            "Département(s)",
            options      = depts,
            format_func  = lambda x: noms_dept.get(x, x),
            default      = depts
        )

    with col_f3:
        vendeurs = sorted(data_store["Seller"].unique())
        vend_sel = st.multiselect(
            "Vendeur(s)",
            options = vendeurs,
            default = vendeurs
        )

    # ── Application des filtres ──────────
    df = data_store[
        (data_store["Year"].isin(annee_sel))       &
        (data_store["Department"].isin(dept_sel))  &
        (data_store["Seller"].isin(vend_sel))
    ].copy()

    if df.empty:
        warning_box("Aucune donnée pour les filtres sélectionnés.")
        return

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 2.1 — KPIs GLOBAUX
    # 9 KPIs du cahier des charges :
    # 1. Total revenue
    # 2. Revenue vs forecast
    # 3. Average revenue
    # 4. Margin
    # 5. Margin vs forecast
    # 6. Sales quantity
    # 7. Average sales quantity
    # 8. Nb customers
    # 9. Average nb customers
    # ════════════════════════════════════════
    st.markdown("## 2.1 KPIs Globaux")

    # ── Calcul des 9 KPIs ───────────────
    total_revenue       = df["Revenue"].sum()
    revenue_vs_forecast = df["Revenue"].sum() - df["Revenue Goal"].sum()
    avg_revenue         = df["Revenue"].mean()
    total_margin        = df["Margin"].mean() * 100
    margin_vs_forecast  = (df["Margin"].mean() - df["Margin Goal"].mean()) * 100
    total_sales         = int(df["Sales Quantity"].sum())
    avg_sales           = df["Sales Quantity"].mean()
    total_customers     = int(df["Customers"].sum())
    avg_customers       = df["Customers"].mean()
    taux_global         = df["Goal_Reached"].mean() * 100

    # ════════════════════════════════════════
    # LIGNE 1 — 4 BIG NUMBER CARDS (ECharts)
    # KPI 1 : Total Revenue
    # KPI 2 : Revenue vs Forecast
    # KPI 6 : Sales Quantity
    # KPI 8 : Nb Customers
    # ════════════════════════════════════════

    def big_number_card(label, value, sous_label="", color=C_DARK):
        """
        Carte KPI ECharts avec big number centré
        label      : titre du KPI (ex: REVENU TOTAL)
        value      : valeur formatée (ex: 179.4 M€)
        sous_label : ligne secondaire (ex: Moy. 4 304 €/jour)
        color      : couleur du chiffre principal
        """
        option = {
            "backgroundColor": "white",
            "graphic": [
                # ── Valeur principale ──
                {
                    "type" : "text",
                    "left" : "center",
                    "top"  : "25%",
                    "style": {
                        "text"      : value,
                        "fontSize"  : 26,
                        "fontWeight": "bold",
                        "fill"      : color,
                        "fontFamily": "DM Sans, sans-serif",
                    }
                },
                # ── Label ──
                {
                    "type" : "text",
                    "left" : "center",
                    "top"  : "58%",
                    "style": {
                        "text"      : label,
                        "fontSize"  : 10,
                        "fill"      : C_MID,
                        "fontFamily": "DM Sans, sans-serif",
                        "fontWeight": "600",
                    }
                },
                # ── Sous-label ──
                {
                    "type" : "text",
                    "left" : "center",
                    "top"  : "75%",
                    "style": {
                        "text"      : sous_label,
                        "fontSize"  : 10,
                        "fill"      : C_WARM,
                        "fontFamily": "DM Sans, sans-serif",
                    }
                }
            ]
        }
        st_echarts(options=option, height="120px")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # KPI 1 — Total Revenue
        big_number_card(
            label      = "REVENU TOTAL",
            value      = f"{total_revenue / 1_000_000:.2f} M€",
            sous_label = f"Moy. {avg_revenue:,.0f} €/jour"
        )

    with col2:
        # KPI 2 — Revenue vs Forecast
        color_rev = C_DARK if revenue_vs_forecast >= 0 else "#c0392b"
        sign      = "▲" if revenue_vs_forecast >= 0 else "▼"
        big_number_card(
            label      = "REVENU VS OBJECTIF",
            value      = f"{sign} {abs(revenue_vs_forecast) / 1_000:.0f} K€",
            sous_label = "vs Revenue Goal",
            color      = color_rev
        )

    with col3:
        # KPI 6 — Sales Quantity
        big_number_card(
            label      = "VENTES TOTALES",
            value      = f"{total_sales:,}",
            sous_label = f"Moy. {avg_sales:.1f} / jour"
        )

    with col4:
        # KPI 8 — Nb Customers
        big_number_card(
            label      = "CLIENTS TOTAUX",
            value      = f"{total_customers:,}",
            sous_label = f"Moy. {avg_customers:.1f} / jour"
        )

    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

    # ════════════════════════════════════════
    # LIGNE 2 — 3 JAUGES (ECharts)
    # KPI 4 : Margin
    # KPI 5 : Margin vs Forecast
    # KPI Goal_Reached : Taux objectif atteint
    # ════════════════════════════════════════

    def gauge_chart(label, value, max_val=100, unit="%", color=C_DARK):
        """
        Jauge ECharts en arc
        label   : titre affiché sous la valeur
        value   : valeur numérique
        max_val : maximum de la jauge
        unit    : unité affichée (%, €...)
        color   : couleur de l'arc rempli
        """
        pct    = min(round(value / max_val, 4), 1.0)
        option = {
            "backgroundColor": "white",
            "series": [{
                "type"       : "gauge",
                "startAngle" : 200,
                "endAngle"   : -20,
                "min"        : 0,
                "max"        : max_val,
                "radius"     : "85%",
                "axisLine"   : {
                    "lineStyle": {
                        "width": 16,
                        "color": [
                            [pct,  color ],
                            [1.0,  C_LIGHT]
                        ]
                    }
                },
                "pointer"   : {"show": False},
                "axisTick"  : {"show": False},
                "splitLine" : {"show": False},
                "axisLabel" : {"show": False},
                "detail"    : {
                    "valueAnimation": True,
                    "formatter"     : f"{{value}}{unit}",
                    "color"         : color,
                    "fontSize"      : 22,
                    "fontWeight"    : "bold",
                    "fontFamily"    : "DM Sans, sans-serif",
                    "offsetCenter"  : [0, "8%"]
                },
                "title": {
                    "offsetCenter": [0, "42%"],
                    "fontSize"    : 11,
                    "color"       : C_MID,
                    "fontFamily"  : "DM Sans, sans-serif",
                },
                "data": [{"value": round(value, 1), "name": label}]
            }]
        }
        st_echarts(options=option, height="200px")

    col_g1, col_g2, col_g3 = st.columns(3)

    with col_g1:
        # KPI 4 — Margin moyenne
        gauge_chart(
            label   = "Marge Moyenne",
            value   = total_margin,
            max_val = 80,
            unit    = "%",
            color   = C_DARK
        )

    with col_g2:
        # KPI 5 — Margin vs Forecast
        color_margin = C_DARK if margin_vs_forecast >= 0 else "#c0392b"
        gauge_chart(
            label   = "Marge vs Objectif",
            value   = abs(margin_vs_forecast),
            max_val = 20,
            unit    = "%",
            color   = color_margin
        )

    with col_g3:
        # Taux Goal_Reached
        color_taux = C_DARK if taux_global >= 50 else "#c0392b"
        gauge_chart(
            label   = "Taux Objectif Atteint",
            value   = taux_global,
            max_val = 100,
            unit    = "%",
            color   = color_taux
        )

    # ════════════════════════════════════════
    # LIGNE 3 — COMMENTAIRES DYNAMIQUES
    # S'adaptent automatiquement aux filtres
    # ════════════════════════════════════════
    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns(3)

    with col_c1:
        if revenue_vs_forecast >= 0:
            success_box(
                f"Le revenu dépasse l'objectif de "
                f"<b>{revenue_vs_forecast:,.0f} €</b> — "
                f"performance positive sur la période."
            )
        else:
            warning_box(
                f"Le revenu est sous l'objectif de "
                f"<b>{abs(revenue_vs_forecast):,.0f} €</b> — "
                f"à surveiller."
            )

    with col_c2:
        if margin_vs_forecast >= 0:
            success_box(
                f"La marge dépasse l'objectif de "
                f"<b>{margin_vs_forecast:+.1f}%</b> — "
                f"rentabilité maîtrisée."
            )
        else:
            warning_box(
                f"La marge est sous l'objectif de "
                f"<b>{abs(margin_vs_forecast):.1f}%</b> — "
                f"rentabilité à améliorer."
            )

    with col_c3:
        if taux_global >= 50:
            success_box(
                f"<b>{taux_global:.1f}%</b> des journées atteignent "
                f"l'objectif — au-dessus du seuil de 50%."
            )
        else:
            warning_box(
                f"Seulement <b>{taux_global:.1f}%</b> des journées "
                f"atteignent l'objectif — en dessous de 50%."
            )

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 2.2 — ÉVOLUTION TEMPORELLE
    # Graphique mixte ECharts :
    # - Barres  = Revenue       (axe Y gauche)
    # - Courbe  = Taux Objectif (axe Y droit)
    # 2 axes Y car unités différentes (€ vs %)
    # ════════════════════════════════════════
    st.markdown("## 2.2 Évolution Temporelle")

    noms_mois = {
        1:"Jan", 2:"Fev", 3:"Mars",
        4:"Avr", 5:"Mai", 6:"Juin",
        7:"Juil", 8:"Aout", 9:"Sep",
        10:"Oct", 11:"Nov", 12:"Dec"
    }

    tab_ann, tab_mens = st.tabs(["Par Année", "Par Mois"])

    with tab_ann:

        evol_year = df.groupby("Year").agg(
            Revenue_Total = ("Revenue",      "sum"),
            Taux_Objectif = ("Goal_Reached", "mean"),
        ).reset_index()

        annees_labels = [str(y) for y in evol_year["Year"].tolist()]
        rev_data      = [round(v / 1_000_000, 2) for v in evol_year["Revenue_Total"].tolist()]
        taux_data     = [round(v * 100, 1) for v in evol_year["Taux_Objectif"].tolist()]

        option_year = {
            "backgroundColor": "white",
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {
                "data": ["Revenu (M€)", "Taux Objectif (%)"],
                "bottom": 0,
                "textStyle": {"color": C_MID, "fontSize": 11}
            },
            "grid": {"left": "5%", "right": "8%", "bottom": "12%", "top": "8%", "containLabel": True},
            "xAxis": {
                "type": "category",
                "data": annees_labels,
                "axisLine": {"lineStyle": {"color": C_LIGHT}},
                "axisLabel": {"color": C_MID, "fontSize": 11}
            },
            "yAxis": [
                {
                    "type": "value",
                    "name": "M€",
                    "nameTextStyle": {"color": C_MID, "fontSize": 10},
                    "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value} M€"},
                    "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}},
                },
                {
                    "type": "value",
                    "name": "%",
                    "min": 40,
                    "max": 55,
                    "nameTextStyle": {"color": C_MID, "fontSize": 10},
                    "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value}%"},
                    "splitLine": {"show": False},
                }
            ],
            "series": [
                {
                    "name": "Revenu (M€)",
                    "type": "bar",
                    "yAxisIndex": 0,
                    "data": rev_data,
                    "barWidth": "40%",
                    "itemStyle": {"color": C_DARK, "borderRadius": [6, 6, 0, 0]},
                    "label": {
                        "show": True, "position": "top",
                        "formatter": "{c} M€", "fontSize": 10, "color": C_DARK
                    }
                },
                {
                    "name": "Taux Objectif (%)",
                    "type": "line",
                    "yAxisIndex": 1,
                    "data": taux_data,
                    "smooth": True,
                    "lineStyle": {"color": C_WARM, "width": 3},
                    "itemStyle": {"color": C_WARM},
                    "symbol": "circle",
                    "symbolSize": 8,
                    "areaStyle": {"color": C_WARM, "opacity": 0.15},
                    "label": {
                        "show": True, "position": "top",
                        "formatter": "{c}%", "fontSize": 10, "color": C_MID
                    }
                }
            ]
        }

        st_echarts(options=option_year, height="380px")

        rev_max_year  = evol_year.loc[evol_year["Revenue_Total"].idxmax(), "Year"]
        taux_max_year = evol_year.loc[evol_year["Taux_Objectif"].idxmax(), "Year"]

        info_box(
            f"📈 L'année <b>{rev_max_year}</b> enregistre le revenu le plus élevé. "
            f"Le taux d'objectif est au plus haut en <b>{taux_max_year}</b>. "
            f"La courbe reste sous les <b>50%</b> sur toute la période — "
            f"confirme que l'objectif n'est jamais atteint en majorité."
        )

    with tab_mens:

        evol_month = df.groupby("Month").agg(
            Revenue_Moy   = ("Revenue",      "mean"),
            Taux_Objectif = ("Goal_Reached", "mean"),
        ).reset_index()

        mois_labels = [noms_mois.get(m, str(m)) for m in evol_month["Month"].tolist()]
        rev_moy     = [int(round(v, 0)) for v in evol_month["Revenue_Moy"].tolist()]
        taux_moy    = [float(round(v * 100, 1)) for v in evol_month["Taux_Objectif"].tolist()]

        option_month = {
            "backgroundColor": "white",
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {
                "data": ["Revenu Moyen (€)", "Taux Objectif (%)"],
                "bottom": 0,
                "textStyle": {"color": C_MID, "fontSize": 11}
            },
            "grid": {"left": "5%", "right": "8%", "bottom": "12%", "top": "8%", "containLabel": True},
            "xAxis": {
                "type": "category",
                "data": mois_labels,
                "axisLine": {"lineStyle": {"color": C_LIGHT}},
                "axisLabel": {"color": C_MID, "fontSize": 10, "rotate": 30}
            },
            "yAxis": [
                {
                    "type": "value",
                    "name": "€",
                    "nameTextStyle": {"color": C_MID, "fontSize": 10},
                    "axisLabel": {"color": C_MID, "fontSize": 10},
                    "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}},
                },
                {
                    "type": "value",
                    "name": "%",
                    "min": 40,
                    "max": 55,
                    "nameTextStyle": {"color": C_MID, "fontSize": 10},
                    "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value}%"},
                    "splitLine": {"show": False},
                }
            ],
            "series": [
                {
                    "name": "Revenu Moyen (€)",
                    "type": "bar",
                    "yAxisIndex": 0,
                    "data": rev_moy,
                    "barWidth": "50%",
                    "itemStyle": {"color": C_MID, "borderRadius": [6, 6, 0, 0]}
                },
                {
                    "name": "Taux Objectif (%)",
                    "type": "line",
                    "yAxisIndex": 1,
                    "data": taux_moy,
                    "smooth": True,
                    "lineStyle": {"color": C_WARM, "width": 3},
                    "itemStyle": {"color": C_WARM},
                    "symbol": "circle",
                    "symbolSize": 7,
                    "areaStyle": {"color": C_WARM, "opacity": 0.15},
                }
            ]
        }

        st_echarts(options=option_month, height="380px")

        mois_max = noms_mois.get(int(evol_month.loc[evol_month["Revenue_Moy"].idxmax(), "Month"]), "")
        mois_min = noms_mois.get(int(evol_month.loc[evol_month["Revenue_Moy"].idxmin(), "Month"]), "")

        info_box(
            f"📅 <b>{mois_max}</b> est le mois avec le revenu moyen le plus élevé. "
            f"<b>{mois_min}</b> est le plus faible — attendu car moins de jours. "
            f"La saisonnalité est <b>modérée</b> — pas de mois clairement dominant."
        )

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 2.3 — PERFORMANCE PAR DÉPARTEMENT
    # Graphique 1 : Barres horizontales Revenue
    # Graphique 2 : Barres Taux Objectif
    # Tableau     : Récap 4 métriques par dept
    # ════════════════════════════════════════
    st.markdown("## 2.3 Performance par Département")

    noms_dept_fr = {
        "Eletrônicos" : "Électronique",
        "Vestuário"   : "Vêtements",
        "Acessórios"  : "Accessoires",
        "Casa"        : "Maison",
        "Brinquedo"   : "Jouets",
        "Esportes"    : "Sports",
        "Papelaria"   : "Papeterie"
    }

    # ── Agrégation par département ───────
    dept_stats = df.groupby("Department").agg(
        Revenue_Total = ("Revenue",       "sum"),
        Revenue_Moy   = ("Revenue",       "mean"),
        Marge_Moy     = ("Margin",        "mean"),
        Taux_Objectif = ("Goal_Reached",  "mean"),
        Nb_Ventes     = ("Sales Quantity","sum"),
    ).reset_index()

    # Tri par Revenue décroissant
    dept_stats = dept_stats.sort_values("Revenue_Total", ascending=True)

    # Labels français
    dept_labels = [noms_dept_fr.get(d, d) for d in dept_stats["Department"].tolist()]
    rev_dept    = [round(v / 1_000_000, 2) for v in dept_stats["Revenue_Total"].tolist()]
    taux_dept   = [float(round(v * 100, 1)) for v in dept_stats["Taux_Objectif"].tolist()]
    marge_dept  = [float(round(v * 100, 1)) for v in dept_stats["Marge_Moy"].tolist()]

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        # ── Barres horizontales — Revenue ──
        option_dept_rev = {
            "backgroundColor": "white",
            "tooltip": {
                "trigger"  : "axis",
                "formatter": "{b} : {c} M€"
            },
            "grid": {"left": "2%", "right": "8%", "top": "4%", "bottom": "4%", "containLabel": True},
            "xAxis": {
                "type"      : "value",
                "axisLabel" : {"color": C_MID, "fontSize": 10, "formatter": "{value} M€"},
                "splitLine" : {"lineStyle": {"color": C_LIGHT, "type": "dashed"}},
            },
            "yAxis": {
                "type"     : "category",
                "data"     : dept_labels,
                "axisLabel": {"color": C_DARK, "fontSize": 11, "fontWeight": "bold"},
                "axisLine" : {"lineStyle": {"color": C_LIGHT}},
            },
            "series": [{
                "type"      : "bar",
                "data"      : rev_dept,
                "barWidth"  : "55%",
                "itemStyle" : {
                    "color"       : C_DARK,
                    "borderRadius": [0, 6, 6, 0]
                },
                "label": {
                    "show"     : True,
                    "position" : "right",
                    "formatter": "{c} M€",
                    "fontSize" : 10,
                    "color"    : C_DARK
                }
            }]
        }
        st.markdown("<div style='background:white; border-radius:14px; padding:12px; box-shadow:0 4px 16px rgba(71,94,114,0.1);'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:11px; font-weight:600; color:#73828E; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Revenu Total par Département</p>", unsafe_allow_html=True)
        st_echarts(options=option_dept_rev, height="280px")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_d2:
        # ── Barres horizontales — Taux Objectif ──
        option_dept_taux = {
            "backgroundColor": "white",
            "tooltip": {
                "trigger"  : "axis",
                "formatter": "{b} : {c}%"
            },
            "grid": {"left": "2%", "right": "8%", "top": "4%", "bottom": "4%", "containLabel": True},
            "xAxis": {
                "type"     : "value",
                "min"      : 0,
                "max"      : 100,
                "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value}%"},
                "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}},
            },
            "yAxis": {
                "type"     : "category",
                "data"     : dept_labels,
                "axisLabel": {"color": C_DARK, "fontSize": 11, "fontWeight": "bold"},
                "axisLine" : {"lineStyle": {"color": C_LIGHT}},
            },
            "series": [{
                "type"    : "bar",
                "data"    : taux_dept,
                "barWidth": "55%",
                "itemStyle": {
                    "color": {
                        "type"         : "linear",
                        "x"            : 0, "y": 0, "x2": 1, "y2": 0,
                        "colorStops"   : [
                            {"offset": 0,   "color": C_MID},
                            {"offset": 1,   "color": C_WARM}
                        ]
                    },
                    "borderRadius": [0, 6, 6, 0]
                },
                "markLine": {
                    "silent"  : True,
                    "lineStyle": {"color": "#c0392b", "type": "dashed", "width": 1.5},
                    "data"    : [{"xAxis": 50, "label": {"formatter": "50%", "color": "#c0392b", "fontSize": 10}}]
                },
                "label": {
                    "show"    : True,
                    "position": "right",
                    "formatter": "{c}%",
                    "fontSize": 10,
                    "color"   : C_MID
                }
            }]
        }
        st.markdown("<div style='background:white; border-radius:14px; padding:12px; box-shadow:0 4px 16px rgba(71,94,114,0.1);'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:11px; font-weight:600; color:#73828E; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Taux Objectif Atteint par Département</p>", unsafe_allow_html=True)
        st_echarts(options=option_dept_taux, height="280px")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tableau récap ────────────────────
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    dept_table = dept_stats.copy()
    dept_table["Département"]    = dept_table["Department"].map(lambda x: noms_dept_fr.get(x, x))
    dept_table["Revenu Total"]   = dept_table["Revenue_Total"].map(lambda x: f"{x/1_000_000:.2f} M€")
    dept_table["Revenu Moyen"]   = dept_table["Revenue_Moy"].map(lambda x: f"{x:,.0f} €")
    dept_table["Marge Moyenne"]  = dept_table["Marge_Moy"].map(lambda x: f"{x*100:.1f}%")
    dept_table["Taux Objectif"]  = dept_table["Taux_Objectif"].map(lambda x: f"{x*100:.1f}%")

    dept_table = dept_table[["Département","Revenu Total","Revenu Moyen","Marge Moyenne","Taux Objectif"]]
    dept_table = dept_table.sort_values("Revenu Total", ascending=False)

    st.dataframe(
        style_dataframe(dept_table.reset_index(drop=True)),
        use_container_width=True,
        hide_index=True
    )

    # ── Commentaire ─────────────────────
    best_dept  = noms_dept_fr.get(dept_stats.loc[dept_stats["Revenue_Total"].idxmax(), "Department"], "")
    best_taux  = noms_dept_fr.get(dept_stats.loc[dept_stats["Taux_Objectif"].idxmax(), "Department"], "")
    worst_dept = noms_dept_fr.get(dept_stats.loc[dept_stats["Revenue_Total"].idxmin(), "Department"], "")

    info_box(
        f"🏆 <b>{best_dept}</b> génère le revenu le plus élevé. "
        f"<b>{best_taux}</b> a le meilleur taux d'objectif atteint. "
        f"<b>{worst_dept}</b> est le département le moins performant en revenu — "
        f"à cibler en priorité pour les actions marketing."
    )

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 2.4 — PERFORMANCE PAR VENDEUR
    # Graphique 1 : Barres horizontales Revenue
    # Graphique 2 : Scatter Revenue vs Taux
    # Tableau     : Classement complet vendeurs
    # ════════════════════════════════════════
    st.markdown("## 2.4 Performance par Vendeur")

    # ── Agrégation par vendeur ───────────
    seller_stats = df.groupby("Seller").agg(
        Revenue_Total = ("Revenue",       "sum"),
        Revenue_Moy   = ("Revenue",       "mean"),
        Marge_Moy     = ("Margin",        "mean"),
        Taux_Objectif = ("Goal_Reached",  "mean"),
        Nb_Ventes     = ("Sales Quantity","sum"),
        Nb_Clients    = ("Customers",     "sum"),
    ).reset_index()

    # Tri par Revenue décroissant pour le classement
    seller_stats = seller_stats.sort_values("Revenue_Total", ascending=False).reset_index(drop=True)
    seller_stats["Rang"] = seller_stats.index + 1

    # Top 10 pour les graphiques (lisibilité)
    top10 = seller_stats.head(10).sort_values("Revenue_Total", ascending=True)

    seller_labels = top10["Seller"].tolist()
    rev_seller    = [round(v / 1_000_000, 2) for v in top10["Revenue_Total"].tolist()]
    taux_seller   = [float(round(v * 100, 1)) for v in top10["Taux_Objectif"].tolist()]

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        # ── Barres horizontales — Revenue Top 10 ──
        option_seller_rev = {
            "backgroundColor": "white",
            "tooltip": {
                "trigger"  : "axis",
                "formatter": "{b} : {c} M€"
            },
            "grid": {"left": "2%", "right": "10%", "top": "4%", "bottom": "4%", "containLabel": True},
            "xAxis": {
                "type"     : "value",
                "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value} M€"},
                "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}},
            },
            "yAxis": {
                "type"     : "category",
                "data"     : seller_labels,
                "axisLabel": {"color": C_DARK, "fontSize": 10},
                "axisLine" : {"lineStyle": {"color": C_LIGHT}},
            },
            "series": [{
                "type"    : "bar",
                "data"    : rev_seller,
                "barWidth": "55%",
                "itemStyle": {
                    "color"       : C_DARK,
                    "borderRadius": [0, 6, 6, 0]
                },
                "label": {
                    "show"    : True,
                    "position": "right",
                    "formatter": "{c} M€",
                    "fontSize": 10,
                    "color"   : C_DARK
                }
            }]
        }
        st.markdown("<div style='background:white; border-radius:14px; padding:12px; box-shadow:0 4px 16px rgba(71,94,114,0.1);'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:11px; font-weight:600; color:#73828E; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Top 10 Vendeurs — Revenu Total</p>", unsafe_allow_html=True)
        st_echarts(options=option_seller_rev, height="300px")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s2:
        # ── Barres horizontales — Top 10 Taux Objectif ──
        top10_taux = seller_stats.sort_values("Taux_Objectif", ascending=False).head(10)
        top10_taux = top10_taux.sort_values("Taux_Objectif", ascending=True)

        taux_labels  = top10_taux["Seller"].tolist()
        taux_vals    = [float(round(v * 100, 1)) for v in top10_taux["Taux_Objectif"].tolist()]

        option_seller_taux = {
            "backgroundColor": "white",
            "tooltip": {
                "trigger"  : "axis",
                "formatter": "{b} : {c}%"
            },
            "grid": {"left": "2%", "right": "10%", "top": "4%", "bottom": "4%", "containLabel": True},
            "xAxis": {
                "type"     : "value",
                "min"      : 0,
                "max"      : 100,
                "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value}%"},
                "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}},
            },
            "yAxis": {
                "type"     : "category",
                "data"     : taux_labels,
                "axisLabel": {"color": C_DARK, "fontSize": 10},
                "axisLine" : {"lineStyle": {"color": C_LIGHT}},
            },
            "series": [{
                "type"    : "bar",
                "data"    : taux_vals,
                "barWidth": "55%",
                "itemStyle": {
                    "color": {
                        "type"      : "linear",
                        "x": 0, "y": 0, "x2": 1, "y2": 0,
                        "colorStops": [
                            {"offset": 0, "color": C_MID},
                            {"offset": 1, "color": C_WARM}
                        ]
                    },
                    "borderRadius": [0, 6, 6, 0]
                },
                "markLine": {
                    "silent"   : True,
                    "lineStyle": {"color": "#c0392b", "type": "dashed", "width": 1.5},
                    "data"     : [{"xAxis": 50, "label": {"formatter": "50%", "color": "#c0392b", "fontSize": 10}}]
                },
                "label": {
                    "show"    : True,
                    "position": "right",
                    "formatter": "{c}%",
                    "fontSize": 10,
                    "color"   : C_MID
                }
            }]
        }
        st.markdown("<div style='background:white; border-radius:14px; padding:12px; box-shadow:0 4px 16px rgba(71,94,114,0.1);'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:11px; font-weight:600; color:#73828E; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Top 10 Vendeurs — Taux Objectif</p>", unsafe_allow_html=True)
        st_echarts(options=option_seller_taux, height="300px")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tableau classement complet ───────
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    seller_table = seller_stats.copy()
    seller_table["Rang"]          = seller_table["Rang"].map(lambda x: f"#{x}")
    seller_table["Revenu Total"]  = seller_table["Revenue_Total"].map(lambda x: f"{x/1_000_000:.2f} M€")
    seller_table["Revenu Moyen"]  = seller_table["Revenue_Moy"].map(lambda x: f"{x:,.0f} €")
    seller_table["Marge Moyenne"] = seller_table["Marge_Moy"].map(lambda x: f"{x*100:.1f}%")
    seller_table["Taux Objectif"] = seller_table["Taux_Objectif"].map(lambda x: f"{x*100:.1f}%")
    seller_table["Nb Ventes"]     = seller_table["Nb_Ventes"].map(lambda x: f"{int(x):,}")
    seller_table["Nb Clients"]    = seller_table["Nb_Clients"].map(lambda x: f"{int(x):,}")

    seller_table = seller_table[["Rang","Seller","Revenu Total","Revenu Moyen","Marge Moyenne","Taux Objectif","Nb Ventes","Nb Clients"]]

    st.dataframe(
        style_dataframe(seller_table),
        use_container_width=True,
        hide_index=True
    )

    # ── Commentaire ─────────────────────
    best_seller  = seller_stats.loc[seller_stats["Revenue_Total"].idxmax(), "Seller"]
    best_taux_s  = seller_stats.loc[seller_stats["Taux_Objectif"].idxmax(), "Seller"]
    worst_seller = seller_stats.loc[seller_stats["Revenue_Total"].idxmin(), "Seller"]

    info_box(
        f"🥇 <b>{best_seller}</b> est le vendeur avec le revenu total le plus élevé. "
        f"<b>{best_taux_s}</b> a le meilleur taux d'objectif atteint. "
        f"Le scatter plot révèle les <b>4 profils</b> de vendeurs — "
        f"les points en haut à droite sont les <b>stars</b>, "
        f"ceux en bas à gauche sont <b>à accompagner</b>."
    )

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 2.5 — SYNTHÈSE
    # Récapitulatif des insights clés
    # Lien avec les pages suivantes
    # ════════════════════════════════════════
    st.markdown("## 2.5 Synthèse & Insights Clés")

    # ── 3 colonnes d'insights ───────────
    col_syn1, col_syn2, col_syn3 = st.columns(3)

    # Calculs pour la synthèse
    best_dept_rev   = noms_dept_fr.get(
        df.groupby("Department")["Revenue"].sum().idxmax(), "")
    best_dept_taux  = noms_dept_fr.get(
        df.groupby("Department")["Goal_Reached"].mean().idxmax(), "")
    best_sell_rev   = df.groupby("Seller")["Revenue"].sum().idxmax()
    best_sell_taux  = df.groupby("Seller")["Goal_Reached"].mean().idxmax()
    taux_global_syn = float(round(df["Goal_Reached"].mean() * 100, 1))
    rev_total_syn   = df["Revenue"].sum()
    marge_syn       = float(round(df["Margin"].mean() * 100, 1))

    with col_syn1:
        st.markdown(f"""
        <div style='
            background: white;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(71,94,114,0.1);
            border-top: 3px solid {C_DARK};
            height: 100%;
        '>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
               text-transform:uppercase; letter-spacing:1px; margin-bottom:14px;'>
               📊 Vue Globale
            </p>
            <p style='font-size:13px; color:{C_DARK}; line-height:1.8; margin:0;'>
                • Revenu total : <b>{rev_total_syn/1_000_000:.1f} M€</b><br>
                • Marge moyenne : <b>{marge_syn:.1f}%</b><br>
                • Taux objectif global : <b>{taux_global_syn:.1f}%</b><br>
                • Seuil 50% <b>jamais atteint</b> sur la période<br>
                • Performance <b>stable</b> sur 6 années
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_syn2:
        st.markdown(f"""
        <div style='
            background: white;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(71,94,114,0.1);
            border-top: 3px solid {C_WARM};
            height: 100%;
        '>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
               text-transform:uppercase; letter-spacing:1px; margin-bottom:14px;'>
               🏬 Meilleurs Performeurs
            </p>
            <p style='font-size:13px; color:{C_DARK}; line-height:1.8; margin:0;'>
                • Dept. revenu : <b>{best_dept_rev}</b><br>
                • Dept. taux : <b>{best_dept_taux}</b><br>
                • Vendeur revenu : <b>{best_sell_rev.split()[0]}</b><br>
                • Vendeur taux : <b>{best_sell_taux.split()[0]}</b><br>
                • Disparités <b>significatives</b> entre vendeurs
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_syn3:
        st.markdown(f"""
        <div style='
            background: white;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(71,94,114,0.1);
            border-top: 3px solid {C_MID};
            height: 100%;
        '>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
               text-transform:uppercase; letter-spacing:1px; margin-bottom:14px;'>
               🔍 Prochaines Analyses
            </p>
            <p style='font-size:13px; color:{C_DARK}; line-height:1.8; margin:0;'>
                • <b>Page 3</b> — Segmenter les vendeurs<br>
                &nbsp;&nbsp;en profils homogènes (K-Means)<br>
                • <b>Page 4</b> — Prédire si un vendeur<br>
                &nbsp;&nbsp;atteindra son objectif (Random Forest)<br>
                • <b>Page 5</b> — Estimer le revenu futur<br>
                &nbsp;&nbsp;(Régression)<br>
                • <b>Page 6</b> — Recommandations<br>
                &nbsp;&nbsp;marketing ciblées
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Message de conclusion ────────────
    success_box(
        f"Le dashboard confirme que le taux d'objectif de <b>{taux_global_syn:.1f}%</b> "
        f"est insuffisant sur l'ensemble de la période. "
        f"Les analyses suivantes (segmentation, classification, prédiction) permettront "
        f"d'identifier les <b>leviers d'amélioration</b> et de produire des "
        f"<b>recommandations actionnables</b> pour le management."
    )
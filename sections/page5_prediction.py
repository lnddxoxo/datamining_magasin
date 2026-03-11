# ─────────────────────────────────────────
# sections/page5_prediction.py
# Page 5 — Prédiction par Régression Linéaire
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts5 import st_echarts
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG
from utils.charts import info_box, success_box, warning_box


def show(data_store):

    st.title("Prédiction — Indicateurs Futurs")
    st.markdown(f"""
    <div style='background:{C_DARK}; border-radius:12px; padding:14px 20px; margin-bottom:20px;'>
        <p style='color:{C_WARM}; font-size:11px; font-weight:700;
          text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>
          Méthodologie KDD — Étape 4
        </p>
        <p style='color:white; font-size:14px; margin:0;'>
          <b>Data Mining</b> —  : Régression supervisée
          &nbsp;·&nbsp; Algorithme : Régression Linéaire
          &nbsp;·&nbsp; Cibles : Sales Quantity · Customers · Revenue
        </p>
    </div>
    """, unsafe_allow_html=True)
     
    st.info(
         "🎯 **Objectif **\n\n"
         "À partir des données historiques 2017–2022, on modélise la tendance de "
        "3 indicateurs clés dans le temps pour **anticiper les mois futurs** "
        "et permettre des actions concrètes :\n\n"
        "- 📦 **Sales Quantity** → ajuster les stocks\n"
        "- 👥 **Customers** → planifier le personnel\n"
        "- 💶 **Revenue** → fixer les objectifs financiers"
    ) 
    st.markdown("---")

    # ── Préparation des données ──────────
    df = data_store.copy()
    df["Date"]  = pd.to_datetime(df["Date"])
    df["Year"]  = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    tab1, tab2 = st.tabs(["📦 Par Département", "👤 Par Vendeur"]) 


    # ════════════════════════════════════════
    # BLOC 5.1 — PAR DÉPARTEMENT
    # ════════════════════════════════════════
    with tab1:

        st.markdown("## 5.1 Prédiction par Département")

        info_box(
            "Choisissez un département et le nombre de mois à prédire. "
            "Le modèle va analyser la <b>tendance historique mensuelle</b> "
            "de chaque indicateur depuis 2017 et l'extrapole sur les prochains mois."
        )

        
        st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

        # ── 5.1.A — Sélecteurs ──────────
        col_sel1, col_sel2 = st.columns(2)

        with col_sel1:
            departements = sorted(df["Department"].unique().tolist())
            dept_choisi  = st.selectbox("📦 Département", departements, key="dept")

        with col_sel2:
            nb_mois = st.slider(
                "📅 Mois à prédire",
                min_value=1, max_value=12, value=6, step=1,
                key="nb_mois_dept"
            )

        st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

        # ── Préparation données département ──
        df_dept = (
            df[df["Department"] == dept_choisi]
            .groupby(["Year", "Month"])
            .agg(
                Revenue   = ("Revenue",        "sum"),
                Sales_Qty = ("Sales Quantity",  "sum"),
                Customers = ("Customers",       "sum"),
            )
            .reset_index()
            .sort_values(["Year", "Month"])
            .reset_index(drop=True)
        )
        df_dept["t"] = range(len(df_dept))

        # Labels historiques
        labels_hist = [
            f"{int(row['Year'])}-{str(int(row['Month'])).zfill(2)}"
            for _, row in df_dept.iterrows()
        ]

        # Labels futurs
        last_year  = int(df_dept["Year"].iloc[-1])
        last_month = int(df_dept["Month"].iloc[-1])
        labels_futurs = []
        y, m = last_year, last_month
        for _ in range(nb_mois):
            m += 1
            if m > 12:
                m = 1
                y += 1
            labels_futurs.append(f"{y}-{str(m).zfill(2)}")

        labels_all = labels_hist + labels_futurs

        # t futurs et t global pour prédiction
        t_max    = int(df_dept["t"].max())
        t_futurs = np.array(range(t_max + 1, t_max + 1 + nb_mois)).reshape(-1, 1)
        t_all    = np.array(range(len(df_dept) + nb_mois)).reshape(-1, 1)

        st.markdown("---")

        # ════════════════════════════════
        # Fonction utilitaire régression
        # ════════════════════════════════
        def bloc_prediction(label, colonne, unite, action, couleur, key_suffix):
            """
            Affiche un bloc complet de prédiction pour un indicateur donné.
            - label    : nom affiché (ex: "Sales Quantity")
            - colonne  : colonne dans df_dept (ex: "Sales_Qty")
            - unite    : unité affichée (ex: "unités", "clients", "€")
            - action   : phrase d'action concrète pour le manager
            - couleur  : couleur de la card tendance
            - key_suffix : suffixe unique pour les clés Streamlit
            """

            st.markdown(f"### 📊 {label}")

            y_vals = df_dept[colonne].values
            X_t    = df_dept[["t"]].values

            # Régression
            reg = LinearRegression()
            reg.fit(X_t, y_vals)

            y_pred_hist = reg.predict(X_t)
            r2   = round(r2_score(y_vals, y_pred_hist), 3)
            mae  = round(mean_absolute_error(y_vals, y_pred_hist), 0)
            coef = round(float(reg.coef_[0]), 1)

            # Prédictions futures
            pred_futurs  = reg.predict(t_futurs)
            tendance_all = reg.predict(t_all)

            # ── Cards métriques ──────────
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)

            with col_m1:
                st.markdown(f"""
                <div style='background:white; border-radius:12px; padding:16px;
                box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
                border-top:3px solid {C_DARK};'>
                    <p style='font-size:10px; font-weight:700; color:{C_MID};
                    text-transform:uppercase; letter-spacing:1px; margin:0 0 6px 0;'>R²</p>
                    <p style='font-size:28px; font-weight:900; color:{C_DARK}; margin:0;'>{r2}</p>
                    <p style='font-size:11px; color:{C_MID}; margin:4px 0 0 0;'>qualité modèle</p>
                </div>
                """, unsafe_allow_html=True)

            with col_m2:
                st.markdown(f"""
                <div style='background:white; border-radius:12px; padding:16px;
                box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
                border-top:3px solid {C_MID};'>
                    <p style='font-size:10px; font-weight:700; color:{C_MID};
                    text-transform:uppercase; letter-spacing:1px; margin:0 0 6px 0;'>MAE</p>
                    <p style='font-size:28px; font-weight:900; color:{C_DARK}; margin:0;'>{mae:,.0f}</p>
                    <p style='font-size:11px; color:{C_MID}; margin:4px 0 0 0;'>{unite} d'erreur moy.</p>
                </div>
                """, unsafe_allow_html=True)

            with col_m3:
                direction  = "📈 Hausse" if coef > 0 else "📉 Baisse"
                dir_color  = "#2ecc71" if coef > 0 else "#e74c3c"
                st.markdown(f"""
                <div style='background:white; border-radius:12px; padding:16px;
                box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
                border-top:3px solid {C_WARM};'>
                    <p style='font-size:10px; font-weight:700; color:{C_MID};
                    text-transform:uppercase; letter-spacing:1px; margin:0 0 6px 0;'>Tendance</p>
                    <p style='font-size:18px; font-weight:900; color:{dir_color}; margin:0;'>{direction}</p>
                    <p style='font-size:11px; color:{C_MID}; margin:4px 0 0 0;'>{abs(coef):,.1f} {unite}/mois</p>
                </div>
                """, unsafe_allow_html=True)

            with col_m4:
                val_prochain = round(float(pred_futurs[0]), 0)
                st.markdown(f"""
                <div style='background:white; border-radius:12px; padding:16px;
                box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
                border-top:3px solid {couleur};'>
                    <p style='font-size:10px; font-weight:700; color:{C_MID};
                    text-transform:uppercase; letter-spacing:1px; margin:0 0 6px 0;'>Mois prochain</p>
                    <p style='font-size:28px; font-weight:900; color:{C_DARK}; margin:0;'>{val_prochain:,.0f}</p>
                    <p style='font-size:11px; color:{C_MID}; margin:4px 0 0 0;'>{unite} prédit(s)</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

            # ── Interprétation R² ────────
            if r2 >= 0.7:
                success_box(
                    f"<b>R² = {r2}</b> — La tendance explique <b>{round(r2*100,1)}%</b> "
                    f"de la variation de <b>{label}</b> pour <b>{dept_choisi}</b>. "
                    f"Prédiction fiable. {action}"
                )
            elif r2 >= 0.4:
                warning_box(
                    f"<b>R² = {r2}</b> — Tendance modérée (<b>{round(r2*100,1)}%</b>). "
                    f"Des variations irrégulières limitent la précision. {action}"
                )
            else:
                warning_box(
                    f"<b>R² = {r2}</b> — Tendance faible (<b>{round(r2*100,1)}%</b>). "
                    f"Ce département est très irrégulier — prédiction à prendre avec précaution. {action}"
                )

            st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

            # ── Graphique ────────────────
            rev_reelle_list   = [round(float(v), 1) for v in y_vals]
            tendance_all_list = [round(float(v), 1) for v in tendance_all]
            pred_futurs_list  = [round(float(v), 1) for v in pred_futurs]

            option = {
                "backgroundColor": "white",
                "tooltip": {"trigger": "axis"},
                "legend": {
                    "data": [label, "Tendance", "Prédiction future"],
                    "textStyle": {"color": C_MID, "fontSize": 11},
                    "bottom": 0
                },
                "grid": {"left": "3%", "right": "3%", "top": "8%", "bottom": "14%", "containLabel": True},
                "xAxis": {
                    "type": "category",
                    "data": labels_all,
                    "axisLabel": {"color": C_MID, "fontSize": 9, "rotate": 45}
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {"color": C_MID, "fontSize": 10},
                    "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}}
                },
                "series": [
                    {
                        "name": label,
                        "type": "line",
                        "data": rev_reelle_list + [None] * nb_mois,
                        "itemStyle": {"color": C_DARK},
                        "lineStyle": {"color": C_DARK, "width": 2},
                        "symbol": "circle",
                        "symbolSize": 4
                    },
                    {
                        "name": "Tendance",
                        "type": "line",
                        "data": tendance_all_list,
                        "itemStyle": {"color": C_MID},
                        "lineStyle": {"color": C_MID, "width": 2, "type": "dashed"},
                        "symbol": "none"
                    },
                    {
                        "name": "Prédiction future",
                        "type": "line",
                        "data": [None] * len(df_dept) + pred_futurs_list,
                        "itemStyle": {"color": C_WARM},
                        "lineStyle": {"color": C_WARM, "width": 3},
                        "symbol": "diamond",
                        "symbolSize": 8,
                        "areaStyle": {"color": C_WARM, "opacity": 0.15}
                    }
                ]
            }

            st.markdown("<div style='background:white; border-radius:12px; padding:12px; box-shadow:0 4px 16px rgba(71,94,114,0.1);'>", unsafe_allow_html=True)
            st_echarts(options=option, height="320px", key=f"chart_{key_suffix}_{dept_choisi}_{nb_mois}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

            # ── Tableau prédictions ──────
            st.markdown("#### Valeurs prédites mois par mois")
            df_table = pd.DataFrame({
                "Mois": labels_futurs,
                f"{label} prédit": [f"{round(float(v), 0):,.0f} {unite}" for v in pred_futurs]
            })
            st.dataframe(df_table, use_container_width=True, hide_index=True)

            st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)

        # ════════════════════════════════
        # 5.1.B — Sales Quantity
        # ════════════════════════════════
        bloc_prediction(
            label      = "Sales Quantity",
            colonne    = "Sales_Qty",
            unite      = "unités",
            action     = "Utilisez cette prévision pour <b>anticiper les commandes de stock</b> avant le mois.",
            couleur    = C_DARK,
            key_suffix = "qty"
        )

        # ════════════════════════════════
        # 5.1.C — Customers
        # ════════════════════════════════
        bloc_prediction(
            label      = "Customers",
            colonne    = "Customers",
            unite      = "clients",
            action     = "Utilisez cette prévision pour <b>planifier le personnel</b> et adapter l'accueil.",
            couleur    = C_MID,
            key_suffix = "cust"
        )

        # ════════════════════════════════
        # 5.1.D — Revenue
        # ════════════════════════════════
        bloc_prediction(
            label      = "Revenue",
            colonne    = "Revenue",
            unite      = "€",
            action     = "Utilisez cette prévision pour <b>fixer les objectifs financiers</b> du département.",
            couleur    = C_WARM,
            key_suffix = "rev"
        )



        
    

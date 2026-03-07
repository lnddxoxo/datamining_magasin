# ─────────────────────────────────────────
# sections/page4_classification.py
# Page 4 — Classification par Arbre de Décision
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts5 import st_echarts
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score,
                              confusion_matrix,
                              precision_score,
                              f1_score)
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG
from utils.charts import info_box, success_box, warning_box, style_dataframe


def show(data_store):

    st.title("Classification — Prédiction d'Objectif")

    st.markdown(f"""
    <div style='background:{C_DARK}; border-radius:12px; padding:14px 20px; margin-bottom:20px;'>
        <p style='color:{C_WARM}; font-size:11px; font-weight:700;
          text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>
          Méthodologie KDD — Étape 4
        </p>
        <p style='color:white; font-size:14px; margin:0;'>
          <b>Data Mining</b> — Technique 2 : Classification supervisée
          &nbsp;·&nbsp; Algorithme : Arbre de Décision
          &nbsp;·&nbsp; Cible : Goal_Reached (0 ou 1)
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 4.1 — JUSTIFICATION
    # ════════════════════════════════════════
    st.markdown("## 4.1 Justification de l'Approche")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Pourquoi la Classification ?")
        info_box(
            "La variable <b>Goal_Reached</b> indique si un vendeur a atteint "
            "son objectif de revenu journalier (1 = oui, 0 = non). "
            "L'objectif est de <b>prédire ce résultat</b> à partir des "
            "caractéristiques de la journée — avant même qu'elle se termine."
        )
        st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
        st.markdown("### Question Métier")
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:16px 20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); border-left:4px solid {C_WARM};'>
            <p style='font-size:15px; color:{C_DARK}; font-style:italic; margin:0;'>
            "Étant donné le revenu, la marge et l'activité d'un vendeur,
            va-t-il <b>atteindre son objectif</b> aujourd'hui ?"
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Pourquoi l'Arbre de Décision ?")
        raisons = [
            ("👁️", "Interprétable",
             "On peut visualiser et expliquer chaque décision — contrairement au Random Forest"),
            ("📐", "Sans standardisation",
             "Les arbres sont insensibles à l'échelle des variables — pas besoin de normaliser"),
            ("🎓", "Conforme au cours",
             "Algorithme classique enseigné en data mining et marketing analytique"),
            ("⚡", "Rapide",
             "S'entraîne en quelques secondes même sur 41 629 lignes"),
        ]
        for icon, titre, desc in raisons:
            st.markdown(f"""
            <div style='background:white; border-radius:10px; padding:10px 14px;
            margin-bottom:8px; box-shadow:0 2px 8px rgba(71,94,114,0.08);'>
                <p style='font-size:13px; font-weight:700; color:{C_DARK}; margin:0 0 2px 0;'>
                {icon} {titre}</p>
                <p style='font-size:12px; color:{C_MID}; margin:0;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    st.markdown("### Variables du Modèle")

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:16px 20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); border-top:3px solid {C_DARK};'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 12px 0;'>
            ⚙️ Variables Prédictives (X)</p>
            <p style='font-size:13px; color:{C_DARK}; line-height:2; margin:0;'>
                • <b>Revenue</b> — chiffre d'affaires journalier<br>
                • <b>Margin</b> — taux de marge<br>
                • <b>Sales Quantity</b> — unités vendues<br>
                • <b>Customers</b> — nombre de clients
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_v2:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:16px 20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); border-top:3px solid {C_WARM};'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 12px 0;'>
            🎯 Variable Cible (Y)</p>
            <p style='font-size:13px; color:{C_DARK}; line-height:2; margin:0;'>
                • <b>Goal_Reached</b> — 1 si objectif atteint, 0 sinon<br><br>
                Distribution dans le dataset :<br>
                • Classe 0 (non atteint) : ~53%<br>
                • Classe 1 (atteint) : ~47%<br><br>
                <span style='color:{C_MID}; font-size:12px;'>
                Classes quasi-équilibrées — pas de biais majeur</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 4.2 — TRAIN / TEST SPLIT
    # ════════════════════════════════════════
    st.markdown("## 4.2 Découpage Train / Test")

    df = data_store.copy()
    features = ["Revenue", "Margin", "Sales Quantity", "Customers"]
    X = df[features]
    y = df["Goal_Reached"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42
    )

    col_t1, col_t2, col_t3 = st.columns(3)

    with col_t1:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_DARK};'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>
            Dataset Complet</p>
            <p style='font-size:32px; font-weight:900; color:{C_DARK}; margin:0;'>
            {len(df):,}</p>
            <p style='font-size:12px; color:{C_MID}; margin:4px 0 0 0;'>lignes</p>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        pct_train = round(len(X_train) / len(df) * 100, 1)
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_DARK};'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>
            Train (70%)</p>
            <p style='font-size:32px; font-weight:900; color:{C_DARK}; margin:0;'>
            {len(X_train):,}</p>
            <p style='font-size:12px; color:{C_MID}; margin:4px 0 0 0;'>
            lignes — {pct_train}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col_t3:
        pct_test = round(len(X_test) / len(df) * 100, 1)
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_WARM};'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>
            Test (30%)</p>
            <p style='font-size:32px; font-weight:900; color:{C_DARK}; margin:0;'>
            {len(X_test):,}</p>
            <p style='font-size:12px; color:{C_MID}; margin:4px 0 0 0;'>
            lignes — {pct_test}%</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Distribution de Goal_Reached")

    train_0 = round(y_train.value_counts(normalize=True)[0] * 100, 1)
    train_1 = round(y_train.value_counts(normalize=True)[1] * 100, 1)
    test_0  = round(y_test.value_counts(normalize=True)[0] * 100, 1)
    test_1  = round(y_test.value_counts(normalize=True)[1] * 100, 1)

    option_dist = {
        "backgroundColor": "white",
        "tooltip": {"trigger": "axis"},
        "legend": {
            "data": ["Classe 0 — Non atteint", "Classe 1 — Atteint"],
            "textStyle": {"color": C_MID, "fontSize": 11}
        },
        "grid": {"left": "3%", "right": "3%", "top": "15%",
                 "bottom": "3%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": ["Train (70%)", "Test (30%)"],
            "axisLabel": {"color": C_DARK, "fontSize": 12, "fontWeight": "bold"}
        },
        "yAxis": {
            "type": "value",
            "max": 100,
            "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value}%"},
            "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}}
        },
        "series": [
            {
                "name": "Classe 0 — Non atteint",
                "type": "bar",
                "stack": "total",
                "data": [train_0, test_0],
                "itemStyle": {"color": C_DARK},
                "label": {"show": True, "formatter": "{c}%", "fontSize": 11, "color": "white"}
            },
            {
                "name": "Classe 1 — Atteint",
                "type": "bar",
                "stack": "total",
                "data": [train_1, test_1],
                "itemStyle": {"color": C_WARM, "borderRadius": [6, 6, 0, 0]},
                "label": {"show": True, "formatter": "{c}%", "fontSize": 11, "color": C_DARK}
            }
        ]
    }

    col_d1, col_d2 = st.columns([1, 2])

    with col_d1:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); margin-top:8px;'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 14px 0;'>Détail</p>
            <p style='font-size:13px; color:{C_DARK}; line-height:2; margin:0;'>
                <b>Train</b><br>Classe 0 : {train_0}%<br>Classe 1 : {train_1}%<br><br>
                <b>Test</b><br>Classe 0 : {test_0}%<br>Classe 1 : {test_1}%
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_d2:
        st.markdown("<div style='background:white; border-radius:12px; padding:12px; box-shadow:0 4px 16px rgba(71,94,114,0.1);'>", unsafe_allow_html=True)
        st_echarts(options=option_dist, height="250px")
        st.markdown("</div>", unsafe_allow_html=True)

    diff = abs(train_1 - test_1)
    if diff < 2:
        success_box(
            f"Distribution équilibrée — Classe 1 à <b>{train_1}%</b> en train "
            f"et <b>{test_1}%</b> en test. "
            f"L'écart de <b>{diff}%</b> est négligeable — le découpage est représentatif."
        )
    else:
        warning_box(
            f"Légère différence de distribution — {round(diff, 2)}% d'écart. "
            f"Résultat acceptable mais à surveiller."
        )

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 4.3 — ENTRAÎNEMENT
    # ════════════════════════════════════════
    st.markdown("## 4.3 Entraînement du Modèle")

    info_box(
        "La <b>profondeur</b> contrôle la complexité de l'arbre. "
        "Trop faible = modèle trop simple (underfitting). "
        "Trop élevée = modèle qui mémorise les données (overfitting). "
        "On cherche l'équilibre où train ≈ test."
    )

    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

    depth = st.slider("Profondeur maximale de l'arbre", min_value=2, max_value=8, value=5, step=1)

    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)

    acc_train = round(accuracy_score(y_train, model.predict(X_train)) * 100, 1)
    acc_test  = round(accuracy_score(y_test,  model.predict(X_test))  * 100, 1)
    diff_acc  = round(acc_train - acc_test, 1)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_MID};'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Profondeur</p>
            <p style='font-size:36px; font-weight:900; color:{C_DARK}; margin:0;'>{depth}</p>
            <p style='font-size:12px; color:{C_MID}; margin:4px 0 0 0;'>niveaux</p>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_DARK};'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Accuracy Train</p>
            <p style='font-size:36px; font-weight:900; color:{C_DARK}; margin:0;'>{acc_train}%</p>
            <p style='font-size:12px; color:{C_MID}; margin:4px 0 0 0;'>sur données d'apprentissage</p>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        color_test = "#2ecc71" if acc_test >= 65 else "#e74c3c"
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_WARM};'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Accuracy Test</p>
            <p style='font-size:36px; font-weight:900; color:{color_test}; margin:0;'>{acc_test}%</p>
            <p style='font-size:12px; color:{C_MID}; margin:4px 0 0 0;'>sur données inconnues</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    if diff_acc <= 3:
        success_box(
            f"Profondeur <b>{depth}</b> — Bon équilibre ! "
            f"Accuracy train <b>{acc_train}%</b> vs test <b>{acc_test}%</b> — "
            f"écart de seulement <b>{diff_acc}%</b>. Pas d'overfitting détecté."
        )
    elif diff_acc <= 8:
        warning_box(
            f"Profondeur <b>{depth}</b> — Léger overfitting. "
            f"Écart train/test de <b>{diff_acc}%</b>. Essaie une profondeur plus faible."
        )
    else:
        warning_box(
            f"Profondeur <b>{depth}</b> — Overfitting important ! "
            f"Écart de <b>{diff_acc}%</b> entre train et test. Réduis la profondeur."
        )

    st.markdown("---")

    # ════════════════════════════════════════
    # BLOC 4.4 — ÉVALUATION
    # ════════════════════════════════════════
    st.markdown("## 4.4 Évaluation du Modèle")

    y_pred = model.predict(X_test)

    precision_0 = round(precision_score(y_test, y_pred, pos_label=0) * 100, 1)
    precision_1 = round(precision_score(y_test, y_pred, pos_label=1) * 100, 1)
    f1          = round(f1_score(y_test, y_pred) * 100, 1)

    st.markdown("### Métriques de Performance")

    col_e1, col_e2, col_e3, col_e4 = st.columns(4)

    with col_e1:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:18px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_DARK};'>
            <p style='font-size:10px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Accuracy</p>
            <p style='font-size:30px; font-weight:900; color:{C_DARK}; margin:0;'>{acc_test}%</p>
            <p style='font-size:11px; color:{C_MID}; margin:4px 0 0 0;'>global</p>
        </div>
        """, unsafe_allow_html=True)

    with col_e2:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:18px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_MID};'>
            <p style='font-size:10px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Précision Cl. 0</p>
            <p style='font-size:30px; font-weight:900; color:{C_DARK}; margin:0;'>{precision_0}%</p>
            <p style='font-size:11px; color:{C_MID}; margin:4px 0 0 0;'>échecs détectés</p>
        </div>
        """, unsafe_allow_html=True)

    with col_e3:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:18px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_WARM};'>
            <p style='font-size:10px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Précision Cl. 1</p>
            <p style='font-size:30px; font-weight:900; color:{C_DARK}; margin:0;'>{precision_1}%</p>
            <p style='font-size:11px; color:{C_MID}; margin:4px 0 0 0;'>succès détectés</p>
        </div>
        """, unsafe_allow_html=True)

    with col_e4:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:18px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); text-align:center;
        border-top:3px solid {C_DARK};'>
            <p style='font-size:10px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>F1-Score</p>
            <p style='font-size:30px; font-weight:900; color:{C_DARK}; margin:0;'>{f1}%</p>
            <p style='font-size:11px; color:{C_MID}; margin:4px 0 0 0;'>synthèse</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Matrice de confusion ─────────────
    st.markdown("### Matrice de Confusion")

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    col_cm, col_exp = st.columns([1, 1])

    with col_cm:
        option_cm = {
            "backgroundColor": "white",
            "tooltip": {"trigger": "item"},
            "xAxis": {
                "type": "category",
                "data": ["Prédit 0", "Prédit 1"],
                "axisLabel": {"color": C_DARK, "fontSize": 12, "fontWeight": "bold"},
                "position": "top"
            },
            "yAxis": {
                "type": "category",
                "data": ["Réel 1", "Réel 0"],
                "axisLabel": {"color": C_DARK, "fontSize": 12, "fontWeight": "bold"},
                "inverse": False
            },
            "series": [{
                "type": "heatmap",
                "data": [
                    [0, 1, int(fn)],
                    [1, 1, int(tp)],
                    [0, 0, int(tn)],
                    [1, 0, int(fp)],
                ],
                "label": {"show": True, "fontSize": 16, "fontWeight": "bold"},
                "itemStyle": {"borderWidth": 3, "borderColor": "white"}
            }],
            "visualMap": {
                "min": 0,
                "max": int(max(tn, tp, fn, fp)),
                "calculable": False,
                "show": False,
                "inRange": {"color": ["#EAE6E2", "#475E72"]}
            }
        }
        st.markdown("<div style='background:white; border-radius:12px; padding:12px; box-shadow:0 4px 16px rgba(71,94,114,0.1);'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:11px; font-weight:600; color:#73828E; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Matrice de Confusion</p>", unsafe_allow_html=True)
        st_echarts(options=option_cm, height="280px")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_exp:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
        box-shadow:0 4px 16px rgba(71,94,114,0.1); height:100%;'>
            <p style='font-size:11px; font-weight:700; color:{C_MID};
            text-transform:uppercase; letter-spacing:1px; margin:0 0 14px 0;'>
            Interprétation Marketing</p>
            <div style='margin-bottom:12px; padding:10px 14px;
            background:#f0f4f0; border-radius:8px; border-left:3px solid #2ecc71;'>
                <p style='font-size:12px; font-weight:700; color:#27ae60; margin:0 0 2px 0;'>
                ✅ Vrai Négatif — {int(tn):,}</p>
                <p style='font-size:12px; color:{C_DARK}; margin:0;'>
                Prédit échec → réel échec. Intervention justifiée.</p>
            </div>
            <div style='margin-bottom:12px; padding:10px 14px;
            background:#f0f4f0; border-radius:8px; border-left:3px solid #2ecc71;'>
                <p style='font-size:12px; font-weight:700; color:#27ae60; margin:0 0 2px 0;'>
                ✅ Vrai Positif — {int(tp):,}</p>
                <p style='font-size:12px; color:{C_DARK}; margin:0;'>
                Prédit succès → réel succès. Vendeur bien identifié.</p>
            </div>
            <div style='margin-bottom:12px; padding:10px 14px;
            background:#fff5f5; border-radius:8px; border-left:3px solid #e74c3c;'>
                <p style='font-size:12px; font-weight:700; color:#e74c3c; margin:0 0 2px 0;'>
                ❌ Faux Positif — {int(fp):,}</p>
                <p style='font-size:12px; color:{C_DARK}; margin:0;'>
                Prédit succès → réel échec. Vendeur félicité à tort.</p>
            </div>
            <div style='padding:10px 14px;
            background:#fff5f5; border-radius:8px; border-left:3px solid #e74c3c;'>
                <p style='font-size:12px; font-weight:700; color:#e74c3c; margin:0 0 2px 0;'>
                ❌ Faux Négatif — {int(fn):,}</p>
                <p style='font-size:12px; color:{C_DARK}; margin:0;'>
                Prédit échec → réel succès. Vendeur découragé à tort.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Visualisation de l'arbre ─────────
    st.markdown("### Visualisation de l'Arbre")

    info_box(
        "L'arbre ci-dessous montre les règles de décision apprises. "
        "Chaque nœud = une question sur une variable. "
        "Chaque feuille = une prédiction finale."
    )

    fig, ax = plt.subplots(figsize=(20, 6))
    fig.patch.set_facecolor("white")
    tree.plot_tree(
        model,
        feature_names=features,
        class_names=["Non atteint", "Atteint"],
        filled=True,
        rounded=True,
        fontsize=9,
        ax=ax,
        impurity=False,
        proportion=False
    )
    st.pyplot(fig)
    plt.close()

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Importance des variables ─────────
    st.markdown("### Importance des Variables")

    importances = model.feature_importances_
    feat_imp    = sorted(zip(features, importances), key=lambda x: x[1])
    feat_labels = [f[0] for f in feat_imp]
    feat_vals   = [round(float(f[1]) * 100, 1) for f in feat_imp]

    option_imp = {
        "backgroundColor": "white",
        "tooltip": {"trigger": "axis", "formatter": "{b} : {c}%"},
        "grid": {"left": "2%", "right": "8%", "top": "4%", "bottom": "4%", "containLabel": True},
        "xAxis": {
            "type": "value",
            "axisLabel": {"color": C_MID, "fontSize": 10, "formatter": "{value}%"},
            "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}}
        },
        "yAxis": {
            "type": "category",
            "data": feat_labels,
            "axisLabel": {"color": C_DARK, "fontSize": 11, "fontWeight": "bold"}
        },
        "series": [{
            "type": "bar",
            "data": feat_vals,
            "barWidth": "55%",
            "itemStyle": {"color": C_DARK, "borderRadius": [0, 6, 6, 0]},
            "label": {"show": True, "position": "right", "formatter": "{c}%",
                      "fontSize": 10, "color": C_DARK}
        }]
    }

    st.markdown("<div style='background:white; border-radius:14px; padding:12px; box-shadow:0 4px 16px rgba(71,94,114,0.1);'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; font-weight:600; color:#73828E; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;'>Importance des Variables dans la Décision</p>", unsafe_allow_html=True)
    st_echarts(options=option_imp, height="200px")
    st.markdown("</div>", unsafe_allow_html=True)

    top_feature = feat_labels[-1]
    top_val     = feat_vals[-1]
    sec_feature = feat_labels[-2]
    sec_val     = feat_vals[-2]

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Conclusion bloc 4.4 ──────────────
    st.markdown("### Interprétation des Résultats")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.metric(label=f"🥇 Variable n°1 — {top_feature}", value=f"{top_val}%", help="Part dans la décision du modèle")
    with col_c2:
        st.metric(label=f"🥈 Variable n°2 — {sec_feature}", value=f"{sec_val}%", help="Part dans la décision du modèle")

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    st.info(
        f"🛒 **{top_feature} — Le volume de ventes détermine le succès**\n\n"
        f"C'est le nombre de ventes réalisées dans la journée qui prédit le mieux "
        f"si un vendeur va atteindre son objectif. Un vendeur actif qui conclut "
        f"beaucoup de transactions génère mécaniquement un chiffre d'affaires plus élevé "
        f"— et se rapproche ainsi de son objectif journalier."
    )

    st.info(
        f"💰 **{sec_feature} — La valeur des ventes affine la prédiction**\n\n"
        f"À volume de transactions égal, c'est le vendeur qui génère le plus de chiffre "
        f"d'affaires qui atteint son objectif. Cela distingue les vendeurs qui savent "
        f"conclure des ventes de valeur élevée de ceux qui multiplient les petites transactions."
    )

    st.info(
        f"🎯 **Conclusion — Ce que le modèle nous dit sur l'atteinte des objectifs**\n\n"
        f"Sur {len(y_test):,} journées testées, le modèle prédit correctement "
        f"**{acc_test}%** des cas. Cela signifie que l'activité commerciale d'un vendeur "
        f"— combien il vend et combien il génère — suffit à prédire avec fiabilité "
        f"s'il va atteindre son objectif, sans avoir besoin de connaître l'objectif lui-même."
    )

    st.warning(
        f"⚠️ **À noter — Chaque vendeur est ancré dans son département**\n\n"
        f"Chaque vendeur est affecté à un seul département sur toute la période 2017–2022. "
        f"Un vendeur Électroménager vend moins d'unités mais à prix plus élevé qu'un vendeur "
        f"Accessoires — leurs objectifs sont fixés en conséquence. "
        f"Le volume de ventes n'est donc pas comparable entre deux vendeurs de départements différents : "
        f"c'est la performance relative à son propre contexte qui compte."
    )

    st.markdown("---")


    # ════════════════════════════════════════
    # BLOC 4.5 — PRÉDICTION INTERACTIVE
    # ════════════════════════════════════════
    st.markdown("## 4.5 Prédiction Interactive")

    st.info(
        "🎮 **Simulez une journée de vente**\n\n"
        "Ajustez les valeurs ci-dessous pour simuler l'activité d'un vendeur "
        "et découvrir si le modèle prédit qu'il va atteindre son objectif journalier."
    )

    mean_revenue   = round(float(df["Revenue"].mean()), 0)
    mean_margin    = round(float(df["Margin"].mean()), 3)
    mean_qty       = round(float(df["Sales Quantity"].mean()), 0)
    mean_customers = round(float(df["Customers"].mean()), 0)

    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        input_revenue = st.slider(
            "💶 Revenue (€)",
            min_value=int(df["Revenue"].min()),
            max_value=int(df["Revenue"].max()),
            value=int(mean_revenue),
            step=500
        )
        input_qty = st.slider(
            "🛒 Sales Quantity (unités)",
            min_value=int(df["Sales Quantity"].min()),
            max_value=int(df["Sales Quantity"].max()),
            value=int(mean_qty),
            step=1
        )

    with col_s2:
        input_margin = st.slider(
            "📊 Margin (taux)",
            min_value=float(round(df["Margin"].min(), 2)),
            max_value=float(round(df["Margin"].max(), 2)),
            value=float(mean_margin),
            step=0.01
        )
        input_customers = st.slider(
            "👥 Customers (nombre)",
            min_value=int(df["Customers"].min()),
            max_value=int(df["Customers"].max()),
            value=int(mean_customers),
            step=1
        )

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    input_data = [[input_revenue, input_margin, input_qty, input_customers]]
    prediction = model.predict(input_data)[0]
    proba      = model.predict_proba(input_data)[0]
    proba_oui  = round(proba[1] * 100, 1)
    proba_non  = round(proba[0] * 100, 1)

    if prediction == 1:
        st.success(
            f"✅ **Objectif atteint**\n\n"
            f"Avec ces chiffres, le modèle prédit que le vendeur **va atteindre** "
            f"son objectif journalier — avec une probabilité de **{proba_oui}%**."
        )
    else:
        st.error(
            f"❌ **Objectif non atteint**\n\n"
            f"Avec ces chiffres, le modèle prédit que le vendeur **ne va pas atteindre** "
            f"son objectif journalier — avec une probabilité de **{proba_non}%**."
        )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.metric("Probabilité — Objectif Atteint", f"{proba_oui}%")
    with col_p2:
        st.metric("Probabilité — Objectif Non Atteint", f"{proba_non}%")

    st.warning(
        "⚠️ **Limite du modèle**\n\n"
        "Cette prédiction est basée sur les patterns historiques 2017–2022. "
        "Le modèle ne connaît pas l'objectif individuel fixé au vendeur — "
        "deux vendeurs avec les mêmes chiffres mais des objectifs différents "
        "peuvent avoir des résultats réels opposés. "
        f"La fiabilité globale du modèle est de **{acc_test}%**."
    )
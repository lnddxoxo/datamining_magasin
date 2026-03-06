# ─────────────────────────────────────────
# pages/page1_donnees.py
# Page 1 — Données & Prétraitement
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG
from utils.charts import style_dataframe
import matplotlib.pyplot as plt
from utils.charts import style_dataframe, info_box, success_box, warning_box

def show(data_store):

    # ── Titre ────────────────────────────
    st.title("Données & Prétraitement")

    # ── Encadré KDD ──────────────────────
    st.info("**Processus KDD — Étapes ① ② ③** : Sélection → Prétraitement → Transformation")

    # ── Bloc 1.1 — Contexte ──────────────
    st.markdown("## 1.1 Contexte Métier")

    col_texte, col_metriques = st.columns([2, 1])

    with col_texte:
        st.markdown(f"""
        <div style='
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(71,94,114,0.15);
            border-left: 5px solid {C_WARM};
        '>
            <p style='color:{C_DARK}; font-size:15px; line-height:1.8;'>
                Ce projet analyse les performances commerciales d'un
                <b>magasin de département brésilien</b> sur la période
                <b>2017 à 2022</b>.<br><br>
                <b>Question centrale :</b> Pourquoi certains vendeurs et
                départements performent-ils mieux que d'autres ?<br><br>
                <b>Objectif :</b> Identifier des segments actionnables et
                produire des recommandations marketing concrètes.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_metriques:
        nb_observations = len(data_store)
        nb_vendeurs     = data_store["Seller"].nunique()
        nb_departements = data_store["Department"].nunique()
        periode         = f"{data_store['Year'].min()} – {data_store['Year'].max()}"

        st.metric("Observations", f"{nb_observations:,}")
        st.metric("Vendeurs",      nb_vendeurs)
        st.metric("Départements",  nb_departements)
        st.metric("Période",       periode)

    # ── Bloc 1.2 — Inventaire des variables ──
    st.markdown("## 1.2 Inventaire des Variables")

    variables = {
        "Variable": [
            "Seller", "Department", "Revenue", "Revenue Goal",
            "Margin", "Margin Goal", "Date", "Sales Quantity", "Customers",
            "Year", "Month", "Goal_Reached"
        ],
        "Type Brut": [
            "object", "object", "float64", "float64",
            "float64", "float64", "object", "int64", "int64",
            "—", "—", "—"
        ],
        "Type Correct": [
            "string", "string", "float64", "float64",
            "float64", "float64", "datetime", "int64", "int64",
            "int64", "int64", "int64"
        ],
        "Rôle": [
            "Identifiant", "Identifiant", "Feature", "Feature",
            "Feature", "Feature", "Temporel", "Feature", "Feature",
            "Temporel", "Temporel", "Cible"
        ],
        "Retenu": [
            "✅ Oui", "✅ Oui", "✅ Oui", "✅ Oui",
            "✅ Oui", "✅ Oui", "✅ Transformée", "✅ Oui", "✅ Oui",
            "✅ Créée", "✅ Créée", "✅ Créée"
        ],
        "Justification": [
            "Identifiant vendeur — utilisé pour l'agrégation",
            "Identifiant département — utilisé pour la segmentation",
            "Mesure la performance réelle du vendeur",
            "Permet de construire la variable cible Goal_Reached",
            "Indicateur de rentabilité — complète le revenu",
            "Permet de mesurer si la marge est atteinte",
            "Transformée en Year et Month pour l'analyse temporelle",
            "Indique le volume de ventes — feature comportementale",
            "Indique l'affluence clients — feature comportementale",
            "Extraite de Date — permet l'analyse par année",
            "Extraite de Date — permet l'analyse de saisonnalité",
            "Créée : 1 si Revenue >= Revenue Goal, sinon 0"
        ]
    }

    df_variables = pd.DataFrame(variables)
    st.dataframe(
        style_dataframe(df_variables),
        use_container_width=True,
        hide_index=True,
        height=420
    )

    # ── Bloc 1.3 — Qualité des données ───
    st.markdown("## 1.3 Qualité des Données")

    tab_a, tab_b, tab_c, tab_d = st.tabs([
        "Valeurs Manquantes",
        "Types & Formats",
        "Statistiques",
        "Outliers"
    ])

    with tab_a:
        st.markdown("### Vérification des valeurs manquantes")

        missing = data_store.isnull().sum().reset_index()
        missing.columns = ["Variable", "Valeurs Manquantes"]
        missing["Pourcentage (%)"] = (
            missing["Valeurs Manquantes"] / len(data_store) * 100
        ).round(2)
        missing["Statut"] = missing["Valeurs Manquantes"].apply(
            lambda x: "✅ Aucune" if x == 0 else "⚠️ À traiter"
        )

        st.dataframe(
            style_dataframe(missing),
            use_container_width=True,
            hide_index=True,
            height=420
        )

        st.success(
            "✅ Le dataset ne contient aucune valeur manquante. "
            "Aucun traitement n'est nécessaire à cette étape. "
            "Cette vérification fait partie du processus KDD — étape ② Prétraitement."
        )

    with tab_b:
        st.markdown("### Conversion des types de données")

        types_data = {
            "Variable"      : ["Date", "Year", "Month", "Goal_Reached"],
            "Type Avant"    : ["object", "—", "—", "—"],
            "Type Après"    : ["datetime64", "int64", "int64", "int64"],
            "Transformation": [
                "pd.to_datetime() — conversion texte vers datetime",
                "dt.year extrait depuis Date",
                "dt.month extrait depuis Date",
                "1 si Revenue >= Revenue Goal sinon 0"
            ]
        }

        df_types = pd.DataFrame(types_data)

        st.dataframe(
            style_dataframe(df_types),
            use_container_width=True,
            hide_index=True,
            height=210
        )

        st.info(
            "**Date** convertie en datetime pour extraire Year et Month. "
            "**Goal_Reached** est la variable cible binaire — "
            "c'est elle qu'on cherche à prédire en page 4."
        )

    with tab_c:
        st.markdown("### Statistiques descriptives")

        cols_numeriques = [
            "Revenue", "Revenue Goal", "Margin",
            "Margin Goal", "Sales Quantity", "Customers"
        ]

        stats = data_store[cols_numeriques].describe().T.round(2)
        stats = stats[["min", "mean", "50%", "max", "std"]]
        stats.columns = ["Min", "Moyenne", "Médiane", "Max", "Écart-type"]
        stats = stats.reset_index()
        stats.rename(columns={"index": "Variable"}, inplace=True)

        st.dataframe(
            style_dataframe(stats),
            use_container_width=True,
            hide_index=True,
            height=250
        )

        st.markdown("### Distribution des variables")

        fig, axes = plt.subplots(2, 3, figsize=(14, 7))
        fig.patch.set_facecolor(C_BG)
        axes = axes.flatten()

        for i, col in enumerate(cols_numeriques):
            axes[i].hist(
                data_store[col].dropna(),
                bins=30,
                color=C_DARK,
                edgecolor=C_BG,
                linewidth=0.5
            )
            axes[i].set_facecolor(C_LIGHT)
            axes[i].set_title(col, fontsize=11, color=C_DARK)
            axes[i].tick_params(colors=C_DARK)
            axes[i].set_xlabel("Valeur", fontsize=9, color=C_MID)
            axes[i].set_ylabel("Fréquence", fontsize=9, color=C_MID)
            for spine in axes[i].spines.values():
                spine.set_edgecolor(C_MID)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        col_w1, col_w2 = st.columns(2)
        marge_moy = round(data_store["Margin"].mean() * 100, 1)

        with col_w1:
            st.warning(
                "⚠️ **Revenue minimum = 0** : certaines journées "
                "affichent un revenu nul. Ces valeurs sont conservées "
                "car elles représentent des journées sans vente — "
                "une réalité commerciale normale."
            )

        with col_w2:
            st.info(
                f"📊 **Marge moyenne = {marge_moy}%** : indicateur global "
                "de rentabilité du magasin sur 2017–2022."
            )

    with tab_d:
        st.markdown("### Détection des valeurs aberrantes")

        cols_numeriques = [
            "Revenue", "Revenue Goal", "Margin",
            "Margin Goal", "Sales Quantity", "Customers"
        ]

        fig, axes = plt.subplots(2, 3, figsize=(14, 8))
        fig.patch.set_facecolor(C_BG)
        axes = axes.flatten()

        for i, col in enumerate(cols_numeriques):
            axes[i].boxplot(
                data_store[col].dropna(),
                patch_artist=True,
                boxprops    = dict(facecolor=C_WARM, color=C_DARK),
                medianprops = dict(color=C_DARK, linewidth=2),
                whiskerprops= dict(color=C_MID),
                capprops    = dict(color=C_MID),
                flierprops  = dict(marker='o', markerfacecolor=C_DARK, markersize=4)
            )
            axes[i].set_facecolor(C_LIGHT)
            axes[i].set_title(col, fontsize=12, color=C_DARK)
            axes[i].tick_params(colors=C_DARK)
            for spine in axes[i].spines.values():
                spine.set_edgecolor(C_MID)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("---")

        commentaires = {
            "Variable": [
                "Revenue", "Revenue Goal",
                "Margin", "Margin Goal",
                "Sales Quantity", "Customers"
            ],
            "Observation métier": [
                "Certains vendeurs génèrent ponctuellement des revenus très élevés — probablement lors de grandes ventes ou promotions exceptionnelles.",
                "Les objectifs fixés varient fortement selon les périodes — certains mois ont des cibles nettement plus ambitieuses que d'autres.",
                "Quelques journées affichent une rentabilité inhabituellement élevée — signe de ventes à forte valeur ajoutée.",
                "Les objectifs de marge sont globalement stables — politique de rentabilité cohérente sur toute la période.",
                "Des pics de ventes ponctuels dépassent largement la normale — liés à des événements commerciaux comme les soldes.",
                "Certaines journées enregistrent une affluence anormalement élevée — des promotions qui attirent massivement les clients."
            ]
        }

        df_comm = pd.DataFrame(commentaires)
        st.dataframe(
            style_dataframe(df_comm),
            use_container_width=True,
            hide_index=True,
            height=250
        )

    # ── Bloc 1.4 — Transformations ───────
    st.markdown("## 1.4 Transformations des Données")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Goal Reached",
        "Extraction Temporelle",
        "Agrégations",
        "Standardisation"
    ])

    with tab1:
        st.markdown("### Variable cible — Goal_Reached")

        st.info(
            "L'objectif du magasin est que chaque vendeur atteigne "
            "son objectif de revenu quotidien. Cette information "
            "n'existe pas directement — on la construit.\n\n"
            "**Formule :** Goal_Reached = 1 si Revenue ≥ Revenue Goal, sinon 0"
        )

        counts  = data_store["Goal_Reached"].value_counts()
        total   = len(data_store)
        pct_oui = round(counts.get(1, 0) / total * 100, 1)
        pct_non = round(counts.get(0, 0) / total * 100, 1)

        col_pie, col_interp = st.columns([1, 1])

        with col_pie:
            fig, ax = plt.subplots(figsize=(5, 5))
            fig.patch.set_facecolor(C_BG)
            ax.set_facecolor(C_BG)

            ax.pie(
                [counts.get(1, 0), counts.get(0, 0)],
                labels    = ["Objectif atteint", "Objectif non atteint"],
                colors    = [C_DARK, C_WARM],
                autopct   = "%1.1f%%",
                startangle= 90,
                textprops = {"color": C_DARK, "fontsize": 12}
            )
            ax.set_title("Distribution Goal_Reached", color=C_DARK, fontsize=13)
            st.pyplot(fig)
            plt.close()

        with col_interp:
            st.metric("Objectif atteint",     f"{pct_oui}%")
            st.metric("Objectif non atteint", f"{pct_non}%")

            st.warning(
                f"⚠️ **{pct_non}% des journées** n'atteignent pas "
                "l'objectif de revenu. C'est le problème central "
                "que ce projet cherche à comprendre et résoudre."
            )

    with tab2:
        st.markdown("### Extraction de Year et Month depuis Date")

        st.info(
            "La date brute est inutilisable mathématiquement par les algorithmes. "
            "En extrayant l'année et le mois, on peut analyser les tendances "
            "et la saisonnalité des ventes."
        )

        col_y, col_m, col_com = st.columns([1, 1, 1])

        with col_y:
            st.markdown("#### Distribution par Année")

            dist_year = data_store["Year"].value_counts().sort_index().reset_index()
            dist_year.columns = ["Année", "Observations"]
            dist_year["Part (%)"] = (
                dist_year["Observations"] / len(data_store) * 100
            ).round(1).apply(lambda x: f"{x}%")

            st.dataframe(
                style_dataframe(dist_year),
                use_container_width=True,
                hide_index=True,
                height=250
            )

        with col_m:
            st.markdown("#### Distribution par Mois")

            noms_mois = {
                1:"Janvier",  2:"Février",  3:"Mars",
                4:"Avril",    5:"Mai",       6:"Juin",
                7:"Juillet",  8:"Août",      9:"Septembre",
                10:"Octobre", 11:"Novembre", 12:"Décembre"
            }

            dist_month = data_store["Month"].value_counts().sort_index().reset_index()
            dist_month.columns = ["Mois", "Observations"]
            dist_month["Mois"] = dist_month["Mois"].map(noms_mois)

            st.dataframe(
                style_dataframe(dist_month),
                use_container_width=True,
                hide_index=True,
                height=430
            )

        with col_com:
            st.markdown("#### Observations métier")
            st.markdown(f"""
            <div style='
                background: white;
                border-radius: 12px;
                padding: 1.2rem;
                box-shadow: 0 4px 15px rgba(71,94,114,0.15);
                border-top: 3px solid {C_MID};
                margin-top: 2rem;
            '>
                <p style='color:{C_MID}; font-size:13px; line-height:1.8; margin:0;'>
                    ✅ Les <b style='color:{C_DARK}'>6 années</b> sont
                    équilibrées — chaque année représente environ
                    <b style='color:{C_DARK}'>16.7%</b> des observations.<br><br>
                    📅 La répartition mensuelle révèle une légère
                    <b style='color:{C_DARK}'>saisonnalité</b> — Février
                    compte moins d'observations en raison de ses 28 jours.<br><br>
                    🎯 Ces deux variables permettront l'analyse des
                    <b style='color:{C_DARK}'>tendances temporelles</b>
                    en page 2 et la
                    <b style='color:{C_DARK}'>prédiction</b> en page 5.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.success(
            "✅ Year et Month extraites avec succès depuis Date. "
            "Le dataset couvre 6 années complètes sans interruption."
        )

    with tab3:
        st.markdown("### Agrégations par Département et Vendeur")

        st.info(
            "Les données brutes sont journalières. Pour comparer "
            "les performances, on agrège par département et par vendeur — "
            "on calcule la moyenne de chaque indicateur sur toute la période."
        )

        st.markdown("---")

        col_dept, col_sell = st.columns(2)

        with col_dept:
            st.markdown("#### Par Département")

            noms_dept = {
                "Eletrônicos" : "Électronique",
                "Vestuário"   : "Vêtements",
                "Acessórios"  : "Accessoires",
                "Casa"        : "Maison",
                "Brinquedo"   : "Jouets",
                "Esportes"    : "Sports",
                "Papelaria"   : "Papeterie"
            }

            dept_data = data_store.copy()
            dept_data["Department"] = dept_data["Department"].map(noms_dept)

            dept_agg = dept_data.groupby("Department").agg(
                Avg_Revenue   = ("Revenue",       "mean"),
                Avg_Margin    = ("Margin",         "mean"),
                Avg_Sales     = ("Sales Quantity", "mean"),
                Avg_Customers = ("Customers",      "mean"),
                Goal_Rate     = ("Goal_Reached",   "mean")
            ).round(2).reset_index()

            dept_agg["Avg_Margin"] = (dept_agg["Avg_Margin"] * 100).round(1).apply(lambda x: f"{x}%")
            dept_agg["Goal_Rate"]  = (dept_agg["Goal_Rate"]  * 100).round(1).apply(lambda x: f"{x}%")

            dept_agg.columns = [
                "Département", "Rev. Moyen",
                "Marge Moy.", "Ventes Moy.",
                "Clients Moy.", "Taux Objectif"
            ]

            st.dataframe(
                style_dataframe(dept_agg),
                use_container_width=True,
                hide_index=True,
                height=280
            )

        with col_sell:
            st.markdown("#### Par Vendeur")

            sell_agg = data_store.groupby("Seller").agg(
                Avg_Revenue   = ("Revenue",       "mean"),
                Avg_Margin    = ("Margin",         "mean"),
                Avg_Sales     = ("Sales Quantity", "mean"),
                Avg_Customers = ("Customers",      "mean"),
                Goal_Rate     = ("Goal_Reached",   "mean")
            ).round(2).reset_index()

            sell_agg["Avg_Margin"] = (sell_agg["Avg_Margin"] * 100).round(1).apply(lambda x: f"{x}%")
            sell_agg["Goal_Rate"]  = (sell_agg["Goal_Rate"]  * 100).round(1).apply(lambda x: f"{x}%")

            sell_agg.columns = [
                "Vendeur", "Rev. Moyen",
                "Marge Moy.", "Ventes Moy.",
                "Clients Moy.", "Taux Objectif"
            ]

            st.dataframe(
                style_dataframe(sell_agg),
                use_container_width=True,
                hide_index=True,
                height=630
            )

        st.markdown("---")

        st.markdown(f"""
        <div style='
            background: white;
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 4px 15px rgba(71,94,114,0.15);
            border-left: 5px solid {C_WARM};
        '>
            <p style='color:{C_MID}; font-size:13px; line-height:1.8; margin:0;'>
                📦 <b style='color:{C_DARK}'>Maison</b> et
                <b style='color:{C_DARK}'>Électronique</b> génèrent
                les revenus moyens les plus élevés — ce sont les moteurs
                commerciaux du magasin.<br><br>
                👤 Les performances varient sensiblement d'un vendeur
                à l'autre — certains atteignent leur objectif dans
                plus de 48% des cas tandis que d'autres peinent à
                dépasser 45%.<br><br>
                🎯 Ces écarts justifient une segmentation approfondie
                pour identifier des profils distincts
                et proposer des actions ciblées.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### 📊 Analyse BCG — Départements & Vendeurs")

        col_bcg1, col_bcg2 = st.columns(2)

        with col_bcg1:
            st.markdown(f"""
            <div style='background:white; border-radius:12px; padding:1.2rem;
                box-shadow:0 4px 15px rgba(71,94,114,0.15);
                border-top:3px solid {C_DARK};'>
                <p style='color:{C_DARK}; font-weight:700; font-size:14px; margin-bottom:10px;'>
                    Départements
                </p>
                <p style='color:{C_MID}; font-size:13px; line-height:1.8; margin:0;'>
                    ⭐ <b style='color:{C_DARK}'>Vedettes</b> —
                    Maison, Sports, Électronique, Jouets : revenus élevés
                    et objectifs atteints — moteurs du magasin.<br><br>
                    ❓ <b style='color:{C_DARK}'>Dilemmes</b> —
                    Accessoires, Papeterie : bons taux d'objectif mais
                    faibles volumes — potentiel à développer.<br><br>
                    🐄 <b style='color:{C_DARK}'>Vache à lait</b> —
                    Vêtements : revenu correct mais taux d'objectif
                    en dessous de la moyenne — à surveiller.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_bcg2:
            st.markdown(f"""
            <div style='background:white; border-radius:12px; padding:1.2rem;
                box-shadow:0 4px 15px rgba(71,94,114,0.15);
                border-top:3px solid {C_WARM};'>
                <p style='color:{C_DARK}; font-weight:700; font-size:14px; margin-bottom:10px;'>
                    Vendeurs
                </p>
                <p style='color:{C_MID}; font-size:13px; line-height:1.8; margin:0;'>
                    ⭐ <b style='color:{C_DARK}'>Vedettes</b> —
                    Guilherme, Enzo, Julia, Lucas, Thiago Carvalho :
                    revenus élevés et objectifs atteints régulièrement.<br><br>
                    🐄 <b style='color:{C_DARK}'>Vaches à lait</b> —
                    Camila Carvalho, Gustavo, Mateus, Jorge :
                    bons revenus mais taux d'objectif perfectible.<br><br>
                    ❓ <b style='color:{C_DARK}'>Dilemmes</b> —
                    Thiago Barbosa, Letícia Ribeiro, Raphael, Caroline :
                    objectifs atteints mais volumes trop faibles.<br><br>
                    🐕 <b style='color:{C_DARK}'>Poids mort</b> —
                    Camila Lima : faibles revenus et taux d'objectif
                    le plus bas — accompagnement prioritaire.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### Standardisation des données")

        st.info(
            "**Pourquoi standardiser ?** Le K-Means calcule des distances "
            "entre les points. Sans standardisation, une variable comme "
            "Revenue (0 à 22 000€) écrase une variable comme Margin (0 à 0.8) "
            "— le résultat serait biaisé. On ramène tout à la même échelle."
        )

        st.markdown("---")

        cols_std = ["Revenue", "Margin", "Sales Quantity", "Customers"]

        from sklearn.preprocessing import StandardScaler
        scaler     = StandardScaler()
        data_std   = data_store[cols_std].copy()
        data_scaled = pd.DataFrame(
            scaler.fit_transform(data_std),
            columns=cols_std
        )

        comparaison = pd.DataFrame({
            "Variable"   : cols_std,
            "Moy. Avant" : data_store[cols_std].mean().round(2).values,
            "Std. Avant" : data_store[cols_std].std().round(2).values,
            "Moy. Après" : data_scaled.mean().round(2).values,
            "Std. Après" : data_scaled.std().round(2).values,
        })

        st.dataframe(
            style_dataframe(comparaison),
            use_container_width=True,
            hide_index=True,
            height=210
        )

        st.success(
            "✅ Après standardisation, toutes les variables ont "
            "une moyenne ≈ 0 et un écart-type ≈ 1. "
            "Elles contribuent désormais de façon équitable "
            "au calcul des distances dans le K-Means."
        )

        st.markdown("---")

        st.markdown("### Visualisation de l'effet de la standardisation")

        fig, axes = plt.subplots(2, 4, figsize=(14, 6))
        fig.patch.set_facecolor(C_BG)

        for i, col in enumerate(cols_std):
            axes[0, i].hist(
                data_store[col].dropna(),
                bins=30, color=C_WARM,
                edgecolor=C_DARK, linewidth=0.5
            )
            axes[0, i].set_title(f"{col}\nAvant", fontsize=10, color=C_DARK)
            axes[0, i].set_facecolor(C_LIGHT)
            axes[0, i].tick_params(colors=C_DARK)
            for spine in axes[0, i].spines.values():
                spine.set_edgecolor(C_MID)

            axes[1, i].hist(
                data_scaled[col],
                bins=30, color=C_DARK,
                edgecolor=C_MID, linewidth=0.5
            )
            axes[1, i].set_title(f"{col}\nAprès", fontsize=10, color=C_DARK)
            axes[1, i].set_facecolor(C_LIGHT)
            axes[1, i].tick_params(colors=C_DARK)
            for spine in axes[1, i].spines.values():
                spine.set_edgecolor(C_MID)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown(f"""
        <div style='
            background: white;
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 4px 15px rgba(71,94,114,0.15);
            border-left: 5px solid {C_DARK};
        '>
            <p style='color:{C_MID}; font-size:13px; line-height:1.8; margin:0;'>
                📊 La <b style='color:{C_DARK}'>forme des distributions</b>
                reste identique avant et après — la standardisation ne
                modifie pas la structure des données, elle change
                uniquement l'échelle.<br><br>
                ⚖️ Sans cette étape, <b style='color:{C_DARK}'>Revenue</b>
                dominerait le calcul K-Means avec ses valeurs en milliers
                pendant que <b style='color:{C_DARK}'>Margin</b> entre 0 et 1
                n'aurait quasiment aucun impact sur les clusters.<br><br>
                🎯 La standardisation garantit que chaque variable
                contribue <b style='color:{C_DARK}'>équitablement</b>
                à la segmentation finale.
            </p>
        </div>
        """, unsafe_allow_html=True)
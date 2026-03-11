import streamlit as st
import pandas as pd
from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG
from utils.charts import info_box, success_box, warning_box


def show(data_store):

    # ── TITRE ──────────────────────────────────────────────
    st.markdown(
        f"""
        <div style='background:{C_DARK}; border-radius:12px; padding:14px 20px; margin-bottom:20px;'>
            <p style='color:{C_WARM}; font-size:11px; font-weight:700;
              text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>
              Méthodologie KDD — Étape 6
            </p>
            <p style='color:white; font-size:14px; margin:0;'>
              <b>Data Mining</b> — Recommandations Marketing
              &nbsp;·&nbsp; Synthèse Segmentation K-Means + Classification
              &nbsp;·&nbsp; 19 vendeurs · 3 profils
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── VÉRIFICATION ───────────────────────────────────────
    if 'cluster_profiles' not in st.session_state:
        warning_box(
            "⚠ <b>Attention :</b> Veuillez d'abord visiter la "
            "<b>Page 3 — Segmentation</b> pour générer les clusters."
        )
        st.stop()

    cluster_profiles = st.session_state['cluster_profiles']

    st.markdown("---")

    # ============================================================
    # SECTION 1 — CROISEMENT DES DEUX ANALYSES
    # ============================================================
    st.markdown("## Croisement Segmentation × Classification")

    info_box(
        "La segmentation K-Means nous dit <b>qui sont les vendeurs</b>. "
        "La classification nous dit <b>pourquoi ils atteignent ou non leurs objectifs</b>. "
        "Ensemble, elles nous donnent les leviers d'action précis pour chaque profil."
    )

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    PROFIL_COLORS = {
        "Stars":       {"bg": "#e8f4e8", "border": "#2d7a2d", "header": "#1a5c1a"},
        "Performants": {"bg": "#e8eef4", "border": "#475E72", "header": "#2c3e50"},
        "accompagner": {"bg": "#fdf3e3", "border": "#c8860a", "header": "#8b5e00"},
    }

    def get_style(nom):
        for key in PROFIL_COLORS:
            if key.lower() in nom.lower():
                return PROFIL_COLORS[key]
        return PROFIL_COLORS["accompagner"]

    # Données croisement
    CROISEMENT = {
        "Stars": {
            "kmeans":  "Fort revenu · Bonne marge · Clients nombreux",
            "classif": "Sales Quantity élevée → le modèle les prédit en succès",
            "levier":  "Maintenir le volume · Challenges premium · Rôle de mentor",
            "risque":  "Malgré leur profil, ~52% des journées sans atteindre l'objectif → pas infaillibles",
            "emoji":   "⭐"
        },
        "Performants": {
            "kmeans":  "Bon volume · Marge correcte · Irréguliers",
            "classif": "Sales Quantity variable → le modèle hésite, résultats mixtes",
            "levier":  "Augmenter la régularité du volume · Coaching ciblé · Objectifs progressifs",
            "risque":  "Proches du profil Stars mais manquent de constance dans le volume journalier",
            "emoji":   "📈"
        },
        "accompagner": {
            "kmeans":  "Faible revenu · Marge la plus élevée · Peu de clients",
            "classif": "Sales Quantity trop faible → le modèle les prédit souvent en échec",
            "levier":  "Augmenter le volume de transactions · Formation · Suivi hebdomadaire",
            "risque":  "Savent vendre des produits rentables mais ne vendent pas assez pour atteindre les objectifs",
            "emoji":   "🔧"
        }
    }

    cols = st.columns(len(cluster_profiles), gap="medium")
    for col, (cluster_id, profil) in zip(cols, cluster_profiles.items()):
        profil_nom = profil['nom']
        style = get_style(profil_nom)
        bg_s  = style['bg']
        brd_s = style['border']
        hdr_s = style['header']

        crois_key = "accompagner"
        for key in CROISEMENT:
            if key.lower() in profil_nom.lower():
                crois_key = key
                break
        c = CROISEMENT[crois_key]

        with col:
            st.markdown(
                "<div style='background:white; border-radius:12px; padding:16px;"
                "box-shadow:0 4px 16px rgba(71,94,114,0.1);"
                "border-top:5px solid " + brd_s + ";'>"

                "<p style='font-size:13px; font-weight:700; color:" + brd_s + ";"
                "margin:0 0 4px 0;'>" + c['emoji'] + " " + profil_nom + "</p>"
                "<p style='font-size:10px; color:" + C_MID + "; margin:0 0 12px 0;'>"
                + str(profil['nb_vendeurs']) + " vendeurs · Cluster " + str(cluster_id) + "</p>"

                "<p style='font-size:10px; font-weight:700; color:" + C_MID + ";"
                "text-transform:uppercase; letter-spacing:1px; margin:0 0 4px 0;'>K-Means</p>"
                "<p style='font-size:11px; color:" + C_DARK + "; margin:0 0 10px 0;'>"
                + c['kmeans'] + "</p>"

                "<p style='font-size:10px; font-weight:700; color:" + C_MID + ";"
                "text-transform:uppercase; letter-spacing:1px; margin:0 0 4px 0;'>Classification</p>"
                "<p style='font-size:11px; color:" + C_DARK + "; margin:0 0 10px 0;'>"
                + c['classif'] + "</p>"

                "<div style='background:" + bg_s + "; border-left:3px solid " + brd_s + ";"
                "border-radius:4px; padding:6px 10px; margin-bottom:8px;'>"
                "<p style='font-size:10px; font-weight:700; color:" + hdr_s + "; margin:0 0 2px 0;'>Levier principal</p>"
                "<p style='font-size:10px; color:" + C_DARK + "; margin:0;'>" + c['levier'] + "</p>"
                "</div>"

                "<div style='background:#fff5f5; border-left:3px solid #e74c3c;"
                "border-radius:4px; padding:6px 10px;'>"
                "<p style='font-size:10px; font-weight:700; color:#c0392b; margin:0 0 2px 0;'>Point de vigilance</p>"
                "<p style='font-size:10px; color:" + C_DARK + "; margin:0;'>" + c['risque'] + "</p>"
                "</div>"

                "</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ============================================================
    # SECTION 2 — PLAN D'ACTION TRIMESTRIEL
    # ============================================================
    st.markdown("## Plan d'action trimestriel par profil")

    PLANS = {
        "Stars": {
            "emoji": "⭐",
            "mois": [
                {
                    "titre": "Mois 1 — Reconnaissance",
                    "objectif": "Renforcer l'engagement",
                    "actions": [
                        "Mettre en place un programme de bonus et awards mensuels",
                        "Réunion individuelle de valorisation des résultats",
                        "Identifier les Stars prêts à devenir mentors",
                    ]
                },
                {
                    "titre": "Mois 2 — Responsabilité",
                    "objectif": "Capitaliser sur leur expertise",
                    "actions": [
                        "Lancer le mentorat vers les vendeurs À accompagner",
                        "Impliquer dans les décisions stratégiques du département",
                        "Objectifs premium avec incentives exclusifs",
                    ]
                },
                {
                    "titre": "Mois 3 — Fidélisation",
                    "objectif": "Ancrer sur le long terme",
                    "actions": [
                        "Présenter un plan de carrière individualisé",
                        "Évaluer l'impact du mentorat sur les autres groupes",
                        "Mesurer taux de rétention et satisfaction",
                    ]
                }
            ],
            "kpis": ["Taux de rétention", "Taux d'atteinte objectifs premium", "Nb vendeurs mentorés avec progression"]
        },
        "Performants": {
            "emoji": "📈",
            "mois": [
                {
                    "titre": "Mois 1 — Diagnostic",
                    "objectif": "Identifier les freins au volume",
                    "actions": [
                        "Analyser les journées en échec : volume ou valeur ?",
                        "Sessions de coaching individuelles sur la régularité",
                        "Binômage avec un vendeur Star",
                    ]
                },
                {
                    "titre": "Mois 2 — Formation",
                    "objectif": "Développer la constance",
                    "actions": [
                        "Formation sur les techniques de vente avancées",
                        "Partage de bonnes pratiques Stars en réunion d'équipe",
                        "Objectifs de volume progressifs avec suivi hebdomadaire",
                    ]
                },
                {
                    "titre": "Mois 3 — Évaluation",
                    "objectif": "Mesurer et ajuster",
                    "actions": [
                        "Comparer le taux Goal_Reached avant/après",
                        "Identifier les Performants proches du profil Stars",
                        "Revoir les objectifs selon la progression réelle",
                    ]
                }
            ],
            "kpis": ["Évolution taux Goal_Reached", "Progression Sales Quantity mensuelle", "Nb Performants passés Stars"]
        },
        "accompagner": {
            "emoji": "🔧",
            "mois": [
                {
                    "titre": "Mois 1 — Stabilisation",
                    "objectif": "Comprendre et poser les bases",
                    "actions": [
                        "Entretien individuel pour identifier les blocages",
                        "Réviser les objectifs pour les rendre atteignables",
                        "Formation produit et techniques fondamentales",
                    ]
                },
                {
                    "titre": "Mois 2 — Accompagnement",
                    "objectif": "Augmenter le volume de transactions",
                    "actions": [
                        "Points hebdomadaires avec le manager direct",
                        "Parrainage par un vendeur Star",
                        "Challenges de volume avec récompenses immédiates",
                    ]
                },
                {
                    "titre": "Mois 3 — Mesure",
                    "objectif": "Évaluer et décider",
                    "actions": [
                        "Comparer Sales Quantity et Goal_Reached avant/après",
                        "Identifier les vendeurs prêts à passer Performants",
                        "Ajuster le plan pour ceux encore en difficulté",
                    ]
                }
            ],
            "kpis": ["Progression Sales Quantity", "Évolution taux Goal_Reached", "Revenu moyen mois/mois"]
        }
    }

    for cluster_id, profil in cluster_profiles.items():
        profil_nom = profil['nom']
        style  = get_style(profil_nom)
        bg_s   = style['bg']
        brd_s  = style['border']
        hdr_s  = style['header']

        plan_key = "accompagner"
        for key in PLANS:
            if key.lower() in profil_nom.lower():
                plan_key = key
                break
        plan = PLANS[plan_key]

        # Bandeau profil
        st.markdown(
            "<div style='background:white; border-radius:10px; padding:14px 18px;"
            "box-shadow:0 2px 8px rgba(71,94,114,0.08); margin-bottom:12px;"
            "border-left:5px solid " + brd_s + ";'>"
            "<span style='font-size:14px; font-weight:700; color:" + brd_s + ";'>"
            + plan['emoji'] + " " + profil_nom + "</span>"
            "<span style='font-size:11px; color:" + C_MID + "; margin-left:12px;'>"
            + str(profil['nb_vendeurs']) + " vendeurs · "
            + f"Revenu moy. {profil['revenue']:,.0f} EUR · "
            + f"Taux objectif {profil['goal_reached']*100:.1f}%"
            + "</span></div>",
            unsafe_allow_html=True
        )

        # 3 colonnes mois
        col1, col2, col3 = st.columns(3, gap="medium")
        for col, mois in zip([col1, col2, col3], plan['mois']):
            with col:
                actions_html = "".join([
                    "<li style='margin-bottom:4px;'>" + a + "</li>"
                    for a in mois['actions']
                ])
                st.markdown(
                    "<div style='background:white; border-radius:10px; padding:14px;"
                    "box-shadow:0 2px 8px rgba(71,94,114,0.08); height:100%;"
                    "border-top:3px solid " + brd_s + ";'>"
                    "<p style='font-size:11px; font-weight:700; color:" + brd_s + ";"
                    "margin:0 0 2px 0;'>" + mois['titre'] + "</p>"
                    "<p style='font-size:10px; color:" + C_MID + "; font-style:italic;"
                    "margin:0 0 10px 0;'>Objectif : " + mois['objectif'] + "</p>"
                    "<ul style='margin:0; padding-left:16px; color:" + C_DARK + ";"
                    "font-size:10px; line-height:1.7;'>"
                    + actions_html +
                    "</ul></div>",
                    unsafe_allow_html=True
                )

        # KPIs
        st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
        kpi_cols = st.columns(len(plan['kpis']), gap="small")
        for kpi_col, kpi in zip(kpi_cols, plan['kpis']):
            with kpi_col:
                st.markdown(
                    "<div style='background:" + bg_s + "; border:1px solid " + brd_s + ";"
                    "border-radius:6px; padding:6px 10px; font-size:10px; text-align:center;"
                    "color:" + hdr_s + ";'>"
                    "📍 <b>" + kpi + "</b></div>",
                    unsafe_allow_html=True
                )

        st.markdown("---")

    # ============================================================
    # SECTION 3 — SYNTHÈSE EXPORTABLE
    # ============================================================
    st.markdown("## Synthèse exportable")

    info_box(
        "Tableau récapitulatif de chaque vendeur avec son profil, "
        "sa stratégie et ses indicateurs clés. Téléchargeable en CSV."
    )

    STRATEGIES = {
        "Stars":       "Fidéliser et valoriser",
        "Performants": "Développer la constance",
        "accompagner": "Accompagnement renforcé sur le volume",
    }

    synthese_rows = []
    for cluster_id, profil in cluster_profiles.items():
        strat_key = "accompagner"
        for key in STRATEGIES:
            if key.lower() in profil['nom'].lower():
                strat_key = key
                break
        for vendeur in profil['vendeurs']:
            synthese_rows.append({
                'Vendeur':           vendeur,
                'Profil':            profil['nom'],
                'Stratégie':         STRATEGIES[strat_key],
                'Revenu moy. (EUR)': round(profil['revenue'], 2),
                'Marge moy.':        f"{profil['margin']*100:.1f}%",
                'Taux objectif':     f"{profil['goal_reached']*100:.1f}%",
                'Cluster':           cluster_id,
            })

    df_synthese = pd.DataFrame(synthese_rows).sort_values('Profil')
    st.dataframe(df_synthese, use_container_width=True, hide_index=True)

    csv = df_synthese.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇ Télécharger la synthèse (CSV)",
        data=csv,
        file_name="synthese_recommandations_vendeurs.csv",
        mime="text/csv"
    )
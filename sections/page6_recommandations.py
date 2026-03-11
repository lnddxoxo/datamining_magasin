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

    # ============================================================
    # SECTION 1 — SYNTHÈSE DES RÉSULTATS
    # ============================================================
    st.markdown("## Synthèse des résultats")

    # Résultats segmentation
    st.markdown(
        f"<p style='font-size:11px; font-weight:700; color:{C_MID};"
        f"text-transform:uppercase; letter-spacing:1px; margin:0 0 10px 0;'>"
        f"Ce que la Segmentation K-Means nous a appris</p>",
        unsafe_allow_html=True
    )

    PROFIL_COLORS = {
        "Stars":       {"bg": "#e8f4e8", "border": "#2d7a2d", "header": "#1a5c1a"},
        "Performants": {"bg": "#e8eef4", "border": "#475E72", "header": "#2c3e50"},
        "accompagner": {"bg": "#fdf3e3", "border": "#c8860a", "header": "#8b5e00"},
    }

    PROFIL_DESC = {
        "Stars":       "Fort revenu, bonne marge, nombreux clients. Les piliers du magasin.",
        "Performants": "Bon volume mais résultats irréguliers. Potentiel d'évolution réel.",
        "accompagner": "Marge la plus élevée mais volume insuffisant. Savent bien vendre, pas assez.",
    }

    PROFIL_EMOJI = {
        "Stars": "⭐", "Performants": "📈", "accompagner": "🔧"
    }

    def get_style(nom):
        for key in PROFIL_COLORS:
            if key.lower() in nom.lower():
                return PROFIL_COLORS[key], key
        return PROFIL_COLORS["accompagner"], "accompagner"

    cols = st.columns(len(cluster_profiles), gap="medium")
    for col, (cluster_id, profil) in zip(cols, cluster_profiles.items()):
        style, key = get_style(profil['nom'])
        bg_s  = style['bg']
        brd_s = style['border']
        hdr_s = style['header']
        emoji = PROFIL_EMOJI.get(key, "🔧")
        desc  = PROFIL_DESC.get(key, "")

        with col:
            st.markdown(
                "<div style='background:white; border-radius:12px; padding:16px;"
                "box-shadow:0 4px 16px rgba(71,94,114,0.1);"
                "border-top:5px solid " + brd_s + ";'>"
                "<p style='font-size:13px; font-weight:700; color:" + brd_s + "; margin:0 0 2px 0;'>"
                + emoji + " " + profil['nom'] + "</p>"
                "<p style='font-size:10px; color:" + C_MID + "; margin:0 0 10px 0;'>"
                + str(profil['nb_vendeurs']) + " vendeurs</p>"
                "<hr style='border-color:" + C_LIGHT + "; margin:8px 0;'>"
                "<p style='font-size:11px; color:" + C_DARK + "; margin:4px 0;'>"
                "💰 <b>" + f"{profil['revenue']:,.0f}" + " EUR</b>/jour</p>"
                "<p style='font-size:11px; color:" + C_DARK + "; margin:4px 0;'>"
                "📊 <b>" + f"{profil['margin']*100:.1f}" + "%</b> marge</p>"
                "<p style='font-size:11px; color:" + C_DARK + "; margin:4px 0;'>"
                "🎯 <b>" + f"{profil['goal_reached']*100:.1f}" + "%</b> objectifs</p>"
                "<hr style='border-color:" + C_LIGHT + "; margin:8px 0;'>"
                "<p style='font-size:10px; color:" + C_MID + "; font-style:italic; margin:0;'>"
                + desc + "</p>"
                "</div>",
                unsafe_allow_html=True
            )

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # Résultats classification
    st.markdown(
        f"<p style='font-size:11px; font-weight:700; color:{C_MID};"
        f"text-transform:uppercase; letter-spacing:1px; margin:0 0 10px 0;'>"
        f"Ce que la Classification nous a appris</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div style='background:white; border-radius:12px; padding:20px;"
        f"box-shadow:0 4px 16px rgba(71,94,114,0.1); border-left:5px solid {C_DARK};'>"

        f"<p style='font-size:13px; color:{C_DARK}; margin:0 0 14px 0;'>"
        f"L'arbre de décision a été entraîné sur <b>41 629 journées de vente</b> "
        f"pour prédire si un vendeur va atteindre son objectif. "
        f"Avec une accuracy de <b>~80%</b>, le modèle identifie clairement "
        f"les deux variables qui déterminent le succès :</p>"

        f"<div style='display:flex; gap:12px;'></div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown(
            f"<div style='background:{C_BG}; border-radius:10px; padding:14px;"
            f"border-left:4px solid {C_DARK};'>"
            f"<p style='font-size:22px; font-weight:900; color:{C_DARK}; margin:0;'>🥇 Sales Quantity</p>"
            f"<p style='font-size:12px; color:{C_MID}; margin:4px 0 8px 0;'>Variable n°1 — ~60% de la décision</p>"
            f"<p style='font-size:11px; color:{C_DARK}; margin:0;'>"
            f"Le <b>volume de transactions journalières</b> est le meilleur prédicteur. "
            f"Un vendeur qui vend beaucoup génère mécaniquement plus de revenu "
            f"et se rapproche de son objectif.</p>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div style='background:{C_BG}; border-radius:10px; padding:14px;"
            f"border-left:4px solid {C_WARM};'>"
            f"<p style='font-size:22px; font-weight:900; color:{C_DARK}; margin:0;'>🥈 Revenue</p>"
            f"<p style='font-size:12px; color:{C_MID}; margin:4px 0 8px 0;'>Variable n°2 — ~30% de la décision</p>"
            f"<p style='font-size:11px; color:{C_DARK}; margin:0;'>"
            f"À volume égal, c'est la <b>valeur des ventes</b> qui fait la différence. "
            f"Les vendeurs qui concluent des ventes à prix élevé atteignent "
            f"plus facilement leurs objectifs.</p>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    success_box(
        "En combinant les deux analyses : les vendeurs <b>À accompagner</b> ont une bonne marge "
        "mais un <b>Sales Quantity trop faible</b> — c'est précisément ce que la classification "
        "identifie comme cause d'échec. Les <b>Stars</b> excellent sur les deux dimensions. "
        "Les <b>Performants</b> manquent de régularité dans le volume."
    )

    st.markdown("---")

    # ============================================================
    # SECTION 2 — RECOMMANDATIONS PAR PROFIL
    # ============================================================
    st.markdown("## Recommandations par profil")

    info_box(
        "Chaque recommandation est ancrée sur les résultats des deux analyses. "
        "Le plan sur <b>3 mois</b> cible les leviers identifiés par la segmentation et la classification."
    )

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    PLANS = {
        "Stars": {
            "emoji": "⭐",
            "synthese": "Fort sur les deux dimensions — volume ET valeur. Objectif : les retenir et capitaliser sur leur expertise.",
            "mois": [
                {
                    "titre": "Mois 1 — Reconnaissance",
                    "objectif": "Renforcer l'engagement",
                    "actions": [
                        "Programme de bonus et awards mensuels",
                        "Réunion individuelle de valorisation",
                        "Identifier les Stars prêts à devenir mentors",
                    ]
                },
                {
                    "titre": "Mois 2 — Responsabilité",
                    "objectif": "Capitaliser sur leur expertise",
                    "actions": [
                        "Lancer le mentorat vers les À accompagner",
                        "Impliquer dans les décisions stratégiques",
                        "Objectifs premium avec incentives exclusifs",
                    ]
                },
                {
                    "titre": "Mois 3 — Fidélisation",
                    "objectif": "Ancrer sur le long terme",
                    "actions": [
                        "Plan de carrière individualisé",
                        "Évaluer l'impact du mentorat",
                        "Mesurer taux de rétention et satisfaction",
                    ]
                }
            ],
            "kpis": ["Taux de rétention", "Taux objectifs premium", "Nb vendeurs mentorés en progression"]
        },
        "Performants": {
            "emoji": "📈",
            "synthese": "Bon volume mais irrégulier — la classification montre que leur Sales Quantity fluctue. Objectif : gagner en constance.",
            "mois": [
                {
                    "titre": "Mois 1 — Diagnostic",
                    "objectif": "Comprendre les journées en échec",
                    "actions": [
                        "Analyser les jours où le volume baisse",
                        "Coaching individuel sur la régularité",
                        "Binômage avec un vendeur Star",
                    ]
                },
                {
                    "titre": "Mois 2 — Formation",
                    "objectif": "Développer la constance du volume",
                    "actions": [
                        "Formation techniques de vente avancées",
                        "Partage bonnes pratiques Stars",
                        "Objectifs de volume progressifs",
                    ]
                },
                {
                    "titre": "Mois 3 — Évaluation",
                    "objectif": "Mesurer et ajuster",
                    "actions": [
                        "Comparer Sales Quantity avant/après",
                        "Identifier les Performants proches Stars",
                        "Revoir les objectifs selon progression",
                    ]
                }
            ],
            "kpis": ["Régularité Sales Quantity", "Évolution taux Goal_Reached", "Nb Performants passés Stars"]
        },
        "accompagner": {
            "emoji": "🔧",
            "synthese": "Marge élevée mais Sales Quantity trop faible — la classification prédit l'échec sur ce seul critère. Objectif : augmenter le volume sans sacrifier la qualité.",
            "mois": [
                {
                    "titre": "Mois 1 — Stabilisation",
                    "objectif": "Comprendre les blocages du volume",
                    "actions": [
                        "Entretien individuel sur les freins",
                        "Réviser les objectifs à la hausse progressive",
                        "Formation produit et techniques de base",
                    ]
                },
                {
                    "titre": "Mois 2 — Accompagnement",
                    "objectif": "Augmenter le volume de transactions",
                    "actions": [
                        "Points hebdomadaires avec le manager",
                        "Parrainage par un vendeur Star",
                        "Challenges de volume avec récompenses",
                    ]
                },
                {
                    "titre": "Mois 3 — Mesure",
                    "objectif": "Évaluer la progression",
                    "actions": [
                        "Comparer Sales Quantity avant/après",
                        "Mesurer évolution Goal_Reached",
                        "Identifier les vendeurs prêts à passer Performants",
                    ]
                }
            ],
            "kpis": ["Progression Sales Quantity", "Évolution Goal_Reached", "Revenu moyen mois/mois"]
        }
    }

    for cluster_id, profil in cluster_profiles.items():
        profil_nom = profil['nom']
        style, key = get_style(profil_nom)
        bg_s  = style['bg']
        brd_s = style['border']
        hdr_s = style['header']

        plan_key = "accompagner"
        for k in PLANS:
            if k.lower() in profil_nom.lower():
                plan_key = k
                break
        plan = PLANS[plan_key]

        # Bandeau profil + synthèse
        st.markdown(
            f"<div style='background:white; border-radius:12px; padding:16px 20px;"
            f"box-shadow:0 4px 16px rgba(71,94,114,0.1); margin-bottom:12px;"
            f"border-left:5px solid " + brd_s + ";'>"
            f"<p style='font-size:14px; font-weight:700; color:" + brd_s + "; margin:0 0 4px 0;'>"
            + plan['emoji'] + " " + profil_nom +
            f"<span style='font-size:11px; color:{C_MID}; font-weight:400; margin-left:12px;'>"
            + str(profil['nb_vendeurs']) + " vendeurs · "
            + f"Revenu moy. {profil['revenue']:,.0f} EUR · "
            + f"Goal_Reached {profil['goal_reached']*100:.1f}%"
            + "</span></p>"
            f"<p style='font-size:11px; color:{C_DARK}; margin:0; font-style:italic;'>"
            + plan['synthese'] +
            "</p></div>",
            unsafe_allow_html=True
        )

        # 3 colonnes mois
        col1, col2, col3 = st.columns(3, gap="medium")
        for col, mois in zip([col1, col2, col3], plan['mois']):
            with col:
                actions_html = "".join([
                    "<li style='margin-bottom:5px;'>" + a + "</li>"
                    for a in mois['actions']
                ])
                st.markdown(
                    "<div style='background:white; border-radius:10px; padding:14px;"
                    "box-shadow:0 2px 8px rgba(71,94,114,0.08);"
                    "border-top:3px solid " + brd_s + ";'>"
                    "<p style='font-size:11px; font-weight:700; color:" + brd_s + "; margin:0 0 2px 0;'>"
                    + mois['titre'] + "</p>"
                    "<p style='font-size:10px; color:" + C_MID + "; font-style:italic; margin:0 0 10px 0;'>"
                    "🎯 " + mois['objectif'] + "</p>"
                    "<ul style='margin:0; padding-left:16px; color:" + C_DARK + "; font-size:10px; line-height:1.8;'>"
                    + actions_html +
                    "</ul></div>",
                    unsafe_allow_html=True
                )

        # KPIs
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        kpi_cols = st.columns(len(plan['kpis']), gap="small")
        for kpi_col, kpi in zip(kpi_cols, plan['kpis']):
            with kpi_col:
                st.markdown(
                    "<div style='background:" + bg_s + "; border:1px solid " + brd_s + ";"
                    "border-radius:6px; padding:6px 10px; font-size:10px;"
                    "text-align:center; color:" + hdr_s + ";'>"
                    "📍 <b>" + kpi + "</b></div>",
                    unsafe_allow_html=True
                )

        st.markdown("---")

    # ============================================================
    # SECTION 3 — SYNTHÈSE EXPORTABLE
    # ============================================================
    st.markdown("## Synthèse exportable")

    info_box(
        "Tableau récapitulatif par vendeur avec profil, stratégie et indicateurs clés."
    )

    STRATEGIES = {
        "Stars":       "Fidéliser et valoriser",
        "Performants": "Développer la constance du volume",
        "accompagner": "Accompagnement renforcé sur le volume",
    }

    synthese_rows = []
    for cluster_id, profil in cluster_profiles.items():
        style, key = get_style(profil['nom'])
        strat = STRATEGIES.get(key, STRATEGIES["accompagner"])
        for vendeur in profil['vendeurs']:
            synthese_rows.append({
                'Vendeur':           vendeur,
                'Profil':            profil['nom'],
                'Stratégie':         strat,
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
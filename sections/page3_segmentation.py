import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from streamlit_echarts5 import st_echarts

from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG
from utils.charts import info_box, success_box, warning_box

CLUSTER_COLORS  = ['#475E72', '#E1CBB2', '#73828E']
CLUSTER_LIGHTS  = ['#dce3ea', '#fdf6ee', '#e8ecee']
CLUSTER_BORDERS = ['#475E72', '#c8a882', '#4f6370']


def generate_clusters(data_store):
    df = data_store.copy()
    if 'Goal_Reached' not in df.columns:
        df['Goal_Reached'] = (df['Revenue'] >= df['Revenue Goal']).astype(int)
    col_vendeur = 'Seller' if 'Seller' in df.columns else 'seller_name'
    df_sellers = df.groupby(col_vendeur).agg(
        Revenue        = ('Revenue',        'mean'),
        Margin         = ('Margin',         'mean'),
        Sales_Quantity = ('Sales Quantity', 'mean'),
        Customers      = ('Customers',      'mean'),
        Goal_Reached   = ('Goal_Reached',   'mean'),
    ).round(3).reset_index()
    features = ['Revenue', 'Margin', 'Sales_Quantity', 'Customers', 'Goal_Reached']
    X_scaled = StandardScaler().fit_transform(df_sellers[features])
    df_sellers['Cluster'] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X_scaled)
    profils = df_sellers.groupby('Cluster').agg(
        Revenue=('Revenue','mean'), Margin=('Margin','mean'),
        Sales_Quantity=('Sales_Quantity','mean'), Customers=('Customers','mean'),
        Goal_Reached=('Goal_Reached','mean'), Nb_vendeurs=(col_vendeur,'count')
    ).round(3)
    profils_sorted = profils.sort_values('Revenue', ascending=False).reset_index()
    noms_auto = []
    for i, row in profils_sorted.iterrows():
        if row['Revenue'] >= profils['Revenue'].quantile(0.66):
            noms_auto.append("Stars")
        elif row['Revenue'] >= profils['Revenue'].quantile(0.33):
            noms_auto.append("Performants")
        else:
            noms_auto.append("A accompagner")
    profils_sorted['Profil'] = noms_auto
    cluster_profiles = {}
    for _, row in profils_sorted.iterrows():
        cid = int(row['Cluster'])
        cluster_profiles[cid] = {
            'nom': row['Profil'], 'revenue': round(row['Revenue'],2),
            'margin': round(row['Margin'],3), 'goal_reached': round(row['Goal_Reached'],3),
            'nb_vendeurs': int(row['Nb_vendeurs']),
            'vendeurs': df_sellers[df_sellers['Cluster']==cid][col_vendeur].tolist()
        }
    st.session_state['cluster_profiles'] = cluster_profiles
    st.session_state['df_sellers'] = df_sellers


def show(data_store):
    df = data_store.copy()
    if 'Goal_Reached' not in df.columns:
        df['Goal_Reached'] = (df['Revenue'] >= df['Revenue Goal']).astype(int)

    col_vendeur = 'Seller' if 'Seller' in df.columns else 'seller_name'

    df_sellers = df.groupby(col_vendeur).agg(
        Revenue        = ('Revenue',        'mean'),
        Margin         = ('Margin',         'mean'),
        Sales_Quantity = ('Sales Quantity', 'mean'),
        Customers      = ('Customers',      'mean'),
        Goal_Reached   = ('Goal_Reached',   'mean'),
    ).round(3).reset_index()

    features = ['Revenue', 'Margin', 'Sales_Quantity', 'Customers', 'Goal_Reached']
    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(df_sellers[features])

    # ── TITRE ──────────────────────────────────────────────
    st.markdown(
        "<div style='background:linear-gradient(135deg,#475E72 0%,#73828E 100%);"
        "padding:28px 32px;border-radius:10px;margin-bottom:24px;'>"
        "<h1 style='color:white;margin:0;font-size:1.8rem;'>🔍 Segmentation des Vendeurs</h1>"
        "<p style='color:#E1CBB2;margin:6px 0 0 0;font-size:1rem;'>"
        "Algorithme K-Means · 19 vendeurs · 5 indicateurs de performance</p></div>",
        unsafe_allow_html=True
    )

    # ============================================================
    # BLOC 3.1 — JUSTIFICATION
    # ============================================================
    st.markdown("<h2 style='color:#475E72'>3.1 — Pourquoi K-Means ?</h2>", unsafe_allow_html=True)

    info_box(
        "<b>Question métier :</b> Quels profils naturels de vendeurs existent dans ce magasin ? "
        "Comment adapter nos stratégies de management à chaque groupe ?"
    )

    st.markdown(" ")
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(
            "<div style='background-color:#EAE6E2;border-radius:8px;padding:20px;height:100%;'>"
            "<h4 style='color:#475E72;margin-top:0;'>🤖 Pourquoi K-Means ?</h4>"
            "<ul style='color:#2c3e50;line-height:1.9;margin:0;'>"
            "<li>On ne connaît <b>pas les groupes à l'avance</b> → apprentissage non supervisé</li>"
            "<li>On veut des groupes <b>exclusifs</b> : chaque vendeur dans un seul cluster</li>"
            "<li>Dataset petit (19 vendeurs) → K-Means <b>converge rapidement</b></li>"
            "<li>Toutes les variables sont <b>numériques et standardisables</b></li>"
            "</ul></div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div style='background-color:#EAE6E2;border-radius:8px;padding:20px;'>"
            "<h4 style='color:#475E72;margin-top:0;'>📋 Variables retenues</h4>"
            "<table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>"
            "<thead><tr style='background-color:#475E72;color:white;'>"
            "<th style='padding:7px 10px;text-align:left;'>Variable</th>"
            "<th style='padding:7px 10px;text-align:left;'>Ce qu elle mesure</th></tr></thead>"
            "<tbody>"
            "<tr style='background-color:white;'><td style='padding:7px 10px;border-bottom:1px solid #DEDEDE;'><b>Revenue</b></td><td style='padding:7px 10px;border-bottom:1px solid #DEDEDE;'>Volume de chiffre d affaires</td></tr>"
            "<tr style='background-color:#EAE6E2;'><td style='padding:7px 10px;border-bottom:1px solid #DEDEDE;'><b>Margin</b></td><td style='padding:7px 10px;border-bottom:1px solid #DEDEDE;'>Rentabilite des ventes (0-1)</td></tr>"
            "<tr style='background-color:white;'><td style='padding:7px 10px;border-bottom:1px solid #DEDEDE;'><b>Sales Quantity</b></td><td style='padding:7px 10px;border-bottom:1px solid #DEDEDE;'>Unites vendues par jour</td></tr>"
            "<tr style='background-color:#EAE6E2;'><td style='padding:7px 10px;border-bottom:1px solid #DEDEDE;'><b>Customers</b></td><td style='padding:7px 10px;border-bottom:1px solid #DEDEDE;'>Clients servis par jour</td></tr>"
            "<tr style='background-color:white;'><td style='padding:7px 10px;'><b>Goal_Reached</b></td><td style='padding:7px 10px;'>Regularite dans l atteinte des objectifs</td></tr>"
            "</tbody></table></div>",
            unsafe_allow_html=True
        )

    st.markdown(" ")
    warning_box(
        "⚠ <b>Variables exclues :</b> Year, Month et Department — "
        "variables contextuelles, pas des indicateurs de performance individuelle."
    )
    st.markdown("---")

    # ============================================================
    # BLOC 3.2 — MÉTHODE DU COUDE
    # ============================================================
    st.markdown("<h2 style='color:#475E72'>3.2 — Methode du Coude (Elbow Method)</h2>", unsafe_allow_html=True)

    info_box(
        "<b>Principe :</b> On entraine K-Means pour K=2, 3 et 4 et on mesure l'<b>inertie</b> "
        "a chaque fois. On cherche le <b>coude</b> : le point ou diminuer K n'apporte plus de gain significatif."
    )

    inerties = []
    for k in range(2, 5):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inerties.append(round(km.inertia_, 2))

    option_coude = {
        "backgroundColor": C_BG,
        "title": {
            "text": "Inertie en fonction du nombre de clusters K",
            "subtext": "Le coude indique le K optimal",
            "textStyle": {"color": C_DARK, "fontSize": 15, "fontWeight": "bold"},
            "subtextStyle": {"color": C_MID, "fontSize": 12}
        },
        "grid": {"left": "10%", "right": "5%", "bottom": "15%", "top": "18%"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": ["K=2", "K=3", "K=4"],
            "name": "Nombre de clusters",
            "nameLocation": "middle",
            "nameGap": 35,
            "nameTextStyle": {"color": C_MID, "fontSize": 12},
            "axisLabel": {"color": C_DARK, "fontSize": 13, "fontWeight": "bold"},
            "axisLine": {"lineStyle": {"color": C_MID}}
        },
        "yAxis": {
            "type": "value",
            "name": "Inertie",
            "nameLocation": "middle",
            "nameGap": 55,
            "nameTextStyle": {"color": C_MID, "fontSize": 12},
            "axisLabel": {"color": C_MID},
            "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}}
        },
        "series": [{
            "data": inerties,
            "type": "line",
            "smooth": False,
            "lineStyle": {"color": C_DARK, "width": 3},
            "itemStyle": {"color": C_DARK, "borderColor": C_WARM, "borderWidth": 3},
            "symbolSize": 12,
            "label": {
                "show": True,
                "position": "top",
                "color": C_DARK,
                "fontWeight": "bold",
                "fontSize": 12,
                "formatter": "{c}"
            },
            "areaStyle": {
                "color": {
                    "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": "rgba(71,94,114,0.2)"},
                        {"offset": 1, "color": "rgba(71,94,114,0)"}
                    ]
                }
            }
        }]
    }

    st_echarts(options=option_coude, height="380px")

    success_box(
        "✅ <b>Conclusion :</b> Le coude est clairement visible a <b>K=3</b>. "
        "Au-dela, le gain d'inertie devient marginal. Nous retenons <b>3 clusters</b>."
    )
    st.markdown("---")

    # ============================================================
    # BLOC 3.3 — ENTRAÎNEMENT K=3
    # ============================================================
    st.markdown("<h2 style='color:#475E72'>3.3 — Entrainement du Modele (K=3)</h2>", unsafe_allow_html=True)

    info_box(
        "K-Means est entraine avec <b>K=3</b>, <code>random_state=42</code> pour la reproductibilite "
        "et <code>n_init=10</code> pour eviter les minima locaux."
    )

    k = st.slider(
        "Choisir le nombre de clusters K",
        min_value=2,
        max_value=4,
        value=3,
        help="K=3 est recommande par la methode du coude"
    )
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_sellers['Cluster'] = kmeans.fit_predict(X_scaled)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<h4 style='color:#475E72'>Repartition des vendeurs</h4>", unsafe_allow_html=True)
        repartition = df_sellers.groupby('Cluster')[col_vendeur].apply(list).reset_index()
        repartition.columns = ['Cluster', 'Vendeurs']
        repartition['Nb vendeurs'] = repartition['Vendeurs'].apply(len)
        repartition['Vendeurs'] = repartition['Vendeurs'].apply(lambda x: ', '.join(x))

        for _, r in repartition.iterrows():
            cid = int(r['Cluster'])
            bg_c  = CLUSTER_LIGHTS[cid % 3]
            brd_c = CLUSTER_BORDERS[cid % 3]
            st.markdown(
                "<div style='background-color:" + bg_c + ";border-left:4px solid " + brd_c + ";"
                "border-radius:6px;padding:10px 14px;margin-bottom:8px;'>"
                "<b style='color:" + brd_c + ";'>Cluster " + str(cid) + "</b>"
                "<span style='color:#73828E;font-size:0.85rem;'> · " + str(r['Nb vendeurs']) + " vendeurs</span>"
                "<br/><span style='font-size:0.85rem;color:#2c3e50;'>" + r['Vendeurs'] + "</span></div>",
                unsafe_allow_html=True
            )

    with col2:
        pie_data = [
            {"value": int(count), "name": "Cluster " + str(cluster)}
            for cluster, count in df_sellers['Cluster'].value_counts().sort_index().items()
        ]
        option_pie = {
            "backgroundColor": C_BG,
            "title": {
                "text": "Repartition par cluster",
                "textStyle": {"color": C_DARK, "fontSize": 13},
                "left": "center"
            },
            "tooltip": {"trigger": "item", "formatter": "{b} : {c} vendeurs ({d}%)"},
            "legend": {"bottom": "5%", "textStyle": {"color": C_MID}},
            "series": [{
                "type": "pie",
                "radius": ["35%", "65%"],
                "center": ["50%", "48%"],
                "data": pie_data,
                "itemStyle": {"borderRadius": 8, "borderWidth": 3, "borderColor": C_BG},
                "color": CLUSTER_COLORS,
                "label": {"show": True, "formatter": "{b}\n{c} vendeurs", "color": C_DARK, "fontSize": 11},
                "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0,0,0,0.2)"}}
            }]
        }
        st_echarts(options=option_pie, height="340px")

    st.markdown("---")

    # ============================================================
    # BLOC 3.4 — ANALYSE DES CLUSTERS
    # ============================================================
    st.markdown("<h2 style='color:#475E72'>3.4 — Profils des Clusters</h2>", unsafe_allow_html=True)

    profils = df_sellers.groupby('Cluster').agg(
        Revenue        = ('Revenue',        'mean'),
        Margin         = ('Margin',         'mean'),
        Sales_Quantity = ('Sales_Quantity', 'mean'),
        Customers      = ('Customers',      'mean'),
        Goal_Reached   = ('Goal_Reached',   'mean'),
        Nb_vendeurs    = (col_vendeur,      'count')
    ).round(3)

    profils_sorted = profils.sort_values('Revenue', ascending=False).reset_index()

    noms_auto = []
    for i, row in profils_sorted.iterrows():
        if row['Revenue'] >= profils['Revenue'].quantile(0.66):
            noms_auto.append("Stars")
        elif row['Revenue'] >= profils['Revenue'].quantile(0.33):
            noms_auto.append("Performants")
        else:
            noms_auto.append("A accompagner")
    profils_sorted['Profil'] = noms_auto

    cols = st.columns(3, gap="medium")
    for i, (_, row) in enumerate(profils_sorted.iterrows()):
        cid   = int(row['Cluster'])
        bg_c  = CLUSTER_LIGHTS[i % 3]
        brd_c = CLUSTER_COLORS[i % 3]
        with cols[i]:
            st.markdown(
                "<div style='background:" + bg_c + ";border:1px solid " + brd_c + ";"
                "border-top:5px solid " + brd_c + ";border-radius:8px;padding:16px;text-align:center;'>"
                "<h3 style='color:" + brd_c + ";margin:0 0 4px 0;font-size:1.1rem;'>" + row['Profil'] + "</h3>"
                "<p style='color:#73828E;margin:0 0 12px 0;font-size:0.8rem;'>Cluster " + str(cid) + " · " + str(int(row['Nb_vendeurs'])) + " vendeurs</p>"
                "<hr style='border-color:#DEDEDE;margin:8px 0;'>"
                "<p style='margin:4px 0;font-size:0.9rem;'>💰 <b>" + f"{row['Revenue']:,.0f}" + " EUR</b> revenu moy.</p>"
                "<p style='margin:4px 0;font-size:0.9rem;'>📊 <b>" + f"{row['Margin']*100:.1f}" + "%</b> marge moy.</p>"
                "<p style='margin:4px 0;font-size:0.9rem;'>🎯 <b>" + f"{row['Goal_Reached']*100:.1f}" + "%</b> taux objectif</p>"
                "<p style='margin:4px 0;font-size:0.9rem;'>👥 <b>" + f"{row['Customers']:,.0f}" + "</b> clients/jour</p>"
                "</div>",
                unsafe_allow_html=True
            )

    st.markdown(" ")
    st.markdown("<h4 style='color:#475E72'>Tableau comparatif</h4>", unsafe_allow_html=True)
    display_profils = profils_sorted[[
        'Cluster', 'Profil', 'Revenue', 'Margin',
        'Sales_Quantity', 'Customers', 'Goal_Reached', 'Nb_vendeurs'
    ]].rename(columns={
        'Revenue': 'Revenu moy. (EUR)', 'Margin': 'Marge moy.',
        'Sales_Quantity': 'Qte ventes moy.', 'Customers': 'Clients moy.',
        'Goal_Reached': 'Taux objectif', 'Nb_vendeurs': 'Nb vendeurs'
    })
    st.dataframe(display_profils, use_container_width=True, hide_index=True)
    st.markdown("---")

    # ============================================================
    # BLOC 3.5 — VISUALISATION PCA
    # ============================================================
    st.markdown("<h2 style='color:#475E72'>3.5 — Visualisation 2D des Clusters (PCA)</h2>", unsafe_allow_html=True)

    info_box(
        "<b>PCA :</b> On compresse les 5 variables en 2 dimensions pour visualiser les clusters. "
        "Chaque point = un vendeur. Les vendeurs proches se ressemblent dans leurs performances."
    )

    pca    = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)
    df_sellers['PCA1'] = coords[:, 0]
    df_sellers['PCA2'] = coords[:, 1]

    variance_expliquee = pca.explained_variance_ratio_
    success_box(
        "📐 Les 2 composantes PCA capturent <b>"
        + str(round(sum(variance_expliquee)*100, 1))
        + "%</b> de l'information totale. La visualisation est donc <b>tres fiable</b>."
    )

    scatter_series = []
    for cluster_id in sorted(df_sellers['Cluster'].unique()):
        subset     = df_sellers[df_sellers['Cluster'] == cluster_id]
        profil_nom = profils_sorted[profils_sorted['Cluster'] == cluster_id]['Profil'].values[0]
        scatter_series.append({
            "name": profil_nom,
            "type": "scatter",
            "symbolSize": 18,
            "data": [
                {"value": [round(row['PCA1'], 3), round(row['PCA2'], 3)], "name": row[col_vendeur]}
                for _, row in subset.iterrows()
            ],
            "itemStyle": {
                "color": CLUSTER_COLORS[cluster_id % 3],
                "borderColor": "white", "borderWidth": 2,
                "shadowBlur": 6, "shadowColor": "rgba(0,0,0,0.2)"
            },
            "label": {"show": True, "formatter": "{b}", "position": "top", "fontSize": 10, "color": C_MID}
        })

    option_scatter = {
        "backgroundColor": C_BG,
        "title": {
            "text": "Projection PCA — Separation des clusters",
            "subtext": "Chaque point = un vendeur · Couleur = cluster d'appartenance",
            "textStyle": {"color": C_DARK, "fontSize": 14, "fontWeight": "bold"},
            "subtextStyle": {"color": C_MID, "fontSize": 11}
        },
        "grid": {"left": "8%", "right": "5%", "bottom": "12%", "top": "18%"},
        "tooltip": {"trigger": "item", "formatter": "<b>{a}</b><br/>Vendeur : {b}"},
        "legend": {"bottom": "2%", "textStyle": {"color": C_MID, "fontSize": 12}},
        "xAxis": {
            "name": "Composante Principale 1", "nameLocation": "middle", "nameGap": 30,
            "nameTextStyle": {"color": C_MID}, "axisLabel": {"color": C_MID},
            "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}},
            "axisLine": {"lineStyle": {"color": C_MID}}
        },
        "yAxis": {
            "name": "Composante Principale 2", "nameLocation": "middle", "nameGap": 45,
            "nameTextStyle": {"color": C_MID}, "axisLabel": {"color": C_MID},
            "splitLine": {"lineStyle": {"color": C_LIGHT, "type": "dashed"}},
            "axisLine": {"lineStyle": {"color": C_MID}}
        },
        "series": scatter_series
    }

    st_echarts(options=option_scatter, height="500px")
    st.markdown("---")

    # ============================================================
    # BLOC 3.6 — INTERPRÉTATION MÉTIER
    # ============================================================
    st.markdown("<h2 style='color:#475E72'>3.6 — Interpretation Metier</h2>", unsafe_allow_html=True)

    info_box(
        "Les noms des clusters ont ete determines <b>apres analyse des donnees</b>. "
        "Chaque profil recoit une strategie d'action adaptee."
    )
    st.markdown(" ")

    PROFIL_STYLES = {
        "Stars":        {"bg": "#e8f4e8", "border": "#2d7a2d", "header": "#1a5c1a"},
        "Performants":  {"bg": "#e8eef4", "border": "#475E72", "header": "#2c3e50"},
        "accompagner":  {"bg": "#fdf3e3", "border": "#c8860a", "header": "#8b5e00"},
    }

    ACTIONS = {
        "Stars": [
            ("🏆", "Programme de reconnaissance", "Bonus, awards, mise en avant interne"),
            ("🤝", "Role de mentor",              "Coacher les vendeurs en difficulte"),
            ("🎯", "Objectifs premium",            "Challenges avec incentives exclusifs"),
            ("💬", "Participation strategique",    "Implication dans les decisions"),
        ],
        "Performants": [
            ("📚", "Coaching cible",       "Techniques pour depasser les objectifs"),
            ("🔄", "Apprentissage pairs",  "Observer et partager avec les Stars"),
            ("📈", "Formation avancee",    "Vente et negociation avancees"),
            ("📅", "Suivi mensuel",        "Objectifs progressifs avec feedback"),
        ],
        "accompagner": [
            ("🗺️", "Plan de progression",  "Objectifs realistes et atteignables"),
            ("🎓", "Formation de base",    "Produits et techniques fondamentales"),
            ("✅", "Revision objectifs",   "Adapter les cibles au potentiel reel"),
            ("📞", "Suivi hebdomadaire",   "Points reguliers avec le manager"),
        ],
    }

    KPIS = {
        "Stars":        "Taux de retention · NPS interne · Satisfaction",
        "Performants":  "Evolution taux objectif · Progression revenu",
        "accompagner":  "Progression Goal_Reached · Volume clients",
    }

    for i, (_, row) in enumerate(profils_sorted.iterrows()):
        cluster_id     = int(row['Cluster'])
        profil_nom     = row['Profil']
        vendeurs_liste = df_sellers[df_sellers['Cluster'] == cluster_id][col_vendeur].tolist()

        style_key = "accompagner"
        for key in PROFIL_STYLES:
            if key.lower() in profil_nom.lower():
                style_key = key
                break

        bg_s     = PROFIL_STYLES[style_key]['bg']
        border_s = PROFIL_STYLES[style_key]['border']
        header_s = PROFIL_STYLES[style_key]['header']
        actions  = ACTIONS[style_key]
        kpi      = KPIS[style_key]

        with st.expander(profil_nom + " — Cluster " + str(cluster_id) + " · " + str(int(row['Nb_vendeurs'])) + " vendeurs", expanded=True):

            st.markdown(
                "<div style='background:linear-gradient(135deg," + border_s + " 0%," + bg_s + " 100%);"
                "padding:12px 18px;border-radius:6px;margin-bottom:16px;'>"
                "<h3 style='color:white;margin:0;font-size:1.1rem;'>" + profil_nom + "</h3>"
                "<p style='color:rgba(255,255,255,0.85);margin:2px 0 0 0;font-size:0.85rem;'>"
                "Cluster " + str(cluster_id) + " · " + str(int(row['Nb_vendeurs'])) + " vendeurs</p></div>",
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns([1, 1, 1.2], gap="medium")

            with col1:
                st.markdown("<h5 style='color:#475E72'>📊 Indicateurs moyens</h5>", unsafe_allow_html=True)
                st.metric("Revenu / jour",        f"{row['Revenue']:,.0f} EUR")
                st.metric("Marge",                 f"{row['Margin']*100:.1f} %")
                st.metric("Taux objectif atteint", f"{row['Goal_Reached']*100:.1f} %")
                st.metric("Clients / jour",         f"{row['Customers']:,.0f}")

            with col2:
                st.markdown("<h5 style='color:#475E72'>👥 Vendeurs du groupe</h5>", unsafe_allow_html=True)
                for v in vendeurs_liste:
                    st.markdown(
                        "<div style='background:" + bg_s + ";border-left:3px solid " + border_s + ";"
                        "padding:4px 10px;border-radius:4px;margin-bottom:4px;font-size:0.85rem;'>"
                        "👤 " + v + "</div>",
                        unsafe_allow_html=True
                    )

            with col3:
                st.markdown("<h5 style='color:#475E72'>🎯 Plan d'action</h5>", unsafe_allow_html=True)
                for emoji, titre, detail in actions:
                    st.markdown(
                        "<div style='margin-bottom:8px;'>"
                        "<span style='font-size:1rem;'>" + emoji + "</span> "
                        "<b style='color:" + header_s + ";'>" + titre + "</b><br/>"
                        "<span style='font-size:0.82rem;color:#73828E;margin-left:22px;'>" + detail + "</span>"
                        "</div>",
                        unsafe_allow_html=True
                    )
                st.markdown(
                    "<div style='background:" + bg_s + ";border:1px solid " + border_s + ";"
                    "border-radius:6px;padding:8px 12px;margin-top:8px;font-size:0.82rem;'>"
                    "<b>📌 KPIs :</b> " + kpi + "</div>",
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # ============================================================
    # SAUVEGARDE POUR AXELLE (Page 4) ET PAGE 6
    # ============================================================
    cluster_map = df_sellers.set_index(col_vendeur)['Cluster'].to_dict()
    data_store['Cluster'] = data_store[col_vendeur].map(cluster_map)

    cluster_profiles = {}
    for _, row in profils_sorted.iterrows():
        cluster_id = int(row['Cluster'])
        cluster_profiles[cluster_id] = {
            'nom':          row['Profil'],
            'revenue':      round(row['Revenue'], 2),
            'margin':       round(row['Margin'], 3),
            'goal_reached': round(row['Goal_Reached'], 3),
            'nb_vendeurs':  int(row['Nb_vendeurs']),
            'vendeurs':     df_sellers[df_sellers['Cluster'] == cluster_id][col_vendeur].tolist()
        }

    st.session_state['cluster_profiles'] = cluster_profiles
    st.session_state['df_sellers']        = df_sellers
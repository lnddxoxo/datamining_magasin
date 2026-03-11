import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from streamlit_echarts5 import st_echarts

from utils.styles import C_DARK, C_MID, C_WARM, C_LIGHT, C_BG
from utils.charts import info_box, success_box, warning_box

CLUSTER_COLORS = ['#475E72', '#E1CBB2', '#73828E', '#a0b4c0', '#d4bfa0']

def show(data_store):
    df = data_store.copy()

    # Créer Goal_Reached si elle n'existe pas
    if 'Goal_Reached' not in df.columns:
        df['Goal_Reached'] = (df['Revenue'] >= df['Revenue Goal']).astype(int)

    st.title("Segmentation des Vendeurs — K-Means")
    st.markdown("---")

    # Détecter automatiquement le nom de la colonne vendeur
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

    # ============================================================
    # BLOC 3.1 — JUSTIFICATION
    # ============================================================
    st.header("3.1 — Pourquoi K-Means ?")

    info_box(
        "<b>Question métier :</b> Quels profils de vendeurs distincts existent dans ce magasin ? "
        "Existe-t-il des groupes naturels en termes de performance commerciale ?"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Algorithme choisi")
        st.markdown("""
        **K-Means** est adapté ici car :
        - On ne connaît pas les groupes à l'avance *(non supervisé)*
        - On veut des groupes **exclusifs** : chaque vendeur appartient à un seul cluster
        - Le dataset est petit (19 vendeurs) → K-Means converge rapidement
        - Les variables sont continues et standardisables
        """)

    with col2:
        st.subheader("Variables utilisées")
        st.markdown("""
        | Variable | Rôle |
        |----------|------|
        | Revenue | Volume de revenus générés |
        | Margin | Rentabilité des ventes |
        | Sales Quantity | Activité commerciale |
        | Customers | Base clientèle |
        | Goal_Reached | Régularité dans l'atteinte des objectifs |
        """)

    warning_box(
        "⚠ <b>Year, Month et Department</b> sont exclus du clustering — "
        "ce sont des variables contextuelles, pas des indicateurs de performance individuelle."
    )

    st.markdown("---")

    # ============================================================
    # BLOC 3.2 — MÉTHODE DU COUDE
    # ============================================================
    st.header("3.2 — Méthode du Coude (Elbow Method)")

    info_box(
        "L'inertie mesure la dispersion <i>à l'intérieur</i> des clusters. "
        "Plus elle est basse, mieux les points sont groupés. "
        "On cherche le <b>'coude'</b> — le point où l'inertie cesse de baisser rapidement."
    )

    inerties = []
    for k in range(2, 4):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inerties.append(round(kmeans.inertia_, 2))

    option_coude = {
        "backgroundColor": C_BG,
        "title": {
            "text": "Inertie selon le nombre de clusters K",
            "textStyle": {"color": C_DARK, "fontSize": 15}
        },
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": list(range(2, 4)),
            "name": "Nombre de clusters K",
            "nameLocation": "middle",
            "nameGap": 30,
            "axisLabel": {"color": C_MID}
        },
        "yAxis": {
            "type": "value",
            "name": "Inertie",
            "nameLocation": "middle",
            "nameGap": 50,
            "axisLabel": {"color": C_MID}
        },
        "series": [{
            "data": inerties,
            "type": "line",
            "smooth": True,
            "lineStyle": {"color": C_DARK, "width": 3},
            "itemStyle": {"color": C_WARM},
            "symbolSize": 8,
            "markPoint": {
                "data": [{"type": "min", "name": "Min"}]
            }
        }]
    }

    st_echarts(options=option_coude, height="400px")

    success_box(
        "📌 <b>Lecture du graphique :</b> Le coude se situe généralement autour de K=3 ou K=4 "
        "pour ce dataset — c'est là que l'inertie cesse de baisser significativement."
    )

    st.markdown("---")

    # ============================================================
    # BLOC 3.3 — ENTRAÎNEMENT AVEC SLIDER
    # ============================================================
    st.header("3.3 — Entraînement du Modèle")

    info_box("Utilise le slider pour tester différentes valeurs de K et observer comment les clusters changent.")

    k = st.slider(
        "Nombre de clusters",
        min_value=2,
        max_value=4,
        value=3,
        help="K=3 est recommandé par la méthode du coude"
    )

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_sellers['Cluster'] = kmeans.fit_predict(X_scaled)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Répartition des vendeurs par cluster")
        repartition = df_sellers.groupby('Cluster')[col_vendeur].apply(list).reset_index()
        repartition.columns = ['Cluster', 'Vendeurs']
        repartition['Nb vendeurs'] = repartition['Vendeurs'].apply(len)
        repartition['Vendeurs'] = repartition['Vendeurs'].apply(lambda x: ', '.join(x))
        st.dataframe(repartition, use_container_width=True)

    with col2:
        pie_data = [
            {"value": int(count), "name": f"Cluster {cluster}"}
            for cluster, count in df_sellers['Cluster'].value_counts().sort_index().items()
        ]
        option_pie = {
            "backgroundColor": C_BG,
            "title": {"text": "Répartition par cluster", "textStyle": {"color": C_DARK}},
            "tooltip": {"trigger": "item"},
            "series": [{
                "type": "pie",
                "radius": "60%",
                "data": pie_data,
                "itemStyle": {
                    "borderRadius": 6,
                    "borderWidth": 2,
                    "borderColor": C_BG
                },
                "color": CLUSTER_COLORS[:k],
                "label": {"color": C_DARK}
            }]
        }
        st_echarts(options=option_pie, height="300px")

    st.markdown("---")

    # ============================================================
    # BLOC 3.4 — ANALYSE DES CLUSTERS
    # ============================================================
    st.header("3.4 — Profils des Clusters")

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
            nom = "⭐ Stars"
        elif row['Revenue'] >= profils['Revenue'].quantile(0.33):
            nom = "📈 Performants"
        else:
            nom = "🔧 À accompagner"
        noms_auto.append(nom)

    profils_sorted['Profil'] = noms_auto

    st.subheader("Tableau comparatif des profils")
    display_profils = profils_sorted[[
        'Cluster', 'Profil', 'Revenue', 'Margin',
        'Sales_Quantity', 'Customers', 'Goal_Reached', 'Nb_vendeurs'
    ]].rename(columns={
        'Revenue':        'Revenu moy. (€)',
        'Margin':         'Marge moy.',
        'Sales_Quantity': 'Qté ventes moy.',
        'Customers':      'Clients moy.',
        'Goal_Reached':   'Taux objectif',
        'Nb_vendeurs':    'Nb vendeurs'
    })
    st.dataframe(display_profils, use_container_width=True)

    st.markdown("---")

    # ============================================================
    # BLOC 3.5 — VISUALISATION PCA
    # ============================================================
    st.header("3.5 — Visualisation 2D des Clusters (PCA)")

    info_box(
        "La PCA réduit les 5 variables en 2 dimensions pour visualiser "
        "les clusters. Chaque point = un vendeur."
    )

    pca    = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)
    df_sellers['PCA1'] = coords[:, 0]
    df_sellers['PCA2'] = coords[:, 1]

    variance_expliquee = pca.explained_variance_ratio_
    success_box(
        f"ℹ️ Les 2 composantes PCA expliquent <b>"
        f"{round(sum(variance_expliquee)*100, 1)}%</b> de la variance totale "
        f"(PC1: {round(variance_expliquee[0]*100,1)}%, "
        f"PC2: {round(variance_expliquee[1]*100,1)}%)."
    )

    scatter_series = []
    for cluster_id in sorted(df_sellers['Cluster'].unique()):
        subset = df_sellers[df_sellers['Cluster'] == cluster_id]
        scatter_series.append({
            "name": f"Cluster {cluster_id}",
            "type": "scatter",
            "symbolSize": 16,
            "data": [
                {
                    "value": [round(row['PCA1'], 3), round(row['PCA2'], 3)],
                    "name": row[col_vendeur]
                }
                for _, row in subset.iterrows()
            ],
            "itemStyle": {"color": CLUSTER_COLORS[cluster_id % len(CLUSTER_COLORS)]}
        })

    option_scatter = {
        "backgroundColor": C_BG,
        "title": {
            "text": "Projection PCA des vendeurs par cluster",
            "textStyle": {"color": C_DARK}
        },
        "tooltip": {"trigger": "item", "formatter": "{a} — {b}"},
        "legend": {"textStyle": {"color": C_MID}},
        "xAxis": {
            "name": "Composante 1",
            "nameLocation": "middle",
            "nameGap": 30,
            "axisLabel": {"color": C_MID},
            "splitLine": {"lineStyle": {"color": C_LIGHT}}
        },
        "yAxis": {
            "name": "Composante 2",
            "nameLocation": "middle",
            "nameGap": 40,
            "axisLabel": {"color": C_MID},
            "splitLine": {"lineStyle": {"color": C_LIGHT}}
        },
        "series": scatter_series
    }

    st_echarts(options=option_scatter, height="450px")

    st.markdown("---")

    # ============================================================
    # BLOC 3.6 — INTERPRÉTATION MÉTIER
    # ============================================================
    st.header("3.6 — Interprétation ")

    for _, row in profils_sorted.iterrows():
        cluster_id     = int(row['Cluster'])
        profil_nom     = row['Profil']
        vendeurs_liste = df_sellers[df_sellers['Cluster'] == cluster_id][col_vendeur].tolist()

        with st.expander(f"{profil_nom} — Cluster {cluster_id} ({int(row['Nb_vendeurs'])} vendeurs)"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Caractéristiques clés**")
                st.metric("Revenu moyen",             f"{row['Revenue']:,.0f} €")
                st.metric("Marge moyenne",             f"{row['Margin']*100:.1f} %")
                st.metric("Taux d'atteinte objectif",  f"{row['Goal_Reached']*100:.1f} %")

            with col2:
                st.markdown("**Vendeurs du groupe**")
                for v in vendeurs_liste:
                    st.markdown(f"- {v}")

            if "Stars" in profil_nom:
                success_box("🎯 <b>Action :</b> Fidéliser — programmes de reconnaissance, mentoring, objectifs premium.")
            elif "Performants" in profil_nom:
                info_box("📚 <b>Action :</b> Former sur l'atteinte des objectifs — coaching ciblé.")
            else:
                warning_box("🤝 <b>Action :</b> Plan de progression individuel — accompagnement renforcé.")

    st.markdown("---")
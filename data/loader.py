# ─────────────────────────────────────────
# data/loader.py
# Gestion du chargement et prétraitement des données
# ─────────────────────────────────────────

import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler

# Mise en cache pour éviter de recharger à chaque interaction
@st.cache_data
def load_data():
    # Chargement du fichier CSV
    data_store = pd.read_csv("department_store_dataset.csv", encoding="utf-8")
    # Conversion de la colonne Date en format datetime
    data_store["Date"] = pd.to_datetime(data_store["Date"])
    # Extraction de l'année et du mois depuis Date
    data_store["Year"]  = data_store["Date"].dt.year
    data_store["Month"] = data_store["Date"].dt.month
    data_store["Quarter"] = data_store["Date"].dt.quarter
    # Création de la variable cible : 1 si objectif atteint, 0 sinon
    data_store["Goal_Reached"] = (data_store["Revenue"] >= data_store["Revenue Goal"]).astype(int)
    return data_store

def get_dept_agg(data_store):
    # Agrégation des données par département
    dept_agg = data_store.groupby("Department").agg(
        Avg_Revenue   = ("Revenue",        "mean"),  # Revenu moyen
        Avg_Margin    = ("Margin",         "mean"),  # Marge moyenne
        Avg_Sales     = ("Sales Quantity", "mean"),  # Ventes moyennes
        Avg_Customers = ("Customers",      "mean"),  # Clients moyens
        Goal_Rate     = ("Goal_Reached",   "mean")   # Taux d'atteinte des objectifs
    ).reset_index()
    return dept_agg

def get_seller_agg(data_store):
    # Agrégation des données par vendeur
    seller_agg = data_store.groupby("Seller").agg(
        Avg_Revenue   = ("Revenue",        "mean"),  # Revenu moyen
        Avg_Margin    = ("Margin",         "mean"),  # Marge moyenne
        Avg_Sales     = ("Sales Quantity", "mean"),  # Ventes moyennes
        Avg_Customers = ("Customers",      "mean"),  # Clients moyens
        Goal_Rate     = ("Goal_Reached",   "mean")   # Taux d'atteinte des objectifs
    ).reset_index()
    return seller_agg
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Dashboard Trafic Aérien", layout="wide")

# Titre de la page
st.title("Tableau de bord du trafic aérien")
st.write("Bienvenue sur le tableau de bord interactif du trafic aérien.")

# Exemple de données simulées pour les KPI
data = {
    "vols_total": 12000,
    "aeroports_total": 400,
    "compagnies_total": 150,
    "vols_annules": 300,
    "retards_moyens": 45,  # en minutes
    "destinations_top": ["Paris", "New York", "Londres", "Tokyo", "Dubaï"]
}

# Section 1 : Affichage des KPI
st.subheader("Indicateurs de performance clés")

col1, col2, col3 = st.columns(3)
col1.metric("Nombre total de vols", data['vols_total'])
col2.metric("Nombre total d'aéroports", data['aeroports_total'])
col3.metric("Nombre total de compagnies", data['compagnies_total'])

col4, col5 = st.columns(2)
col4.metric("Vols annulés", data['vols_annules'])
col5.metric("Retard moyen (minutes)", data['retards_moyens'])

# Section 2 : Destinations les plus fréquentées
st.subheader("Top 5 des destinations les plus fréquentées")
st.write(", ".join(data['destinations_top']))

# Section 3 : Graphiques d'évolution du trafic
st.subheader("Évolution du trafic aérien")

# Simulation des données pour le graphique
traffic_data = pd.DataFrame({
    "Mois": pd.date_range("2023-01-01", periods=12, freq='M').strftime("%b %Y"),
    "Nombre de vols": [950, 1050, 1200, 1100, 1000, 1300, 1350, 1250, 1400, 1500, 1550, 1600]
})

# Utilisation de Matplotlib et Seaborn pour visualiser les données
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='Mois', y='Nombre de vols', data=traffic_data, marker='o', ax=ax)
plt.xticks(rotation=45)
plt.title("Évolution du trafic aérien (2023)", fontsize=14)

# Affichage du graphique dans Streamlit
st.pyplot(fig)

# Si tu veux ajouter plus de graphiques pour différentes périodes
st.subheader("Trafic aérien par année")
traffic_annual = pd.DataFrame({
    "Année": ["2020", "2021", "2022", "2023"],
    "Nombre de vols": [8500, 9000, 11500, 13000]
})

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(x='Année', y='Nombre de vols', data=traffic_annual, palette="Blues_d", ax=ax2)
plt.title("Nombre de vols par année", fontsize=14)

st.pyplot(fig2)

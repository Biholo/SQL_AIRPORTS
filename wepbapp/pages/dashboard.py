import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.database import Database

# Configuration de la page
st.set_page_config(page_title="Dashboard Trafic Aérien", layout="wide")

# Titre de la page
st.title("Tableau de bord du trafic aérien")
st.write("Bienvenue sur le tableau de bord interactif du trafic aérien.")

# Créer une instance de la classe Database
db = Database()

# Récupérer les données réelles depuis la base de données
try:
    vols_total = db.fetch_all("SELECT COUNT(*) FROM flights")[0][0]
    aeroports_total = db.fetch_all("SELECT COUNT(*) FROM airports")[0][0]
    compagnies_total = db.fetch_all("SELECT COUNT(*) FROM airlines")[0][0]
    vols_annules = db.fetch_all("SELECT COUNT(*) FROM flights WHERE dep_time = ''")[0][0]
    retards_moyens = db.fetch_all("SELECT AVG(dep_delay) FROM flights WHERE dep_delay IS NOT NULL")[0][0]

    destinations_top = db.fetch_all("""
    SELECT a.name AS airport_name, f.dest, d.count
    FROM (
        SELECT dest, COUNT(*) AS count
        FROM flights
        GROUP BY dest
        ORDER BY count DESC 
        LIMIT 5
    ) d
    JOIN airports a ON d.dest = a.faa
""")



    print('Vols total', vols_total)
    print('Aeroport total', aeroports_total)
    print('Companies total', compagnies_total)
    print('Vols annulée',vols_annules)
    print('Retard moyen',retards_moyens)
    print('top destination:', destinations_top)

    destinations_top = [d[0] for d in destinations_top]
except Exception as e:
    st.error(f"Erreur lors de la récupération des données : {e}")
    vols_total, aeroports_total, compagnies_total, vols_annules, retards_moyens, destinations_top = 0, 0, 0, 0, 0, []

# Section 1 : Affichage des KPI
st.subheader("Indicateurs de performance clés")

col1, col2, col3 = st.columns(3)
col1.metric("Nombre total de vols", vols_total)
col2.metric("Nombre total d'aéroports", aeroports_total)
col3.metric("Nombre total de compagnies", compagnies_total)

col4, col5 = st.columns(2)
col4.metric("Vols annulés", vols_annules)
col5.metric("Retard moyen (minutes) (quand il y a retard)", float(round(retards_moyens, 2)))

# Section 2 : Destinations les plus fréquentées
st.subheader("Top 5 des destinations les plus fréquentées")
st.write(", ".join(destinations_top))

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

# Trafic annuel
st.subheader("Trafic aérien par année")
traffic_annual = pd.DataFrame({
    "Année": ["2020", "2021", "2022", "2023"],
    "Nombre de vols": [8500, 9000, 11500, 13000]
})

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(x='Année', y='Nombre de vols', data=traffic_annual, palette="Blues_d", ax=ax2)
plt.title("Nombre de vols par année", fontsize=14)

st.pyplot(fig2)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Statistiques sur les aéroports", layout="wide")

# Titre et introduction
st.title("Statistiques sur les aéroports")
st.write("Analyse des statistiques des aéroports d'origine et de destination.")

# Exemple de données de vols (à remplacer par des données réelles)
data = pd.DataFrame({
    'origin_airport': ['JFK', 'LAX', 'SFO', 'ORD', 'MIA', 'JFK', 'LAX', 'SFO', 'ORD', 'MIA'],
    'dest_airport': ['LAX', 'JFK', 'MIA', 'SFO', 'ORD', 'LAX', 'JFK', 'MIA', 'SFO', 'ORD'],
    'company': ['United', 'American', 'Delta', 'Southwest', 'United', 'Delta', 'American', 'United', 'Southwest', 'Delta'],
    'flights': [150, 120, 110, 90, 80, 100, 130, 115, 85, 95],
    'month': ['2024-01', '2024-01', '2024-01', '2024-01', '2024-01', '2024-02', '2024-02', '2024-02', '2024-02', '2024-02'],
    'origin_airport_full': ['John F. Kennedy International', 'Los Angeles International', 'San Francisco International', 'O\'Hare International', 'Miami International',
                            'John F. Kennedy International', 'Los Angeles International', 'San Francisco International', 'O\'Hare International', 'Miami International'],
    'dest_airport_full': ['Los Angeles International', 'John F. Kennedy International', 'Miami International', 'San Francisco International', 'O\'Hare International',
                          'Los Angeles International', 'John F. Kennedy International', 'Miami International', 'San Francisco International', 'O\'Hare International']
})

# Section 1 : Indicateurs de performance (KPI)
st.subheader("Indicateurs de performance clés")

# Nombre total d'aéroports de départ et de destination
total_origin_airports = data['origin_airport'].nunique()
total_dest_airports = data['dest_airport'].nunique()

# Aéroport de départ le plus emprunté
most_used_origin_airport = data.groupby('origin_airport_full')['flights'].sum().idxmax()
most_used_origin_airport_flights = data.groupby('origin_airport_full')['flights'].sum().max()

# Affichage des KPI en colonnes
col1, col2, col3 = st.columns(3)
col1.metric("Nombre total d'aéroports de départ", total_origin_airports)
col2.metric("Nombre total d'aéroports de destination", total_dest_airports)
col3.metric(f"Aéroport le plus emprunté", most_used_origin_airport, f"{most_used_origin_airport_flights} vols")

# Section 2 : Top 10 des destinations les plus/moins populaires
st.subheader("Top 10 des destinations les plus et les moins populaires")

# Calcul des top 10 destinations
top_10_destinations = data.groupby('dest_airport_full')['flights'].sum().sort_values(ascending=False).head(10)
bottom_10_destinations = data.groupby('dest_airport_full')['flights'].sum().sort_values(ascending=True).head(10)

# Affichage des destinations les plus populaires
col1, col2 = st.columns(2)

with col1:
    st.write("### Top 10 des destinations les plus populaires")
    st.dataframe(top_10_destinations)

with col2:
    st.write("### Top 10 des destinations les moins populaires")
    st.dataframe(bottom_10_destinations)

# Section 3 : Visualisation de l'évolution du trafic par aéroport
st.subheader("Évolution du trafic par aéroport (comparaison mensuelle)")

# Calcul de la somme des vols par mois pour chaque aéroport de départ
traffic_evolution = data.groupby(['month', 'origin_airport_full'])['flights'].sum().reset_index()

# Visualisation avec Seaborn
plt.figure(figsize=(10, 6))
sns.lineplot(data=traffic_evolution, x='month', y='flights', hue='origin_airport_full', marker='o')
plt.title("Évolution du trafic par aéroport d'origine")
plt.xlabel("Mois")
plt.ylabel("Nombre de vols")
plt.xticks(rotation=45)
st.pyplot(plt)

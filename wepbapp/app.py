import streamlit as st
import pandas as pd
import pydeck as pdk

# Barre latérale pour la navigation
# Exemple de données de vols (à remplacer par des données réelles)
data = pd.DataFrame({
    'origin_lat': [40.6413, 33.9416, 37.6213, 41.9742, 25.7959],
    'origin_lon': [-73.7781, -118.4085, -122.3790, -87.9073, -80.2870],
    'dest_lat': [34.0522, 40.7128, 25.7617, 29.7604, 36.1699],
    'dest_lon': [-118.2437, -74.0060, -80.1918, -95.3698, -115.1398],
    'company': ['United', 'American', 'Delta', 'Southwest', 'United'],
    'flights': [150, 120, 110, 90, 80],
    'period': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05']
})

# Filtres pour sélectionner la compagnie et la période
selected_company = st.sidebar.selectbox("Sélectionner une compagnie aérienne", data['company'].unique())
selected_period = st.sidebar.selectbox("Sélectionner une période", data['period'].unique())

# Filtrer les données en fonction de la sélection
filtered_data = data[(data['company'] == selected_company) & (data['period'] == selected_period)]

# Préparer les données pour Pydeck
layers = pdk.Layer(
    "ArcLayer",
    data=filtered_data,
    get_source_position=["origin_lon", "origin_lat"],
    get_target_position=["dest_lon", "dest_lat"],
    get_source_color=[255, 0, 0, 160],
    get_target_color=[0, 128, 200, 160],
    auto_highlight=True,
    width_scale=0.05,
    get_width="flights / 100",  # La largeur des arcs est proportionnelle au nombre de vols
    pickable=True
)

# Configurer la vue initiale de la carte
view_state = pdk.ViewState(
    latitude=37.7749,
    longitude=-95.7129,
    zoom=3,
    pitch=50
)

# Créer la carte
st.pydeck_chart(pdk.Deck(
    layers=[layers],
    initial_view_state=view_state,
    tooltip={"text": "Nombre de vols : {flights}"}
))

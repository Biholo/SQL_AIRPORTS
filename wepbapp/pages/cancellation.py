import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Retards et Annulations de Vols", layout="wide")

# Titre de la page
st.title("Retards et Annulations de Vols")
st.write("Analyse des retards et annulations de vols par compagnie et par destination.")

# Exemple de données simulées (à remplacer par des données réelles)
n = 100  # nombre total de lignes
data = pd.DataFrame({
    'flight_number': [f'FL{str(i).zfill(4)}' for i in range(1, n + 1)],
    'company': ['United', 'American', 'Delta', 'Southwest'] * (n // 4),
    'departure_delay': [5, 10, 0, 15] * (n // 4),
    'arrival_delay': [3, 8, 2, 12] * (n // 4),
    'cancellations': [0, 1, 0, 0] * (n // 4),
    'destination': ['NYC', 'LAX', 'ORD', 'DFW'] * (n // 4),
    'flight_type': ['Long-Courrier', 'Moyen-Courrier'] * (n // 2),
})

# Section 1 : Statistiques sur les retards
st.subheader("Statistiques sur les retards à l’arrivée et au départ")

# Calcul des retards moyens
average_departure_delay = data['departure_delay'].mean()
average_arrival_delay = data['arrival_delay'].mean()

st.write(f"**Retard moyen au départ :** {average_departure_delay:.2f} minutes")
st.write(f"**Retard moyen à l’arrivée :** {average_arrival_delay:.2f} minutes")

# Section 2 : Graphiques des lignes de vols les plus touchées par les retards
st.subheader("Lignes de vols les plus touchées par les retards")

# Calcul des retards par compagnie
delays_by_company = data.groupby('company')[['departure_delay', 'arrival_delay']].mean().reset_index()

# Graphique des retards moyens par compagnie
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x='company', y='departure_delay', data=delays_by_company, ax=ax1, color='orange', label='Retard au départ')
sns.barplot(x='company', y='arrival_delay', data=delays_by_company, ax=ax1, color='blue', label='Retard à l’arrivée', alpha=0.5)
plt.title("Retards moyens par compagnie")
plt.xlabel("Compagnie")
plt.ylabel("Retard (minutes)")
plt.legend()
st.pyplot(fig1)

# Section 3 : Détails sur les vols annulés
st.subheader("Détails sur les vols annulés")

# Filtrer les vols annulés
cancellations_data = data[data['cancellations'] > 0]

# Affichage du tableau des vols annulés
if not cancellations_data.empty:
    st.write("### Vols annulés")
    st.table(cancellations_data[['flight_number', 'company', 'destination', 'cancellations']])
else:
    st.write("Aucun vol annulé.")

# Section 4 : Analyse des retards par type de vol
st.subheader("Analyse des retards par type de vol")

# Calcul des retards moyens par type de vol
delays_by_type = data.groupby('flight_type')[['departure_delay', 'arrival_delay']].mean().reset_index()

# Graphique des retards par type de vol
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x='flight_type', y='departure_delay', data=delays_by_type, ax=ax2, color='orange', label='Retard au départ')
sns.barplot(x='flight_type', y='arrival_delay', data=delays_by_type, ax=ax2, color='blue', label='Retard à l’arrivée', alpha=0.5)
plt.title("Retards moyens par type de vol")
plt.xlabel("Type de vol")
plt.ylabel("Retard (minutes)")
plt.legend()
st.pyplot(fig2)

# Section 5 : Chargement dynamique des données
st.subheader("Données complètes des retards et annulations")

# Initialiser le nombre de lignes à afficher dans session_state
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 10  # On commence par afficher 10 lignes

# Afficher un tableau avec les données limitées au nombre de lignes actuelles
st.table(data.head(st.session_state.num_rows))

# Bouton pour charger plus de données
if st.button("Charger plus de données"):
    st.session_state.num_rows += 10  # Augmenter le nombre de lignes affichées de 10

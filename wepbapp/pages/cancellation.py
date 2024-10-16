import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.database import Database

# Configuration de la page
st.set_page_config(page_title="Retards et Annulations de Vols", layout="wide")

# Titre de la page
st.title("Retards et Annulations de Vols")
st.write("Analyse des retards et annulations de vols par compagnie et par destination.")

# Créer une instance de la classe Database
db = Database()

# Récupérer les données réelles depuis la base de données
try:
    # Récupérer les informations sur les vols
    data = db.fetch_all("""
        SELECT 
            flight AS flight_number,
            carrier AS company,
            dep_delay AS departure_delay,
            arr_delay AS arrival_delay,
            dep_time,
            dest AS destination
        FROM flights
    """)

    # Convertir les données récupérées en DataFrame
    columns = ['flight_number', 'company', 'departure_delay', 'arrival_delay', 'dep_time', 'destination']
    data = pd.DataFrame(data, columns=columns)

    data['cancellations'] = data['dep_time'].isnull() | (data['dep_time'] == "")  # True si annulé, False sinon
    data['cancellations'] = data['cancellations'].astype(int)

    # Section 1 : Statistiques sur les retards
    st.subheader("Statistiques sur les retards à l’arrivée et au départ")

    average_departure_delay = data['departure_delay'].mean()
    average_arrival_delay = data['arrival_delay'].mean()

    st.write(f"**Retard moyen au départ :** {average_departure_delay:.2f} minutes")
    st.write(f"**Retard moyen à l’arrivée :** {average_arrival_delay:.2f} minutes")

    # Section 2 : Graphiques des lignes de vols les plus touchées par les retards
    st.subheader("Lignes de vols les plus touchées par les retards")

    delays_by_company = data.groupby('company')[['departure_delay', 'arrival_delay']].mean().reset_index()

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

    cancellations_data = data[data['cancellations'] > 0]

    if not cancellations_data.empty:
        st.write("### Vols annulés")
        st.table(cancellations_data[['flight_number', 'company', 'destination']])
    else:
        st.write("Aucun vol annulé.")


    # Section 4 : Chargement dynamique des données
    st.subheader("Données complètes des retards et annulations")

    if 'num_rows' not in st.session_state:
        st.session_state.num_rows = 10

    st.table(data.head(st.session_state.num_rows))

    if st.button("Charger plus de données"):
        st.session_state.num_rows += 10

except Exception as e:
    st.error(f"Erreur lors de la récupération des données : {e}")

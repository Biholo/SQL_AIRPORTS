import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.database import Database  # Importer la classe Database depuis ton fichier utils
 
# Configuration de la page
st.set_page_config(page_title="Statistiques sur les Avions", layout="wide")
 
# Connexion à la base de données en utilisant la classe Database
@st.cache_resource
def get_db_connection():
    try:
        db = Database()  # Crée une instance de la classe Database
        return db
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None
 
# Récupération des données des avions
@st.cache_data
def load_planes_data(_db):  # Utilisation de l'underscore pour éviter le hash de db
    if _db:
        try:
            query = """
            SELECT tailnum, year, type, manufacturer, model, engines, seats, speed, engine
            FROM planes
            """
            data = _db.fetch_all(query)
            df = pd.DataFrame(data, columns=['tailnum', 'year', 'type', 'manufacturer', 'model', 'engines', 'seats', 'speed', 'engine'])
            return df
        except Exception as e:
            st.error(f"Erreur lors de la récupération des données : {e}")
            return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur
    else:
        st.error("Connexion à la base de données non disponible.")
        return pd.DataFrame()
 
# Charger la connexion à la base de données
db = get_db_connection()
 
# Charger les données des avions
planes_data = load_planes_data(db)
 
# Section 1 : Affichage général des données des avions
st.subheader("Informations générales sur les avions")
 
if not planes_data.empty:
    st.write(f"Nombre total d'avions dans la base de données : {planes_data.shape[0]}")
    st.write("Voici les 10 premiers avions enregistrés :")
    st.dataframe(planes_data.head(10))
else:
    st.write("Aucune donnée disponible pour les avions.")
 
# Section 2 : Indicateurs de performance (KPI)
st.subheader("Indicateurs de performance clés pour les avions")
 
# Vérification pour éviter des erreurs sur un DataFrame vide
if not planes_data.empty:
    # Nombre total de fabricants
    total_manufacturers = planes_data['manufacturer'].nunique()
 
    # Avion le plus récent
    most_recent_plane = planes_data.loc[planes_data['year'].idxmax(), 'tailnum']
    most_recent_year = planes_data['year'].max()
 
    # Avion le plus ancien
    oldest_plane = planes_data.loc[planes_data['year'].idxmin(), 'tailnum']
    oldest_year = planes_data['year'].min()
 
    # Affichage des KPI en colonnes
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre total de fabricants", total_manufacturers)
    col2.metric(f"Avion le plus récent", most_recent_plane, f"Année {most_recent_year}")
    col3.metric(f"Avion le plus ancien", oldest_plane, f"Année {oldest_year}")
else:
    st.write("Pas assez de données pour afficher les indicateurs de performance.")
 
# Section 3 : Top 10 des fabricants d'avions
st.subheader("Top 10 des fabricants d'avions")
 
if not planes_data.empty:
    # Calcul des top 10 fabricants avec le plus d'avions
    top_10_manufacturers = planes_data['manufacturer'].value_counts().head(10)
 
    # Affichage des fabricants les plus populaires
    st.write("### Fabricants avec le plus d'avions")
    st.dataframe(top_10_manufacturers)
else:
    st.write("Aucune donnée de fabricant disponible.")
 
# Section 4 : Distribution du nombre de sièges
st.subheader("Distribution du nombre de sièges des avions")
 
if not planes_data.empty and 'seats' in planes_data.columns:
    # Histogramme de la distribution du nombre de sièges
    plt.figure(figsize=(10, 6))
    sns.histplot(planes_data['seats'], bins=30, kde=True)
    plt.title("Distribution du nombre de sièges")
    plt.xlabel("Nombre de sièges")
    plt.ylabel("Nombre d'avions")
    st.pyplot(plt)
else:
    st.write("Aucune donnée sur le nombre de sièges disponible.")
 
# Section 5 : Répartition du type d'avion (Type d'avion et moteur)
st.subheader("Répartition du type d'avions et type de moteurs")
 
if not planes_data.empty:
    # Répartition des types d'avions
    type_count = planes_data['type'].value_counts()
    engine_count = planes_data['engine'].value_counts()
 
    # Affichage de la répartition
    col1, col2 = st.columns(2)
 
    with col1:
        st.write("### Répartition par type d'avion")
        st.bar_chart(type_count)
 
    with col2:
        st.write("### Répartition par type de moteur")
        st.bar_chart(engine_count)
else:
    st.write("Aucune donnée sur le type d'avions disponible.")
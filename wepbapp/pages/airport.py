import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.database import Database 

st.set_page_config(page_title="Statistiques sur les aéroports", layout="wide")
 
@st.cache_resource
def get_db_connection():
    try:
        db = Database()
        return db
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None
 
@st.cache_data
def load_airport_data(_db):
    if _db:
        try:
            query = """
            SELECT faa, name, lat, lon, alt, tz, dst, tzone
            FROM airports
            """
            data = _db.fetch_all(query)
            df = pd.DataFrame(data, columns=['faa', 'name', 'lat', 'lon', 'alt', 'tz', 'dst', 'tzone'])
            return df
        except Exception as e:
            st.error(f"Erreur lors de la récupération des données : {e}")
            return pd.DataFrame()
    else:
        st.error("Connexion à la base de données non disponible.")
        return pd.DataFrame()
 
db = get_db_connection()
 
airport_data = load_airport_data(db)
 
# Section 1 : Affichage général des données des aéroports
st.subheader("Informations générales sur les aéroports")
 
if not airport_data.empty:
    st.write(f"Nombre total d'aéroports dans la base de données : {airport_data.shape[0]}")
    st.write("Voici les 10 premiers aéroports enregistrés :")
    st.dataframe(airport_data.head(10))
else:
    st.write("Aucune donnée disponible pour les aéroports.")
 
# Section 2 : Indicateurs de performance (KPI)
st.subheader("Indicateurs de performance clés pour les aéroports")
 
if not airport_data.empty:
    total_timezones = airport_data['tz'].nunique()
 
    highest_altitude_airport = airport_data.loc[airport_data['alt'].idxmax(), 'name']
    highest_altitude_value = airport_data['alt'].max()
 
    lowest_altitude_airport = airport_data.loc[airport_data['alt'].idxmin(), 'name']
    lowest_altitude_value = airport_data['alt'].min()
 
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre total de fuseaux horaires", total_timezones)
    col2.metric(f"Aéroport avec la plus grande altitude", highest_altitude_airport, f"{highest_altitude_value} pieds")
    col3.metric(f"Aéroport avec la plus faible altitude", lowest_altitude_airport, f"{lowest_altitude_value} pieds")
else:
    st.write("Pas assez de données pour afficher les indicateurs de performance.")
 
# Section 3 : Top 10 des aéroports par fuseau horaire
st.subheader("Top 10 des fuseaux horaires les plus populaires")
 
if not airport_data.empty:
    top_10_timezones = airport_data['tz'].value_counts().head(10)
 
    st.write("### Fuseaux horaires avec le plus d'aéroports")
    st.dataframe(top_10_timezones)
else:
    st.write("Aucune donnée de fuseau horaire disponible.")
 
# Section 4 : Carte des aéroports
st.subheader("Localisation géographique des aéroports")
 
if not airport_data.empty and 'lat' in airport_data.columns and 'lon' in airport_data.columns:
    st.map(airport_data[['lat', 'lon']])
else:
    st.write("Aucune donnée de localisation disponible.")
 

if not airport_data.empty:
    dst_count = airport_data['dst'].value_counts()
 
    st.write("### Nombre d'aéroports par type de DST")
    st.bar_chart(dst_count)
else:
    st.write("Aucune donnée DST disponible.")
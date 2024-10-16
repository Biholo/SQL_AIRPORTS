import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Statistiques sur les compagnies aériennes", layout="wide")

# Titre de la page
st.title("Statistiques sur les compagnies aériennes")
st.write("Analyse des performances des compagnies aériennes en termes de vols et de destinations desservies.")

# Exemple de données simulées (à remplacer par des données réelles)
data = pd.DataFrame({
    'company': ['United', 'American', 'Delta', 'Southwest', 'United', 'American', 'Delta', 'Southwest'] * 50,
    'destinations': [25, 30, 20, 22, 26, 31, 21, 23] * 50,
    'flights': [150, 180, 120, 130, 155, 185, 125, 135] * 50,
    'delays': [10, 15, 5, 8, 12, 18, 7, 9] * 50,
    'cancellations': [3, 2, 4, 1, 2, 3, 2, 1] * 50,
    'month': ['2024-01', '2024-01', '2024-01', '2024-01', '2024-02', '2024-02', '2024-02', '2024-02'] * 50
})

# Initialiser le nombre de lignes à afficher dans session_state
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 10  # On commence par afficher 10 lignes

# Section 1 : Nombre de destinations desservies par chaque compagnie
st.subheader("Nombre de destinations par compagnie aérienne")

# Calcul du nombre total de destinations desservies par chaque compagnie
company_destinations = data.groupby('company')['destinations'].max().reset_index()

# Affichage du tableau des destinations
st.table(company_destinations.rename(columns={"company": "Compagnie", "destinations": "Nombre de destinations"}))

# Section 2 : Tableau des données avec bouton pour charger plus de lignes
st.subheader("Données complètes des compagnies aériennes")

# Afficher un tableau avec les données limitées au nombre de lignes actuelles
st.table(data.head(st.session_state.num_rows))

# Bouton pour charger plus de données
if st.button("Charger plus de données"):
    st.session_state.num_rows += 10  # Augmenter le nombre de lignes affichées de 10

# Section 3 : Compagnies qui desservent toutes les destinations ou certaines seulement
st.subheader("Compagnies desservant toutes les destinations ou certaines seulement")

# On suppose ici que le nombre de destinations total est 31
total_destinations = 31
company_full_coverage = company_destinations[company_destinations['destinations'] == total_destinations]
company_partial_coverage = company_destinations[company_destinations['destinations'] < total_destinations]

col5, col6 = st.columns(2)

with col5:
    st.write("### Compagnies desservant toutes les destinations")
    if not company_full_coverage.empty:
        st.table(company_full_coverage.rename(columns={"company": "Compagnie", "destinations": "Nombre de destinations"}))
    else:
        st.write("Aucune compagnie ne dessert toutes les destinations.")

with col6:
    st.write("### Compagnies desservant seulement certaines destinations")
    if not company_partial_coverage.empty:
        st.table(company_partial_coverage.rename(columns={"company": "Compagnie", "destinations": "Nombre de destinations"}))
    else:
        st.write("Toutes les compagnies desservent toutes les destinations.")

# Section 4 : Graphiques de comparaison des performances des compagnies (retards, annulations)
st.subheader("Comparaison des performances des compagnies aériennes")

# Graphique 1 : Nombre de retards par compagnie
st.write("### Nombre de retards par compagnie")

# Calcul des retards par compagnie
delays_data = data.groupby('company')['delays'].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(6, 4))
sns.barplot(x='company', y='delays', data=delays_data, ax=ax1)
plt.title("Nombre total de retards par compagnie")
plt.xlabel("Compagnie")
plt.ylabel("Nombre de retards")
st.pyplot(fig1)

# Graphique 2 : Nombre d'annulations par compagnie
st.write("### Nombre d'annulations par compagnie")

# Calcul des annulations par compagnie
cancellations_data = data.groupby('company')['cancellations'].sum().reset_index()

fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(x='company', y='cancellations', data=cancellations_data, ax=ax2)
plt.title("Nombre total d'annulations par compagnie")
plt.xlabel("Compagnie")
plt.ylabel("Nombre d'annulations")
st.pyplot(fig2)

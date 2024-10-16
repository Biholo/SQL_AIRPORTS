# utils/database.py

import mysql.connector
import os
from mysql.connector import Error

class Database:
    def __init__(self):
        """Initialise la connexion à la base de données lors de la création de l'objet"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            if self.connection.is_connected():
                print("Connexion réussie à la base de données MySQL")
        except Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        """Exécuter une requête SQL (INSERT, UPDATE, DELETE)"""
        if self.connection is None:
            print("Connexion non disponible")
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print("Requête exécutée avec succès")
        except Error as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Exécuter une requête SELECT et retourner tous les résultats"""
        if self.connection is None:
            print("Connexion non disponible")
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return []
        finally:
            cursor.close()

    def close_connection(self):
        """Fermer la connexion à la base de données"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connexion MySQL fermée")

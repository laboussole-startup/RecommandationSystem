import os
import csv
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy.orm import sessionmaker
from recommendation.model import Filiere,Faculte,metiers,Universite
from core.config import CSV_FILE_PATH
from core.database import get_db
from sqlalchemy.orm import joinedload

# Chemin du fichier CSV
CSV_FILE_PATH = 'data.csv'

def fetch_data_and_save_to_csv():
    with get_db() as db:
        # Utilisation de joinedload pour éviter les boucles multiples et les jointures incorrectes
        results = db.query(Filiere, Faculte, Universite.ville,Universite.pays,Universite.logo,Universite.nom,Universite.universite_id) \
                     .join(Faculte, Filiere.faculte_id == Faculte.faculte_id) \
                     .join(Universite, Faculte.universite_id == Universite.universite_id) \
                     .all()

        # Récupérer les noms des colonnes de chaque table
        filiere_columns = [column.name for column in Filiere.__table__.columns]
        faculte_columns = [column.name for column in Faculte.__table__.columns]

        # Ajouter la colonne 'ville' spécifiquement
        universite_columns = ['ville', 'pays','logo','nom',"universite_id"]

        # Écrire les résultats dans un fichier CSV
        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Écrire les en-têtes de colonnes
            writer.writerow(filiere_columns + faculte_columns + universite_columns)
            # Écrire les lignes de données
            for filiere, faculte, ville ,pays,nom,logo,universite_id in results:
                filiere_values = [getattr(filiere, column) for column in filiere_columns]
                faculte_values = [getattr(faculte, column) for column in faculte_columns]
                universite_values = [ville,pays,nom,logo,universite_id]  # Ajoutez la ville seule
                writer.writerow(filiere_values + faculte_values + universite_values)

    # Ajouter un message de debug pour vérifier que le fichier a été créé
    if os.path.exists(CSV_FILE_PATH):
        print("a été créé avec succès.")
    else:
        print("Erreur : Le fichier CSV  n'a pas été trouvé.")




def load_metiers_data():
    with get_db() as db:
        results = db.query(metiers).all()
        
        # Convert SQLAlchemy results to DataFrame
        metiers_data = []
        for result in results:
            metier_dict = {column.name: getattr(result, column.name) for column in metiers.__table__.columns}
            metiers_data.append(metier_dict)
        
        df = pd.DataFrame(metiers_data)
        return df
    

    



def fetch_data_and_save_to_df():
    
    try:
        fetch_data_and_save_to_csv()
        # Utilisation de pandas pour lire le fichier CSV
        df = pd.read_csv(CSV_FILE_PATH)

        return df
    except FileNotFoundError:
        print(f"Erreur : Le fichier {CSV_FILE_PATH} n'a pas été trouvé")

    except pd.errors.EmptyDataError:
        print(f"Erreur : Aucune colonne à analyser dans le fichier {CSV_FILE_PATH}")

    except Exception as e:
        print(f"Erreur inattendue lors de la lecture du fichier CSV : {str(e)}")




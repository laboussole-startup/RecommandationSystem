import os
import csv
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy.orm import sessionmaker
from recommendation.model import Filiere,Faculte,metiers
from core.config import CSV_FILE_PATH
from core.database import get_db
from sqlalchemy.orm import joinedload
# Chemin du fichier CSV
CSV_FILE_PATH = 'formations_with_centres_interet.csv'

SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def get_last_update_time():
    if os.path.exists(CSV_FILE_PATH):
        # Récupérer la date de modification du fichier CSV
        modification_time = datetime.fromtimestamp(os.path.getmtime(CSV_FILE_PATH))
        return modification_time
    else:
        return None

def save_last_update_time(update_time):

    #Enregistrer la date et l'heure de la dernière mise à jour dans le fichier
    with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Last Update Time', update_time])





def fetch_data_and_save_to_csv():
    with get_db() as db:
        # Query to join Faculte and Filiere tables
        results = db.query(Filiere, Faculte).join(Faculte, Filiere.faculte_id == Faculte.faculte_id).all()

        # Get column names from both tables
        filiere_columns = [column.name for column in Filiere.__table__.columns]
        faculte_columns = [column.name for column in Faculte.__table__.columns]

        # Write results to a CSV file
        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write column headers
            writer.writerow(filiere_columns + faculte_columns)
            # Write data rows
            for filiere, faculte in results:
                filiere_values = [getattr(filiere, column) for column in filiere_columns]
                faculte_values = [getattr(faculte, column) for column in faculte_columns]
                writer.writerow(filiere_values + faculte_values)


CSV_FILE_PATH = 'metiers_data.csv'
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
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import desc, func
from sqlalchemy.orm import sessionmaker
from recommendation.model import Filiere,Faculte, Recherches,metiers,Universite
from core.config import CSV_FILE_PATH
from core.database import get_db
from sqlalchemy.orm import joinedload



# Chemin du fichier CSV
CSV_FILE_PATH = 'data.csv'

# def fetch_data_and_save_to_csv():
#     with get_db() as db:
#         # Utilisation de joinedload pour éviter les boucles multiples et les jointures incorrectes
#         results = db.query(Filiere, Faculte, Universite.ville,Universite.pays,Universite.logo,Universite.nom,Universite.universite_id) \
#                      .join(Faculte, Filiere.faculte_id == Faculte.faculte_id) \
#                      .join(Universite, Faculte.universite_id == Universite.universite_id) \
#                      .all()

#         # Récupérer les noms des colonnes de chaque table
#         filiere_columns = [column.name for column in Filiere.__table__.columns]
#         faculte_columns = [column.name for column in Faculte.__table__.columns]

#         # Ajouter la colonne 'ville' spécifiquement
#         universite_columns = ['ville', 'pays','logo','nom',"universite_id"]

#         # Écrire les résultats dans un fichier CSV
#         with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             # Écrire les en-têtes de colonnes
#             writer.writerow(filiere_columns + faculte_columns + universite_columns)
#             # Écrire les lignes de données
#             for filiere, faculte, ville ,pays,nom,logo,universite_id in results:
#                 filiere_values = [getattr(filiere, column) for column in filiere_columns]
#                 faculte_values = [getattr(faculte, column) for column in faculte_columns]
#                 universite_values = [ville,pays,nom,logo,universite_id]  # Ajoutez la ville seule
#                 writer.writerow(filiere_values + faculte_values + universite_values)

#     # Ajouter un message de debug pour vérifier que le fichier a été créé
#     if os.path.exists(CSV_FILE_PATH):
#         print("a été créé avec succès.")
#     else:
#         print("Erreur : Le fichier CSV  n'a pas été trouvé.")





def load_data():
    with get_db() as db:
        # Utilisation de joinedload pour éviter les boucles multiples et les jointures incorrectes
        results = db.query(Filiere, Faculte, Universite.ville, Universite.pays, Universite.logo, Universite.nom, Universite.universite_id) \
                     .join(Faculte, Filiere.faculte_id == Faculte.faculte_id) \
                     .join(Universite, Faculte.universite_id == Universite.universite_id) \
                     .options(joinedload(Filiere.faculte).joinedload(Faculte.universite)) \
                     .all()
        
        # Convert SQLAlchemy results to DataFrame
        formation_data = []
        for result in results:
            filiere, faculte, ville, pays, logo, nom, universite_id = result
            data_dict = {
                'filiere_id': filiere.filieres_id,
                'filiere_nom': filiere.nom,
                'filiere_descriptif': filiere.descriptif,
                'filiere_duree': filiere.duree,
                'filiere_cout': filiere.cout,
                'filiere_langue_enseignement': filiere.langue_enseignement,
                'filiere_diplome_delivre': filiere.diplome_delivre,
                'filiere_images_pc': filiere.images_pc,
                'filiere_images_telephone': filiere.images_telephone,
                'filiere_images_tablettes': filiere.images_tablettes,
                'filiere_centre_interet': filiere.centre_interet,
                'faculte_id': faculte.faculte_id,
                'faculte_nom': faculte.nom,
                'faculte_descriptif': faculte.descriptif,
                'faculte_condition_admission': faculte.condition_admission,
                'faculte_email': faculte.email,
                'faculte_telephone': faculte.telephone,
                'faculte_images_pc': faculte.images_pc,
                'faculte_images_telephone': faculte.images_telephone,
                'faculte_images_tablettes': faculte.images_tablettes,
                'universite_ville': ville,
                'universite_pays': pays,
                'universite_logo': logo,
                'universite_nom': nom,
                'universite_id': universite_id
            }
            formation_data.append(data_dict)
        
        df = pd.DataFrame(formation_data)
        return df

    

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
    




def load_search_history_as_string():
    try:
        with get_db() as db:
            # Sous-requête pour obtenir les cinq dernières recherches de chaque utilisateur
            subquery = db.query(
                Recherches.id_utilisateur,
                Recherches.id,
                Recherches.mots_cles,
                Recherches.date_heure,
                func.row_number().over(
                    partition_by=Recherches.id_utilisateur,
                    order_by=desc(Recherches.date_heure)
                ).label('row_num')
            ).subquery()

            # Filtrer les résultats pour ne garder que les cinq dernières recherches par utilisateur
            filtered_subquery = db.query(subquery).filter(subquery.c.row_num <= 5).subquery()

            # Requête principale
            results = db.query(
                filtered_subquery.c.id_utilisateur,
                filtered_subquery.c.mots_cles,
                filtered_subquery.c.date_heure
            ).order_by(filtered_subquery.c.id_utilisateur, filtered_subquery.c.date_heure.desc()).all()

            # Construction de la chaîne de caractères
            search_history_string = ""
            for result in results:
                search_history_string += f"{result.mots_cles}"

            return search_history_string



    except Exception as e:
        return f"Erreur lors du chargement de l'historique de recherche : {e}"

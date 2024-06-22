from fastapi import APIRouter, Query
from pydantic import BaseModel
import numpy as np
from joblib import load

router_orientation = APIRouter()

# Chargement du modèle
load_model = load("model_orientation/orientation.joblib")

# Définition de la structure des données d'entrée
class InputData(BaseModel):
    Sexe: str
    Age: int
    Baccalaureat: str
    Math: int
    Science: int
    Langues: int
    Informatique: int
    Intérêt_Science: int
    Intérêt_Langue: int
    Note_Moyenne: float
    Projets_Personnels: str
    Facteur_Socioéconomique: str
    Passion_1: str
    Passion_2: str

# Endpoint pour la prédiction

@router_orientation.post("/Orrientation_academique")
def orrientation(Sexe: str = Query(..., min_length=1), Projets_Personnels: str = Query(..., min_length=1), Age: str = Query(..., min_length=1), Baccalaureat: str = Query(..., min_length=1), Math: str = Query(..., min_length=1), Science: str = Query(..., min_length=1), Langues: str = Query(..., min_length=1), Informatique: str = Query(..., min_length=1), Intérêt_Science: str = Query(..., min_length=1), Intérêt_Langue: str = Query(..., min_length=1), Note_Moyenne: str = Query(..., min_length=1),Facteur_Socioéconomique: str = Query(..., min_length=1), Passion_1: str = Query(..., min_length=1), Passion_2: str = Query(..., min_length=1)):

    # Conversion des données catégorielles
    Sexe = 0 if Sexe == 'M' else 1
    Baccalaureat = 0 if Baccalaureat == 'L' else 1
    Projets_Personnels = {'Agriculture': 0, 'Medécine': 1, 'Informatique': 2, 'Education': 3}.get(Projets_Personnels)
    Facteur_Socioéconomique = {'Faible': 0, 'Moyen': 1, 'Élevé': 2}.get(Facteur_Socioéconomique)
    Passion_1 = {'Science': 0, 'Agriculture': 1, 'Programmation': 2, 'Jeux vidéo': 3, 'IA': 4, 'Art': 5, 'Medécine': 6}.get(Passion_1)
    Passion_2 = {'Science': 0, 'Agriculture': 1, 'Programmation': 2, 'Jeux vidéo': 3, 'IA': 4, 'Art': 5, 'Medécine': 6}.get(Passion_2)
    

    
    # Préparation des données pour la prédiction
    new_data = np.array([Sexe, Age, Baccalaureat, Math, Science, Langues, Informatique, Intérêt_Science, Intérêt_Langue, Note_Moyenne, Projets_Personnels, Facteur_Socioéconomique, Passion_1, Passion_2]).reshape(1, -1)
    
    # Prédiction
    case_idx = load_model.predict(new_data)[0]
    
     # Mapping des index prédits à des labels explicites
    orientation_label = {
        0: 'Agriculteure',
        1: 'Médecin',
        2: 'Informaticient'
    }
    
    # Renvoyer la prédiction sous forme de dictionnaire JSON
    return {"orientation": orientation_label[case_idx]}


import re
from typing import Dict, List, Union
from datetime import datetime, timedelta
from recommendation.load_data import fetch_data_and_save_to_df #,fetch_data_and_save_to_csv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel




df=fetch_data_and_save_to_df()
CSV_FILE_PATH = 'data.csv'

# Charger les données à partir du fichier CSV


df.drop(df.index[-1], inplace=True)  # Supprimer la dernière ligne (potentiellement vide)

# Fonction de prétraitement pour mettre le texte en minuscules
def preprocess(text):
    text = str(text)
    text = text.lower()
    return text

# Combinaison de colonnes pour former une colonne de texte à vectoriser
df["descriptions_and_caracteristiques"] = df["descriptif"] + " " + df["nom"] + " " + df["nom.1"] + " " + df["descriptif.1"]+""+df["condition_admission"]

# Initialisation du vectoriseur TF-IDF et transformation des descriptions et caractéristiques
vectorizer = TfidfVectorizer()
descriptions_and_caracteristiques_tfidf = vectorizer.fit_transform(df["descriptions_and_caracteristiques"].apply(preprocess))
# Initialisation du vectoriseur TF-IDF et transformation des condition d'adminssion
vectorizer_condition_admission = TfidfVectorizer()
condition_dadmission_tfidf = vectorizer_condition_admission.fit_transform(df["condition_admission"].apply(preprocess))
vectorizer_pays = TfidfVectorizer()
vectorizer_pays_tfidf = vectorizer_pays.fit_transform(df["pays"].apply(preprocess))

# Fonction de recommandation de cours
def recommend_courses(user_interests: List[str], pays_utilisateur: str, historique_recherche_utilisateur: List[str], user_diplome: str, page: int = 1, page_size: int = 10, interest_weight: float = 1.5, history_weight: float = 1.0) -> List[Dict[str, Union[str, float]]]:
    # Prétraitement des centres d'intérêt de l'utilisateur
    user_interests = preprocess(" ".join(user_interests))
    
    # Prétraitement et vectorisation de l'historique de recherche de l'utilisateur
    historique_recherche_utilisateur_vectortfidf = vectorizer.transform([" ".join(historique_recherche_utilisateur)])
    
    # Prétraitement et vectorisation du pays de l'utilisateur
    pays_vectortfidf = vectorizer_pays.transform([preprocess(pays_utilisateur)])
    
    # Prétraitement et vectorisation du diplôme de l'utilisateur
    user_diplome_diplometfidf = vectorizer_condition_admission.transform([preprocess(user_diplome)])

    # Vectorisation des centres d'intérêt de l'utilisateur
    user_vectortfidf = vectorizer.transform([user_interests])

    # Calcul des scores de similarité cosinus entre le pays de l'utilisateur et les pays des universités
    cosine_scores_pays = linear_kernel(pays_vectortfidf, vectorizer_pays_tfidf).flatten()

    # Calcul des scores de similarité cosinus entre les centres d'intérêt de l'utilisateur et les descriptions des cours
    cosine_scores = linear_kernel(user_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()
    
    # Calcul des scores de similarité cosinus entre l'historique de recherche et les descriptions des cours
    similarite_historique_recherche = linear_kernel(historique_recherche_utilisateur_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()

    # Calcul des scores de similarité cosinus entre le diplôme de l'utilisateur et les conditions d'admission
    cosine_scores_diplome_user = linear_kernel(user_diplome_diplometfidf, condition_dadmission_tfidf).flatten()
    
    # Combinaison des scores de similarité en pondérant davantage les centres d'intérêt
    combined_scores = (interest_weight * cosine_scores) + (history_weight * similarite_historique_recherche) + cosine_scores_diplome_user + cosine_scores_pays
    
    # Triage des indices des cours en fonction des scores combinés en ordre décroissant
    similar_indices = combined_scores.argsort()[::-1]
    
    # Récupération des données des cours recommandés
    recommended_courses_data = df.iloc[similar_indices]
    
    # Conversion des données en une liste de dictionnaires
    recommended_courses = []
    for _, row in recommended_courses_data.iterrows():
        course_dict = {}
        for column, value in row.items():
            course_dict[column] = value
        recommended_courses.append(course_dict)
    
    # Remplacement des valeurs NaN par une valeur par défaut (0.0)
    for course in recommended_courses:
        for key, value in course.items():
            if isinstance(value, float) and np.isnan(value):
                course[key] = 0.0

    # Implémentation de la pagination
    start_index = (page - 1) * page_size  # Calcul de l'index de début
    end_index = start_index + page_size  # Calcul de l'index de fin
    paginated_courses = recommended_courses[start_index:end_index]  # Extraction de la sous-liste correspondant à la page
    
    return paginated_courses

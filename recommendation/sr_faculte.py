import re
from typing import Dict, List, Union
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from recommendation.load_data import load_data

# Fonction de prétraitement pour convertir le texte en minuscules
def preprocess(text):
    text = str(text)
    text = text.lower()
    return text

try:
    # Charger les données depuis une source externe
    df = load_data()
  
    # Supprimer la dernière ligne (potentiellement vide)
    df.drop(df.index[-1], inplace=True)
    
    # Combinaison de colonnes pour former une colonne de texte à vectoriser
    df["descriptions_and_caracteristiques"] = df["filiere_descriptif"] + " " + df["filiere_nom"] + " " + df["faculte_nom"] + " " + df["faculte_descriptif"]

    # Initialisation du vectoriseur TF-IDF et transformation des descriptions et caractéristiques
    vectorizer = TfidfVectorizer()
    descriptions_and_caracteristiques_tfidf = vectorizer.fit_transform(df["descriptions_and_caracteristiques"].apply(preprocess))

    # Initialisation du vectoriseur TF-IDF et transformation des conditions d'admission
    vectorizer_condition_admission = TfidfVectorizer()
    condition_dadmission_tfidf = vectorizer_condition_admission.fit_transform(df["faculte_condition_admission"].apply(preprocess))

    # Initialisation du vectoriseur TF-IDF et transformation des pays
    vectorizer_pays = TfidfVectorizer()
    vectorizer_pays_tfidf = vectorizer_pays.fit_transform(df["universite_pays"].apply(preprocess))

except Exception as e:
    print(f"Erreur lors du chargement des données : {e}")

def faculty_recommendation(user_interests: List[str] = None, pays_utilisateur: str = None, historique_recherche_utilisateur: List[str] = None, user_diplome: str = None, page: int = 1, page_size: int = 10, interest_weight: float = 1.5, history_weight: float = 1.0) -> List[Dict[str, Union[str, float]]]:
    try:
        # Prétraitement et vectorisation des centres d'intérêt de l'utilisateur
        if user_interests:
            user_interests = preprocess(" ".join(user_interests))
            user_vectortfidf = vectorizer.transform([user_interests])
            cosine_scores = linear_kernel(user_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()
        else:
            # Si les centres d'intérêt ne sont pas fournis, initialiser les scores à zéro
            cosine_scores = np.zeros(descriptions_and_caracteristiques_tfidf.shape[0])

        # Prétraitement et vectorisation de l'historique de recherche de l'utilisateur
        if historique_recherche_utilisateur:
            historique_recherche_utilisateur_vectortfidf = vectorizer.transform([" ".join(historique_recherche_utilisateur)])
            similarite_historique_recherche = linear_kernel(historique_recherche_utilisateur_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()
        else:
            # Si l'historique de recherche n'est pas fourni, initialiser les scores à zéro
            similarite_historique_recherche = np.zeros(descriptions_and_caracteristiques_tfidf.shape[0])

        # Prétraitement et vectorisation du pays de l'utilisateur
        if pays_utilisateur:
            pays_vectortfidf = vectorizer_pays.transform([preprocess(pays_utilisateur)])
            cosine_scores_pays = linear_kernel(pays_vectortfidf, vectorizer_pays_tfidf).flatten()
        else:
            # Si le pays n'est pas fourni, initialiser les scores à zéro
            cosine_scores_pays = np.zeros(vectorizer_pays_tfidf.shape[0])

        # Prétraitement et vectorisation du diplôme de l'utilisateur
        if user_diplome:
            user_diplome_diplometfidf = vectorizer_condition_admission.transform([preprocess(user_diplome)])
            cosine_scores_diplome_user = linear_kernel(user_diplome_diplometfidf, condition_dadmission_tfidf).flatten()
        else:
            # Si le diplôme n'est pas fourni, initialiser les scores à zéro
            cosine_scores_diplome_user = np.zeros(condition_dadmission_tfidf.shape[0])

        # Combinaison des scores de similarité en pondérant davantage les centres d'intérêt
        combined_scores = (interest_weight * cosine_scores) + (history_weight * similarite_historique_recherche) + cosine_scores_diplome_user + cosine_scores_pays
        
        # Triage des indices des cours en fonction des scores combinés en ordre décroissant
        similar_indices = combined_scores.argsort()[::-1]
        
        # Récupération des données des cours recommandés
        recommended_courses_data = df.iloc[similar_indices]

        # Colonnes à inclure dans les résultats
        columns_to_include = ["faculte_id", "faculte_nom", "faculte_descriptif", "faculte_condition_admission", "faculte_email", "faculte_telephone", "faculte_images_pc", "faculte_images_telephone", "faculte_images_tablettes", "universite_id"]

        # Conversion des données en une liste de dictionnaires en incluant seulement les colonnes spécifiées
        recommended_courses = []
        seen_courses = set()  # Ensemble pour suivre les identifiants uniques des cours
        for _, row in recommended_courses_data.iterrows():
            course_id = row["faculte_id"]
            if course_id not in seen_courses:
                course_info = {column: row[column] if column in row else None for column in columns_to_include}
                recommended_courses.append(course_info)
                seen_courses.add(course_id)  # Ajouter l'identifiant du cours à l'ensemble pour éviter les doublons

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

    except Exception as e:
        print(f"Erreur lors de la recommandation des cours: {e}")
        return []

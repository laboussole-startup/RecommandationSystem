import re
from typing import Dict, List, Union
from datetime import datetime, timedelta
from recommendation.load_data import load_data
from recommendation.prepocess import preprocess
from recommendation.load_data import load_search_history_as_string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Définir la fonction preprocess (voir ci-dessus)
# ...

try:
    # Charger les données depuis une source externe
    df = load_data()
except Exception as e:
    print(f"Erreur lors du chargement des données de formations: {e}")


try:
    # Charger les données depuis une source externe
    rechers_users = load_search_history_as_string()
    print(rechers_users)
except Exception as e:
    print(f"Erreur lors du chargement des données de l'historique de recherche: {e}")



try:
    # Combinaison de colonnes pour former une colonne de texte à vectoriser
    df["descriptions_and_caracteristiques"] = df["filiere_descriptif"] + " " + df["filiere_nom"] + " " + df["faculte_nom"] + " " + df["faculte_descriptif"]

    # Prétraitement des descriptions et caractéristiques
    df["descriptions_and_caracteristiques"] = df["descriptions_and_caracteristiques"].apply(preprocess)

    # Prétraitement des conditions d'admission
    df["faculte_condition_admission"] = df["faculte_condition_admission"].apply(preprocess)

    # Prétraitement des pays
    df["universite_pays"] = df["universite_pays"].apply(preprocess)

    # Initialisation du vectoriseur TF-IDF et transformation des descriptions et caractéristiques
    vectorizer = TfidfVectorizer()
    descriptions_and_caracteristiques_tfidf = vectorizer.fit_transform(df["descriptions_and_caracteristiques"])

except Exception as e:
    print(f"Erreur lors du chargement et du traitement des données: {e}")



def formations_recommandation_populaire(page: int = 1, page_size: int = 10,  history_weight: float = 2.0) -> List[Dict[str, Union[str, float]]]:
    try:
        # Prétraitement et vectorisation des centres d'intérêt de l'utilisateur
        if rechers_users:
            rechers_users = preprocess(" ".join(rechers_users))
            user_vectortfidf = vectorizer.transform([rechers_users])
            cosine_scores = linear_kernel(user_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()
        else:
            # Si les centres d'intérêt ne sont pas fournis, initialiser les scores à zéro
            cosine_scores = np.zeros(descriptions_and_caracteristiques_tfidf.shape[0])

       
        # Combinaison des scores de similarité en pondérant davantage les centres d'intérêt
        combined_scores = cosine_scores
        
        # Triage des indices des cours en fonction des scores combinés en ordre décroissant
        similar_indices = combined_scores.argsort()[::-1]
        
        # Récupération des données des cours recommandés
        recommended_formation_data = df.iloc[similar_indices]

        # Colonnes à inclure dans les résultats
        columns_to_include = ["filiere_id", "filiere_nom", "filiere_descriptif", "filiere_email", "filiere_telephone", "filiere_images_pc", "filiere_images_telephone", "filiere_images_tablettes", "faculte_id"]

        # Conversion des données en une liste de dictionnaires en incluant seulement les colonnes spécifiées
        recommended_courses = []
        seen_courses = set()  # Ensemble pour suivre les identifiants uniques des cours
        for _, row in recommended_formation_data.iterrows():
            course_id = row["filiere_id"]
            if course_id not in seen_courses:
                course_info = {column: row[column] if column in row else None for column in columns_to_include}
                recommended_courses.append(course_info)
                seen_courses.add(course_id)  # Ajouter l'identifiant du cours à l'ensemble pour éviter les doublons
        
        # Remplacer les valeurs NaN par une valeur par défaut (0.0)
        for metier in recommended_courses:
            for key, value in metier.items():
                if isinstance(value, float) and np.isnan(value):
                    metier[key] = 0.0

        # Implémentation de la pagination
        start_index = (page - 1) * page_size  # Calcul de l'index de début
        end_index = start_index + page_size  # Calcul de l'index de fin
        paginated_courses = recommended_courses[start_index:end_index]  # Extraction de la sous-liste correspondant à la page

        return paginated_courses

    except Exception as e:
        print(f"Erreur lors de la recommandation des cours: {e}")
        return []

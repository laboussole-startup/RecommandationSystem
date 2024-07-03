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

# Charger les données
try:
    df = load_data()
except Exception as e:
    print(f"Erreur lors du chargement des données de formations: {e}")

# Charger et traiter l'historique des recherches
try:
    rechers_users = load_search_history_as_string()
    if "Erreur" in rechers_users:
        rechers_users = ""
    print(rechers_users)
except Exception as e:
    print(f"Erreur lors du chargement des données de l'historique de recherche: {e}")
    rechers_users = ""

# Prétraiter les données
try:
    df["descriptions_and_caracteristiques"] = df["filiere_descriptif"] + " " + df["filiere_nom"] + " " + df["faculte_nom"] + " " + df["faculte_descriptif"]
    df["descriptions_and_caracteristiques"] = df["descriptions_and_caracteristiques"].apply(preprocess)
    df["faculte_condition_admission"] = df["faculte_condition_admission"].apply(preprocess)
    df["universite_pays"] = df["universite_pays"].apply(preprocess)

    vectorizer = TfidfVectorizer()
    descriptions_and_caracteristiques_tfidf = vectorizer.fit_transform(df["descriptions_and_caracteristiques"])
except Exception as e:
    print(f"Erreur lors du chargement et du traitement des données: {e}")

# Fonction de recommandation
def formations_recommandation_populaire(page: int = 1, page_size: int = 10, history_weight: float = 2.0) -> List[Dict[str, Union[str, float]]]:
    try:
        if rechers_users:
            rechers_users_processed = preprocess(rechers_users)
            user_vectortfidf = vectorizer.transform([rechers_users_processed])
            cosine_scores = linear_kernel(user_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()
        else:
            cosine_scores = np.zeros(descriptions_and_caracteristiques_tfidf.shape[0])

        combined_scores = cosine_scores
        similar_indices = combined_scores.argsort()[::-1]
        recommended_formation_data = df.iloc[similar_indices]

        columns_to_include = ["filiere_id", "filiere_nom", "filiere_descriptif", "filiere_email", "filiere_telephone", "filiere_images_pc", "filiere_images_telephone", "filiere_images_tablettes", "faculte_id"]

        recommended_courses = []
        seen_courses = set()
        for _, row in recommended_formation_data.iterrows():
            course_id = row["filiere_id"]
            if course_id not in seen_courses:
                course_info = {column: row[column] if column in row else None for column in columns_to_include}
                recommended_courses.append(course_info)
                seen_courses.add(course_id)

        for metier in recommended_courses:
            for key, value in metier.items():
                if isinstance(value, float) and np.isnan(value):
                    metier[key] = 0.0

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_courses = recommended_courses[start_index:end_index]

        return paginated_courses

    except Exception as e:
        print(f"Erreur lors de la recommandation des cours: {e}")
        return []

# Exemple d'appel de la fonction de recommandation
recommended_courses = formations_recommandation_populaire(page=1, page_size=10)
print(recommended_courses)

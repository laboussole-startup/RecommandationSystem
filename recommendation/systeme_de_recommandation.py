from datetime import datetime, timedelta
from typing import Dict, List, Union
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from recommendation.load_data import fetch_data_and_save_to_csv, get_last_update_time, save_last_update_time 

# Charger les données à partir du fichier CSV
data = get_last_update_time()
if data is not None and datetime.now() - data < timedelta(days=30):
    print("Les données sont à jour, pas besoin de les mettre à jour.")
else:
        # Les données CSV n'existent pas ou datent de plus de deux jours, mettre à jour à partir de la base de données
    fetch_data_and_save_to_csv()
    save_last_update_time(datetime.now())

df = pd.read_csv("formations_with_centres_interet.csv")

# Fonction pour prétraiter les données
def preprocess(text):
    text = str(text)
    text = text.lower()
    return text

# Prétraiter les données
df['descriptif'] = df['descriptif'].apply(preprocess)
df['nom.1'] = df['nom.1'].apply(preprocess)

# Initialiser le vectoriseur TF-IDF avec des paramètres personnalisés
tfidf_vectorizer = TfidfVectorizer(stop_words='english', min_df=0.05, max_df=0.95)

# Transformer les données en matrice TF-IDF
tfidf_matrix = tfidf_vectorizer.fit_transform(df['descriptif'] + ' ' + df['nom.1'])

# Définir une fonction pour recommander des formations
# def recommend_courses(user_interests: str) -> List[Dict[str, Union[str, float]]]:
#     # Prétraiter les centres d'intérêt de l'utilisateur
#     user_interests = preprocess(user_interests)
#     # Transformer les centres d'intérêt de l'utilisateur en vecteur TF-IDF
#     user_vector = tfidf_vectorizer.transform([user_interests])

#     # Calculer les scores de similarité cosinus entre les centres d'intérêt de l'utilisateur et les caractéristiques des cours
#     cosine_scores = linear_kernel(user_vector, tfidf_matrix).flatten()

#     # Trier les indices des cours en fonction des scores de similarité cosinus
#     similar_indices = cosine_scores.argsort()[::-1]

#     # Obtenir les noms des cours recommandés à partir des indices triés
#     #recommended_courses = df[["filieres_id","nom","descriptif","centre_interet","duree","cout","langue_enseignement","diplome_delivre","faculte_id","faculte_id","nom","descriptif","condition_admission","email","telephone","universite_id","universite_id","nom","ville","descriptif","email","telephone","site_web"]].iloc[similar_indices[:]].tolist()
#     recommended_courses_df = df.iloc[similar_indices[:]].values.tolist()
#     # recommended_courses = recommended_courses_df.to_dict(orient='records')
#     # for course in recommended_courses:
#     #     for key, value in course.items():
#     #         if isinstance(value, float) and np.isnan(value):
#     #             course[key] = 0.0  # Remplacer NaN par 0.0 ou une autre valeur par défaut selon votre choix

#     # return recommended_courses
#  # Convertir la liste en DataFrame si ce n'est pas déjà le cas
#     if not isinstance(recommended_courses_df, pd.DataFrame):
#         recommended_courses_df = pd.DataFrame(recommended_courses_df)

#     # Convertir le DataFrame en liste de dictionnaires
#     recommended_courses = recommended_courses_df.to_dict(orient='records')

#     # Remplacer les valeurs NaN par une valeur par défaut
#     recommended_courses = []
#     for index, row in recommended_courses_df.iterrows():
#         course_dict = {}
#         for column, value in row.iteritems():
#             course_dict[column] = value
#         recommended_courses.append(course_dict)

#     # Remplacer les valeurs NaN par une valeur par défaut
#     for course in recommended_courses:
#         for key, value in course.items():
#             if isinstance(value, float) and np.isnan(value):
#                 course[key] = 0.0  # Remplacer NaN par 0.0 ou une autre valeur par défaut selon votre choix

#     return recommended_courses

def recommend_courses(user_interests: str) -> List[Dict[str, Union[str, float]]]:
    # Prétraiter les centres d'intérêt de l'utilisateur
    user_interests = preprocess(user_interests)
    # Transformer les centres d'intérêt de l'utilisateur en vecteur TF-IDF
    user_vector = tfidf_vectorizer.transform([user_interests])

    # Calculer les scores de similarité cosinus entre les centres d'intérêt de l'utilisateur et les caractéristiques des cours
    cosine_scores = linear_kernel(user_vector, tfidf_matrix).flatten()

    # Trier les indices des cours en fonction des scores de similarité cosinus
    similar_indices = cosine_scores.argsort()[::-1]

    # Obtenir les données des cours recommandés
    recommended_courses_data = df.iloc[similar_indices]

    # Convertir les données en une liste de dictionnaires contenant le nom de la colonne et sa valeur pour chaque cours recommandé
    recommended_courses = []
    for _, row in recommended_courses_data.iterrows():
        course_dict = {}
        for column, value in row.items():
            course_dict[column] = value
        recommended_courses.append(course_dict)

    # Remplacer les valeurs NaN par une valeur par défaut
    for course in recommended_courses:
        for key, value in course.items():
            if isinstance(value, float) and np.isnan(value):
                course[key] = 0.0  # Remplacer NaN par 0.0 ou une autre valeur par défaut selon votre choix

    return recommended_courses
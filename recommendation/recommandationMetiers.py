from fastapi import FastAPI, Query, HTTPException
import numpy as np
from sqlalchemy.orm import Session
from typing import Dict, List, Union
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from recommendation.load_data import load_metiers_data
from recommendation.sr_faculte import preprocess

# Charger les données à partir de la base de données
try:
    df = load_metiers_data()
except Exception as e:
    raise Exception(f"Erreur lors du chargement des données : {e}")

# Fonction de prétraitement pour mettre le texte en minuscules
def preprocess(text):
    text = str(text)
    text = text.lower()
    return text

# Combinaison de colonnes pour former une colonne de texte à vectoriser
try:
    df["descriptions_and_caracteristiques"] = df["description"] + " " + df["nom"] + " " + df["entreprisesrecrutent"] + " " + df["competencescles"]
except KeyError as e:
    raise KeyError(f"Colonne manquante dans les données : {e}")

# Initialisation du vectoriseur TF-IDF et transformation des descriptions et caractéristiques
try:
    vectorizer = TfidfVectorizer()
    descriptions_and_caracteristiques_tfidf = vectorizer.fit_transform(df["descriptions_and_caracteristiques"].apply(preprocess))
except Exception as e:
    raise Exception(f"Erreur lors de la vectorisation des descriptions : {e}")

def recommend_metiers(user_interests: List[str], user_competence: List[str] = None, historique_recherche_utilisateur: List[str] = None, page: int = 1, page_size: int = 10, interest_weight: float = 1.5, history_weight: float = 1.0, competence_weight: float = 1.5) -> List[Dict[str, Union[str, float]]]:
    try:
        # Prétraiter les centres d'intérêt de l'utilisateur
        user_interests = preprocess(" ".join(user_interests))
        
        # Prétraiter et vectoriser l'historique de recherche de l'utilisateur s'il est fourni
        if historique_recherche_utilisateur:
            historique_recherche_utilisateur_vectortfidf = vectorizer.transform([" ".join(historique_recherche_utilisateur)])
        else:
            historique_recherche_utilisateur_vectortfidf = vectorizer.transform([""])
        
        # Vectoriser les centres d'intérêt de l'utilisateur
        user_vectortfidf = vectorizer.transform([user_interests])
        
        # Vectoriser les compétences de l'utilisateur si elles sont fournies
        if user_competence:
            user_competence_vectortfidf = vectorizer.transform([" ".join(user_competence)])
            competence_scores = linear_kernel(user_competence_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()
        else:
            competence_scores = np.zeros(len(descriptions_and_caracteristiques_tfidf))
        
        # Calculer les scores de similarité cosinus entre les intérêts de l'utilisateur et les descriptions des métiers
        cosine_scores = linear_kernel(user_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()
        
        # Calculer les scores de similarité cosinus entre l'historique de recherche et les descriptions des métiers s'il est fourni
        if historique_recherche_utilisateur:
            similarite_historique_recherche = linear_kernel(historique_recherche_utilisateur_vectortfidf, descriptions_and_caracteristiques_tfidf).flatten()
        else:
            similarite_historique_recherche = np.zeros(len(descriptions_and_caracteristiques_tfidf))
        
        # Combiner les scores de similarité en pondérant les intérêts, les compétences et l'historique de recherche
        combined_scores = (interest_weight * cosine_scores) + (competence_weight * competence_scores) + (history_weight * similarite_historique_recherche)
        
        # Trier les indices des métiers en fonction des scores combinés en ordre décroissant
        similar_indices = combined_scores.argsort()[::-1]
        
        # Obtenir les données des métiers recommandés
        recommended_metiers_data = df.iloc[similar_indices]
        
        # Convertir les données en une liste de dictionnaires
        recommended_metiers = []
        for _, row in recommended_metiers_data.iterrows():
            metier_dict = {}
            for column, value in row.items():
                metier_dict[column] = value
            recommended_metiers.append(metier_dict)
        
        # Remplacer les valeurs NaN par une valeur par défaut (0.0)
        for metier in recommended_metiers:
            for key, value in metier.items():
                if isinstance(value, float) and np.isnan(value):
                    metier[key] = 0.0

        # Implémentation de la pagination
        start_index = (page - 1) * page_size  # Calcul de l'index de début
        end_index = start_index + page_size  # Calcul de l'index de fin
        paginated_metiers = recommended_metiers[start_index:end_index]  # Extraire la sous-liste correspondant à la page
        
        return paginated_metiers
    except Exception as e:
        print(f"Erreur lors de la recommandation des métiers : {e}")
        return []



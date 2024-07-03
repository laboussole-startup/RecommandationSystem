import re
from typing import Dict, List, Union
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizer, TFBertModel
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from recommendation.load_data import load_data
from recommendation.prepocess import preprocess

# Charger les données
try:
    df = load_data()
except Exception as e:
    print(f"Erreur lors du chargement des données de formations: {e}")


# Appliquer le prétraitement sur les descriptions de cours
df["descriptions_and_caracteristiques"] = (df["filiere_descriptif"] + " " + 
                                           df["filiere_nom"] + " " + 
                                           df["faculte_nom"] + " " + 
                                           df["faculte_descriptif"]).apply(preprocess)

# Encoder les labels pour les pays et les diplômes
label_encoder_country = LabelEncoder()
df["universite_pays_encoded"] = label_encoder_country.fit_transform(df["universite_pays"])

label_encoder_diploma = LabelEncoder()
df["faculte_condition_admission_encoded"] = label_encoder_diploma.fit_transform(df["faculte_condition_admission"])

# Utiliser BERT pour obtenir des embeddings de texte
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = TFBertModel.from_pretrained('bert-base-uncased')

def get_bert_embeddings(texts):
    inputs = tokenizer(texts, return_tensors='tf', padding=True, truncation=True, max_length=128)  # Tokenizer le texte
    outputs = bert_model(inputs)  # Obtenir les embeddings de BERT
    embeddings = outputs.last_hidden_state[:, 0, :]  # Prendre le vecteur [CLS] pour chaque entrée
    return embeddings

# Obtenir les embeddings pour les descriptions
descriptions_embeddings = get_bert_embeddings(df["descriptions_and_caracteristiques"].tolist())

# Combiner les caractéristiques
X = np.hstack([
    descriptions_embeddings.numpy(),  # Embeddings de descriptions
    df["universite_pays_encoded"].values.reshape(-1, 1),  # Encodages des pays
    df["faculte_condition_admission_encoded"].values.reshape(-1, 1)  # Encodages des conditions d'admission
])

# Les labels peuvent être générés ou obtenus à partir des interactions utilisateur
# Ici, nous supposons que vous avez une forme de label indiquant la pertinence
y = np.random.rand(len(df))  # Placeholder pour les labels de pertinence

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner un réseau de neurones
model = MLPRegressor(hidden_layer_sizes=(128, 64), activation='relu', solver='adam', max_iter=100)
model.fit(X_train, y_train)

# Fonction de recommandation
def formations_recommandation(user_interests: List[str] = None, pays_utilisateur: str = None, user_diplome: str = None, page: int = 1, page_size: int = 10) -> List[Dict[str, Union[str, float]]]:
    try:
        # Prétraitement et embeddings des centres d'intérêt de l'utilisateur
        user_interests_embeddings = get_bert_embeddings([" ".join(user_interests) if user_interests else ""]).numpy()

        # Encodage du pays et du diplôme
        pays_encoded = label_encoder_country.transform([pays_utilisateur]) if pays_utilisateur else np.array([0])
        diplome_encoded = label_encoder_diploma.transform([user_diplome]) if user_diplome else np.array([0])

        # Création du vecteur de caractéristiques de l'utilisateur
        user_features = np.hstack([user_interests_embeddings, pays_encoded.reshape(-1, 1), diplome_encoded.reshape(-1, 1)])

        # Calcul des scores de pertinence
        scores = model.predict(user_features).flatten()

        # Triage des indices des cours en fonction des scores en ordre décroissant
        similar_indices = scores.argsort()[::-1]

        # Récupération des données des cours recommandés
        recommended_formation_data = df.iloc[similar_indices]

        # Colonnes à inclure dans les résultats
        columns_to_include = ["filiere_id", "filiere_nom", "filiere_descriptif", "filiere_email", "filiere_telephone", "filiere_images_pc", "filiere_images_telephone", "filiere_images_tablettes", "faculte_id"]

        # Conversion des données en une liste de dictionnaires en incluant seulement les colonnes spécifiées
        recommended_courses = []
        seen_courses = set()
        for _, row in recommended_formation_data.iterrows():
            course_id = row["filiere_id"]
            if course_id not in seen_courses:
                course_info = {column: row[column] if column in row else None for column in columns_to_include}
                recommended_courses.append(course_info)
                seen_courses.add(course_id)

        # Implémentation de la pagination
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_courses = recommended_courses[start_index:end_index]

        return paginated_courses

    except Exception as e:
        print(f"Erreur lors de la recommandation des cours: {e}")
        return []

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Télécharger les stop words et les lemmatizers
nltk.download('stopwords')
nltk.download('wordnet')

# Initialiser lemmatizer et stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    # Convertir le texte en minuscules
    text = text.lower()
    
    # Supprimer les caractères spéciaux et les chiffres
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenisation (découper le texte en mots)
    tokens = text.split()
    
    # Suppression des stop words et lemmatisation
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    
    # Rejoindre les tokens pour reformer le texte
    text = ' '.join(tokens)
    
    return text

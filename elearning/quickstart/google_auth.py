import os
import json
from urllib.request import Request
from dotenv import load_dotenv
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Les scopes de l'API Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Charger les variables d'environnement pour les utiliser dans votre fichier credentials.json
            client_id = os.getenv("GOOGLE_CLIENT_ID")
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

            # Créer un fichier credentials.json temporaire en utilisant les variables d'environnement
            credentials_json = {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
                }
            }

            # Sauvegarder ce fichier temporaire
            with open('temp_credentials.json', 'w') as temp_file:
                json.dump(credentials_json, temp_file)

            # Utiliser ce fichier pour l'authentification
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'temp_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Sauvegarder les informations d'accès dans token.json pour réutilisation
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        # Supprimer le fichier temporaire après utilisation
        os.remove('temp_credentials.json')

    return creds

def get_calendar_service():
    creds = get_credentials()
    return googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

# Exemple d'utilisation
service = get_calendar_service()

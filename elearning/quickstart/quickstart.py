from __future__ import print_function
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Vérifiez le répertoire de travail actuel
print("Current working directory:", os.getcwd())

# Vérifiez la présence du fichier token.json
if os.path.exists('token.json'):
    print("Found token.json")
else:
    print("token.json not found")

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    # Le fichier token.json stocke les jetons d'accès et de rafraîchissement de l'utilisateur, et est
    # créé automatiquement lorsque le flux d'autorisation se termine pour la première fois.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # S'il n'y a pas de (valide) crédentials disponibles, laissez l'utilisateur se connecter.
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'temp_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Sauvegarder les informations d'accès dans token.json pour réutilisation
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        # Supprimer le fichier temporaire après utilisation
        os.remove('temp_credentials.json')

    return creds

def main():
    """Montre l'utilisation de base de l'API Google Calendar pour créer une réunion Google Meet."""
    creds = get_credentials()

    try:
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': 'Réunion Google Meet',
            'description': 'Créer une réunion Google Meet.',
            'start': {
                'dateTime': '2024-08-01T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2024-08-01T10:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': 'randomString',  # Un identifiant unique pour chaque demande
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                },
            },
            'attendees': [
                {'email': 'example@example.com'},
            ],
        }

        event_result = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        print(f'Event created: {event_result.get("htmlLink")}')
    except Exception as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()

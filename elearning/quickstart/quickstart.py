from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Vérifiez le répertoire de travail actuel
print("Current working directory:", os.getcwd())

# Vérifiez la présence du fichier credentials.json
if os.path.exists('credentials.json'):
    print("Found credentials.json")
else:
    print("credentials.json not found")

# Vérifiez la présence du fichier token.json
if os.path.exists('token.json'):
    print("Found token.json")
else:
    print("token.json not found")

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Montre l'utilisation de base de l'API Google Calendar pour créer une réunion Google Meet."""
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'elearning\quickstart\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Enregistrez les credentials pour la prochaine exécution
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

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
        # TODO(developer) - Gérer les erreurs de l'API Calendar.
        print(f'An error occurred: {error}')



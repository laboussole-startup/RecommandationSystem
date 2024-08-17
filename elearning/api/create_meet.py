from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_current_user
from core.database import get_db
from elearning.quickstart.google_auth import get_calendar_service
from elearning.schemas.SchemasPydantic import EventCreate, EventRead
from elearning.models.modelsSQLAlchemy import Module, Event, Utilisateur

router = APIRouter()

@router.post("/module/{module_id}/create_event", response_model=EventRead)
def create_event(module_id: int, event_data: EventCreate, db: Session = Depends(get_db), current_user: Utilisateur = Depends(get_current_user)):
    """
    Endpoint pour créer un événement Google Calendar avec un lien Google Meet pour un module spécifique.
    """
    module = db.query(Module).filter(Module.id_module == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module introuvable")

    service = get_calendar_service()

    event = {
        'summary': event_data.summary,
        'description': event_data.description,
        'start': {
            'dateTime': event_data.start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': event_data.end_time,
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'randomString',  # Un identifiant unique pour chaque demande
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
            },
        },
        'attendees': [{'email': attendee} for attendee in event_data.attendees],
    }

    created_event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()

    new_event = Event(
        event_id=created_event['id'],
        module_id=module_id,
        summary=event_data.summary,
        description=event_data.description,
        start_time=event_data.start_time,
        end_time=event_data.end_time,
        hangout_link=created_event.get('hangoutLink')
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

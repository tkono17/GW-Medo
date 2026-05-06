from fastapi import APIRouter, Depends, FastAPI

from ..tools.common import SessionDep, get_token_header
from ..model import Event, EventPublic, EventCreate, EventUpdate,\
      EventType, EventTypePublic, EventTypeCreate, EventTypeUpdate,\
      EventTopicLink

router = APIRouter(tags=['Event'], dependencies=[Depends(get_token_header)],
                   responses={404: {"description": "Not found"}})

#----------------------------------------------
# EventType
#----------------------------------------------
@router.post('/eventType/create')
async def create_eventType(data: EventTypeCreate, session: SessionDep)  -> EventTypePublic:
    return create_db(data, EventType, session)

@router.get('/eventType/')
async def get_eventTypes(session: SessionDep, offset: int = 0, limit: int = 100) -> list[EventTypePublic]:
    return getall_db(EventType, offset, limit)

@router.get('/eventType/{id}')
async def get_eventType(id: int, session: SessionDep) -> EventTypePublic | None:
    return get_db(id, EventType, session)

@router.post('/eventType/update/{id}')
async def update_eventType(id: int, data: EventTypeUpdate, session: SessionDep) -> EventTypePublic | None:
    return update_db(id, data, EventType, session)

@router.post('/eventType/delete/{id}')
async def delete_eventType(id: int, session: SessionDep):
    return delete_db(id, EventType, session)

#----------------------------------------------
# Event-X Link
#----------------------------------------------

#----------------------------------------------
# Event
#----------------------------------------------
@router.post('/event/create')
async def create_event(data: EventCreate, session: SessionDep)  -> EventPublic:
    data_db = Event.model_validate(data)
    session.add(data_db)
    session.commit()
    session.refresh(data_db)
    return data_db

@router.get('/event/')
async def get_events(session: SessionDep, offset: int = 0, limit: int = 100) -> list[EventPublic]:
    return getall_db(Event, session, offset, limit)

@router.get('/event/{id}')
async def get_event(id: int, session: SessionDep) -> EventPublic | None:
    return get_db(id, Event, session)

@router.post('/event/update/{id}')
async def update_event(id: int, data: EventUpdate, session: SessionDep) -> EventPublic | None:
    return update_db(id, data, Event, session)

@router.post('/event/delete/{id}')
async def delete_event(id: int, session: SessionDep):
    return delete_db(id, Event, session)

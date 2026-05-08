from fastapi import APIRouter, Depends, FastAPI

from ..tools.common import SessionDep, get_token_header
from ..tools import TableAccess
from ..model import (
    Event, EventPublic, EventCreate, EventUpdate,
    EventType, EventTypePublic, EventTypeCreate, EventTypeUpdate,
    EventTopicLink
)

router = APIRouter(tags=['Event'], dependencies=[Depends(get_token_header)],
                   responses={404: {"description": "Not found"}})

#----------------------------------------------
# EventType
#----------------------------------------------
@router.post('/eventType/create')
async def create_eventType(data: EventTypeCreate, session: SessionDep)  -> EventTypePublic:
    table = TableAccess('eventtype')
    return create_db(data, EventType, session)

@router.get('/eventType/')
async def get_eventTypes(session: SessionDep, offset: int = 0, limit: int = 100) -> list[EventTypePublic]:
    table = TableAccess('eventtype')
    return table.get(offset, limit)

@router.get('/eventType/{id}')
async def get_eventType(id: int, session: SessionDep) -> EventTypePublic | None:
    table = TableAccess('eventtype')
    return table.get(id)

@router.post('/eventType/update/{id}')
async def update_eventType(id: int, data: EventTypeUpdate, session: SessionDep) -> EventTypePublic | None:
    table = TableAccess('eventtype')
    return table.update(id, data)

@router.post('/eventType/delete/{id}')
async def delete_eventType(id: int, session: SessionDep):
    table = TableAccess('eventtype')
    return table.delete(id)

#----------------------------------------------
# Event-X Link
#----------------------------------------------

#----------------------------------------------
# Event
#----------------------------------------------
@router.post('/event/create')
async def create_event(data: EventCreate, session: SessionDep)  -> EventPublic:
    table = TableAccess('event')
    return table.create(data)

@router.get('/event/')
async def get_events(session: SessionDep, offset: int = 0, limit: int = 100) -> list[EventPublic]:
    table = TableAccess('event')
    return table.getall(offset, limit)

@router.get('/event/{id}')
async def get_event(id: int, session: SessionDep) -> EventPublic | None:
    table = TableAccess('event')
    return table.get(id)

@router.post('/event/update/{id}')
async def update_event(id: int, data: EventUpdate, session: SessionDep) -> EventPublic | None:
    table = TableAccess('event')
    return table.update(id, data)

@router.post('/event/delete/{id}')
async def delete_event(id: int, session: SessionDep):
    table = TableAccess('event')
    return table.delete(id)

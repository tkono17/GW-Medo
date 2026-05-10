from fastapi import APIRouter
import logging

from ..app import getApp
from ..model import (
    EventTypePublic, EventTypeCreate, EventTypeUpdate,
)

log = logging.getLogger(__name__)

#----------------------------------------------
# EventType
#----------------------------------------------
router = APIRouter(tags=['EventType'], 
                   responses={404: {"description": "Not found"}})

@router.post('/eventType/create')
async def create_eventType(data: EventTypeCreate)  -> EventTypePublic:
    app = getApp()
    table = app.dbAccess.getTable('eventtype')
    return table.create(data)

@router.get('/eventType/')
async def get_eventType(offset: int = 0, limit: int = 100) -> list[EventTypePublic]:
    app = getApp()
    table = app.dbAccess.getTable('eventtype')
    return table.getall(offset=offset, limit=limit)

@router.get('/eventType/{id}')
async def get_eventType(id: int) -> EventTypePublic | None:
    app = getApp()
    table = app.dbAccess.getTable('eventtype')
    return table.get(id)

@router.post('/eventType/update/{id}')
async def update_eventType(id: int, data: EventTypeUpdate) -> EventTypePublic | None:
    app = getApp()
    table = app.dbAccess.getTable('eventtype')
    return table.update(id, data)

@router.post('/eventType/delete/{id}')
async def delete_eventType(id: int):
    app = getApp()
    table = app.dbAccess.getTable('eventtype')
    return table.delete(id)

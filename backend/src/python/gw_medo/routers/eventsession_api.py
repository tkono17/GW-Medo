from fastapi import APIRouter
import logging

from ..app import getApp
from ..model import (
    EventSessionPublic, EventSessionCreate, EventSessionUpdate,
)

log = logging.getLogger(__name__)

#----------------------------------------------
# Event
#----------------------------------------------
router = APIRouter(tags=['EventSession'], 
                   responses={404: {"description": "Not found"}})

@router.post('/eventSession/create')
async def create_eventSession(data: EventSessionCreate)  -> EventSessionPublic:
    app = getApp()
    table = app.dbAccess.getTable('eventsession')
    return table.create(data)

@router.get('/eventSession/')
async def get_eventSession(offset: int = 0, limit: int = 100) -> list[EventSessionPublic]:
    app = getApp()
    table = app.dbAccess.getTable('eventsession')
    return table.getall(offset=offset, limit=limit)

@router.get('/eventSession/{id}')
async def get_eventSession(id: int) -> EventSessionPublic | None:
    app = getApp()
    table = app.dbAccess.getTable('eventsession')
    return table.get(id)

@router.post('/eventSession/update/{id}')
async def update_eventSession(id: int, data: EventSessionUpdate) -> EventSessionPublic | None:
    app = getApp()
    table = app.dbAccess.getTable('eventsession')
    return table.update(id, data)

@router.post('/eventSession/delete/{id}')
async def delete_eventSession(id: int):
    app = getApp()
    table = app.dbAccess.getTable('eventsession')
    return table.delete(id)


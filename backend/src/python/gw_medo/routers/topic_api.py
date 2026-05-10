from fastapi import APIRouter, Depends, FastAPI
import logging

from ..app import getApp
from ..model import (
    TopicPublic, TopicCreate, TopicUpdate
)

log = logging.getLogger(__name__)

router = APIRouter(tags=['Topic'], 
                   responses={404: {"description": "Not found"}})

@router.post('/topic/create')
async def create_topic(data: TopicCreate)  -> TopicPublic:
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.create(data)

@router.get('/topic/')
async def get_topics(offset: int = 0, limit: int = 100) -> list[TopicPublic]:
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.getall(offset=offset, limit=limit)

@router.get('/topic/{id}')
async def get_topic(id: int) -> TopicPublic | None:
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.get(id)

@router.post('/topic/update/{id}')
async def update_topic(id: int, data: TopicUpdate) -> TopicPublic | None:
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.update(id, data)

@router.post('/topic/delete/{id}')
async def delete_topic(id: int):
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.delete(id)

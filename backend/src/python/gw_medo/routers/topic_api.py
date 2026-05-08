from fastapi import APIRouter, Depends

from ..tools.common import SessionDep, get_token_header
from ..tools import TableAccess
from ..model import (
    Topic, TopicPublic, TopicCreate, TopicUpdate
)

router = APIRouter(tags=['Topic'])

session = None

@router.post('/topic/create')
async def create_topic(data: TopicCreate, session: SessionDep)  -> TopicPublic:
    table = TableAccess(Topic)
    return table.create(data)

@router.get('/topic/')
async def get_topics(session: SessionDep, offset: int = 0, limit: int = 100) -> list[TopicPublic]:
    table = TableAccess(Topic)
    return table.getall(offset, limit)

@router.get('/topic/{id}')
async def get_topic(id: int, session: SessionDep) -> TopicPublic | None:
    table = TableAccess(Topic)
    return table.get(id)

@router.post('/topic/update/{id}')
async def update_topic(id: int, data: TopicUpdate, session: SessionDep) -> TopicPublic | None:
    table = TableAccess(Topic)
    return table.update(id, data)

@router.post('/topic/delete/{id}')
async def delete_topic(id: int, session: SessionDep):
    table = TableAccess(Topic)
    return table.delete(id)

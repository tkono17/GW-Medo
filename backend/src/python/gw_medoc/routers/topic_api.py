from fastapi import APIRouter, Depends

from ..tools.common import SessionDep, get_token_header
from ..model import Topic, TopicPublic, TopicCreate, TopicUpdate

router = APIRouter(tags=['Topic'])

session = None

@router.post('/topic/create')
async def create_topic(data: TopicCreate, session: SessionDep)  -> TopicPublic:
    return create_db(data, Topic, session)

@router.get('/topic/')
async def get_topics(session: SessionDep, offset: int = 0, limit: int = 100) -> list[TopicPublic]:
    return getall_db(Topic, offset, limit)

@router.get('/topic/{id}')
async def get_topic(id: int, session: SessionDep) -> TopicPublic | None:
    return get_db(id, Topic, session)

@router.post('/topic/update/{id}')
async def update_topic(id: int, data: TopicUpdate, session: SessionDep) -> TopicPublic | None:
    return update_db(id, data, Topic, session)

@router.post('/topic/delete/{id}')
async def delete_topic(id: int, session: SessionDep):
    return delete_db(id, Topic, session)

from fastapi import APIRouter
import logging

from ..app import getApp
from ..model import (
    CategoryPublic, CategoryCreate, CategoryUpdate
)

log = logging.getLogger(__name__)

router = APIRouter(tags=['Category'], 
                   responses={404: {"description": "Not found"}})

@router.post('/category/create')
async def create_category(data: CategoryCreate)  -> CategoryPublic:
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.create(data)

@router.get('/category/')
async def get_categories(offset: int = 0, limit: int = 100) -> list[CategoryPublic]:
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.getall(offset=offset, limit=limit)

@router.get('/category/{id}')
async def get_category(id: int) -> CategoryPublic | None:
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.get(id)

@router.post('/category/update/{id}')
async def update_category(id: int, data: CategoryUpdate) -> CategoryPublic | None:
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.update(id, data)

@router.post('/category/delete/{id}')
async def delete_category(id: int):
    app = getApp()
    table = app.dbAccess.getTable('topic')
    return table.delete(id)

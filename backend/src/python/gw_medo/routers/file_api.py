from fastapi import APIRouter
import logging

from ..app import getApp
from ..model import (
    FilePublic, FileCreate, FileUpdate
)

log = logging.getLogger(__name__)

router = APIRouter(tags=['File'], 
                   responses={404: {"description": "Not found"}})

@router.post('/file/create')
async def create_file(data: FileCreate)  -> FilePublic:
    app = getApp()
    table = app.dbAccess.getTable('file')
    return table.create(data)

@router.get('/file/')
async def get_files(offset: int = 0, limit: int = 100) -> list[FilePublic]:
    app = getApp()
    table = app.dbAccess.getTable('file')
    return table.getall(offset=offset, limit=limit)

@router.get('/file/{id}')
async def get_file(id: int) -> FilePublic | None:
    app = getApp()
    table = app.dbAccess.getTable('file')
    return table.get(id)

@router.post('/file/update/{id}')
async def update_file(id: int, data: FileUpdate) -> FilePublic | None:
    app = getApp()
    table = app.dbAccess.getTable('file')
    return table.update(id, data)

@router.post('/file/delete/{id}')
async def delete_file(id: int):
    app = getApp()
    table = app.dbAccess.getTable('file')
    return table.delete(id)

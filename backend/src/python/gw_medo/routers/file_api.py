from fastapi import APIRouter, Depends

from ..tools.common import SessionDep, get_token_header
from ..tools import TableAccess
from ..model import (
    File, FilePublic, FileCreate, FileUpdate
)

router = APIRouter(tags=['File'])

session = None

@router.post('/file/create')
async def create_file(data: FileCreate, session: SessionDep)  -> FilePublic:
    table = TableAccess(File)
    return table.create(data)

@router.get('/file/')
async def get_files(session: SessionDep, offset: int = 0, limit: int = 100) -> list[FilePublic]:
    table = TableAccess(File)
    return table.getall(offset, limit)

@router.get('/file/{id}')
async def get_file(id: int, session: SessionDep) -> FilePublic | None:
    table = TableAccess(File)
    return table.get(id)

@router.post('/file/update/{id}')
async def update_file(id: int, data: FileUpdate, session: SessionDep) -> FilePublic | None:
    table = TableAccess(File)
    return table.update(id, data)

@router.post('/file/delete/{id}')
async def delete_file(id: int, session: SessionDep):
    table = TableAccess(File)
    return table.delete(id)

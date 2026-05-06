from fastapi import APIRouter, Depends

from ..tools.common import SessionDep, get_token_header
from ..model import File, FilePublic, FileCreate, FileUpdate

router = APIRouter(tags=['File'])

session = None

@router.post('/file/create')
async def create_file(data: FileCreate, session: SessionDep)  -> FilePublic:
    return create_db(data, File, session)

@router.get('/file/')
async def get_files(session: SessionDep, offset: int = 0, limit: int = 100) -> list[FilePublic]:
    return getall_db(File, offset, limit)

@router.get('/file/{id}')
async def get_file(id: int, session: SessionDep) -> FilePublic | None:
    return get_db(id, File, session)

@router.post('/file/update/{id}')
async def update_file(id: int, data: FileUpdate, session: SessionDep) -> FilePublic | None:
    return update_db(id, data, File, session)

@router.post('/file/delete/{id}')
async def delete_file(id: int, session: SessionDep):
    return delete_db(id, File, session)

from fastapi import APIRouter, Depends, FastAPI

from ..tools.common import SessionDep, get_token_header
from ..model import Category, CategoryPublic, CategoryCreate, CategoryUpdate
from ..tools import TableAccess

router = APIRouter(tags=['Category'], 
                   responses={404: {"description": "Not found"}})

@router.post('/category/create')
async def create_category(data: CategoryCreate, session: SessionDep)  -> CategoryPublic:
    table = TableAccess(Category, session)
    return table.create(data)

@router.get('/category/')
async def get_categories(session: SessionDep, offset: int = 0, limit: int = 100) -> list[CategoryPublic]:
    table = TableAccess(Category, session)
    return table.getall(offset, limit)

@router.get('/category/{id}')
async def get_category(id: int, session: SessionDep) -> CategoryPublic | None:
    table = TableAccess(Category, session)
    return table.get(id)

@router.post('/category/update/{id}')
async def update_category(id: int, data: CategoryUpdate, session: SessionDep) -> CategoryPublic | None:
    table = TableAccess(Category, session)
    return table.update(id, data)

@router.post('/category/delete/{id}')
async def delete_category(id: int, session: SessionDep):
    table = TableAccess(Category, session)
    return table.delete(id)

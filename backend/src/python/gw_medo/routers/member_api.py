from fastapi import APIRouter, Depends, FastAPI
import logging

from ..app import getApp
from ..model import (
    MemberPublic, MemberCreate, MemberUpdate
)

log = logging.getLogger(__name__)

router = APIRouter(tags=['Member'], 
                   responses={404: {"description": "Not found"}})

@router.post('/member/create')
async def create_member(data: MemberCreate)  -> MemberPublic:
    app = getApp()
    table = app.dbAccess.getTable('member')
    return table.create(data)

@router.get('/member/')
async def get_members(offset: int = 0, limit: int = 100) -> list[MemberPublic]:
    app = getApp()
    table = app.dbAccess.getTable('member')
    return table.getall(offset=offset, limit=limit)

@router.get('/member/{id}')
async def get_member(id: int) -> MemberPublic | None:
    table = app.dbAccess.getTable('member')
    return table.get(id)

@router.post('/member/update/{id}')
async def update_member(id: int, data: MemberUpdate) -> MemberPublic | None:
    app = getApp()
    table = app.dbAccess.getTable('member')
    return table.update(id, data)

@router.post('/member/delete/{id}')
async def delete_member(id: int):
    app = getApp()
    table = app.dbAccess.getTable('member')
    return table.delete(id)

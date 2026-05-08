from fastapi import APIRouter, Depends

from ..tools.common import SessionDep, get_token_header
from ..tools import TableAccess
from ..model import (
    Member, MemberPublic, MemberCreate, MemberUpdate
)

router = APIRouter(tags=['Member'])

session = None

@router.post('/member/create')
async def create_member(data: MemberCreate, session: SessionDep)  -> MemberPublic:
    table = TableAccess(Member)
    return table.create(data)

@router.get('/member/')
async def get_members(session: SessionDep, offset: int = 0, limit: int = 100) -> list[MemberPublic]:
    table = TableAccess(Member)
    return table.getall(offset, limit)

@router.get('/member/{id}')
async def get_member(id: int, session: SessionDep) -> MemberPublic | None:
    table = TableAccess(Member)
    return table.get(id)

@router.post('/member/update/{id}')
async def update_member(id: int, data: MemberUpdate, session: SessionDep) -> MemberPublic | None:
    table = TableAccess(Member)
    return table.update(id, data)

@router.post('/member/delete/{id}')
async def delete_member(id: int, session: SessionDep):
    table = TableAccess(Member)
    return table.delete(id)

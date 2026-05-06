from fastapi import APIRouter, Depends

from ..tools.common import SessionDep, get_token_header
from ..model import Member, MemberPublic, MemberCreate, MemberUpdate

router = APIRouter(tags=['Member'])

session = None

@router.post('/member/create')
async def create_member(data: MemberCreate, session: SessionDep)  -> MemberPublic:
    return create_db(data, Member, session)

@router.get('/member/')
async def get_members(session: SessionDep, offset: int = 0, limit: int = 100) -> list[MemberPublic]:
    return getall_db(Member, offset, limit)

@router.get('/member/{id}')
async def get_member(id: int, session: SessionDep) -> MemberPublic | None:
    return get_db(id, Member, session)

@router.post('/member/update/{id}')
async def update_member(id: int, data: MemberUpdate, session: SessionDep) -> MemberPublic | None:
    return update_db(id, data, Member, session)

@router.post('/member/delete/{id}')
async def delete_member(id: int, session: SessionDep):
    return delete_db(id, Member, session)

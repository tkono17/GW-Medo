import logging
from typing import Annotated, TypeVar
from fastapi import Depends, Header, HTTPException
from sqlmodel import Session, select, create_engine

log = logging.getLogger(__name__)


# def create_db(data: ClsCreate, TDb: ClsDb, session: Session) -> ClsDb:
#     data_db = TDb.model_validate(data)
#     session.add(data_db)
#     session.commit()
#     session.refresh(data_db)
#     return data_db

# def getall_db(TDb: ClsDb, session: Session, offset: int = 0, limit: int = 100) -> list[ClsDb] | None:
#     statement = select(TDb).offset(offset).limit(limit)
#     v = session.exec(statement).all()
#     return v

# def get_db(id: int, TDb: ClsDb, session: Session) -> ClsDb:
#     data = session.get(TDb, id)
#     return data

# def update_db(id: int, data: ClsUpdate, TDb: ClsDb, session: Session) -> ClsDb:
#     data_db = session.get(TDb, id)
#     if data_db is None:
#         raise HTTPException(status_code=404, detail=f'Entry with {id} not found in {TDb}')
#     data_update = data.model_dump(exclude_unset=True)
#     data_db.sqlmodel_update(data_update)
#     session.add(data_db)
#     session.commit()
#     session.refresh(data_db)
#     return data_db

# def delete_db(id: int, TDb: ClsDb, session: Session):
#     data_db = session.get(TDb, id)
#     if data_db is None:
#         raise HTTPException(status_code=404, detail=f'Entry with {id} not found in {TDb}')
#     session.delete(data_db)
#     session.commit()
#     return { 'ok': True }


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
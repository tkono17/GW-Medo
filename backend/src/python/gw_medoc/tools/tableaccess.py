import logging
from typing import Optional, TypeVar
from sqlmodel import Session, select
from ..routers import *
from .common import getEngine

log = logging.getLogger(__name__)

ClsDb = TypeVar('Cls')
TPublic = TypeVar('TPublic')
TCreate = TypeVar('TCreate')
TUpdate = TypeVar('TUpdate')

class TableAccess:
    def __init__(self, TDb: ClsDb):
        self.TDb = TDb

    def create(self, data: TCreate):
        data_db = self.TDb.model_validate(data)
        with Session(getEngine()) as session:
            log.info(f'  create {data_db}')
            session.add(data_db)
            session.commit()
            session.refresh(data_db)
            log.info(f'  created {data_db}')
        return data_db

    def exec(self, statement, offset: int=0, limit: int=100):
        v = None
        with Session(getEngine()) as session:
            v = session.exec(statement).all()
        return v
    
    def getall(self, offset: int = 0, limit: int = 100):
        statement = select(self.TDb).offset(offset).limit(limit)
        v = []
        with Session(getEngine()) as session:
            results = session.exec(statement)
            v = results.all()
        return v

    def get(self, id: int):
        data = None
        with Session(getEngine()) as session:
            data = session.get(self.TDb, id)
        return data
    
    def update(self, id: int, data: TUpdate):
        data_db = self.get(id)
        if data_db is None:
            log.warning(f'Entry id={id} not found in {self.TDb.__name__}')
            return None
        data_update = data.model_dump(exclude_unset=True)
        data_db.sqlmodel_update(data_update)
        with Session(getEngine()) as session:
            session.add(data_db)
            session.commit()
            session.refresh(data_db)
        return data_db
    
    def delete(self, id: int):
        data_db = self.get(id)
        if data_db is None:
            log.warning(f'Entry id={id} not found in {self.TDb.__name__}')
            return None
        with Session(getEngine()) as session:
            session.delete(data_db)
            session.commit()
        return 0
    

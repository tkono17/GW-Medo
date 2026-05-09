from typing import TypeVar
import logging
from sqlmodel import create_engine
from dataclasses import dataclass
from .tableaccess import TableAccess, setEngine

log = logging.getLogger(__name__)

Cls = TypeVar('Cls')

class DbAccess:
    def __init__(self):
        self.engine = None
        self.tables = {}

    def connectDb(self, url: str):
        log.info(f'Connecting to database {url}')
        # connect_args = {
        #     'check_same_thread': False
        # }
        self.engine = create_engine(url)
        setEngine(self.engine)

    def addTable(self, tablename: str, 
                 TDb: Cls, 
                 TCreate: Cls|None = None, 
                 TUpdate: Cls|None = None):
        if TCreate is None: TCreate = TDb
        if TUpdate is None: TUpdate = TDb
        self.tables[tablename] = TableAccess(TDb, TCreate, TUpdate)
        
    def getTable(self, tablename):
        table = None
        if tablename in self.tables.keys():
            table = self.tables[tablename]
        return table
        
    def create(self, tablename, keyValues):
        table = self.getTable(tablename)
        TCreate = table.TCreate
        data = None
        if table is not None:
            data = table.create(TCreate(**keyValues))
        else:
            log.warning(f'  Cannot create entry in table {tablename}, table not found')
        return data

    def get(self, tablename: str, id: int):
        table = self.getTable(tablename)
        data = None
        if table is not None:
            data = table.get(id)
        else:
            log.warning(f'  Cannot get entry {id} in table {tablename}, table not found')
        return data

    def getall(self, tablename: str, selectModifier=None, offset: int=0, limit: int=100):
        table = self.getTable(tablename)
        data = None
        log.info(f'call getall: {table}')
        if table is not None:
            log.info(f'call getall: {tablename}')
            data = table.getall(selectModifier, offset, limit)
        else:
            log.warning(f'  Cannot get entries in table {tablename}, table not found')
        return data

    def getone(self, tablename: str, selectModifier=None):
        table = self.getTable(tablename)
        data = None
        if table is not None:
            data = table.getone(selectModifier)
        else:
            log.warning(f'  Cannot get entries in table {tablename}, table not found')
        return data

    def update(self, tablename, id, keyValues):
        table = self.getTable(tablename)
        TUpdate = table.TUpdate
        data = None
        if table is not None:
            data = table.update(id, TUpdate(**keyValues))
        else:
            log.warning(f'  Cannot update entry {id} in table {tablename}, table not found')
        return data
    
    def delete(self, tablename: str, id: int):
        table = self.getTable(tablename)
        if table is not None:
            table.delete(id)
        else:
            log.warning(f'  Cannot get entry {id} in table {tablename}, table not found')
        return 0
    
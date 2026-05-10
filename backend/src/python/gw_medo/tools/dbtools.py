from typing import TypeVar, Callable, Any
from appbasics import DbAccess

TCreate = TypeVar('TCreate')

def getUniqueCheck(tablename: str, 
                   data: TCreate) -> Callable[[Any], Any]:
    T = data.__class__
    modifier: Callable[[Any], Any] | None = None
    if tablename in ('eventtype', 'category', 'member'):
        def uniqueName(statement: Any) -> Any:
            statement = statement.where(T.name == data.name)
            return statement
        modifier = uniqueName
    elif tablename == 'eventsession':
        def uniqueNameDate(statement: Any) -> Any:
            statement = statement.where(T.name == data.name)
            statement = statement.where(T.date == data.date)
            return statement
        modifier = uniqueName
    elif tablename == 'topic':
        def uniqueNameDate(statement: Any) -> Any:
            statement = statement.where(T.name == data.name)
            statement = statement.where(T.eventSession_id == data.eventSession_id)
            return statement
        modifier = uniqueName
    elif tablename == 'file':
        def uniqueNameDate(statement: Any) -> Any:
            statement = statement.where(T.name == data.name)
            statement = statement.where(T.topic_id == data.topic_id)
            return statement
        modifier = uniqueName
    return modifier

def checkDuplicate(dbAccess: DbAccess, 
                   tablename: str, 
                   data: TCreate):
    ok = True
    modifier = getUniqueCheck(tablename, data)
    if modifier is not None:
        v = dbAccess.getall(tablename, modifier)
        if v is not None and len(v)>0:
            ok = False
    return ok

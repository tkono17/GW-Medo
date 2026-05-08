import logging
import re
import datetime
import re
from zoneinfo import ZoneInfo
from sqlmodel import select

from ..model import (
    Category, CategoryCreate, CategoryUpdate,
    Member, MemberCreate, MemberUpdate,
    Event, EventCreate, EventUpdate,
    EventType, EventTypeCreate, EventTypeUpdate,
    Topic, TopicCreate, TopicUpdate,
    File, FileCreate, FileUpdate,
    TopicMemberLink, TopicFileLink
)
from ..tools import TableAccess, getEngine, connectDb

log = logging.getLogger(__name__)

def typedValue(value):
    x = None
    for T in (int, float, str):
        try:
            x = T(value)
        except ValueError:
            pass
        if x is not None:
            break
    if x is None:
        x = value
    return x

def splitKeyValue(keyValue):
    log.info(f'  keyvalue: {keyValue}')
    i = keyValue.find(':')
    if i>0:
        key, value = keyValue[0:i], keyValue[i+1:]
    value = typedValue(value)
    return key, value

def clsCreate(tablename):
    cls = None
    match tablename:
        case 'member': cls = MemberCreate
        case 'eventtype': cls = EventTypeCreate
        case 'category': cls = CategoryCreate
        case 'event': cls = EventCreate
        case 'topic': cls = TopicCreate
        case 'file': cls = FileCreate
        case 'topicmemberlink': cls = TopicMemberLink
        case 'topicfilelink': cls = TopicFileLink
    return cls
    
def clsUpdate(tablename):
    cls = None
    match tablename:
        case 'member': cls = MemberUpdate
        case 'eventtype': cls = EventTypeUpdate
        case 'category': cls = CategoryUpdate
        case 'event': cls = EventUpdate
        case 'topic': cls = TopicUpdate
        case 'file': cls = FileUpdate
        case 'topicmemberlink': cls = TopicMemberLink
        case 'topicfilelink': cls = TopicFileLink
    return cls

class App:
    def __init__(self):
        self.tables = {}
        self.init()

    def init(self):
        self.tables = {
            'member': TableAccess(Member),
            'eventtype': TableAccess(EventType),
            'category': TableAccess(Category),
            'event': TableAccess(Event),
            'topic': TableAccess(Topic),
            'file': TableAccess(File),
            'topicmemberlink': TableAccess(TopicMemberLink),
            'topicfilelink': TableAccess(TopicFileLink)
        }

    def connectDb(self, dbfile):
        connectDb(dbfile)

    def getTable(self, tablename):
        table = None
        if tablename in self.tables.keys():
            table = self.tables[tablename]
        return table
        
    def create(self, tablename, keyValues):
        table = self.getTable(tablename)
        TCreate = clsCreate(tablename)
        data = None
        if table is not None:
            data = table.create(TCreate(**keyValues))
        else:
            log.warning(f'  Cannot create entry in table {tablename}, table not found')
        return data

    def getall(self, tablename: str, selectModifier=None, offset: int=0, limit: int=100):
        table = self.getTable(tablename)
        data = None
        log.info(f'call getall: {table}')
        if table is not None:
            engine = getEngine()
            log.info(f'call getall: {tablename}')
            data = table.getall(selectModifier, offset, limit)
        else:
            log.warning(f'  Cannot get entries in table {tablename}, table not found')
        return data

    def getone(self, tablename: str, selectModifier=None, offset: int=0, limit: int=100):
        table = self.getTable(tablename)
        data = None
        if table is not None:
            engine = getEngine()
            data = table.getone(selectModifier, offset, limit)
        else:
            log.warning(f'  Cannot get entries in table {tablename}, table not found')
        return data

    def get(self, tablename: str, id: int):
        table = self.getTable(tablename)
        data = None
        if table is not None:
            data = table.get(id)
        else:
            log.warning(f'  Cannot get entry {id} in table {tablename}, table not found')
        return data

    def update(self, tablename, id, keyValues):
        table = self.getTable(tablename)
        TUpdate = clsUpdate(tablename)
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
    
    # Create
    def addMember(self, name: str, position: str, active: bool = False):
        table = self.getTable('member')
        if table is None:
            log.warning(f'  Table member not found')
            return None
        data = MemberCreate(name=name, position=position, active=active)
        return table.create(data)
    
    def addCategory(self, categoryName: str):
        table = self.getTable('category')
        if table is None:
            log.warning(f'  Table category not found')
            return None
        data = CategoryCreate(name=categoryName)
        return table.create(data)
    
    def addEvent(self, category_id: int, *keyValues):
        table = self.getTable('event')
        if table is None:
            log.warning(f'  Table event not found')
            return None
        log.info(f'key values: {keyValues}')
        kvmap = { key: value for key, value in map(splitKeyValue, keyValues) }
        log.info(f'kvmap: {kvmap}')
        data = EventCreate(category_id=category_id, **kvmap)
        return table.create(data)
    
    def addTopic(self, event_id: int, *keyValues):
        table = self.getTable('topic')
        if table is None:
            log.warning(f'  Table topic not found')
            return None
        kvmap = { key: value for key, value in map(splitKeyValue, keyValues) }
        log.info(f'  kvmap {kvmap}')
        data = TopicCreate(event_id=event_id, **kvmap)
        return table.create(data)
    
    def addFile(self, topic_id: int, *keyValues):
        table = self.getTable('file')
        if table is None:
            log.warning(f'  Table file not found')
            return None
        kvmap = { key: value for key, value in map(splitKeyValue, keyValues) }
        log.info(f'  kvmap {kvmap}')
        data = TopicCreate(topic_id=topic_id, **kvmap)
        return table.create(data)
    
    def addTopicFile(self, topic_id: int, *keyValues):
        table = self.getTable('file')
        linktable = self.getTable('topicfilelink')
        kvmap = { key: value for key, value in map(splitKeyValue, keyValues) }
        file = table.create(FileCreate(**kvmap))
        linktable.create(TopicFileLink(topic_id=topic_id, file_id=file.id))
        return file
    
    def addTopicMember(self, topic_id: int, name: str, position: str, active: bool):
        table = self.getTable('member')
        linktable = self.getTable('topicmemberlink')
        ms = self.findMembers(name)
        member = None
        if len(ms)>0:
            member = ms[0]
        else:
            member = table.create(MemberCreate(name=name, position=position, active=active))
        if member is not None:
            linktable.create(TopicMemberLink(topic_id=topic_id, member_id=member.id))
        return member
    
    # Read
    def findMembers(self, name: str|None = None, topic_id: int | None = None):
        v = []
        table = self.getTable('member')
        if topic_id is not None:
            linktable = self.getTable('topicmemberlink')
            statement = select(TopicFileLink).offset(0).limit(100).where(TopicMemberLink.topic_id == topic_id)
            links = linktable.exec(statement)
            for link in links:
                statement = select(Member).offset(0).limit(100)
                statement = statement.where(Member.id == link.file_id)
                if name is not None:
                    statement = statement.where(Member.name.contains(name))
                v2 = table.exec(statement)
                v.extend(v2)
        else:
            statement = select(Member).offset(0).limit(100)
            if name is not None:
                statement = statement.where(Member.name.contains(name))
            v = table.exec(statement)
        return v
        
    def findCategories(self, categoryName: str|None = None):
        v = []
        table = self.getTable('category')
        if table is None:
            log.warning(f'  Cannot find category with name "{categoryName}", table not found')
            return v  
        statement = select(Category).offset(0).limit(100)
        if categoryName is not None:
            statement = statement.where(Category.name.contains(categoryName))
        v = table.exec(statement)
        return v
    
    def findEvents(self, category_id: int, 
                   name: str|None = None,
                   startTime: str|None = None, 
                   endTime: str|None = None):
        def selectFilter(statement):
            statement = statement.where(Event.category_id == category_id)
            if name is not None:
                statement = statement.where(Event.name.contains(name))
            if startTime is not None:
                mg = re.match(r'([\d]{4}-[\d]{2}-[\d]{2})', startTime)
                if mg is not None:
                    ds = datetime.date.fromisoformat(mg.group(0))
                    statement = statement.where(Event.date >= ds)
            if endTime is not None:
                mg = re.match(r'([\d]{4}-[\d]{2}-[\d]{2})', endTime)
                if mg is not None:
                    ds = datetime.date.fromisoformat(mg.group(0))
                    statement = statement.where(Event.date <= ds)
            return statement
        return self.getall('event', selectFilter)
    
    def findTopics(self, event_id: int):
        def selectFilter(statement):
            statement = statement.where(Topic.event_id == event_id)
            return statement 
        return self.getall('topic', selectFilter)

    def findTopicFiles(self, topic_id: int):
        v = []
        table = self.getTable('file')
        linktable = self.getTable('topicfilelink')
        statement = select(TopicFileLink).offset(0).limit(100).where(TopicFileLink.topic_id == topic_id)
        links = linktable.exec(statement)
        for link in links:
           statement = select(File).offset(0).limit(100)
           statement = statement.where(File.id == link.file_id)
           v2 = table.exec(statement)
           v.extend(v2)
        return v
    
sApp = App()

def getApp():
    global sApp
    return sApp

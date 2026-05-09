import logging
import re
import datetime
import re
from zoneinfo import ZoneInfo
from sqlmodel import select, SQLModel

from ..model import (
    Category, CategoryCreate, CategoryUpdate,
    Member, MemberCreate, MemberUpdate,
    EventSession, EventSessionCreate, EventSessionUpdate,
    EventType, EventTypeCreate, EventTypeUpdate,
    Topic, TopicCreate, TopicUpdate,
    File, FileCreate, FileUpdate,
    TopicMemberLink
)
from appbasics import DbAccess, getEngine, typedValue, keyValueToTuple

log = logging.getLogger(__name__)

class App:
    def __init__(self):
        self.dbAccess = DbAccess()
        self.init()

    def init(self):
        self.dbAccess.addTable('member', Member, MemberCreate, MemberUpdate)
        self.dbAccess.addTable('eventtype', EventType, EventTypeCreate, EventTypeUpdate)
        self.dbAccess.addTable('category', Category, CategoryCreate, CategoryUpdate)
        self.dbAccess.addTable('eventsession', EventSession, EventSessionCreate, EventSessionUpdate)
        self.dbAccess.addTable('topic', Topic, TopicCreate, TopicUpdate)
        self.dbAccess.addTable('file', File, FileCreate, FileUpdate)
        self.dbAccess.addTable('topicmemberlink', TopicMemberLink)

    def initializeDb(self, dburl):
        self.connectDb(dburl)
        SQLModel.metadata.create_all(self.dbAccess.engine)

    def connectDb(self, dburl):
        self.dbAccess.connectDb(dburl)

    # Create
    def addMember(self, name: str, position: str, active: bool = False):
        params = {
            'name': name, 
            'position': position,
            'active': active
        }
        return self.dbAccess.create('member', params)
    
    def addEventType(self, name: str):
        params = {
            'name': name
        }
        return self.dbAccess.create('eventtype', params)
    
    def addCategory(self, categoryName: str):
        params = {
            'name': categoryName
        }
        return self.dbAccess.create('category', params)
    
    def addEventSession(self, category_id: int, **keyValues):
        params = {
            'category_id': category_id
        }
        params.update(keyValues)
        return self.dbAccess.create('eventsession', params)
    
    def addTopic(self, eventsession_id: int, **keyValues):
        params = {
            'eventSession_id': eventsession_id
        }
        params.update(keyValues)
        return self.dbAccess.create('topic', params)
    
    def addFile(self, topic_id: int, *keyValues):
        params = {
            'topic_id': topic_id
        }
        params.update(keyValues)
        return self.dbAccess.create('file', params)
    
    def addTopicMember(self, topic_id: int, name: str):
        def selectByName(statement):
            statement.where(Member.name == name)
            return statement
        member = self.dbAccess.getone('member', selectByName)
        if member is not None:
            params = {
                'topic_id': topic_id,
                'member_id': member.id
            }
            self.dbAccess.create('topicmemberlink', params)
        else:
            log.warning(f'  Cannot add member {member} to topic, the member does not exist. Add the member first')
    
    # Read
    def findMembers(self, name: str|None = None, topic_id: int | None = None):
        pass
        
    def findEventTypes(self, categoryName: str|None = None):
        pass
    
    def findCategories(self, categoryName: str|None = None):
        pass
    
    def findEvents(self, category_id: int, 
                   name: str|None = None,
                   startTime: str|None = None, 
                   endTime: str|None = None):
        def selectFilter(statement):
            statement = statement.where(EventSession.category_id == category_id)
            if name is not None:
                statement = statement.where(EventSession.name.contains(name))
            if startTime is not None:
                mg = re.match(r'([\d]{4}-[\d]{2}-[\d]{2})', startTime)
                if mg is not None:
                    ds = datetime.date.fromisoformat(mg.group(0))
                    statement = statement.where(EventSession.date >= ds)
            if endTime is not None:
                mg = re.match(r'([\d]{4}-[\d]{2}-[\d]{2})', endTime)
                if mg is not None:
                    ds = datetime.date.fromisoformat(mg.group(0))
                    statement = statement.where(EventSession.date <= ds)
            return statement
        return self.getall('event', selectFilter)
    
    def findTopics(self, event_id: int):
        def selectFilter(statement):
            statement = statement.where(Topic.event_id == event_id)
            return statement 
        return self.getall('topic', selectFilter)

    def findTopicFiles(self, topic_id: int):
        def selectByTopicId(statement):
            statement = statement.where(TopicFileLink.topic_id == topic_id)
            return statement
        links = self.dbAccess.getall('topicfilelink', selectByTopicId)
        v = []
        for link in links:
            def selectByFileId(statement):
                statement = statement.where(File.id == link.file_id)
                return statement
            x = self.dbAccess.getone('file', selectByFileId)
            if x is not None:
                v.append(x)
        return v
    
sApp = App()
def getApp():
    global sApp
    return sApp

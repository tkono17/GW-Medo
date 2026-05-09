import os
import logging
import re
import datetime
import re
import dotenv
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
from ..model import Settings

log = logging.getLogger(__name__)

class App:
    def __init__(self):
        self.settings = Settings()
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

    def configFromEnv(self, envFile='.env'):
        dotenv.load_dotenv(envFile)
        vars = os.environ.keys()
        if 'GW_MEDO_DBTYPE' in vars:
            self.settings.DBTYPE = os.getenv('GW_MEDO_DBTYPE')
        if 'GW_MEDO_DBTYPE' in vars:
            self.settings.DBTYPE = os.getenv('GW_MEDO_DBTYPE')
        if 'GW_MEDO_FILESDIR' in vars:
            self.settings.FILESDIR = os.getenv('GW_MEDO_FILESDIR')

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
    
    def addEventSession(self, category_id: int, 
                        name: str, 
                        date: str, 
                        startTime: str, 
                        endTime: str, 
                        place: str|None = None, 
                        eventType_id: int|None = None):
        params = {
            'category_id': category_id,
            'name': name,
            'date': date,
            'startTime': startTime,
            'endTime': endTime
        }
        if place is not None:
            params.update({ 'place': place })
        if eventType_id is not None:
            params.update({ 'eventType_id': eventType_id })
        return self.dbAccess.create('eventsession', params)
    
    def addTopic(self, eventsession_id: int, 
                 name: str, 
                 duration: str, 
                 startTime: str, 
                 endTime: str, 
                 members: list[str]):
        params = {
            'eventSession_id': eventsession_id,
            'name': name,
            'duration': duration,
            'startTime': startTime,
            'endTime': endTime
        }
        topic = self.dbAccess.create('topic', params)
        for member in members:
            self.addTopicMember(topic.id, member)
        return topic
    
    def addFile(self, topic_id: int, name: str, path: str):
        params = {
            'topic_id': topic_id,
            'name': name,
            'path': path
        }
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
    def findMembers(self, name: str|None = None):
        def selector(statement):
            if name is not None:
                statement = statement.where(Member.name == name)
            return statement
        return self.dbAccess.getall('member', selector)
        
    def findEventTypes(self, name: str|None = None):
        def selector(statement):
            if name is not None:
                statement = statement.where(EventType.name == name)
            return statement
        return self.dbAccess.getall('eventtype', selector)
    
    def findCategories(self, categoryName: str|None = None):
        def selector(statement):
            if categoryName is not None:
                statement = statement.where(Category.name == categoryName)
            return statement
        return self.dbAccess.getall('category', selector)
    
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
        def selectById(statement):
            statement = statement.where(Topic.id == topic_id)
            return statement
        files = self.dbAccess.getall('file', selectById)
        v = []
        for f in files:
            def selectByFileId(statement):
                statement = statement.where(File.id == f.id)
                return statement
            x = self.dbAccess.getone('file', selectByFileId)
            if x is not None:
                v.append(x)
        return v
    
    def findTopicMembers(self, topic_id: int):
        def selectByTopicId(statement):
            statement = statement.where(TopicMemberLink.topic_id == topic_id)
            return statement
        links = self.dbAccess.getall('topicmemberlink', selectByTopicId)
        v = []
        for link in links:
            def selectById(statement):
                statement = statement.where(Member.id == link.member_id)
                return statement
            x = self.dbAccess.getone('file', selectById)
            if x is not None:
                v.append(x)
        return v
    
sApp = App()
def getApp():
    global sApp
    return sApp

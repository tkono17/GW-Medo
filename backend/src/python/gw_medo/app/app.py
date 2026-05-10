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
    def addMember(self, name: str, position: str, active: bool = True):
        log.info(f'  addMember: {name}, {position}, {active}')
        v = self.findMembers(name)
        if len(v)>0:
            log.warning(f'  Member {name} already exists')
            return None
        params = {
            'name': name, 
            'position': position,
            'active': active
        }
        return self.dbAccess.create('member', params)
    
    def addEventType(self, name: str):
        v = self.findEventTypes(name)
        if len(v)>0:
            log.warning(f'  Event type {name} already exists')
            return None
        params = {
            'name': name
        }
        return self.dbAccess.create('eventtype', params)
    
    def addCategory(self, name: str):
        v = self.findCategories(name)
        if len(v)>0:
            log.warning(f'  Category {name} already exists')
            return None
        params = {
            'name': name
        }
        return self.dbAccess.create('category', params)
    
    def addEventSession(self, category_id: int, 
                        name: str, 
                        date: str, 
                        startTime: str, 
                        endTime: str, 
                        place: str|None = None, 
                        eventType_id: int|None = None):
        v = self.findEventSessions(name=name, startDate=date, endDate=date)
        if len(v)>0:
            log.warning(f'  Event session {name} on {date} already exists')
            return None
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
    
    def addTopic(self, eventSession_id: int, 
                 name: str, 
                 duration: str, 
                 startTime: str, 
                 endTime: str, 
                 members: list[str]):
        v = self.findTopics(eventSession_id=eventSession_id, name=name)
        if len(v)>0:
            log.warning(f'  Topic {name} in event session {eventSession_id} already exists')
            return None
        params = {
            'eventSession_id': eventSession_id,
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
        v = self.findFiles(topic_id=topic_id, name=name)
        if len(v)>0:
            log.warning(f'  File {name} in topic {topic_id} already exists')
            return None
        params = {
            'topic_id': topic_id,
            'name': name,
            'path': path
        }
        return self.dbAccess.create('file', params)
    
    def addTopicMember(self, topic_id: int, name: str):
        member = None
        def selectByName(statement):
            statement = statement.where(Member.name == name)
            return statement
        member = self.dbAccess.getone('member', selectByName)
        if member is not None:
            def selectById(statement):
                statement = statement.where(TopicMemberLink.member_id == member.id)
                return statement
            v = self.dbAccess.getall('topicmemberlink', selectById)
            if v is not None or len(v)>0:
                log.warning(f'  Member {name} in topic {topic_id} already exists')
                return None
            params = {
                'topic_id': topic_id,
                'member_id': member.id
            }
            member = self.dbAccess.create('topicmemberlink', params)
        else:
            log.warning(f'  Cannot add member {member} to topic, the member does not exist. Add the member first')
        return member
    
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
    
    def findEventSessions(self, category_id: int|None = None, 
                   name: str|None = None,
                   startDate: str|None = None, 
                   endDate: str|None = None):
        def selectFilter(statement):
            if category_id is not None:
                statement = statement.where(EventSession.category_id == category_id)
            if name is not None:
                statement = statement.where(EventSession.name.contains(name))
            if startDate is not None:
                statement = statement.where(EventSession.date >= startDate)
            if endDate is not None:
                statement = statement.where(EventSession.date <= endDate)
            return statement
        return self.dbAccess.getall('eventsession', selectFilter)
    
    def findTopics(self, eventSession_id: int, name: str|None = None):
        def selectFilter(statement):
            statement = statement.where(Topic.eventSession_id == eventSession_id)
            if name is not None:
                statement = statement.where(Topic.name == name)
            return statement
        return self.dbAccess.getall('topic', selectFilter)

    def findTopicFiles(self, topic_id: int, name: str|None = None):
        def selectById(statement):
            statement = statement.where(File.topic_id == topic_id)
            if name is not None:
                statement = statement.where(File.name == name)
            return statement
        v = self.dbAccess.getall('file', selectById)
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

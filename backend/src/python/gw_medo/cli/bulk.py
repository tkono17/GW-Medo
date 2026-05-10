import os
import sys
from enum import Enum
import yaml
from typing import Any
import logging
import typer
import datetime

from appbasics import getEngine
from ..app import getApp

log = logging.getLogger(__name__)

tapp = typer.Typer()
app = getApp()

MembersTemplate = """Members:
  - name: Person A
    position: M1
  - name: Person B
    position: D2
    active: false
  - name: Person C
    position: NEET
  - name: Person D
    position: retired
"""
EventTypesTemplate = """EventTypes:
  - ミーティング
  - 研究会
  - 演習
  - リハーサル
"""
CategoriesTemplate = """Categories:
  - グループ 1
  - グループ 2
  - プロジェクト A
  - プロジェクト B
"""
EventSessionTemplate = """EventSession:
  name: 'Some event'
  date: '2026-05-10'
  startTime: '14:00:00'
  endTime: '15:30:00'
  category_id: 1
  eventType_id: 1
  #place: 'Some room'
  topics:
    - name: topic 1
      duration: 00:10:00
      members: 
        - Person A
    - name: topic 2
      duration: 00:20:00
      members:
        - Person B
    - name: topic 3
      duration: 00:20:00
      members:
        - Person C
        - Person D
"""

class BulkType(Enum):
    Members = 'Members'
    EventTypes = 'EventTypes'
    Categories = 'Categories'
    EventSession = 'EventSession'

def readYamlFile(fn: str) -> dict[str, Any]:
    data = None
    if os.path.exists(fn):
        with open(fn, 'r', encoding='utf8') as fin:
            data = yaml.load(fin, Loader=yaml.SafeLoader)
    else:
        log.warning(f'  Input YAML file {fn} does not exist')
    return data

@tapp.command('upload')
def upload(bulktype: str, filename: str) -> None:
    data = readYamlFile(filename)
    app.connectDb(app.settings.DBURL)
    if bulktype == BulkType.Members.value:
        members = data['Members']
        for member in members:
            name, position = member['name'], member['position']
            active = member['active'] if 'active' in member.keys() else True
            app.addMember(name, position, active)
    elif bulktype == BulkType.EventTypes.value:
        eventTypes = data['EventTypes']
        for eventType in eventTypes:
            app.addEventType(eventType)
    elif bulktype == BulkType.Categories.value:
        categories = data['Categories']
        for category in categories:
            app.addCategory(category)
    elif bulktype == BulkType.EventSession.value:
        event = data['EventSession']
        name, date, startTime, endTime = event['name'], event['date'], event['startTime'], event['endTime']
        category_id, eventType_id = event['category_id'], event['eventType_id']
        place = event['place'] if 'place' in event.keys() else None
        event1 = app.addEventSession(category_id=category_id, name=name, date=date, 
                            startTime=startTime, endTime=endTime, eventType_id=eventType_id,
                            place=place)
        if event1 is None:
            v = app.findEventSessions(name=name, startDate=date, endDate=date)
            if v is not None and len(v)==1:
                event1 = v[0]
        etime1 = datetime.datetime.fromisoformat(date + 'T' + endTime)
        topics = event['topics']
        for topic in topics:
            name, duration = topic['name'], topic['duration']
            members = topic['members']
            words = duration.split(':')
            dt = datetime.timedelta(minutes=1)
            if len(words)==1:
                h = int(words[0])
                dt = datetime.timedelta(hours=h)
            elif len(words)==2:
                h, m = int(words[0]), int(words[1])
                dt = datetime.timedelta(hours=h, minutes=m)
            elif len(words)==2:
                h, m, s = int(words[0]), int(words[1]), int(words[2])
                dt = datetime.timedelta(hours=h, minutes=m, seconds=s)
            else:
                log.warning(f'  duration must be in the form HH[:MM[:SS]], given value was {duration}')
            stime1 = etime1
            etime1 = stime1 + dt
            st1, et1 = stime1.time(), etime1.time()
            startTime = st1.strftime('%H:%M:%S')
            endTime = et1.strftime('%H:%M:%S')
            app.addTopic(eventSession_id=event1.id, 
                         name=name, duration=duration, startTime=startTime, endTime=endTime, members=members)

@tapp.command('download')
def download(bulktype: str, filename: str) -> None:
    pass

@tapp.command('template')
def template(bulktype: str, filename: str) -> None:
    data = ''
    if bulktype == BulkType.Members.value:
        data = MembersTemplate
    elif bulktype == BulkType.EventTypes.value:
        data = EventTypesTemplate
    elif bulktype == BulkType.Categories.value:
        data = CategoriesTemplate
    elif bulktype == BulkType.EventSession.value:
        data = EventSessionTemplate
    with open(filename, 'w', encoding='utf8') as fout:
        fout.write(data)
        log.info(f'{bulktype} template written to {filename}')

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    log.info(f'GW-Medoc bulk upload/download')
    app.configFromEnv()

    dburl = app.settings.DBURL
    if dburl is not None:
        app.connectDb(dburl)
        tapp()
    else:
        if sys.argv.count('--help')>0:
            tapp()
        else:
            log.error(f'DB file not found')

if __name__ == '__main__':
    main()
    
import typer
import logging
from ..app import getApp

log = logging.getLogger(__name__)
topic_app = typer.Typer()
app = getApp()

#------------------------------------------------------
# CLI for topic
#------------------------------------------------------
@topic_app .command('create')
def create(name: str):
    return app.addEvent(name)

@topic_app .command('find')
def find(name: str|None = None,
         startDate: str|None = None,
         endDate: str|None = None):
    return app.findEvents(name=name, startDate=startDate, endDate=endDate)

@topic_app .command('delete')
def delete(name: str):
    topics = app.findEvents()
    if len(topics)==1:
        app.delete(topics[0].id)

@topic_app .command('dump')
def dump():
    topics = app.findEvents()
    for topic in topics:
        log.info(f'  topic: {topic}')

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    app()

if __name__ == '__main__':
    main()

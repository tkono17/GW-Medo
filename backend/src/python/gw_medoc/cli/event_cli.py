import typer
import logging
from ..app import getApp

log = logging.getLogger(__name__)
event_app = typer.Typer()
app = getApp()

#------------------------------------------------------
# CLI for event
#------------------------------------------------------
@event_app .command('create')
def create(name: str):
    return app.addEvent(name)

@event_app .command('find')
def find(name: str):
    return app.findEvents(name)

@event_app .command('delete')
def delete(name: str):
    events = app.findEvents()
    if len(events)==1:
        app.delete(events[0].id)

@event_app .command('dump')
def dump():
    events = app.findEvents()
    for event in events:
        log.info(f'  event: {event}')

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    app()

if __name__ == '__main__':
    main()

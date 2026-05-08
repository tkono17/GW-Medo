import typer
import logging
from ..app import getApp

log = logging.getLogger(__name__)
file_app = typer.Typer()
app = getApp()

#------------------------------------------------------
# CLI for file
#------------------------------------------------------
@file_app .command('create')
def create(name: str):
    return app.addEvent(name)

@file_app .command('find')
def find(name: str|None = None,
         startDate: str|None = None,
         endDate: str|None = None):
    return app.findEvents(name=name, startDate=startDate, endDate=endDate)

@file_app .command('delete')
def delete(name: str):
    files = app.findEvents()
    if len(files)==1:
        app.delete(files[0].id)

@file_app .command('dump')
def dump():
    files = app.findEvents()
    for file in files:
        log.info(f'  file: {file}')

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    app()

if __name__ == '__main__':
    main()

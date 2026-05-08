import os, sys
import typer
import logging
import dotenv

from ..app import getApp
from ..tools import connectDb
from .db_cli import db_app
from .member_cli import member_app
from .category_cli import category_app
from .event_cli import event_app
from .topic_cli import topic_app
from .file_cli import file_app

log = logging.getLogger(__name__)
client_app = typer.Typer()

client_app.add_typer(db_app, name='db')
client_app.add_typer(member_app, name='member')
client_app.add_typer(category_app, name='category')
client_app.add_typer(event_app, name='event')
client_app.add_typer(topic_app, name='topic')
client_app.add_typer(file_app, name='file')

#------------------------------------------------------
# CLI
#------------------------------------------------------
app = getApp()

@client_app.command('addMember')
def addMember(name: str, position: str, active: bool = True):
    app.addMember(name, position, active) 

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    log.info(f'GW-Medoc client application')
    dotenv.load_dotenv('.env')
    dbfile = os.getenv('GW_MEDOC_DBFILE')
    log.info(f'  DB file: {dbfile}')

    if dbfile is not None:
        connectDb(dbfile)
        client_app()
    else:
        if sys.argv.count('--help')>0:
            client_app()
        else:
            log.error(f'DB file not found')

if __name__ == '__main__':
    main()

import os, sys
import typer
import logging
import dotenv

from appbasics import AppRunner, getEngine
from ..app import getApp, CliApp

log = logging.getLogger(__name__)

cliapp = CliApp(getApp())
runner = AppRunner(cliapp)

tapp = typer.Typer()

@tapp.command('initializeDb')
def initializeDb():
    cliapp.initializeDb('sqlite:///' + os.getenv('GW_MEDO_DBFILE'))

@tapp.command('macro')
def macro(macrofile: str):
    runner.run(macrofile)

@tapp.command('list')
def listCommands():
    cmds = runner.allCommands()
    log.info('List all commands:')
    for cmd in cmds:
        log.info(f'  - {cmd}')

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    log.info(f'GW-Medoc client application')
    dotenv.load_dotenv('.env')
    dbfile = os.getenv('GW_MEDO_DBFILE')
    dburl = 'sqlite:///' + dbfile
    log.info(f'  DB file: {dbfile} --> URL: {dburl}')

    if dburl is not None:
        log.info(f'  Engine before connect: {getEngine()}')
        cliapp.connectDb(dburl)
        log.info(f'  Engine in main: {getEngine()}')
        tapp()
    else:
        if sys.argv.count('--help')>0:
            tapp()
        else:
            log.error(f'DB file not found')

if __name__ == '__main__':
    main()

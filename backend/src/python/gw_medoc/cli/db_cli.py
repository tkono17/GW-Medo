import os
import logging
import typer
import sqlite3
from sqlmodel import SQLModel
from ..app import getApp

from ..tools import connectDb, getEngine
from .. import model

log = logging.getLogger(__name__)

db_app = typer.Typer()

@db_app.command('init')
def init(db_file):
    log.info('Initialize database')
    connectDb(db_file)
    SQLModel.metadata.create_all(getEngine())

@db_app.command('tables')
def tables(dbfile, show_columns: bool = False):
    log.info(f'Show tables in {dbfile}')
    connect_args = {
        'check_same_thread': False
    }
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
    tables = cursor.fetchall()
    for table in tables:
        print(f'  table: {table[0]}')
        if show_columns:
            statement = f'PRAGMA table_info({table[0]});'
            print(f'    {statement}')
            cursor.execute(statement)
            rows = cursor.fetchall()
            for row in rows:
                print(f'      {row}')
            statement = f'SELECT * FROM {table[0]};'
            cursor.execute(statement)
            rows = cursor.fetchall()
            for row in rows:
                print(f'    {row}')
    conn.close()

@db_app.command('getall')
def getall(tablename: str):
    app = getApp()
    v = app.getall(tablename)
    log.info(f'Get all entries in {tablename}')
    for x in v:
        log.info(f'  Entry {x}')

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(name)-20s %(levelname)-8s %(message)s')
    db_app()
    
if __name__ == '__main__':
    main()

import os
import typer
import logging
import dotenv

from .db_cli import app as db_app

log = logging.getLogger(__name__)
app = typer.Typer()

app.add_typer(db_app, name='db')

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    log.info(f'GW-Medoc server management')
    dotenv.load_dotenv()
    dbfile = os.getenv('GW_MEDOC_DBFILE')
    dburl = os.getenv('GW_MEDOC_DBURL')
    log.info(f'  DB file: {dbfile}, url={dburl}')
    app()

if __name__ == '__main__':
    main()

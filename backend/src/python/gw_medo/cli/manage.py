import os
import typer
import logging

from .db_cli import db_app
from ..app import getApp

log = logging.getLogger(__name__)
tapp = typer.Typer()

tapp.add_typer(db_app, name='db')

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    log.info(f'GW-Medoc server management')

    app = getApp()
    app.configFromEnv()
    app.connectDb(app.settings.DBURL)
    tapp()

if __name__ == '__main__':
    main()

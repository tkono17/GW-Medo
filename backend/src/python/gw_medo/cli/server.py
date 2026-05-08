import logging
import typer
import uvicorn
from ..main import app as webapp1

log = logging.getLogger(__name__)
cliapp = typer.Typer()
webapp = webapp1

def stringToLogLevel(sloglevel: str):
    level = logging.INFO
    match sloglevel:
        case 'DEBUG': level = logging.DEBUG
        case 'INFO': level = logging.INFO
        case 'WARNING': level = logging.WARNING
        case 'ERROR': level = logging.ERROR
    return level

@cliapp.command('server')
def startServer(host: str = 'localhost',
                port: int = 7611,
                log_level: str = 'INFO'):
    logging.basicConfig(level=stringToLogLevel(log_level))
    
    config = uvicorn.Config('gw_medo.cli.server:webapp',
                            host=host, port=port,
                            log_level='info')
    server = uvicorn.Server(config)
    server.run()

def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)-20s %(levelname)-8s %(message)s')
    log.info('Start server program')
    cliapp()

if __name__ == '__main__':
    main()

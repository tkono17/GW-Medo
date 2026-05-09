import logging
from dataclasses import dataclass, field
from typing import Optional

log = logging.getLogger(__name__)

@dataclass
class Settings:
    name: str = field(default='GW-Medo')
    version: Optional[str] = None
    DBTYPE: str = field(default='sqlite3')
    DBFILE: str = field(default='gwmedo.db')
    DBURL: str = field(default='sqlite:///gwmedo.db')
    FILESDIR: str = field(default='.files')

    def __post_init__(self):
        if self.DBTYPE in ('sqlite', 'sqlite3'):
            self.DBURL = 'sqlite:///' + self.DBFILE
            log.info(f'  Settings.DBURL is set to {self.DBURL}')

import typer
import logging
from ..app import getApp

log = logging.getLogger(__name__)
member_app = typer.Typer()
app = getApp()

#------------------------------------------------------
# CLI for member
#------------------------------------------------------
@member_app.command('create')
def create(name: str):
    return app.addMember(name)

@member_app.command('find')
def find(name: str):
    return app.findMembers(name)

@member_app.command('delete')
def delete(name: str):
    members = app.findMembers()
    if len(members)==1:
        app.delete(members[0].id)

@member_app.command('dump')
def dump():
    members = app.findMembers()
    for member in members:
        log.info(f'  member: {member}')

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    app()

if __name__ == '__main__':
    main()

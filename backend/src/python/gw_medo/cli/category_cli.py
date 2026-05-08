import typer
import logging
from ..app import getApp

log = logging.getLogger(__name__)
category_app = typer.Typer()
app = getApp()

#------------------------------------------------------
# CLI for category
#------------------------------------------------------
@category_app.command('create')
def create(name: str):
    return app.addCategory(name)

@category_app.command('find')
def find(name: str):
    return app.findCategories(name)

@category_app.command('delete')
def delete(name: str):
    categories = app.findCategories()
    if len(categories)==1:
        app.delete(categories[0].id)

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)6s %(message)s')
    app()

if __name__ == '__main__':
    main()

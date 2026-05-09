import logging

log = logging.getLogger(__name__)

#------------------------------------------------------
# Wrapped application for CLI
#------------------------------------------------------
class CliApp:
    def __init__(self, app):
        self.app = app
        self.initializeDb = self.app.initializeDb
        self.connectDb = self.app.dbAccess.connectDb
        self.create = self.app.dbAccess.create
        self.get = self.app.dbAccess.get
        #self.getall = self.app.dbAccess.getall
        #self.getone = self.app.dbAccess.getone
        self.update = self.app.dbAccess.update
        self.delete = self.app.dbAccess.delete

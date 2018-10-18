import db
import logging

class Mongo(db.Database):

    def __init__(self):
        self.logger = logging.getLogger()
        pass

    def detect_client(self):
        pass

    def do_backup(self):
        self.logger.info("Performing MongoDB Backup")
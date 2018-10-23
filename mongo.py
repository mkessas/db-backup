import db
import logging
from util import Util

class Mongo(db.Database):

    def __init__(self):
        self.logger = logging.getLogger()
        pass

    def detect_client(self):
        self.logger.info("Detecting MongoDB Client...")
        Util.run(["mongodump", "--version" ] )
        self.logger.info("mongodump found, continuing")


    def do_backup(self):
        self.logger.info("Performing MongoDB Backup...")

    def cleanup(self):
        pass


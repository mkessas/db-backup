import db
import logging
from util import Util

class Mongo(db.Database):

    def __init__(self, conf):
        self.logger = logging.getLogger()
        self.conf = conf

    def detect_client(self):
        self.logger.info("Detecting MongoDB Client...")
        Util.run(["mongodump", "--version" ] )
        self.logger.info("mongodump found")

    def backup_db(self, name):
        self.logger.info("Performing MongoDB Backup...")

    def backup_all_dbs(self):
        self.logger.info("Backing up all databases")
        pass

    def get_db_names(self):
        self.logger.info("Getting list of databases")
        return ""

    def cleanup(self):
        pass


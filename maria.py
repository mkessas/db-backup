import db
import logging
from util import Util


class Maria(db.Database):

    def __init__(self):
        self.logger = logging.getLogger()
        pass

    def detect_client(self):
        self.logger.info("Detecting Maria Client...")
        Util.run(["mysqldump", "--version" ] )
        self.logger.info("mysqldump found, continuing")


    def do_backup(self):
        self.logger.info("Performing Maria Backup...")

    def cleanup(self):
        pass
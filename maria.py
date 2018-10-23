import db
import logging
import time
from util import Util


class Maria(db.Database):

    def __init__(self, conf):
        self.logger = logging.getLogger()
        self.conf = conf

    def detect_client(self):
        self.logger.info("Detecting Maria Client...")
        Util.run(["mysqldump", "--version" ] )
        self.logger.info("mysqldump found")
        Util.run(["mysql", "--version" ] )
        self.logger.info("mysql found")


    def backup_db(self, db):
        self.logger.info("Backing up database '" + db + "'")
        
        tmpfile = self.conf.get("general", "tmp") + "/.backup-" + db + ".sql"

        start = time.time()
        cmd = ["mysqldump"] + self.conf.get('maria', 'options').split(" ") + [
            "-u", self.conf.get('maria','username'), 
            "-p" + self.conf.get('maria','password'), 
            "-h", self.conf.get('maria', 'hostname'), 
            db,
        ]

        data, err = Util.stream(cmd)


        with file(tmpfile, 'w') as fp:
            fp.write(data)

        if err == '':
            self.logger.info("Backup of '" + db + "' completed in " + str(time.time() - start) + " seconds")
            return None
        else:
            return err

    def backup_all_dbs(self):

        dbs, err = self.get_db_names()

        if err != '': 
            return err.rstrip()

        for db in dbs.rstrip().split('\n'):
            backup, err = self.backup_db(db)
            if err != '':
                self.logger.error(err.rstrip())
                continue

            print backup

    def get_db_names(self):
        self.logger.info("Retrieving list of databases...")
        dbs, err = Util.run(["mysql", "-u", self.conf.get('maria','username'), "-p" + self.conf.get('maria','password'), "-h", self.conf.get('maria', 'hostname'), "-se", "show databases"])
        
        if err == '': self.logger.debug("Database list: " + dbs.replace('\n', ' '))
        
        return dbs, err
        
    def cleanup(self):
        pass
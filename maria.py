import db
import logging
import time
from util import Util
from s3 import S3

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
        
        tmpfile = "backup-" + db + "-" + time.strftime('%Y%m%d', time.localtime()) + ".sql"
        start = time.time()
        cmd = ["mysqldump"] + self.conf.get('maria', 'options').split(" ") + [
            "-u", self.conf.get('maria','username'), 
            "-p" + self.conf.get('maria','password'), 
            "-h", self.conf.get('maria', 'hostname'), 
            db,
        ]

        stream = Util.stream(cmd)

        if self.conf.get("maria", "compress") == "true":
            tmpfile += ".gz"
            gzip = Util.stream(["gzip", "-9"], stream.stdout)
            stream.stdout.close()
            stream = gzip

        if self.conf.get("maria", "encrypt") == "true":
            tmpfile += ".enc"
            enc = Util.stream(["openssl", "enc", "-aes-256-cbc", "-k", self.conf.get("general", "key")], stream.stdout)
            stream.stdout.close()
            stream = enc

        aws = S3.stream(self.conf.get("maria","s3_bucket") + "/maria/" + tmpfile, stream.stdout)
        stream.stdout.close()
        
        err = aws.communicate()[1]

        if err == '':
            self.logger.info("Backup of '" + db + "' completed in " + str(time.time() - start) + " seconds")
            return None
        else:
            return err.strip()

    def backup_all_dbs(self):

        dbs, err = self.get_db_names()

        if err != '': 
            return err.rstrip()

        for db in dbs.rstrip().split('\n'):
            err = self.backup_db(db)
            if err != None:
                self.logger.error(err.strip())
                continue


    def get_db_names(self):
        self.logger.info("Retrieving list of databases...")
        dbs, err = Util.run(["mysql", "-u", self.conf.get('maria','username'), "-p" + self.conf.get('maria','password'), "-h", self.conf.get('maria', 'hostname'), "-se", "show databases"])
        
        if err == '': self.logger.debug("Database list: " + dbs.replace('\n', ' '))
        
        return dbs, err
        
    def cleanup(self):
        pass
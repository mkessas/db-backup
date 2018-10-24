import db
import logging
import time
import re
from util import Util
from s3 import S3

class Mongo(db.Database):

    def __init__(self, conf):
        self.logger = logging.getLogger()
        self.conf = conf

    def detect_client(self):
        self.logger.info("Detecting MongoDB Client...")
        Util.run(["mongodump", "--version" ] )
        self.logger.info("mongodump found")
        Util.run(["mongo", "--version" ] )
        self.logger.info("mongo found")


    def backup_db(self, db):
        self.logger.info("Backing up database '" + db + "'")
        
        tmpfile = "backup-" + db + "-" + time.strftime('%Y%m%d', time.localtime()) + ".sql"
        start = time.time()
        cmd = ["mongodump"] + self.conf.get('mongo', 'options').split(" ") + [
            "-u", self.conf.get('mongo','username'), 
            "-p", self.conf.get('mongo','password'), 
            "-h", self.conf.get('mongo', 'hostname'),
            "--archive=-",
            "--db",
            db,
        ]

        if self.conf.get("mongo", "compress") == "true":
            tmpfile += ".gz"
            cmd.append("--gzip")

        stream = Util.stream(cmd)

        if self.conf.get("mongo", "encrypt") == "true":
            tmpfile += ".enc"
            enc = Util.stream(["openssl", "enc", "-aes-256-cbc", "-k", self.conf.get("general", "key")], stream.stdout)
            stream.stdout.close()
            stream = enc

        aws = S3.stream(self.conf.get("mongo","s3_bucket") + "/" + tmpfile, stream.stdout)
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

        for db in dbs:
            err = self.backup_db(db)
            if err != None:
                self.logger.error(err.strip())
                continue


    def get_db_names(self):

        dbs = []

        self.logger.info("Retrieving list of databases...")
        
        echo = Util.stream(["echo", "'show dbs'"])
        stream = Util.stream([
            "mongo", 
            "-u", self.conf.get('mongo','username'),
            "-p", self.conf.get('mongo','password'),
            self.conf.get('mongo','hostname'),
            self.conf.get('mongo','options')
        ], echo.stdout)
        echo.stdout.close()
        
        data, err = stream.communicate()

        if err != '':
            return None, err

        for name in data.split('\n'):
            name = name.strip()
            match = re.match(r'^(\w+)\s+\d+\.\d+.B$', name)
            if match:
                dbs.append(match.group(1))

        self.logger.debug("Database list: " + ",".join(dbs))
        
        return dbs, err
        
    def cleanup(self):
        pass
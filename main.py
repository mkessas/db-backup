#!/usr/bin/env python

import ConfigParser
import argparse
import logging
import os
from colors import bcolors
from mongo import Mongo
from maria import Maria
from s3 import S3

def configure_logging(level):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level.upper())
    return logger

def parse_args():
    parser = argparse.ArgumentParser(description='''Perform database backups.
        Encrypts and sends the archive to an S3 destination.  
        Enforces a customisable retention period.''')
    parser.add_argument('--conf', type=str, dest='conf', default='backup.ini', help='Path to configuration file')
    return parser.parse_args()

def read_conf(file):
    parser = ConfigParser.SafeConfigParser()
    dataset = parser.read(file)
    if len(dataset) != 1:
        raise ValueError("Failed to read configuration file")
    return parser


# Parse command line arguments
args = parse_args()

# Parse configuration file
conf = read_conf(args.conf)
logger = configure_logging(conf.get("general", "level"))

s3 = S3()

# Perform Backup for each database engine
for name in [ "maria", "mongo" ]:

    if conf.get(name, "enabled") == "true":

        db = eval(name.capitalize() + "(conf)")

        try:
            db.detect_client()
        except:
            logger.error("Client for " + name + " not detected, skipping")
            continue

        # Validate S3 Bucket destination
        logger.info("Checking S3 bucket '" + conf.get(name, "s3_bucket") + "'")

        ret, err = s3.check_bucket(conf.get(name, "s3_bucket"))
        if err != '':
            logger.error("Bucket  not found: " + err.strip())
            exit(1)
        else:
            logger.info("Bucket found")
            
        if conf.get(name, "databases") == '*':
            err = db.backup_all_dbs()
            if err != '':
                logger.error(err)
                continue
        else:
            for name in conf.get(name, "databases").split(','):
                err = db.backup_db(name.rstrip())
                if err != None:
                    logger.error(err)


        db.cleanup()
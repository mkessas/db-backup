#!/usr/bin/env python

import ConfigParser
import argparse
import logging
import os
from colors import bcolors
from mongo import Mongo
from maria import Maria

mongo = Mongo()
maria = Maria()

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


args = parse_args()
parser = read_conf(args.conf)

logger = configure_logging(parser.get("general", "level"))

print "got here"
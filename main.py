#!/usr/bin/env python

import ConfigParser
from mongo import Mongo
from maria import Maria


mongo = Mongo()
maria = Maria()

parser = ConfigParser.ConfigParser()
parser.read("backup.ini")

print parser.get("general", "logfile")
print parser.items("general")
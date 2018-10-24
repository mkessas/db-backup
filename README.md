# Database Backup Script  [![Build status](https://9spokes.visualstudio.com/9Spokes/_apis/build/status/infra/db-backup)](https://9spokes.visualstudio.com/9Spokes/_build/latest?definitionId=74)

## Overview

This script is used to backup MariaDB and MongoDB databases on remote or local hosts and upload the archive to an S3 bucket destination.

The script uses a configuration file (by default `backup.ini` in the local directory) which can be passed using the `--conf=` command line argument.  A sample configuration file is found below for reference.

For both MariaDB and MongoDB, the backup is done using the native command line interface from the shell.  First the list of databases is acquired, then for each database, a separate backup file is created.  Individual databases can be selected in the `backup.ini` if a comma-separated list of database names is defined under the `databases` key in the respective section.

The script will optionally compress and/or encrypt the backup files as they are being streamed directly to the S3 destination.  If the destination folder under the designated S3 backup is missing, it will be automatically created.

For each database engine, additional command line parameters can be specified in the `options` key.  They are appended to the export/dump commands.

## Requirements

As the script starts, it will attempt to auto-detect the tools needed to perform the backup operation.  At the very least, the following should be available:

- Python 2.7 interpreter
- AWS CLI
- At least one of the `mariadb-client` or `mongodb-client` libraries

Additionally, the `aws` command needs to be pre-configured with the correct API key and secret to connect to the destination S3 bucket.  The script will attempt to list the contents of the bucket and will fail if this is not feasible.

Valid credentials for each database type are also required.  Read-only access is sufficient to initiate the backups

## Run

Below is a sample `backup.ini` used to backup both MariaDB and MongoDB in a development server:

```ini
[general]
level = debug ; info, error, and critical are also supported
key = ******  ; used to encrypt each backup file

[mongo]
enabled = true ; determins whether this database type is to be backed up or not
hostname = localhost
username = root
password = *****
databases = *   ; can be either '*' for all databases, or a comma-separated list of databases
compress = true ; activates gzip compression
options = --authenticationDatabase admin  ; additional command line arguments to mysqldump
encrypt = true  ; uses the 'key' in the 'general' section to encrypt the payload prior to streaming it
s3_bucket = 9spokes-db-ops/dev02/mongo ; the destination S3 bucket and subfolders

[maria]
enabled = true
username = backup
password = ********
hostname = 127.0.0.1
databases = *
encrypt = true
retention = 7
compress = true
options = --skip-lock-tables --single-transaction --routines --opt
s3_bucket = 9spokes-db-ops/dev02/maria

```

The resulting output is

```sh
$ python main.py
2018-10-24 16:27:19,312 INFO     Detecting Maria Client...
2018-10-24 16:27:19,324 INFO     mysqldump found
2018-10-24 16:27:19,341 INFO     mysql found
2018-10-24 16:27:19,342 INFO     Checking S3 bucket '9spokes-db-ops/dev02/maria'
2018-10-24 16:27:21,869 INFO     Bucket found
2018-10-24 16:27:21,870 INFO     Retrieving list of databases...
2018-10-24 16:27:22,058 DEBUG    Database list: 9spokes information_schema mysql performance_schema scripts shopify test
2018-10-24 16:27:22,059 INFO     Backing up database '9spokes'
2018-10-24 16:28:52,976 INFO     Backup of '9spokes' completed in 90.9162900448 seconds
2018-10-24 16:28:52,977 INFO     Backing up database 'information_schema'
2018-10-24 16:29:12,317 INFO     Backup of 'information_schema' completed in 19.3399701118 seconds
2018-10-24 16:29:12,318 INFO     Backing up database 'mysql'
2018-10-24 16:29:27,829 INFO     Backup of 'mysql' completed in 15.5111129284 seconds
2018-10-24 16:29:27,830 INFO     Backing up database 'performance_schema'
2018-10-24 16:29:52,150 INFO     Backup of 'performance_schema' completed in 24.3195621967 seconds
2018-10-24 16:29:52,151 INFO     Backing up database 'scripts'
2018-10-24 16:29:54,339 INFO     Backup of 'scripts' completed in 2.186866045 seconds
2018-10-24 16:29:54,340 INFO     Backing up database 'shopify'
2018-10-24 16:29:57,529 INFO     Backup of 'shopify' completed in 3.18860793114 seconds
2018-10-24 16:29:57,530 INFO     Backing up database 'test'
2018-10-24 16:30:00,939 INFO     Backup of 'test' completed in 3.40870404243 seconds
2018-10-24 16:30:00,940 INFO     Detecting MongoDB Client...
2018-10-24 16:30:01,022 INFO     mongodump found
2018-10-24 16:30:01,175 INFO     mongo found
2018-10-24 16:30:01,176 INFO     Checking S3 bucket '9spokes-db-ops/dev02/mongo'
2018-10-24 16:30:04,203 INFO     Bucket found
2018-10-24 16:30:04,204 INFO     Retrieving list of databases...
2018-10-24 16:30:04,871 DEBUG    Database list: 9spokes,admin,local,shopify
2018-10-24 16:30:04,872 INFO     Backing up database '9spokes'
2018-10-24 16:38:35,653 INFO     Backup of '9spokes' completed in 510.780964136 seconds
2018-10-24 16:38:35,654 INFO     Backing up database 'admin'
2018-10-24 16:38:38,061 INFO     Backup of 'admin' completed in 2.40630698204 seconds
2018-10-24 16:38:38,062 INFO     Backing up database 'local'
2018-10-24 16:38:40,219 INFO     Backup of 'local' completed in 2.15637111664 seconds
2018-10-24 16:38:40,219 INFO     Backing up database 'shopify'
2018-10-24 16:38:42,439 INFO     Backup of 'shopify' completed in 2.21865487099 seconds
```

## Todo

The script does not currently enforce a retention policy

## Bugs

None so far

## Authors

- Mourad Kessas
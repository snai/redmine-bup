#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# redmine-bup: A small Tool to backup existing redmine instances
# Copyright (C) 2014 Martin Grohmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Creative Commomns - Share Alike License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Creative Commons - Share Alike License for more details.
#
# You should have received a copy of the License along with this program.
# If not, see <https://creativecommons.org/licenses/by-sa/3.0/>

import yaml
import subprocess
import os
import shutil

REDMINE_DATABSE_CONFIG = '/var/lib/redmine/config/database.yml'
REDMINE_FILES_DIR = '/var/lib/redmine/files'
BACKUP_DIR = '/root/redmine.bak'
BACKUP_DIR_FILES = os.path.join(BACKUP_DIR, 'files/')
SQL_BACKUP_FILE = os.path.join(BACKUP_DIR, 'redmine.sql')

with open(REDMINE_DATABSE_CONFIG, "r") as f:
    redmine_db_config = yaml.load(f)

# Check if the backup directory exists, if not create it
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

adapter = redmine_db_config["production"]["adapter"]
database = redmine_db_config["production"]["database"]
host = redmine_db_config["production"]["host"]
username = redmine_db_config["production"]["username"]
password = redmine_db_config["production"]["password"]

if adapter == 'postgresql':
    os.environ["PGPASSWORD"] = password
    subprocess.call(['pg_dump', '-d', database, '-h', host, '-U', username,
                     '-Z', '9', '-f', SQL_BACKUP_FILE])
    del os.environ['PGPASSWORD']
elif adapter == 'mysql2':
    subprocess.call(['/usr/bin/mysqldump', '--user=', username, '--password=',
                     password, '--host=', host, database, ' > redmine.sql'])
elif adapter == 'sqlite3':
    shutil.copy2(database, SQL_BACKUP_FILE)

# Copy the redmine files to backup dir
shutil.copytree(REDMINE_FILES_DIR, BACKUP_DIR_FILES)

A small tool to backup Redmine Instances

## == Installation ==

Just copy the script file to desired location.
The run it manually with

```
python3 redmine-bup.py
```

or create a cron job; like

```
0 	0 	* 	* 	* python3 /root/redmine-bup.py 2>&1 /var/log/redmine-bup.log
```

## == Configuration ==

The database configuration is fetched from the `database.yml` file of the redmine installation.
Just configure `REDMINE_DATABSE_CONFIG` to point to the right location.
The script works with postgresql, mysql2 and sqlite3 databases. The right one is fetched from
the `database.yml` file as well.

Furthermore the `files` directory of the redmine installation needs to be configured with
`REDMINE_FILES_DIR`

## == To-Do ==

* backing up to a remote location
* snapshots
* restoring

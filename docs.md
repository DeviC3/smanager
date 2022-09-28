
# SystemManager docs

Starting application depends installation type. Recomended way is to add binary to ```bin``` path.
After downloading binary file (smanager) copy or symlink to ```/bin``` or ```/usr/bin```


```
ln -s /path/smanager /bin/smanager
path - is full path where You downloaded smanager i.e. /usr/local/smanager
```
and then call this from terminal just typing ```smanager``` to run app.

Application works with TAB autocomplete.

## Basic mode

It is active after entering to the ```smanager```. Commands :

1. show
- cpu   - actual percent od used CPU
- load  - load with 3 time values by minute (1/5/15)
- ram   - nice actual RAM usage
- disk  - amount of used disk space
- uptime - machine uptime
- users - who is logged into TTY and/or PTS
- services - all running services (nice systemd wrapper)
1. restart [service_name]   - restart service if configured
1. status [service_name]    - actual status of service
1. exit - exit from this mode to main menu

## File mode

Easy operations on files or directories. It is also have "easy" rsync like tool.

1. set
- source-path   - source path i.e. ```/home/user/path/```
- dest-path     - destination path i.e. ```/home/user/path/```
- server-username - name of user on remote machine
- server-address  - IP or hostname of remote machine
- exclude         - files/directories to exclude from rsync

You can also set this variables in ```rsync.conf``` file (store it in application directory)

1. sync - starting to sync configured files
1. remotesync - syncing files from remote localization to local system (source destination variable is on remote machine)
1. get - shows configured variables to sync
1. move - moving files/dirs on local machine (source -> destination)
1. copy - copy files on local machine (source -> destination)
1. copydir - moving directories on local machine (source -> destination)
1. deldir - deleting given directory
1. chown - changing owner i.e. when ```chown username /path/to/file``` chown will be username:username .../file
1. exit - exit from this mode to main menu

## Mysql mode

Opertions on mysql database

1. dump 
- all [filename] - dumping all databases to file
- singledb [dbname] - dumps single DB
- multipledb [db1 db2] - dumps multiple databases
- structure [dbname]- dumping only structure of database without data
- table [dbname tablename] - give name of database and table to dump
- version5 - use it when You want to migrate all DB from Mysql 5.x -> Mysql 8.0, it is dumping without unnecessary data
1. restore [file.sql] - restores data from .sql file
1. upgrade - wrapper of ```mysqld_safe --upgrade=FORCE```
1. exit - exit from this mode to main menu


## Network mode

1. scan [ip/hostname from_port-to_port]- it gives results in json format
1. check
- cert - checking if there is valid SSL connection with domain
- headers - checking for response headers
1. exit - exit from this mode to main menu

## PID mode

Some process information and manipulation

1. show
- top-cpu - top 5 long running processes with highest value of using CPU
- memory-usage [n]- processes which using more than n memory (n is value i.e. 250)
- opened-files - Which files is opened by which PID
- running-time - How long is running process (by name i.e, nginx)
- name - Type name of process, and return its number/s
- opened-ports - all opened remote(ethernet) connections
1. terminate [number] - sending SIGTERM signal to process ID (number)
1. kill [number] - sending SIGKILL signal to process ID (number)
1. list_all_services - showing all running pids
1. exit - exit from this mode to main menu

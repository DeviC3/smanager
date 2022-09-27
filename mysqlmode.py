from cmd import Cmd
import subprocess, logging

logging.basicConfig(filename='error.log', format='%(asctime)s - %(message)s - %(levelname)s', level=logging.INFO)

class MysqlMode(Cmd):

    doc_header = ' List of commands '
    ruler = '<?><?>'


    def dump_multipledb(self, dbname, *args):
        return ' '.join(dbname)


    def do_dump(self, user_value, *args):
        """Help with MySQL/MariaDB database dumping
        all [name of .sql file]           Dumping all databases
        singledb [name of database]       Only one database
        multipledb [dbname1 dbname2 ...]  More than one db
        structure [name of .sql file]     Dumping structure of db without data
        table [dbname tablename]          Dumping only one table from given database
        version5 [name of .sql file]      Dump old 5.7 version which will be restored to MySQL 8
        """
        try:
            args = user_value.split()

            get_args = {
                'all': lambda: subprocess.run(f'mysqldump --all-databases > {args[1]}', shell=True, capture_output=True),
                'singledb': lambda: subprocess.run(f'mysqldump --opt --routines {args[1]} > {args[1]}.sql ', shell=True, capture_output=True),
                'multipledb': lambda: subprocess.run(f'mysqldump --databases {self.dump_multipledb(args)} > multiple.sql'),
                'structure': lambda: subprocess.run(f'mysqldump --no-data {args[1]} > {args[1]}.sql', capture_output=True, shell=True),
                'table': lambda: subprocess.run(f'mysqldump {args[1]} {args[2]} > {args[2]}_table.sql', shell=True, capture_output=True),
                'version5': lambda: subprocess.run(f'mysqldump --opt --routines --ignore-table=mysql.innodb_index_stats --ignore-table=mysql.innodb_table_stats -A > {args[1]}.sql', capture_output=True, shell=True)
            }

            if args[0] in get_args:
                get_args[args[0]]()
        except Exception as e:
            print(e)
            logging.exception(e)


    def complete_dump(self, text, line, begidx, endidx):
        _AVAILABLE_SHOW = ('all', 'singledb', 'multipledb', 'structure', 'table', 'version5')
        return [i for i in _AVAILABLE_SHOW if i.startswith(text)]


    def do_restore(self, user_value, *args):
        """Help with MySQL/MariaDB database restoring
        file       Restore from .sql file
        """
        try:
            args = user_value.split()

            get_args = {
                'file': lambda: subprocess.run(f'mysql {args[1]} < {args[2]}.sql', capture_output=True, shell=True)
            }

            if args[0] in get_args:
                get_args[args[0]]()
        except Exception as e:
            print(e)
            logging.exception(e)


    def complete_show(self, text, line, begidx, endidx):
        _AVAILABLE_SHOW = ('file')
        return [i for i in _AVAILABLE_SHOW if i.startswith(text)]


    def do_upgrade(self, *args):
        """Upgrade MySQL database with force mode"""
        subprocess.run(f'mysqld_safe --upgrade=FORCE', capture_output=True, shell=True)

    def do_exit(self, *args):
        """Exit from this mode"""
        return True

    def emptyline(self):
        pass

    def default(self, *args):
        print('Unknown command, type help')

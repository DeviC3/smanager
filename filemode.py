from cmd import Cmd
from configparser import ConfigParser
import sysrsync, shutil, logging

logging.basicConfig(filename='error.log', format='%(asctime)s - %(message)s - %(levelname)s', level=logging.INFO)

class FileMode(Cmd):
    
    doc_header = ' List of commands '
    ruler = '<?><?>'

    config = ConfigParser(allow_no_value=True)
    config.read('rsync.conf')

    def do_set(self, new_value, *args):
        """Set new options to rsync"""
        try:
            args = new_value.split()

            setme = {
                'source-path': lambda: self.config.set('Directory', 'source', f'{args[1]}'),
                'dest-path': lambda: self.config.set('Directory', 'destination', f'{args[1]}'),
                'server-username': lambda: self.config.set('Server', 'username', f'{args[1]}'),
                'server-address': lambda: self.config.set('Server', 'ip', f'{args[1]}'),
                'exclude': lambda: self.config.set('Directory', 'exclude', f'{args[1]}'),
            }

            if args[0] in setme:
                setme[args[0]]()
                with open('rsync.conf', 'w+') as __file:
                    self.config.write(__file)
            else:
                print('Not found')
        except Exception as e:
            print(e)
            logging.exception(e)


    def complete_set(self, text, line, begidx, endidx):
        _AVAILABLE_SHOW = ('source-path', 'dest-path', 'server-address', 'server-username', 'exclude')
        return [i for i in _AVAILABLE_SHOW if i.startswith(text)]


    def do_sync(self, *args):
        """Synchronizing configured files (rsync.conf) from local to remote
        Files will be sent to remote destination directory configured in rsync.conf
        use set and get command for more
        """
        try:
            if self.config.get('Directory', 'options') == '':
                self.config.set('Directory', 'options', '-q')

            sysrsync.run(source=f"{self.config.get('Directory', 'source')}",
                destination=f"{self.config.get('Directory', 'destination')}",
                destination_ssh=f"{self.config.get('Server', 'username')}@{self.config.get('Server', 'ip')}",
                sync_source_contents=True,
                exclusions=self.config.get('Directory', 'exclude').split(','),
                options=self.config.get('Directory', 'options').split(','))
        except Exception as e:
            print(e)
            logging.exception(e)

    def do_remotesync(self, *args):
        """Synchronizing configured files (rsync.conf) from remote to local
        Files will be sent from remote to local destination directory configured in rsync.conf
        use set and get command for more
        """
        try:
            if self.config.get('Directory', 'options') == '':
                self.config.set('Directory', 'options', '-q')

            sysrsync.run(source=f"{self.config.get('Directory', 'source')}",
            destination=f"{self.config.get('Directory', 'destination')}",
            source_ssh=f"{self.config.get('Server', 'username')}@{self.config.get('Server', 'ip')}",
            sync_source_contents=True,
            exclusions=self.config.get('Directory', 'exclude').split(','),
            options=self.config.get('Directory', 'options').split(','))            
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_get(self, *args):
        """Show all configured info from rsync.conf"""
        try:
            print(f"""
            Source path - {self.config.get('Directory', 'source')}
            Destination path - {self.config.get('Directory', 'destination')}
            Username - {self.config.get('Server', 'username')}
            IP Address - {self.config.get('Server', 'ip')}
            Files to exclude - {self.config.get('Directory', 'exclude')}
            Used rsync options - {self.config.get('Directory', 'options')}
            """)
        except Exception as e:
            print(e)
            logging.exception(e)

### Other file/directory actions ###

    def do_move(self, values, *args):
        """move [source destination] - source -> dest"""
        try:
            args = values.split()
            shutil.move(args[0], args[1])
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_copy(self, values, *args):
        """copy [source destination] - source -> dest (only files)"""
        try:
            args = values.split()
            shutil.copy2(args[0], args[1], follow_symlinks=True)
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_copydir(self, values, *args):
        """copydir [source destination] - source -> dest"""
        try:
            args = values.split()
            shutil.copytree(args[1], args[2])
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_deldir(self, values, *args):
        """deldir [dirname] - deletes directory recursively"""
        try:
            args = values.split()
            shutil.rmtree(args[0])
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_chown(self, values, *args):
        """owner [path user group] - changes chown, default group is same as username"""
        try:
            args = values.split()
            shutil.chown(args[0], args[1], args[2])
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_exit(self, *args):
        """Exit from this mode"""
        return True

    def emptyline(self):
        pass

    def default(self, *args):
        print('Unknown command, type help')

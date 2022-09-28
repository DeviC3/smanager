from cmd import Cmd
from basiccommands import *
from filemode import *
from pidmode import *
from mysqlmode import *
from networkmode import *

class CoreCommands(Cmd, UserCommands):
    
    def do_quit(self, *args):
        """Quit from application"""
        print ("Logging off :(")
        raise SystemExit
    
    def do_exit(self, *args):
        """Quit from application"""
        print ("Logging off :(")
        raise SystemExit


    def emptyline(self):
        pass


    def default(self, *args):
        print('Unknown command, type help')

    def do_filemode(self, *args):
        """Enter in file mode - use rsync and local files manipulation"""
        __newshell = FileMode()
        __newshell.prompt = self.prompt[:1] + '(files): '
        __newshell.cmdloop()

    def do_pid(self, *args):
        """Enter in pid mode to look on working processes"""
        __newshell = PidMode()
        __newshell.prompt = self.prompt[:1] + '(PID): '
        __newshell.cmdloop()

    def do_mysql(self, *args):
        """Enter in mysql mode to work with this database"""
        __newshell = MysqlMode()
        __newshell.prompt = self.prompt[:1] + '(msql): '
        __newshell.cmdloop()

    def do_networking(self, *args):
        """Enter in network mode to manage networking module"""
        __newshell = NetworkMode()
        __newshell.prompt = self.prompt[:1] + '(net): '
        __newshell.cmdloop()
from cmd import Cmd
from datetime import datetime
from signal import SIGKILL, SIGTERM, signal
import psutil, os, subprocess, logging

logging.basicConfig(filename='error.log', format='%(asctime)s - %(message)s - %(levelname)s', level=logging.INFO)

class PidMode(Cmd):

    doc_header = ' List of commands '
    ruler = '<?><?>'

    def check_used_ports(self, *args):
        subprocess.run('lsof -Pi', stdout=True, shell=True)

    def memory_usage(self, amount: int, *args):
        
        for p in psutil.process_iter(['name', 'memory_info']):
            if p.info['memory_info'].rss > amount * 1024 * 1024:
                print(f"PID: {p.pid} Name: {p.info['name']} Usage: {p.info['memory_info'].rss} bytes of RAM")
            

    def top_cpu(self, *args):

        for p in sorted(psutil.process_iter(['name', 'cpu_times']), key=lambda p: sum(p.info['cpu_times'][:2]))[-5:]:
            print(f"Pid number:{p.pid} - Name: {p.info['name']} -  {sum(p.info['cpu_times'])}")        


    def opened_files(self, filename, *args):

        for p in psutil.process_iter(['name', 'open_files']):
            for file in p.info['open_files'] or []:
                if file.path.endswith(f'{filename}'):
                    print(f"Pid name: {p.pid} - {p.info['name']} - {file.path}")


    def get_is_running(self, name, *args):

        for p in psutil.process_iter(['name']):
            if p.info['name'] == name:
                print(f"Process: {p.info['name']} exists with PID - {p.pid}")


    def get_proc_time(self, name, *args):

        for p in psutil.process_iter(['name', 'create_time']):
            if p.info['name'] == name:
                print(f"Process: {p.info['name']} - started at: {datetime.fromtimestamp(p.info['create_time']).strftime('%Y-%m-%d %H:%M:%S')}") 


    def do_list_all_services(self, *args):
        """Show all services with PID and name"""
        try:
            for proc in psutil.process_iter():
                print(f"{proc.pid} - {proc.name()}")
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_show(self, user_value, *args):
        """Lookup for PID information
        top-cpu		    Top 5 long running processes with highest value of using CPU
        memory-usage	Processes which using more than n memory (n is value from user)
        opened-files    Which files is opened by which PID
        running-time    How long is running process (by name i.e, nginx)
        name            Type name of process, and return its number/s
        opened-ports    All opened remote(ethernet) connections
        """
        try:
            args = user_value.split()

            list_pids = {
                'top-cpu': lambda: self.top_cpu(),
                'memory-usage': lambda: self.memory_usage(int(args[1])),
                'opened-files': lambda: self.opened_files(args[1]),
                'running-time': lambda: self. get_proc_time(args[1]),
                'name': lambda: self.get_is_running(args[1]),
                'opened-ports': lambda: self.check_used_ports()
            }

            if args[0] in list_pids:
                list_pids[args[0]]()
        except Exception as e:
            print(e)
            logging.exception(e)


    def complete_show(self, text, line, begidx, endidx):
        _AVAILABLE_SHOW = ('top-cpu', 'memory-usage', 'opened-files', 'running-time', 'name', 'opened-ports')
        return [i for i in _AVAILABLE_SHOW if i.startswith(text)]


    def do_terminate(self, name, *args):
        """Sending SIGTERM to process id"""
        try:
            os.kill(int(name), SIGTERM)
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_kill(self, name, *args):
        """Sending SIGKILL to process id"""
        try:
            os.kill(int(name), SIGKILL)
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
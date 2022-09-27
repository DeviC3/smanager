import subprocess, os, psutil, time, logging

logging.basicConfig(filename='error.log', format='%(asctime)s - %(message)s - %(levelname)s', level=logging.INFO)

class UserCommands():

    def get_cpu(self, *args):
        print(f'All CPUs usage - {psutil.cpu_percent(interval=None, percpu=False)} %')

    def get_load(self, *args):
        __result = f"""
        Load from 1 minute / 5 minutes / 15 minutes:
        {psutil.getloadavg()}
        """
        print(__result)

    def get_ram(self, *args):

        show_ram_usage = f"""
        Total - {round(psutil.virtual_memory().total / (1024 ** 3), 3)} GB
        Free - {round(psutil.virtual_memory().free / (1024 ** 3), 3)} GB
        Active - {round(psutil.virtual_memory().active / (1024 ** 3), 3)} GB
        Cache - {round(psutil.virtual_memory().cached / (1024 ** 3), 3)} GB
        Inactive - {round(psutil.virtual_memory().inactive / (1024 ** 3), 3)} GB
        """
        print(show_ram_usage)

    def get_disk(self, *args):

        disk_info = f"""
        Total disk- {round(psutil.disk_usage('/').total / (1024 ** 3), 4)} GB
        Using - {round(psutil.disk_usage('/').used / (1024 ** 3), 4)} GB
        Free - {round(psutil.disk_usage('/').free / (1024 ** 3), 4)} GB
        Percent usage - {psutil.disk_usage('/').percent} %
        """
        print(disk_info)


    def get_uptime(self, *args):
        
        uptime_info = f"""
        Hour's running - {time.strftime('%H:%M:%S', time.gmtime(time.time() - psutil.boot_time()))}
        Running from - {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(psutil.boot_time()))}
        """

        print(uptime_info)
        

    def show_logged_users(self, *args):
        print(psutil.users())


    def show_all_active_services(self, *args):
        cmd2 = 'systemctl list-units --type=service --state=masked'
        print(subprocess.run('systemctl list-units --type=service', shell=True, stdout=True))


    def do_show(self, user_value, *args):
        """Shows hardware and system info
        cpu         Amount of used CPU (now)
        load        Actual machine load
        ram         RAM info
        disk        Disk usage
        uptime      Pretty uptime info
        users       Logged users to tty/pts
        services    Show all running/failed services from systemd
        """
        try:
            args = user_value.split()

            all_show = {
                'cpu': lambda: self.get_cpu(),
                'load': lambda: self.get_load(),
                'ram': lambda: self.get_ram(),
                'disk': lambda: self.get_disk(),
                'uptime': lambda: self.get_uptime(),
                'users': lambda: self.show_logged_users(),
                'services': lambda: self.show_all_active_services()
            }

            if args[0] in all_show:
                all_show[args[0]]()
            else:
                print('Command not found')
        except Exception as e:
            print(e)
            logging.exception(e)


    def complete_show(self, text, line, begidx, endidx):
        _AVAILABLE_SHOW = ('cpu', 'load', 'ram', 'disk', 'uptime', 'users', 'services')
        return [i for i in _AVAILABLE_SHOW if i.startswith(text)]


    def do_restart(self, *args):
        """Restart given service"""
        try:
            if os.getuid() != 0:
                print('You need more permissions')
            else:
                subprocess.getoutput(f'systemctl restart {args[0]}')
        except Exception as e:
            print(e)
            logging.exception(e)


    def do_status(self, *args):
        """Checking status of given service"""
        try:
            subprocess.getoutput(f'systemctl status {args[0]}')
        except Exception as e:
            print(e)
            logging.exception(e)

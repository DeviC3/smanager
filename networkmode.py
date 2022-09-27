from cmd import Cmd
import subprocess, logging, nmap, requests, json

logging.basicConfig(filename='error.log', format='%(asctime)s - %(message)s - %(levelname)s', level=logging.INFO)

class NetworkMode(Cmd):
    
    def do_scan(self, value, *args):
        """Scanning given hostname/IP address for open ports. Results is in json
        scan [hostname/ip] [port number from] [port number to] (i.e. scan 1.1.1.1 1-100)
        """
        try:
            args = value.split()
            n = nmap.PortScanner()
            results = json.dumps(n.scan(args[0], f'{args[1]}-{args[2]}'), indent=2)
            return print(results)
        except Exception as e:
            print(e)


    def checkcert(self, values, *args):
        args = values.split()
        if requests.get(f'https://{values}').status_code == 200:
            return print('Connection is secure')


    def checkhdrs(self, values, *args):
        args = values.split()
        response = requests.get(f'https://{values}').headers
        modify = json.dumps(dict(response), indent=2)
        print(modify)


    def do_check(self, values, *args):
        """Check hostnames and IPs
        cert    show if connection is secured by valid https
        """
        try:
            args = values.split()

            list_checks = {
                'cert': lambda: self.checkcert(args[1]),
                'headers': lambda: self.checkhdrs(args[1])
            }

            if args[0] in list_checks:
                list_checks[args[0]]()
        except Exception as e:
            print(e)
            logging.exception(e)


    def complete_check(self, text, line, begidx, endidx):
        _AVAILABLE_SHOW = ('cert', 'headers')
        return [i for i in _AVAILABLE_SHOW if i.startswith(text)]

    def do_exit(self, *args):
        """Exit from this mode"""
        return True

    def emptyline(self):
        pass

    def default(self, *args):
        print('Unknown command, type help')
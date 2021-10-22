# Modules
from colorama import Style, Fore        # Colored text
from icecream import ic                 # Debugging
from json import dump                   # Json Output
from nmap import PortScanner            # Nmap official library

from nmap.nmap import PortScannerError

# ic.disable()    # Disable debugging by default


# Main Code:
class Nmapper(PortScanner):

    def __init__(self, target: str, port: str, technique: str, output: str = None, verbose: bool = False):
        self.TARGET = ic(target)
        self.PORT = ic(port)
        self.OUTPUT_FILE = ic(output)
        self.VERBOSE = ic(verbose)
        self.nm = PortScanner()

        try:
            if technique == '-sT':
                self.data = ic(self).tcp_scan()
            elif technique == '-sU':
                self.data = self.udp_scan()
            elif technique == '-sP':
                self.data = self.icmp_scan()
            elif technique == '-sS':
                self.data = self.syn_scan()
            elif technique == '-sN':
                self.data = self.noisy_scan()
            else:
                self.data = self.tcp_scan()

            self.stdout()
        except KeyboardInterrupt:
            exit(f'{Fore.RED}[!]{Style.RESET_ALL} User terminated the program (ctrl + c)')
        except PortScannerError as err:
            if args.debug:
                exit(f"{Fore.RED}[!]{Style.RESET_ALL} {err}")
            if 'root' in str(err):
                exit(f'{Fore.RED}[!]{Style.RESET_ALL} This scan type requires root privileges')
            else:
                exit(f'{Fore.RED}[!]{Style.RESET_ALL} Error while scanning the target')
                


    ''' TCP Scan '''
    def tcp_scan(self):
        results: dict = self.nm.scan(self.TARGET, self.PORT, arguments='-sT -sV')
        return ic(results)

    ''' UDP Scan '''
    def udp_scan(self):
        results: dict = self.nm.scan(self.TARGET, self.PORT, arguments='-sU -sV')
        return ic(results)

    ''' Host Discovery Scan '''
    def icmp_scan(self):
        results: dict = self.nm.scan(self.TARGET, arguments='-sP -sV')
        return ic(results)

    ''' SYN Scan '''
    def syn_scan(self):
        results: dict = self.nm.scan(self.TARGET, self.PORT, arguments='-sS -sV')
        return ic(results)

    ''' Fully Aggressive Scan '''
    def noisy_scan(self):
        results: dict = self.nm.scan(self.TARGET, self.PORT, arguments='-sT -A -sV -T4')
        return ic(results)

    ''' Send results to stdout '''
    def stdout(self):
        try:
            if self.data['nmap']['scaninfo']['error']:
                exit(Fore.RED + self.data['nmap']['scaninfo']['error'][0].replace('\\n', ''))
        except KeyError:
            pass


        if self.OUTPUT_FILE:
            self.json_output()
            
        self.data: dict = self.data['nmap']['scanstats']

        print('-'*40)
        print(f"{self.data['timestr']} - Elapsed time: {self.data['elapsed']}")
        print(f"Found {self.data['uphosts']} hosts actives of {self.data['totalhosts']} hosts scanned.")
        print('-'*40)
        for target in self.nm.all_hosts():
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Host: {target} {self.nm[target].hostname()}")
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Status: {self.nm[target].state()}\n")

            ''' Sort port numbers '''
            for protocol in self.nm[target].all_protocols():
                port_list = list(self.nm[target][protocol].keys())
                port_list.sort()

                ''' Show port status, protocol & service '''
                for port in ic(port_list):
                    port_info = self.nm[target][protocol][port]
                    ic(port_info)
                    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Port: {port:>5}/{protocol}\t{port_info['state']}\t{port_info['name']}") if not self.VERBOSE else print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Port: {port:>5}/{protocol}\t{port_info['state']}\t{port_info['name']}\t {port_info['product']} {port_info['version']}")

        
    ''' Output results to external JSON file '''
    def json_output(self):
        with open(self.OUTPUT_FILE + '.json', 'w') as output:
            dump(self.data, output, indent=4)
            output.write('\n')


if __name__ == '__main__':

    import argparse                     # CLI Arguments

    parser = argparse.ArgumentParser()
    # Debug
    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        required=False
    )

    # Target
    parser.add_argument(
        dest='target',
        metavar='TARGET',
        help='Target specification',
    )

    # Port
    parser.add_argument(
        '-p', '--port',
        dest='port',
        metavar='RANGE',
        help='Port range specification',
        default='1-65535',
        required=False
    )

    # TCP Scan
    parser.add_argument(
        '-sT', '--tcp-scan',
        dest='technique',
        help='Runs a TCP Scan',
        action='store_const',
        const='-sT',
        required=False
    )

    # UDP Scan
    parser.add_argument(
        '-sU', '--udp-scan',
        dest='technique',
        help='Runs a UDP Scan',
        action='store_const',
        const='-sU',
        required=False
    )

    # ICMP Scan
    parser.add_argument(
        '-sP', '--ping-scan',
        dest='technique',
        help='Runs a ICMP Scan',
        action='store_const',
        const='-sP',
        required=False
    )

    # SYN Scan
    parser.add_argument(
        '-sS', '--syn-scan',
        dest='technique',
        help='Runs a SYN/Stealth Scan',
        action='store_const',
        const='-sS',
        required=False
    )

    # Noisy Scan
    parser.add_argument(
        '-sN', '--noisy-scan',
        dest='technique',
        help='Runs a "Noisy" Scan (might draw attention)',
        action='store_const',
        const='-sN',
        required=False
    )

    # Verbose
    parser.add_argument(
        '-v', '--verbose',
        dest='verbose',
        action='store_true',
        help='Enables detailed information (verbose mode)',
        default=False,
        required=False
    )

    # Output
    parser.add_argument(
        '--output',
        dest='output',
        help='Output results to external file',
        type=str,
        metavar='FILE',
        required=False
    )

    args = parser.parse_args()

    ic.configureOutput(prefix='[DEBUG] ')
    ic.enable() if args.debug else ic.disable()

    nmapper = Nmapper(args.target, args.port, args.technique, args.output, args.verbose)
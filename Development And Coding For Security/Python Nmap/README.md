# Custom Python Portscanner
Custom python portscanner developed using **python-nmap** library. It has a few custom functions such as Intensive Fast Scan a.k.a. Noisy Scan. Once the scan has finished the user will get the results showing useful information, like current time, elapsed scan time, found hosts & ports and their states.

![Nmap results example](https://user-images.githubusercontent.com/64245567/138417446-f79d1d1e-343c-4cf0-b374-3b99f0c3bf40.png)

## Dependencies:
 - Colorama (for colored output)
 - Icecream (for debugging function)
 - Python-nmap (for host scanning)

## Techniques:
 - TCP Scan
 - UDP Scan
 - ICMP Scan
 - SYN (Stealth) Scan
 - Noisy Scan (custom)

## How to use:

If the user does not provide any options, the script will start a Full TCP Scan on every all ports (1-65535).
Some scan techniques require root privileges (UDP/TCP/SYN/ICMP) and will not work on non-privileged users.

To scan a target, simply use the command `$ python nmap_scanner.py <options> <target>`:
  
  `$ python nmap_scanner.py -p 2000-3000 <target>`
  
Note that it's possible to set a custom port range by using `-p` option, otherwise all ports will be scanned.

It's also possible to check service version by using the `-v` or `--verbose` flag, like so:

  `$ python nmap_scanner.py -sN localhost --verbose`
  
  ![Verbose flag demonstration](https://user-images.githubusercontent.com/64245567/138424013-d8dc24d9-1bb7-439a-8d2b-67fc759c8371.png)

The script also allows the user to scan a network range, for instace, by passing the range instead of a hostname or address:

  `S python nmap_scanner.py -sP 192.168.0.1/24`
  
  ![Host discovery scan results](https://user-images.githubusercontent.com/64245567/138426469-08a8d55b-b3ce-4211-8a47-05f159a010a0.png)
  
The **Noisy Scan** is a custom feature which enables all aggressive flags on the scanner, it's called Noisy as it will make "noise" on the network and might draw unwanted attention.
  

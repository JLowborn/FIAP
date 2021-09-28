#!/usr/bin/env python3

''' ROT Cipher Custom API '''

# Modules
import requests
import re

# Color variables
BOLD = '\033[1m'
RED = '\033[91m'
ENDC = '\033[0m'

# Main Code
api = "http://theblob.org/rot.cgi?text=" # api url for rotating
tag_re = re.compile(r'<[^>]+>') # regex for removing html tags

def banner():
    print(f''' {BOLD}
                             ____       _   __  __
                            |  _ \ ___ | |_|  \/  | ___
                            | |_) / _ \| __| |\/| |/ _ \\
                            |  _ | (_) | |_| |  | |  __/
                            |_| \_\___/ \__|_|  |_|\___|
                                    By {RED}Rebellion{ENDC}
    ''')

def main():

    try:
        while True:
            phrase = input(f"[-] Phrase to rotate: ")
            response = requests.get(api + phrase.strip())

            print(tag_re.sub('', response.text)) # Remove HTML tags from response
    except KeyboardInterrupt:
        print('\n\n\t\tBye ;)')
    except requests.ConnectionError:
        print(f"{RED}[!] {ENDC}Check internet connection!")

if __name__ == '__main__':
    banner()
    main()
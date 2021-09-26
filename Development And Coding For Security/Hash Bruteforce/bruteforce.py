''' Blowfish (BCrypt) Hash Bruteforce '''

# Modules
import argparse                                     # Parse arguments
from crypt import crypt                             # Hash password
from pathlib import Path                            # Check files existence


# NOTE: In order for the program to works, it requires a hashfile
# just create a custom name file containing the hash


# Main Code
''' Parse arguments, both hash and wordlist are required '''
parser = argparse.ArgumentParser()
parser.add_argument('--wordlist',
                    help='Path to wordlist',
                    metavar='PATH', dest='wordlist',
                    required=True)
parser.add_argument('--hashfile',
                    help='Hash file to bruteforce',
                    metavar='FILE', dest='hashfile',
                    required=True)
args = parser.parse_args()

''' Check files existence '''
wordlist = args.wordlist if Path(args.wordlist).is_file() else exit("[!] Wordlist doesn't seen to exist!")
hashfile = args.hashfile if Path(args.hashfile).is_file() else exit("[!] Hash file doesn't seen to exist!")

''' Parse hash file '''
hashes = open(hashfile).read().split('\n')

''' Bruteforce hash '''
try:
    valid_hashes = 0
    for _hash in hashes:
        if '$' in _hash:
            valid_hashes += 1
            with open(wordlist) as wordlist:
                for passwd in wordlist:
                    print(f'[+] Trying password: {passwd.strip()}')
                    if crypt(passwd.strip(), _hash) == _hash: exit(f"[+] Found password: {_hash} -> {passwd}")
            exit("[+] Couldn't find the password for given hash")
    if valid_hashes == 0:
        exit("[-] No valid hashes found!")
except KeyboardInterrupt:
    exit('[!] User terminated the program')
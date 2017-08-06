import os, sys
from Crypto.Cipher import AES

fn = sys.argv[1]
data = open(fn,'rb').read()

# Secure CTR mode encryption using random key and random IV, taken from
# http://stackoverflow.com/questions/3154998/pycrypto-problem-using-aesctr
secret = os.urandom(16)
crypto = AES.new(os.urandom(32), AES.MODE_CTR, counter=lambda: secret)

encrypted = crypto.encrypt(data)
open(fn+'.enc','wb').write(encrypted)


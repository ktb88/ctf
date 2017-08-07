from Crypto.Cipher import AES
import base64
import random, string

def get_iv():
    iv = ""
    random.seed(1497950081+60*60*7)
    for i in range(0,16):
        iv += random.choice(string.letters + string.digits)
    return iv

def decrypt(m, p, i):
    aes = AES.new(p, AES.MODE_CFB, i)
    return aes.decrypt(base64.b64decode(m))

k = "Hb8jnSKzaNQr5f7p"
target = "f09086061f03f080d0851d9154e11653.png"

data = open(target, "rb").read().split("IEND")[1:]
data[0] = data[0][5:]

c_data = data[0]
for i in range(1, len(data)):
    c_data += "IEND" + data[i]
data = decrypt(c_data, k, get_iv())

fd = open("flag.png","wb")
fd.write(data)
fd.close()
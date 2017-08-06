from Crypto.Cipher import AES
import base64
import random, string, sys, os, time

k = "Hb8jnSKzaNQr5f7p"
target = "78d14f37ae413511b119776c2294c414.png"

print os.path.getmtime(target)

def get_iv(i):
    iv = ""
    random.seed(1497950081+i+60*60*7)
    for i in range(0,16):
        iv += random.choice(string.letters + string.digits)
    return iv

def decrypt(m, p, i):
    aes = AES.new(p, AES.MODE_CFB, i)
    return aes.decrypt(base64.b64decode(m))

def find_images():
    i = []
    #for r, d, f in os.walk(os.environ['HOME']):
    for r, d, f in os.walk("."):
        for g in f:
            if g.endswith(".png"):
                i.append((os.path.join(r, g)))
    return i

c_data = open("dump", "rb").read()

data = decrypt(c_data, k, get_iv(0))
fd = open("res.png","wb")
fd.write(data)
fd.close()

exit()

for i in range(0, 10000000):
    if i % 100 == 0:
        print i

    data = decrypt(c_data, k, get_iv(i))
    if data[1:4] == "PNG":
        print "FOUND : %d" % (i)
        fd = open("res.png","w")
        fd.write(data)
        fd.close()
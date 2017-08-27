import base64
import hashlib
from PIL import Image

def encode(s):
    return (''.join([ chr(ord(c)+4) for c in s[::-1] ]))

def base64encode(s):
    return base64.b64encode(s.encode("utf8")).decode("utf8")

def check_one(ch):
    b64_flag = base64encode(ch)
    encrypted_flag = ""
    temp_str = ""

    for i in b64_flag:
        temp_str += i
        encrypted_flag += encode(temp_str)

    #print(encrypted_flag)
    pixels_list = []

    for i in encrypted_flag:
        m = hashlib.md5()
        m.update(i)
        m = m.hexdigest()
        m = int(m, 16)
        m = str(hex(m))
        for j in range(0, len(m)-3, 3):
            pixels_list.append((128 + ord(m[j])^ord(m[j+1]), 128 + ord(m[j+1])^ord(m[j+2]), 128 + ord(m[j+2])^ord(m[j+3])))

    return pixels_list

def enc(msg):
    b64_flag = base64encode(msg)
    encrypted_flag = ""
    temp_str = ""
    for i in b64_flag:
        temp_str += i
        encrypted_flag += encode(temp_str)

    return encrypted_flag

img = Image.open("digest.png", "r")
(width, height) = img.size
enc_data = img.getdata()

# flag = "d4r"
# flag = "d4rk{n"
# flag = "d4rk{no00"
# flag = "d4rk{no00000"
# flag = "d4rk{no00000oo_"
# flag = "d4rk{no00000oo_not"
# flag = "d4rk{no00000oo_not0x_"
# flag = "d4rk{no00000oo_not0x_myf"
# flag = "d4rk{no00000oo_not0x_myfaUl"
# flag = "d4rk{no00000oo_not0x_myfaUltXX"
# flag = "d4rk{no00000oo_not0x_myfaUltXXX}c"
# flag = "d4rk{no00000oo_not0x_myfaUltXXX}c0de"
flag = "d4rk{no00000oo_not0x_myfaUltXXX}c0de"
block_list = ["d4r", "k{n", "o00", "000", "oo_", "not", "0x_", "myf", "aUl", "tXX", "X}c", "0de"]

table = "abcdefghijklmnopqrstuvwxyz0123456789_{}ABCDEFGHIJKLMNOPQRSTUVWXYZ"

global_found = False
for i in table:
    for j in table:
        for k in table:

            if (i + j + k) in block_list:
                continue

            tmp = flag + i + j + k

            chk = check_one(tmp)
            found = True
            for l in range(0, len(chk)):
                if enc_data[l] != chk[l]:
                    found = False
                    break

            if found == False:
                continue

            flag = tmp
            print flag
            global_found = True
            exit()
            #break
        if global_found:
            break
    if global_found:
        break

print chk
print len(chk)

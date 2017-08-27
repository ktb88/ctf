# 2017 HackCon - [Crypto] VizHash

## Key words

- Reversing encrypt algorithm
- Bruteforcing

## Solution

문제에 `hash.py`와 `digest.png`파일을 제공해줍니다.

```python
# I was bored and high af and thought of making a visual hash function where instead of a digest we get a png as hash of a string 
# So I developed this algorithm to hash the flag. (Patent pending, don't even think of copying it)
# It is so secure that you need more computation to break this than to break a sha256 hash

import base64
import math
import hashlib
from PIL import Image

flag = "d4rk{sample_flag123}c0de"

def encode(s):
    return (''.join([ chr(ord(c)+4) for c in s[::-1] ]))

def base64encode(s):
    return base64.b64encode(s.encode("utf8")).decode("utf8")

b64_flag = base64encode(flag)

encrypted_flag = ""
temp_str = ""

for i in b64_flag:
    temp_str += i
    encrypted_flag += encode(temp_str)

print(encrypted_flag)

pixels_list = []

checksum = 0
for i in encrypted_flag:
    m = hashlib.md5()
    m.update(i)
    m = m.hexdigest()
    m = int(m, 16)
    checksum += m
    m = str(hex(m))
    for j in range(0, len(m)-3, 3):
        pixels_list.append((128 + ord(m[j])^ord(m[j+1]), 128 + ord(m[j+1])^ord(m[j+2]), 128 + ord(m[j+2])^ord(m[j+3])))

print(checksum)
while checksum>0:
    pixels_list.append(((checksum%256), ((checksum/256)%256), ((checksum/(256*256))%256)))
    checksum = checksum/(256**3)
    
image_out = Image.new("RGB",(int(math.ceil(math.sqrt(len(pixels_list)))),int(math.ceil(math.sqrt(len(pixels_list))))))
image_out.putdata(pixels_list)
image_out.save('digest.png')
```

플래그로 부터 `digest.png`가 어떻게 나오는지 분석해보면 다음과 같습니다.

- flag = "d4rk{ ... }c0de"
- flag를 base64 인코딩
- 인코딩된 문자열을 encode() 함수를 거쳐 `encrypted_flag` 생성
- `encrypted_flag`를 한글자씩 `md5`하고 해당 `md5`의 값으로 픽셀들을 생성
- checksum 추가

플래그의 형태가 `d4rk{ ... }c0de` 이기 때문에 처음 한 바이트 `d`를 이용하여 위와 동일하게 암호 과정을 거친 뒤, `digest.png`의 32바이트 (`md5`)와 동일한지 확인합니다. 

이를 이용하여 프린터블한 스트링 내의 모든 값들을 전수조사 합니다.

`d4rk{n` 까지 정상적으로 동작하는데 이 이후로 값을 찾을수가 없다고 뜹니다. 그 이유는 `base64` 때문에 저의 스트링은 패딩이 붙기 때문에 실제 값이랑 달라지게 됩니다. 따라서 3바이트씩 전수조사를 하게 되면 정상적으로 구할 수 있게 됩니다.

## Solution Code

```python
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
```

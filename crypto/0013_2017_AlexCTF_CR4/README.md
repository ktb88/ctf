# 2017 AlexCTF - [Crypto] CR4

## Key words

- small primes

## Solution

`flag.b64`dhk `key.pub`을 제공해줍니다.

- flag.b64
```
Ni45iH4UnXSttNuf0Oy80+G5J7tm8sBJuDNN7qfTIdEKJow4siF2cpSbP/qIWDjSi+w=
```

- key.pub
```
-----BEGIN PUBLIC KEY-----
ME0wDQYJKoZIhvcNAQEBBQADPAAwOQIyUqmeJJ7nzzwMv5Y6AJZhdyvJzfbh4/v8
bkSgel4PiURXqfgcOuEyrFaD01soulwyQkMCAwEAAQ==
-----END PUBLIC KEY-----
```

`key.pub`을 열어 `n`과 `e`를 확인해보면 `n`이 너무 작아 쉽게 인수 분해가 가능합니다.

`factordb` 사이트를 통해 인수분해를 하면 다음과 같습니다.

[factordb](https://factordb.com)

```
p = 863653476616376575308866344984576466644942572246900013156919
q = 965445304326998194798282228842484732438457170595999523426901
```

암호를 풀기에 필요한 모든 데이터를 갖추었으니 위 내용을 기반으로 암호를 풀면 됩니다.

## Solution Code 

```python
from Crypto.PublicKey import RSA

def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return gcd, x, y

key = RSA.importKey(open("pub.key").read())

# n = 965445304326998194798282228842484732438457170595999523426901
n = key.n
# e = 65537
e = key.e

p = 863653476616376575308866344984576466644942572246900013156919
q = 965445304326998194798282228842484732438457170595999523426901
phi = (p-1) * (q-1)
_, d, _ = egcd(e, phi)
d = d % phi

#ct = int(open("flag.b64").read().decode("base64").encode("hex"), 16)
ct = int(open("flag.b64").read().decode("base64").encode("hex"), 16)
pt = pow(ct, d, n)
pt = hex(pt)[2:-1]
if len(pt) % 2 != 0:
    pt = "0" + pt

print pt.decode("hex")
```

## Result

```
tbkim@ubuntu:~/ctfing/2017_alex/crypto$ python sol_CR4.py 
&ݤ #Hu6Lۮ:ALEXCTF{SMALL_PRIMES_ARE_BAD}
```

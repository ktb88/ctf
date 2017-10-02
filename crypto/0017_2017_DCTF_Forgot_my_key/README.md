# 2017 DCTF - [Misc (Crypto)] Forgot my key

## Key words

- Reversing simple encrypt logic (+, %)
- z3 solver

## Solution

문제 코드는 다음과 같습니다.

```php
/*
    5616f5962674d26741d2810600a6c5647620c4e3d2870177f09716b2379012c342d3b584c5672195d653722443f1c39254360007010381b721c741a532b03504d2849382d375c0d6806251a2946335a67365020100f160f17640c6a05583f49645d3b557856221b2
*/
function my_encrypt($flag, $key) {
    $key = md5($key);
    $message = $flag . "|" . $key;

    $encrypted = chr(rand(0, 126));
    for($i=0;$i<strlen($message);$i++) {
        $encrypted .= chr((ord($message[$i]) + ord($key[$i % strlen($key)]) + ord($encrypted[$i])) % 126);
    }
    $hexstr = unpack('h*', $encrypted);
    return array_shift($hexstr);
}
```

위 주석으로 된 값이 암호화 결과 임을 유추 할 수 있습니다. 문제 코드는 php 인데 unpack의 h 옵션이 니블 단위로 변경을 합니다. 따라서 5616f5... 이렇게 시작하는 값을 65615f... 이런식으로 다시 변경을 해야 합니다.

```
5616f5962674d26741d2810600a6c5647620c4e3d2870177f09716b2379012c342d3b584c5672195d653722443f1c39254360007010381b721c741a532b03504d2849382d375c0d6806251a2946335a67365020100f160f17640c6a05583f49645d3b557856221b2
```

```
65615f6962472d76142d1860006a5c4667024c3e2d7810770f79612b7309213c243d5b485c7612596d352742341f3c29456300701030187b127c145a230b53402d4839283d570c6d0826152a4936536a37562010001f061f67046c0a55384f69543d5b755826122b
```

이 로직에서 몇 가지 유추 할수 있는 부분은 다음과 같습니다.

```
첫 한 바이트는 랜덤 값 (1 바이트)
65

플래그 포멧은 DCTF{SHA256}
615f6962472d76142d1860006a5c4667024c3e2d7810770f79612b7309213c243d5b485c7612596d352742341f3c29456300701030187b127c145a230b53402d4839283d570c

중간에 '|' 한 바이트 (1 바이트)
6d

마지막 md5 키 값 (32 바이트)
0826152a4936536a37562010001f061f67046c0a55384f69543d5b755826122b
```

my_encrypt 로직을 보면 다음 암호 값이 이전 암호 값에 연산되어 결과가 나오게 됩니다. 그런데 메시지가 뒷 부분은 키 이기 때문에 뒤쪽 키를 암호화 할때는 키와 키끼리 연산을 하는 부분이 생기게 됩니다. 이를 이용해서 풀어 보도록 하겠습니다.

먼저, for 문에서 키를 만낫을때 키의 인덱스는 첫 바이트를 제외하고 마지막 md5 키값 전 이기 때문에 python 코드로 생각을 해보면 다음과 같습니다.

enc = chr(0x6d)
for i in range(0, len(message)):
    enc += chr( ord(message[i]) + ord(key[i % len(key)]) + ord(enc[i]) % 126 )

이 때 i 값이 72 라면 메세지의 위치는 키 값이 md5 된 값을 만나게 됩니다.

i % len(key) = 71 % 32 = 7 이 나오게 되기 때문에 i 가 71 때 다음과 같이 됨을 알 수 있습니다.

enc[72] = chr( (ord(message[71]) + ord(key[7]) + ord(enc[71])) % 126 )
-> 08 = (ord(key[0]) + ord(key[7]) + 0x6d) % 126

이를 식으로 만들면 다음과 같습니다.

```
(key[0] + key[7] + 0x6d) % 126 == 0x08 )
(key[1] + key[8] + 0x08) % 126 == 0x26 )
(key[2] + key[9] + 0x26) % 126 == 0x15 )
(key[3] + key[10] + 0x15) % 126 == 0x2a )
(key[4] + key[11] + 0x2a) % 126 == 0x49 )
(key[5] + key[12] + 0x49) % 126 == 0x36 )
(key[6] + key[13] + 0x36) % 126 == 0x53 )
(key[7] + key[14] + 0x53) % 126 == 0x6a )
(key[8] + key[15] + 0x6a) % 126 == 0x37 )
(key[9] + key[16] + 0x37) % 126 == 0x56 )
(key[10] + key[17] + 0x56) % 126 == 0x20 )
(key[11] + key[18] + 0x20) % 126 == 0x10 )
(key[12] + key[19] + 0x10) % 126 == 0x00 )
(key[13] + key[20] + 0x00) % 126 == 0x1f )
(key[14] + key[21] + 0x1f) % 126 == 0x06 )
(key[15] + key[22] + 0x06) % 126 == 0x1f )
(key[16] + key[23] + 0x1f) % 126 == 0x67 )
(key[17] + key[24] + 0x67) % 126 == 0x04 )
(key[18] + key[25] + 0x04) % 126 == 0x6c )
(key[19] + key[26] + 0x6c) % 126 == 0x0a )
(key[20] + key[27] + 0x0a) % 126 == 0x55 )
(key[21] + key[28] + 0x55) % 126 == 0x38 )
(key[22] + key[29] + 0x38) % 126 == 0x4f )
(key[23] + key[30] + 0x4f) % 126 == 0x69 )
(key[24] + key[31] + 0x69) % 126 == 0x54 )
(key[25] + key[0] + 0x54) % 126 == 0x3d )
(key[26] + key[1] + 0x3d) % 126 == 0x5b )
(key[27] + key[2] + 0x5b) % 126 == 0x75 )
(key[28] + key[3] + 0x75) % 126 == 0x58 )
(key[29] + key[4] + 0x58) % 126 == 0x26 )
(key[30] + key[5] + 0x26) % 126 == 0x12 )
(key[31] + key[6] + 0x12) % 126 == 0x2b )
```

간단히 솔버를 이용하여 key 를 구합니다.

```python
import z3

s = z3.Solver()

a = []
for i in xrange(32):
    a.append(z3.Int('a[' + str(i) + ']'))
    s.add(a[i] >= 0x30)
    s.add(a[i] <= 0x66)

s.add( (a[0] + a[7] + 109) % 126 == 8 )
s.add( (a[1] + a[8] + 8) % 126 == 38 )
s.add( (a[2] + a[9] + 38) % 126 == 21 )
s.add( (a[3] + a[10] + 21) % 126 == 42 )
s.add( (a[4] + a[11] + 42) % 126 == 73 )
s.add( (a[5] + a[12] + 73) % 126 == 54 )
s.add( (a[6] + a[13] + 54) % 126 == 83 )
s.add( (a[7] + a[14] + 83) % 126 == 106 )
s.add( (a[8] + a[15] + 106) % 126 == 55 )
s.add( (a[9] + a[16] + 55) % 126 == 86 )
s.add( (a[10] + a[17] + 86) % 126 == 32 )
s.add( (a[11] + a[18] + 32) % 126 == 16 )
s.add( (a[12] + a[19] + 16) % 126 == 0 )
s.add( (a[13] + a[20] + 0) % 126 == 31 )
s.add( (a[14] + a[21] + 31) % 126 == 6 )
s.add( (a[15] + a[22] + 6) % 126 == 31 )
s.add( (a[16] + a[23] + 31) % 126 == 103 )
s.add( (a[17] + a[24] + 103) % 126 == 4 )
s.add( (a[18] + a[25] + 4) % 126 == 108 )
s.add( (a[19] + a[26] + 108) % 126 == 10 )
s.add( (a[20] + a[27] + 10) % 126 == 85 )
s.add( (a[21] + a[28] + 85) % 126 == 56 )
s.add( (a[22] + a[29] + 56) % 126 == 79 )
s.add( (a[23] + a[30] + 79) % 126 == 105 )
s.add( (a[24] + a[31] + 105) % 126 == 84 )
s.add( (a[25] + a[0] + 84) % 126 == 61 )
s.add( (a[26] + a[1] + 61) % 126 == 91 )
s.add( (a[27] + a[2] + 91) % 126 == 117 )
s.add( (a[28] + a[3] + 117) % 126 == 88 )
s.add( (a[29] + a[4] + 88) % 126 == 38 )
s.add( (a[30] + a[5] + 38) % 126 == 18 )
s.add( (a[31] + a[6] + 18) % 126 == 43 )

if s.check() != z3.sat:
    print "[*] not sat"
    exit()

flag = []
for i in xrange(32):
    flag.append(0)

m = s.model()

print m

for x in m.decls():
    print str(m[x])
    flag[int(str(x)[2:-1])] = str(m[x])

flag = "".join(flag[i] for i in range(0, len(flag)))
print "[*] SAT : " + flag
```

솔버 결과를 통해 key = 6941f4cac9b7784fdd77e11b51cd0d64 를 구할 수 있습니다.

키를 찾았으니 암호 로직을 이용하여 복호화 하면 플래그를 얻을 수 있습니다.

## Solution Code

```python
import hashlib

msg = "5616f5962674d26741d2810600a6c5647620c4e3d2870177f09716b2379012c342d3b584c5672195d653722443f1c39254360007010381b721c741a532b03504d2849382d375c0d6806251a2946335a67365020100f160f17640c6a05583f49645d3b557856221b2"
key = "0826152a4936536a37562010001f061f67046c0a55384f69543d5b755826122b".decode("hex")
enc = 0x6d

''' solver.py
t = "199c6d939d6b9b954b9d486e6e9d6597c61be61cc961959869679c98614c6a97".decode("hex")

x = 0
y = 7
N = 32
for i in range(0, len(t)):
    #print "s.add( (a[{:d}] + a[{:d}] + {:d}) % 126 == {:d} )".format( (x+i)%N, (y+i)%N, enc, ord(key[i]) )
    print "(key[{:d}] + key[{:d}] + 0x{:02x}) % 126 == 0x{:02x} )".format( (x+i)%N, (y+i)%N, enc, ord(key[i]) )
    enc = ord(key[i])

a = []
for i in xrange(32):
    a.append(0)

res = ""
for i in range(0, 32):
    res += chr(a[i])
print res

exit()
'''

''' challenge.php
for($i=0;$i<strlen($message);$i++)
    $encrypted .= chr((ord($message[$i]) + ord($key[$i % strlen($key)]) + ord($encrypted[$i])) % 126);
'''
enc_msg = "65615f6962472d76142d1860006a5c4667024c3e2d7810770f79612b7309213c243d5b485c7612596d352742341f3c29456300701030187b127c145a230b53402d4839283d570c6d0826152a4936536a37562010001f061f67046c0a55384f69543d5b755826122b".decode("hex")
print repr(enc_msg)
key = "6941f4cac9b7784fdd77e11b51cd0d64"
res = ""

enc = ord(enc_msg[0])
for i in range(1, len(enc_msg)):
    o_enc = ord( enc_msg[i] )
    o_key = ord(key[(i-1) % len(key)])

    found = False
    for j in range(0x30, 0x7f):
        if (j + o_key + enc) % 126 == o_enc:
            found = True
            res += chr(j)
            break

    if found == False:
        print "Not found"
        exit()

    enc = ord(enc_msg[i])

print res
```

## Result

```
VDCTF{f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b}|806251a2946335a67365020100f160f17640c6a05583f49645d3b557856221b2
```
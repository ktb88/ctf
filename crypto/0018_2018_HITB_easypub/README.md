# 2018 HITB - [Crypto] easy pub

## Key words

- strlen does count `\x00`
- size doesn't count `\x00`

## Solution

문제 코드는 다음과 같습니다.

```python
#/usr/bin/python3
from Crypto.PublicKey import RSA, ElGamal
from Crypto.Util.number import bytes_to_long, long_to_bytes, GCD, inverse, size
from Crypto import Random
from hashlib import sha256
from time import time
from random import randint, seed
from signal import alarm
from os import urandom

class cipher(object):
    def __init__(self):
        self.rsa = RSA.generate(1024, Random.new().read)
		self.elgamal = ElGamal.generate(128, Random.new().read)

    def encrypt(self, msg):
        return self.rsa.encrypt(msg, None)[0]

    def decrypt(self, sec):
        return self.rsa.decrypt(sec)

    def sign(self, msg):
        msg = long_to_bytes(msg)
        h = sha256(msg).digest()

        seed(time())
        k = randint(1, self.elgamal.p - 1)
        while GCD(k, self.elgamal.p - 1) != 1:
            k = randint(1, self.elgamal.p - 1)

        return self.elgamal.sign(h, k)

    def verify(self, msg, sig):
        msg = long_to_bytes(msg)
        h = sha256(msg).digest()
        return self.elgamal.verify(h, sig)


def main():
    with open('admin.key', 'r') as f:
        admin_k = f.readline()
    cry = cipher()
    print('welcome to Fantasy Terram')
    print(cry.rsa.e)
    print(cry.rsa.n)
    print(cry.elgamal.p)
    print(cry.elgamal.g)
    print(cry.elgamal.y)

    alarm(200)
    while True:
        choice = input("Please [r]egister or [l]ogin :>>")

        if not choice:
            break
        if choice[0] == 'r':
            r = randint(1, 3)
            # if r in(2, 3):
            #     print('Sorry, you cannot register now. Good luck.')
            #     exit()
            name = input('please input your username:>>')
            name = bytes(name, 'ISO-8859-1')
            if name == b'admin':
                tmp = input("please impurt admin's key:>>")
                if tmp != admin_k:
                    print('Liar! Get out of here!')
                    exit()
                else:
                    print('Welcom admin!')
                    with open('flag', 'r') as f:
                        print(f.readline())
                        exit()
            msg = name + b'\x00' + bytes(admin_k, 'ISO-8859-1')
            if size(bytes_to_long(msg)) > 700:
                print('Too long username')
                continue
            msg = msg + urandom(120 - len(msg))
            msg = bytes_to_long(msg)
            if msg % 2 == 1:
                msg += 1
            sig = cry.sign(msg)
            ticket = cry.encrypt(msg)
            print(ticket)
            print(sig[0])
            print(sig[1])

        elif choice[0] == 'l':
            ticket = int(input('ticket:>>'))
            sig0 = int(input('sig[0]'))
            sig1 = int(input('sig[1]'))
            msg = cry.decrypt(ticket)
            if msg % 2 == 1:
                print('A bit is wrong, may be something is wrong.')
                continue
            if cry.verify(msg, (sig0, sig1)) == cry.verify(msg, (sig1, sig0)):
                print('Wrong signature!')
            msg = long_to_bytes(msg)
            name = msg.split(b'\x00')[0]
            print('Welcome!{}'.format(name))
        else:
            break


if __name__ == '__main__':
    main()
```

로직을 분석해보면 크게 회원 가입과 로그인 기능이 존재합니다.

회원 가입 시, 이름 뒤에 `\x00` 한바이트를 넣고 그 뒤에 `admin_k`를 넣은뒤 120 글자에 맞춰 남는 패딩 바이트를 랜덤하게 넣습니다. 그리고 사용자에게 ticket과 signature를 출력해줍니다.

로그인 시, 메시지와 signature를 입력 받고 `\x00`를 기준으로 이름 부분인 첫 부분을 출력해줍니다.

문제를 풀기 위해 이름이 `admin`이 될 수 있는 키를 찾아야 플래그를 얻을 수 있습니다.

문제를 풀기 위해 가장 먼저 보아야 할 부분은 다음과 같습니다.

```python
msg = name + b'\x00' + bytes(admin_k, 'ISO-8859-1')
if size(bytes_to_long(msg)) > 700:
    print('Too long username')
    continue
msg = msg + urandom(120 - len(msg))
```

`admin_k`를 노출 시킬 수 있는 가장 유일한 부분인데 메시지 뒷 부분에 랜덤 바이트를 넣어서 알 수가 없습니다. 한 가지, 트릭은 urandom 함수에 있습니다. urandom의 경우 인자가 음수가 들어갈 경우 에러가 발생하게 됩니다. 따라서, name을 한 글자씩 키우면서 테스트를 해보면 에러가 발생하는 지점이 있는데 이를 이용하여 admin_k의 길이를 알 수 있습니다.

추가적인 트릭으로는 `\x00` 값이 size에서는 계산되지 않지만 len함수에서는 착실히 카운트가 됩니다.

따라서, 700이 넘으면 `Too long username`이 뜨게 되는데 이를 우회 하면서 len(msg)를 120을 만들기 위해 `\x00`을 넣습니다.

마지막으로 name = `\x00` x `X` + `\x00` + bytes(admin_k) 을 숫자로 변경하게 되는데 이름이 전부 `\x00`이라면 결국엔 남는건 bytes(admin_k)밖에 없게 됩니다.

따라서, msg가 120 글자가 될 수 있도록 name을 `\x00`로 채우고 가입을 하게 되어 나온 암호화된 값은 사실 admin_k 값만 들어 있게 되는 것이고, 이를 이용하여 로그인을 하게 되면 admin_k가 출력이 되게 됩니다.

출력된 admin_k를 이용하여 가입 시 이름에 `admin`을 넣고 키를 넣게 되면 플래그가 출력되게 됩니다.

# 2017 SHA - [CRYPTO] Secure Login

## Key words

- RSA
- no padding

## Solution

문제 서버에서 동작하는 파이썬 코드를 제공해줍니다.

> d 값이 공개 되지 않아 임의로 getPrime(1024) 2개를 넣어 새롭게 N과 d를 만들었습니다.

```python
import SocketServer,threading
import os

def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return x

p = 122393459642722715193508803338542206847651199104157034101901924367393290934998109518127197921357057965651363461495646489924392985126604671445241184587580086506941330238866801122301302482735364698974701123276213503102347555197266179750135524475763752922326614949176378421073363097486484940695242289746980388463
q = 133300336978107715331632886132210333124971739104027612877718732100345095048024966592792491983973801217967424585553062016226983458965633742347459768034630253066926503982017000225921857150785008634550090092282020402493896538543688354044017384128130488713660821776540113235126497327793261484261440017516736459081
n = 16315089414291365072804956105526619397880822648675320383852140885712340615983082870173758725944399423152738344037428151973965538500069936447639534890845531199613678184294237628125057316342510982776407156694815184917000970306121657284237906532814224632215370256293838582309545956565555297923401741307034617986383052120572516847847033937942436031190316937147957112647856482484333571961544221830208413154823809272644578945534650200125045586420565951106372262848424400490694183992092842805959840817463523575339840959190636863559402670693269438649657323364034745897181633739006582260227361430715116697654601217320483982503
e = 65537

d = egcd(e, (p-1)*(q-1))
if d < 0:
	d = d % ((p-1)*(q-1))

f = open("hackability.flag")
flag = f.readline().strip()

# Translate a number to a string (byte array), for example 5678 = 0x162e = \x16\x2e
def num2str(num):
    t = ('%x' % num)
    if len(t) % 2 == 1:
        t = '0' + t
    return t.decode('hex')

# Translate byte array back to number \x16\x2e = 0x162e = 5678
def str2num(s):
    return int(s.encode('hex'),16)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            self.request.sendall("\nWelcome to the secure login server, make your choice from the following options:\n1. Register yourself as a user.\n2. Collect flag\n3. Sign a message\n4. Exit\nChoice: ")
            inp = self.request.recv(1024).strip()
            if inp == '1':
                self.request.sendall("Pick a username: ")
                uname = self.request.recv(1024).strip()
                self.request.sendall("Enter your full name: ")
                full = self.request.recv(1024).strip()
                ticket = 'ticket:user|%s|%s' % (uname,full)
                ticket = pow(str2num(ticket),d,n)
                ticket = num2str(ticket)
                self.request.sendall("Your ticket:\n")
                self.request.sendall(ticket.encode('hex') + "\n")
            elif inp == '2':
                self.request.sendall("Enter your ticket: ")
                ticket = self.request.recv(1024).strip()
                try:
                    ticket = int(ticket,16)
                except:
                    ticket = 0
                ticket = pow(ticket,e,n)
                ticket = num2str(ticket)
                if ticket.startswith('ticket:'):
                    if ticket.startswith('ticket:admin|root|'):
                        self.request.sendall("Here you go!\n")
                        self.request.sendall(flag + "\n")
                        break
                    else:
                        self.request.sendall("Sorry that function is only available to admin user root\n")
                else:
                    self.request.sendall("That doesn't seem to be a valid ticket\n")
            elif inp == '3':
                self.request.sendall("Enter your message, hex encoded (i.e. 4142 for AB): ")
                msg = self.request.recv(1024).strip()
                try:
                    msg = msg.decode('hex')
                except:
                    self.request.sendall("That's not a valid message\n!")
                    continue
                msg = '\xff' + msg # Add some padding at the start so users can't use this to sign a ticket
                if str2num(msg) >= n:
                    self.request.sendall("That's not a valid message\n!")
                    continue
                signed = pow(str2num(msg),d,n)
                signed = num2str(signed)
                self.request.sendall("Your signature:\n")
                self.request.sendall(signed.encode('hex') + "\n")
            elif inp == '4':
                self.request.sendall("Bye!\n")
                break
            else:
                self.request.sendall("Invalid choice!\n")

SocketServer.TCPServer.allow_reuse_address = True
server = ThreadedTCPServer(("0.0.0.0", 12345), MyTCPHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
server.serve_forever()
```

기능은 다음과 같습니다.

```
1. 티켓 생성
  - username, fullname을 입력 받아 다음의 형태를 만듬
  - ticket:user|username|fullname
  - 위 티켓을 암호화
2. 유저 인증
  - 암호화된 티켓을 전송 받아 복호화. 복호화 된 값이 아래와 같다면 플래그를 출력
  - ticket:admin|root|
3. 메시지 암호화
  - 유저가 제공한 메시지의 맨 앞 부분에 "\xff"를 넣어 암호화
```

여기서 문제가 생기는 부분은 암호화 시에 패딩이 존재 하지 않는다는 점 입니다.

따라서, 다음과 같은 연산이 가능합니다.

```
x = y * z
x^d = (y * z)^d = y^d * z^d
```

여기서 x, y, z를 각각 root_ticket, user_ticket, message라고 가정하면 다음과 같습니다.

```
x = root_ticket = ticket:admin|root|
y = user_ticket = ticket:user|hackability|{something}
z = message     = \xff + message

x = y * z
root_ticket = user_ticket * message
-> root_ticket / user_ticket = message
-> root_ticket * user_ticket^-1 = message
```

`root_ticket`과 `user_ticket`은 고정적이고 message는 처음에 `\xff`으로 시작하기 때문에 `root_ticket * user_ticket^-1`이 `\xff`로 시작하는 값을 찾으면 결론적으로 x, y, z를 모두 찾을 수가 있습니다.

`\xff`로 시작하는 값을 구하기 위해 `{something}`부분을 무작위 대입을하여 `\xff`로 시작하는 값을 찾습니다.

주의할점은 message의 값은 처음 `ff`이후 부터의 값 입니다.

우리가 플래그를 얻기 위해 서버에 전달해야 하는 값은 `x^d`이기 때문에 패딩이 없기 때문에 발생했던 처음 연산에 의해 `x^d`를 구할 수 있습니다.

```
x^d = y^d * z^d
root_ticket^d = user_ticket^d * message^d
```

따라서 위에서 구한 `user_ticket`과 `message`를 서버에 전달하여 암호화된 값을 받으면 각각 `user_ticket^d`와 `message^d`가 되기 때문에 이 두개를 곱하면 결국엔 우리가 필요했던 값이 됩니다.

> root_ticket^d = user_ticket^d * message^d

## Solution code

```python
# Goal
# ticket:admin|root|

# My Ticket
# ticket:user|hackability|{}

import itertools
from pwn import *

def egcd(a, b):
	x, y, u, v = 0, 1, 1, 0
	while a != 0:
		q, r = b // a, b % a
		m, n = x - u * q, y - v * q
		b, a, x, y, u, v = a, r, u, v, m, n
		gcd = b
	return x

n = 16315089414291365072804956105526619397880822648675320383852140885712340615983082870173758725944399423152738344037428151973965538500069936447639534890845531199613678184294237628125057316342510982776407156694815184917000970306121657284237906532814224632215370256293838582309545956565555297923401741307034617986383052120572516847847033937942436031190316937147957112647856482484333571961544221830208413154823809272644578945534650200125045586420565951106372262848424400490694183992092842805959840817463523575339840959190636863559402670693269438649657323364034745897181633739006582260227361430715116697654601217320483982503

# root = hackability * msg
# -> root * hackability^-1 = msg
root = "ticket:admin|root|"
hackability = "ticket:user|hackability|"
msg = ""

r = int(root.encode("hex"), 16)

table = "abcdefghijklmnopqrstuvwxyz0123456789"
comb = itertools.permutations(table,5)
for _c in comb:
	c = "".join(_c)
	h = int((hackability + c).encode("hex"), 16)
	#msg = hex( (r * egcd(h, n)) % n )[2:]
	msg = hex( (r * egcd(h, n)) % n)[2:]

	#print "[*] Try : {}".format(hackability + c)

	# msg must start with ff
	# msg must be even-string
	# msg must less than N
	if len(msg)%2 == 0 and msg[:2] == "ff" and int(msg, 16) < n:
		print "[*] found it : {}".format(hackability + c)
		hackability += c
		print msg
		break

# remove first "ff"
msg = msg[2:]

# root^d = hackability^d * msg^d

server = "0.0.0.0"
port = 12345
p = remote(server, port)
print p.recv()

p.sendline("3")
print p.recv()

p.sendline(msg)
print p.recv()

print "[*] encrypt message"
recv = p.recv()
enc_msg = recv.split("\n")[0]
print enc_msg

p.sendline("1")
print p.recv()
p.sendline(hackability.split("|")[1])
print p.recv()
p.sendline(hackability.split("|")[2])
print p.recv()

print "[*] encrypt ticket"
recv = p.recv()
enc_hackability = recv.split("\n")[0]
print enc_hackability

print "[*] got enc_root = encrypt ticket * encrypt message"
enc_root = hex( (int(enc_msg, 16) * int(enc_hackability, 16)) % n )[2:]
print enc_root

p.sendline("2")
print p.recv()
p.sendline(enc_root)
print p.recv()
```

## Result

```
hackability@ubuntu:~/ctfing/2017_SHA/crypto/200$ cat hackability.flag
hackability{THIS_IS_YOUR_FLAG_:P}
hackability@ubuntu:~/ctfing/2017_SHA/crypto/200$ python sol_200.py
[*] found it : ticket:user|hackability|acd70
ff9dc420d9562caafa3ed89e72628943ee6df70bc86dc7a9ede8df7eb033f7ed72fb4b16cf8e1ab2f98e8f20ce962f745d548683a208f902f00a70c747904b6a34566d9457a078743db6e3a26f0149d3717c7ae4a6660c8584874bbcf6e8f8670214fc50a95270473549280f8e0d4632ef16caa8b972ad113e151a7fa1512cb61b751a999c3d084776d8be66f6d239b7c8dd1d6f6f3c62dc6cf2f9feea5867b3edcbfb0f16586d7d9170c7c807e6c1038dbacecbd6fe06ea38119a4037018de13c9d7450f237eb9e5c0a201b243afdb3f028f93523843d1f933522a866742d120dac98e43b3240c7674592da7a8459a5da92979bcffc3a932d969c3520dd7e
[+] Opening connection to 0.0.0.0 on port 12345: Done

Welcome to the secure login server, make your choice from the following options:
1. Register yourself as a user.
2. Collect flag
3. Sign a message
4. Exit
Choice:
Enter your message, hex encoded (i.e. 4142 for AB):
Your signature:

[*] encrypt message
72ec5f8b741d1a5d8714ec02a3101e60afb6b6f5890cc5bd8b0038638506f20851c497a3f44cf0ac7f9d76e5aa8c23df55a9180dc66a185371d885ed8f453a200ea690659ba5c0333dffa8c0591fae073233b6785d107ec9defe783776c6e254d91611d4813a446577a6d1009575c0e07ab040583cadf4dd472ede3b2695beb34308c97d09e6a54a8ad6866e283df1e0388a6925af435f19467182721759115ea7da5fc86fea7950070d23b0986f84f0c512412c6adc08452190d736c7259b9bcdc5351b29584a96b9242e438aea26f8f42217d4234115d0b7b10d1736da4618f1a2f7bf25679f8b73ff996b9984df623573d96fae0263d18736c36456056bfb
Pick a username:
Enter your full name:
Your ticket:

[*] encrypt ticket
358b90fc0d49df231c08d4caf0e86c0b2bc6dcf63c576fae08ae8c35508c52ef4f3b81c676d105ecd34a7a63914d8bae3dce3dcee5cdb40e3f8bfcfc6a114fd215b672e03784d0d3ae584a56ee5cd41e262b1785f3b80e5b3ff28da029f27950e8e1c72159ef8572b931b155c5a8e8ef53fb706a9fe2bc9c78c324213f00c901ed029c254c57fbd075c5f54b47909c8fcc4ffa163b2d6b8d0062a5797a97cad53231988410943d6bb173b30603acefe78369994aaa6f38743659b2ddff722beb3a7b02130c1e45c1896e52bfe95c8f777129fd070c9551d6ade9bb44fffea6a6473d05cc63d80567ea498b8ff2391a155fd4449bac677d19261eaaf4461fe777
[*] got enc_root = encrypt ticket * encrypt message
6eb5bb5b499234e7368596a4ff6b91a3e7740d1e0192553b42c6a9a1abe0bcf2c13e142299466f62fe5c10170f7918ee10178afd022a82a58930c116ecf9500aef9707604ec8e631b68b57baf833c3707dd4cc408d45e9ee6927e3cb2d02a992847ed6cacd2cd6826f666237d2581cf9651ac45c6a80ec00685d4bbbef4846c791e7d875f50f850eb8ca9b8cff15ae58076c1705dd316b6c3997ed2b5d947693d2b157719471fa7edd5ff8f86ec378d69398f6fbac0613179aad1786cf4e31dc71183d9c5bbad572a4df36466bcea314cbd1cb62d24911270c0b7108dbb9f385e9bf10edf62dfff2fd27ebbba0cd5cb3525e1f73fdd22dc08213e93f8ef0ed00
Enter your ticket:
Here you go!
hackability{THIS_IS_YOUR_FLAG_:P}

[*] Closed connection to 0.0.0.0 port 12345
```

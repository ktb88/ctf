#-*- coding: utf-8 -*-
from pwn import *
from Crypto.Util.number import inverse, GCD

#I've heard that the old crypto system causes some errors intermittently.
#I don't know why but something weird behave in some point.
#[*] RSA, Fault Attack

#1초동안 같은 서명을 해준다. 그러나 가끔 이상한 서명을 해준다.
#정상적인 서명과 정상적이지 않은 서명의 쌍을 찾는다.
sock = remote('crypto.tendollar.kr', 10000)
sock.recvn(93)
prev = [""]
while(True):
  sock.send('1\n')
  sock.recvn(30)
  sock.send('1\n')
  sock.recvn(6)
  sock.send('tyhan\n')
  data = sock.recvuntil("Choice:")
  data = data.split("\n")
  if data[0] == prev[0]:
    if data[2] != prev[2]:
      a = int(data[2], 16)
      b = int(prev[2], 16)
      n = int(data[4], 16)
      break
  prev = data

#https://cryptologie.net/article/371/fault-attacks-on-rsas-signatures/
#위의 사이트의 말대로 CRT에서 한쪽만 에러가 있을 경우 p의 값을 찾는다.

p = GCD(a-b,n)

#p를 찾았으니 d를 찾는건 학교에서 배운대로 해줍니다.
q = n/p
d = inverse(65537, (p-1) * (q-1))
sock.send("3\n")
sock.recv(timeout=0.1)
sock.send(str(d) + "\n")
flag = sock.recvuntil("Choice:")
sock.close()

#끝
print flag.split("\n")[1]

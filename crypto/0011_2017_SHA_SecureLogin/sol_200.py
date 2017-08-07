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


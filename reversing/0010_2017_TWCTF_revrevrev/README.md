# 2017 TWCTF - [REV] rev rev rev

## Key words

- x86 ELF Reversing
- angr automation

## Solution

문제는 32바이트 입력을 받고 특정 로직을 거쳐 전역 변수 0x08048870의 값과 같은지 확인합니다.

로직이 간단해 수작업으로 구해도 되지만 angr을 이용하여 해결해보았습니다.

```
.text:08048668                 push    eax             ; s2
.text:08048669                 lea     eax, [ebp+s]
.text:0804866C                 push    eax             ; s1
.text:0804866D                 call    _strcmp
.text:08048672                 add     esp, 10h
.text:08048675                 test    eax, eax
.text:08048677                 jnz     short loc_804868B
.text:08048679                 sub     esp, 0Ch
.text:0804867C                 push    offset aCorrect ; "Correct!"
.text:08048681                 call    _puts
.text:08048686                 add     esp, 10h
.text:08048689                 jmp     short loc_804869B
.text:0804868B ; ---------------------------------------------------------------------------
.text:0804868B
.text:0804868B loc_804868B:                            ; CODE XREF: main+CCj
.text:0804868B                 sub     esp, 0Ch
.text:0804868E                 push    offset aInvalid ; "Invalid!"
.text:08048693                 call    _puts
.text:08048698                 add     esp, 10h
```

Find 는 `0x0804867c`로 잡고 Avoid는 `0x0804868B`로 설정하고 angr을 구동합니다.

## Solution Code

```python
import angr

project = angr.Project("./rev_rev_rev", load_options={'auto_load_libs':False})
path_group = project.factory.path_group()
path_group.explore(find=0x0804867c,avoid=0x0804868b)

print path_group.found[0].state.posix.dumps(0)
```

## Result

```
tbkim@ubuntu:~/ctfing/2017_mma/rev$ python sol_rev1.py
WARNING | 2017-09-11 19:17:31,756 | claripy | Claripy is setting the recursion limit to 15000. If Python segfaults, I am sorry.
ÿTWCTF{qpzisyDnbmboz76oglxpzYdk}
```
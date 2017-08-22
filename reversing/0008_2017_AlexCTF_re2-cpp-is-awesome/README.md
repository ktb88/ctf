# 2017 AlexCTF - [REV] re2-cpp-is-awesome

## Key words

- cpp ELF reversing
- custom python gdb plugin

## Solution

문제는 `cpp` 로 만들어진 `ELF` 파일 입니다. 정적으로 살펴 봐도 한눈에 어느 부분이 뭔가 비교 하는 루틴인지 들어 오지 않습니다.

IDA에서 제공해주는 `CFG`를 이용하여 분석해본 결과 다음 위치에서 저의 입력과 특정 값을 비교 하는 구문이 나오게 됩니다.

```
.text:0000000000400C64                 cdqe
.text:0000000000400C66                 mov     eax, dword_6020C0[rax*4]
.text:0000000000400C6D                 cdqe
.text:0000000000400C6F                 add     rax, rcx
.text:0000000000400C72                 movzx   eax, byte ptr [rax]
-> .text:0000000000400C75                 cmp     dl, al
.text:0000000000400C77                 setnz   al
.text:0000000000400C7A                 test    al, al
.text:0000000000400C7C                 jz      short loc_400C83
.text:0000000000400C7E                 call    sub_400B56
```

여기서 `dl`은 제가 인자로 넣은 값이고, `al`이 맞추어야 하는 대상입니다.

디버거로 여러번 반복하면 플래그를 쉽게 얻을 수 있지만 자동화를 해보도록 합니다.

요즘에 `angr`이 최근에 무슨 업데이트를 햇는지 도무지 되질 않고, `pwntools`에서 제공 되는 `gdb`기능도 제 입맛에 맛질 않아 기본 `gdb`에 필요한 기능을 넣어서 python module 형태로 gdb를 만들어 보았습니다.

[hackability gdb](https://github.com/ktb88/hackability_gdb)

아직 기본적인 기능 뿐이 없지만 필요한 기능들을 조금씩 넣으면 좋을것 같네요.

## Solution Code 

```python
from pwn import *
from hackability_gdb import Gdb as hgdb

target = "./re2"

d = hgdb(target)
d.bp("*0x400c75")
d.r("A"*0x20, prompt=True)

def get_one():
    temp = d.getReg("al")[2:]
    d.setR2R("dl", "al")
    d.c()
    return temp.decode("hex")

res = ""
for i in range(0, 0x20):
    res += get_one()
    print res

    if res[len(res)-1] == "}":
        break
```

## Result

```
tbkim@ubuntu:~/ctf/reversing/0008_2017_AlexCTF_re2-cpp-is-awesome$ python sol_re2.py 
[+] Starting local process '/bin/bash': pid 113454
A
AL
ALE
ALEX
ALEXC
ALEXCT
ALEXCTF
ALEXCTF{
ALEXCTF{W
ALEXCTF{W3
ALEXCTF{W3_
ALEXCTF{W3_L
ALEXCTF{W3_L0
ALEXCTF{W3_L0v
ALEXCTF{W3_L0v3
ALEXCTF{W3_L0v3_
ALEXCTF{W3_L0v3_C
ALEXCTF{W3_L0v3_C_
ALEXCTF{W3_L0v3_C_W
ALEXCTF{W3_L0v3_C_W1
ALEXCTF{W3_L0v3_C_W1t
ALEXCTF{W3_L0v3_C_W1th
ALEXCTF{W3_L0v3_C_W1th_
ALEXCTF{W3_L0v3_C_W1th_C
ALEXCTF{W3_L0v3_C_W1th_CL
ALEXCTF{W3_L0v3_C_W1th_CL4
ALEXCTF{W3_L0v3_C_W1th_CL45
ALEXCTF{W3_L0v3_C_W1th_CL455
ALEXCTF{W3_L0v3_C_W1th_CL4553
ALEXCTF{W3_L0v3_C_W1th_CL45535
ALEXCTF{W3_L0v3_C_W1th_CL45535}
[*] Stopped process '/bin/bash' (pid 113454)
```

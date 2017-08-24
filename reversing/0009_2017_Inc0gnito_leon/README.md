# 2017 Inc0gnito - [REV] leon

## Key words

- anti reversing (ptrace)

## Solution

문제는 다음과 같습니다.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  size_t v3; // rax@1
  int result; // eax@4
  __int64 v5; // rbx@4
  char s; // [sp+0h] [bp-60h]@1
  __int64 v7; // [sp+48h] [bp-18h]@1

  v7 = *MK_FP(__FS__, 40LL);
  ptrace(0, 0LL, 1LL, 0LL);
  fgets(&s, 64, _bss_start);
  v3 = strlen(buf);
  if ( !strncmp(&s, buf, v3) )
    puts("Good job!");
  else
    puts("Wrong..");
  result = 0;
  v5 = *MK_FP(__FS__, 40LL) ^ v7;
  return result;
}
```

그래서 스트링에 플래그가 있을것 같아서 스트링을 봣더니 다음과 같았습니다. (`buf`)

```
B6B1BCCF849B909A8C91D88BA08C9A9A92A08B90A09D9AA0888D968B9AA08C90929A8B97969198D1D18200
```

띠용! 일단 뭔지 모르겠으니 `strncmp`에 `bp`를 걸고 뛰어 봅니다. 하지만 `ptrace`가 앞을 막고 있으니 이놈을 제거 해줍니다. `(leon_patch)`

먼저 아래처럼 레지스터에 플래그 나옵니다.

```
   0x400852 <main+107>: lea    rax,[rbp-0x60]
   0x400856 <main+111>: mov    esi,0x601080
   0x40085b <main+116>: mov    rdi,rax
=> 0x40085e <main+119>: call   0x4005f0 <strncmp@plt>
   0x400863 <main+124>: test   eax,eax
   0x400865 <main+126>: jne    0x400873 <main+140>
   0x400867 <main+128>: mov    edi,0x400924
   0x40086c <main+133>: call   0x400600 <puts@plt>
Guessed arguments:
arg[0]: 0x7fffffffe450 --> 0xa31 ('1\n')
arg[1]: 0x601080 ("INC0{doesn't_seem_to_be_write_something..}")
arg[2]: 0x2a ('*')
[---------------------------stack[---------------------------
0000| 0x7fffffffe450 --> 0xa31 ('1\n')
0008| 0x7fffffffe458 --> 0x601080 ("INC0{doesn't_seem_to_be_write_something..}")
```

한 가지 의문점은 저 플래그 스트링은 바이너리에서 보이지 않았는데 갑자기 어디서 나왓는지 입니다.

추적 해본결과 `_init_` 함수에 다음과 같이 되어 있었습니다.

```c
int init_()
{
  return memset(buf, 0xFFFFFFFFLL, 0x2ALL);
}
```

이 루틴을 거치면 플래그가 생성되는데 평소에 `memset`이 `assign` 연산인줄 알았는데 `xor` 연산을 거칩니다. 읭?? 그렇습니다. `memset`이 정의가 되어 있습니다.

```
unsigned __int64 __fastcall memset(__int64 a1, char a2, unsigned __int64 a3)
{
  unsigned __int64 result; // rax@3
  unsigned __int64 i; // [sp+18h] [bp-10h]@1

  for ( i = 0LL; ; ++i )
  {
    result = i;
    if ( i >= a3 )
      break;
    *(_BYTE *)(i + a1) = *(_BYTE *)(a1 + i) ^ a2;
  }
  return result;
}
```

`바이트 스트림 xor 0xFF` 을 하게 되면 정상적으로 플래그를 얻을 수 있습니다. 
# 2017 BugsBunny - [REV] Rev100

## Key words

- ELF Reversing
- Xor operation
- Anti-Debugging

## Solution

문제는 다음과 같습니다.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax@2
  size_t v4; // rax@3
  size_t v5; // rax@5
  int i; // [sp+Ch] [bp-4h]@5

  std::operator<<<std::char_traits<char>>(&std::cout, "try to find me :D\n", envp);
  if ( (unsigned int)i_am_debugged() != 0 )
  {
    result = 1;
  }
  else
  {
    v4 = strlen(&A);
    memcpy(&dest1, &A, v4 + 1);
    if ( (unsigned int)i_am_debugged() != 0 )
    {
      result = 1;
    }
    else
    {
      v5 = strlen(&B);
      memcpy(&dest2, &B, v5 + 1);
      for ( i = 0; (unsigned __int64)i < 0x16; ++i )
      {
        if ( (unsigned int)i_am_debugged() != 0 )
          return 1;
        *(_BYTE *)(i + C) = *(_BYTE *)(C + i) + (*(&A + i) ^ *(&B + i));
      }
      result = 0;
    }
  }
  return result;
}
```

소스 중에 `i_am_debugged()` 라는 함수를 살펴 보면 다음과 같이 안티리버싱 기술이 적용되어 있습니다.

```c
__int64 i_am_debugged(void)
{
  return (unsigned __int64)ptrace(PTRACE_TRACEME, 0LL, 1LL, 0LL) >> 63 != 0;
}
```

`ptrace(PTRACE_TRACEME)` 는 현재 디버깅 중인지 아닌지 판단할 수 있습니다. 이 부분을 우회 하기 위해서는 바이너리에서 해당 함수에 대해 항상 0 으로 리턴 하게끔 패치를 해주면 됩니다.

일단 이 부분은 뒤로하고, 다음 로직을 살펴 보면 단순히 `C[i]` 배열에 `A[i]^B[i]` 를 넣고 있습니다. 그 뒤로 딱히 출력해 주는 구문이 없기 때문에 파이썬 코드를 짜서 직접 `xor`을 해줍니다.

## Solution Code

```python
A = "\x61\x41\x40\x37\x6d\x77\x34\x2c\x5f\x41\x42\x60\x07\x34\x7d\x12\x57\x7a\x22\x25\x4f\x28"
B = "\x23\x34\x27\x44\x32\x35\x41\x42\x31\x38\x39\x38\x37\x46\x22\x23\x24\x25\x44\x50\x21\x55"
C = ""

for i in range(0, len(A)):
    C += chr(ord(A[i]) ^ ord(B[i]))

print C
```

## Result

```
tbkim@ubuntu:~/ctf/reversing/0002_2017_bugsbunny_rev100$ python sol_rev100.py 
Bugs_Bunny{X0r_1s_fun}
```

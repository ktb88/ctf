# 2017 BugsBunny - [REV] Rev50

## Key words

- ELF Reversing
- Dictionary Attack

## Solution

문제 코드는 다음과 같습니다.

```c 
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax@10
  __int64 v4; // rbx@10
  signed int i; // [sp+1Ch] [bp-64h]@2
  __int64 src; // [sp+20h] [bp-60h]@2
  int v7; // [sp+28h] [bp-58h]@2
  __int16 v8; // [sp+2Ch] [bp-54h]@2
  char v9; // [sp+2Eh] [bp-52h]@2
  char dest; // [sp+30h] [bp-50h]@2
  __int64 v11; // [sp+68h] [bp-18h]@1

  v11 = *MK_FP(__FS__, 40LL);
  if ( argc <= 1 )
  {
    puts("usage ./rev50 password");
  }
  else
  {
    src = 'sedecrem';
    v7 = 0;
    v8 = 0;
    v9 = 0;
    memcpy(&dest, &src, 9uLL);
    for ( i = 0; i <= 999; ++i )
    {
      if ( !strcmp(argv[1], (&dict)[8 * i]) && !strcmp(&dest, (&dict)[8 * i]) )
      {
        puts("Good password ! ");
        goto LABEL_10;
      }
    }
    puts("Bad ! password");
  }
LABEL_10:
  puts(&byte_40252A);
  result = 0;
  v4 = *MK_FP(__FS__, 40LL) ^ v11;
  return result;
}
```

문제의 조건은 단순히 입력한 값과 `mercedes (sedecrem의 반대)`값이 같은지 확인하고 이 값이 `dict`에 존재하면 됩니다.

`dict`는 사전 형태로 여러가지 단어와 문자열이 나열되어 있는데요. 아마 이 사전의 단어를 이용하여 `dictionary attack` 느낌으로 문제를 구성한것 같습니다.

일단 이 문제의 정답은 `Bugs_Bunny{mercedes}` 입니다만 출제자의 의도로 한 번 풀어 보도록 하겠습니다.

먼저, `strings` 명령을 이용하여 ELF의 스트링을 덤프 한 뒤에, 하나씩 바이너리에 입력 시켜 보면서 `Good password !`가 나오는 부분을 찾으면 됩니다.

## Solution Code

```python
from pwn import *

fd = open("rev50_strings","r")
lines = fd.read().splitlines()
fd.close()

target = "./rev50"

for i in range(0, len(lines)):
  print "[%10d] [%s] Try" % (i, lines[i])
  p = process([target, lines[i]])

  if "Good" in p.recv():
    print "[*] found : [{}]".format(lines[i])
    break

  p.close()
```

## Result

```
[*] Process './rev50' stopped with exit code 0 (pid 70606)
[       164] [andrea] Try
[+] Starting local process './rev50': pid 70608
[*] Process './rev50' stopped with exit code 0 (pid 70608)
[       165] [smokey] Try
[+] Starting local process './rev50': pid 70610
[*] Process './rev50' stopped with exit code 0 (pid 70610)
[       166] [steelers] Try
[+] Starting local process './rev50': pid 70612
[*] Process './rev50' stopped with exit code 0 (pid 70612)
[       167] [joseph] Try
[+] Starting local process './rev50': pid 70614
[*] Stopped process './rev50' (pid 70614)
[       168] [mercedes] Try
[+] Starting local process './rev50': pid 70616
[*] Process './rev50' stopped with exit code 0 (pid 70616)
[*] found : [mercedes]
```
# 2017 BugsBunny - [REV] Rev150

## Key words

- ELF Reversing
- SMT Solver

## solution

문제를 보면 다음과 같습니다.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("####################################");
  puts("#i know you can do it just focus :D#");
  puts("#        use only numbers          #");
  puts("#       author:Aymen Borgi         #");
  puts("####################################");
  if ( argc <= 1 )
  {
    puts("usage: ./rev150 password\n");
  }
  else
  {
    if ( !(unsigned int)numeric((__int64)argv[1]) )
      puts("this is not a number try again\n");
    if ( (unsigned __int8)ksjqdh((__int64)argv[1])
      && (unsigned __int8)uiyzr((__int64)argv[1])
      && (unsigned __int8)qdsdqq((__int64)argv[1])
      && (unsigned __int8)euziry((__int64)argv[1])
      && (unsigned __int8)mlhkjg((__int64)argv[1])
      && (unsigned __int8)sndsqd((__int64)argv[1])
      && (unsigned __int8)toyiup((__int64)argv[1])
      && (unsigned __int8)huhgeg((__int64)argv[1])
      && (unsigned __int8)nvjfkv((__int64)argv[1])
      && (unsigned __int8)jncsdkjf((__int64)argv[1])
      && (unsigned __int8)ieozau((__int64)argv[1])
      && (unsigned __int8)jqsgdd((__int64)argv[1])
      && (unsigned __int8)msdlmkfd((__int64)argv[1])
      && (unsigned __int8)nhdgrer((__int64)argv[1])
      && (unsigned __int8)fs546sdf((__int64)argv[1])
      && (unsigned __int8)sdff564sd((__int64)argv[1])
      && (unsigned __int8)sdff564s((__int64)argv[1])
      && (unsigned __int8)sdff564s7((__int64)argv[1])
      && (unsigned __int8)sdff564s8((__int64)argv[1])
      && (unsigned __int8)sdff564((__int64)argv[1])
      && (unsigned __int8)sdff564g5((__int64)argv[1])
      && (unsigned __int8)sdff564g8((__int64)argv[1])
      && (unsigned __int8)sdff564k3((__int64)argv[1])
      && (unsigned __int8)fhsjdgfyezf((__int64)argv[1]) )
    {
      printf((__int64)"good job the flag is BugsBunny{%s}\n", argv[1]);
    }
    else
    {
      puts("wrong password\n");
    }
  }
  return 0;
}
```

위 함수를 모두 통과 하는 `argv[1]` 을 만들어야 하는 것 같습니다. 

처음에 `numeric` 함수를 통해 우리가 넣는 인자는 `'0' < argv[i] < '9'` 의 값을 갖는 것을 알 수 있습니다.

먼저, 함수 하나를 보면 다음과 같습니다.

```c
__int64 __fastcall ksjqdh(__int64 a1)
{
  __int64 v1; // rax@1
  __int64 result; // rax@2

  LODWORD(v1) = strlen(a1);
  if ( v1 == 20 )
  {
    result = (unsigned int)(*(_BYTE *)(a1 + 15) - '0' + *(_BYTE *)(a1 + 4) - '0');
    if ( (_DWORD)result != 10 )
      result = 0LL;
  }
  else
  {
    result = 0LL;
  }
  return result;
}
```

함수 마다 모두 `True`를 리턴해야 하기 때문에 `a[15] + a[4] == 10` 이 되어야 합니다. 그 밑에 함수들도 이런식으로 구성이 되어 있어서 전체적으로 보면 다음과 같은 식이 나오게 됩니다.

```
a[15] + a[4] == 10
a[1] * a[18] == 2
a[15] / a[9] == 1
a[5] - a[17] == -1
a[15] - a[1] == 5
a[1] * a[10] == 18
a[8] + a[13] == 14
a[18] * a[8] == 5
a[4] * a[11] == 0
a[8] + a[9] == 12
a[12] - a[19] == 1
a[9] % a[17] == 7
a[14] * a[16] == 40
a[7] - a[4] == 1
a[6] + a[0] == 6
a[2] - a[16] == 0
a[4] - a[6] == 1
a[0] % a[5] == 4
a[5] * a[11] == 0
a[10] % a[15] == 2
a[11] / a[3] == 0
a[14] - a[13] == -4
a[18] + a[19] == 3
a[3] + a[17] == 9
```

직접 손으로 몇개만 풀어 보면 다음과 같습니다.

```
a[1] = 1 or 2, a[18] = 1 or 2, | a[1] - a[18] | = 1
a[11] = 0
a[3] != 0
a[15] = a[1] + 5 = 1 or 7
a[9] = a[15] = 1 or 7
... snip ...
```

이런식으로 값들을 유추하거나 수학적인 방법을 이용하여 해를 구할 수 있습니다. 여기서는 방정식의 해를 찾아 주는 SMT Solver 인 z3를 이용하여 문제를 해결하였습니다.

## Solution Code

```python
import z3

s = z3.Solver()

a = []
for i in xrange(20):
    a.append(z3.Int('a[' + str(i) + ']'))
    s.add(a[i] >= 0)
    s.add(a[i] <= 9)

s.add(a[11] == 0) # added
s.add(a[15] + a[4] == 10)
s.add(a[1] * a[18] == 2)
s.add(a[15] / a[9] == 1)
s.add(a[5] - a[17] == -1)
s.add(a[15] - a[1] == 5)
s.add(a[1] * a[10] == 18)
s.add(a[8] + a[13] == 14)
s.add(a[18] * a[8] == 5)
#s.add(a[4] * a[11] == 0)
s.add(a[8] + a[9] == 12)
s.add(a[12] - a[19] == 1)
s.add(a[9] % a[17] == 7)
s.add(a[14] * a[16] == 40)
s.add(a[7] - a[4] == 1)
s.add(a[6] + a[0] == 6)
s.add(a[2] - a[16] == 0)
s.add(a[4] - a[6] == 1)
s.add(a[0] % a[5] == 4)
#s.add(a[5] * a[11] == 0)
s.add(a[10] % a[15] == 2)
#s.add(a[11] / a[3] == 0)
s.add(a[14] - a[13] == -4)
s.add(a[18] + a[19] == 3)
s.add(a[3] + a[17] == 9)


if s.check() != z3.sat:
    print "[*] not sat"
    exit()

flag = []
for i in xrange(20):
    flag.append(0)

m = s.model()
for x in m.decls():
    flag[int(str(x)[2:-1])] = str(m[x])

flag = "".join(flag[i] for i in range(0, len(flag)))
print "[*] SAT : " + flag

from pwn import *
target = "./rev150"
p = process([target, flag])
print p.recv()
```

## Result

```
tbkim@ubuntu:~/ctf/reversing/0003_2017_bugsbunny_rev150$ python sol_rev150.py 
[*] SAT : 42813724579039578812
[+] Starting local process './rev150': pid 70731
[*] Process './rev150' stopped with exit code 0 (pid 70731)
####################################
#i know you can do it just focus :D#
#        use only numbers          #
#       author:Aymen Borgi         #
####################################
good job the flag is BugsBunny{42813724579039578812}
```
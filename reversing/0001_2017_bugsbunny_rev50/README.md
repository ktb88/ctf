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

asdasd

# 2017 Asis - [REV] ABC

## Key words

- x86 ELF Reversing
- angr automation

## Solution

문제 코드는 다음과 같습니다.

```c
__int64 __fastcall main(signed int a1, char **argv, char **a3)
{
  __int64 result; // rax@2
  void *m3; // ST38_8@3
  unsigned int len_m1; // eax@3
  unsigned int len_m2; // eax@3
  unsigned int len_m3; // eax@3
  char *v8; // ST00_8@16
  unsigned int v9; // eax@16
  __int64 v10; // rsi@22
  char **v_argv; // [sp+0h] [bp-190h]@1
  signed int i; // [sp+1Ch] [bp-174h]@3
  signed int j; // [sp+1Ch] [bp-174h]@6
  signed int k; // [sp+1Ch] [bp-174h]@9
  signed int l; // [sp+1Ch] [bp-174h]@16
  int v16; // [sp+20h] [bp-170h]@3
  int v17; // [sp+24h] [bp-16Ch]@3
  void *m1; // [sp+28h] [bp-168h]@3
  char *m2; // [sp+30h] [bp-160h]@3
  char v20[32]; // [sp+40h] [bp-150h]@3
  char v21[32]; // [sp+60h] [bp-130h]@3
  char v22[32]; // [sp+80h] [bp-110h]@3
  char v23[32]; // [sp+A0h] [bp-F0h]@16
  char v24[48]; // [sp+C0h] [bp-D0h]@4
  char v25[48]; // [sp+F0h] [bp-A0h]@7
  char s1[48]; // [sp+120h] [bp-70h]@10
  char v27[56]; // [sp+150h] [bp-40h]@17
  __int64 v28; // [sp+188h] [bp-8h]@1

  v_argv = argv;
  v28 = *MK_FP(__FS__, 40LL);
  if ( a1 > 1 )
  {
    m1 = malloc(4uLL);
    m2 = (char *)malloc(4uLL);
    m3 = malloc(4uLL);
    memset(m1, 0, 4uLL);
    memset(m2, 0, 4uLL);
    memset(m3, 0, 4uLL);
    *(_DWORD *)m1 = *(_DWORD *)argv[1];
    memcpy(m3, argv[1] + 3, 6uLL);
    *(_DWORD *)m2 = *((_DWORD *)argv[1] + 2);
    v16 = strtol((const char *)m1, 0LL, 16);
    v17 = strtol(m2, 0LL, 16);
    len_m1 = strlen((const char *)m1);
    get_sha1_4024DF((__int64)v20, (char *)m1, len_m1);
    len_m2 = strlen((const char *)m3);
    get_sha1_4024DF((__int64)v22, (char *)m3, len_m2);
    len_m3 = strlen(m2);
    get_sha1_4024DF((__int64)v21, m2, len_m3);
    for ( i = 0; i <= 19; ++i )
      sprintf(&v24[2 * i], "%02x", (unsigned __int8)v20[i], v_argv);
    for ( j = 0; j <= 19; ++j )
      sprintf(&v25[2 * j], "%02x", (unsigned __int8)v21[j], v_argv);
    for ( k = 0; k <= 19; ++k )
      sprintf(&s1[2 * k], "%02x", (unsigned __int8)v22[k], v_argv);
    if ( !strcmp(s1, "69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9")
      && v16 < v17
      && !strncmp(v24, (const char *)m1, 4uLL)
      && !strncmp(v25, m2, 4uLL) )
    {
      printf("gj, you got the flag: ", m2, v_argv);
      v9 = strlen(*((const char **)v8 + 1));
      get_sha1_4024DF((__int64)v23, *((char **)v8 + 1), v9);
      for ( l = 0; l <= 19; ++l )
        sprintf(&v27[2 * l], "%02x", (unsigned __int8)v23[l]);
      printf("ASIS{%s}\n", v27);
      exit(0);
    }
    puts("Sorry, try harder :(");
    result = 0LL;
  }
  else
  {
    puts("give me flag... :D");
    result = 0LL;
  }
  v10 = *MK_FP(__FS__, 40LL) ^ v28;
  return result;
}
```

위 내용을 요약해보면 다음과 같습니다.

- 인자로 받는 글자의 크기는 12 글자 (예: AAAABBBBCCCC)
- 12글자가 총 3 부분으로 나뉘어 첫 번째 부분은 AAAA 두 번째 부분은 ABBBC 세 번째 부분은 CCCC로 나뉨
- AAAA의 SHA1 값의 첫 4바이트가 AAAA와 같아야 함
- CCCC의 SHA1 값의 첫 4바이트가 CCCC와 같아야 함
- strtol(AAAA) < strtol(CCCC)
- ABBBBC의 SHA1 값이 69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9 와 같아야 함

먼저 AAAA, CCCC의 SHA1 값 첫 4바이트가 자기 자신이 되는걸 찾아 보면 다음과 같이 2개가 나옵니다.

```
[*] found it
57d9 57d918b9f067a058d006c704a7e598dafe520557
[*] found it
b53a b53a80f26b6fc17c878e8432bba7a7cc1ea746ea
```

조건이 `strtol(AAAA) < strtol(CCCC)` 이기 때문에 AAAA = 57d9, CCCC = b53a가 됩니다.

그러면 ABBBBC = 5BBBBb 가 됩니다. 4바이트 브포를 해서 sha1(5BBBBb) = 69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9 가 되는 BBBB를 찾으면 됩니다.

(* Hashcat 을 사용합시다...)

```
[*] found it
9:-*)b 69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9
```

따라서 총 입력은 `57d9:-*)b53a` 가 됩니다.

## Solution Code

```python
import hashlib
import itertools

t = "0123456789abcdef"
size = 4
n = len(t) ** size

def test():
    n = len(t) ** size
    i = 0

    print "started"
    for _t in itertools.product(t, repeat=size):
        if i % 0x10000 == 0:
            print "[%x : %x]" % (i, n)

        tmp = ''.join(_t)
        sha1 = hashlib.sha1(tmp).hexdigest()

        if sha1 == "69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9":
            print "[*] found it"
            print tmp, sha1
            break

        i += 1

def find_len_cond(size=4):
    i = 0
    for _t in itertools.product(t, repeat=size):
        if i % 0x100000 == 0:
            print "[%x : %x]" % (i, n)

        tmp = ''.join(_t)
        sha1 = hashlib.sha1(tmp).hexdigest()

        if tmp == sha1[:4]:
            print "[*] found it"
            print tmp, sha1

        i += 1

def last_try():
    AAAA = "57d9"
    CCCC = "b53a"

    new_t = ''
    for i in range(0, 0x100):
        new_t += chr(i)

    i = 0
    for _t in itertools.product(new_t, repeat=4):
        if i % 0x100000 == 0:
            print "[%x : %x]" % (i, n)

        tmp = '9' + ''.join(_t) + 'b'
        sha1 = hashlib.sha1(tmp).hexdigest()
        if sha1 == "69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9":
            print "[*] found it"
            print tmp, sha1
            break

        i += 1

'''
[0 : 10000]
[*] found it
57d9 57d918b9f067a058d006c704a7e598dafe520557
[*] found it
b53a b53a80f26b6fc17c878e8432bba7a7cc1ea746ea

[*] found it
9:-*)b 69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9

57d9:-*)b53a
'''
```


## Result

```
tbkim@ubuntu:~/ctfing/2017_asis/reversing$ ./abc "57d9:-*)b53a"
gj, you got the flag: ASIS{477408a4d4ad68aa7abdfd2be0e4717154497c42}
```
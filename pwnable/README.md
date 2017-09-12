# Pwnable Challenges

* [ ] 2017 Meepwn anotherarena
  - not working yet
* [ ] 2017 HUST RR2L
  - solved but not working yet
* [ ] 2017 HUST wind
  - solved but not working yet
* [x] 2017 0ctf babyheap
  - x86-64 | FULL RELRO | NX | PIE
  - heap (overlay fast bin and small bin)
* [ ] 2017 0ctf EasiestPrintf
  - TODO: there is execution problem
  - i386 application running on debian
  - FSB
  - printf malloc, free condition (width)
* [x] 2017 BostonKeyParty memo
  - x86-64 | FULL RELO | NX
  - heap (fast bin)
  - logic bug to leak the libc address
* [x] 2016 openCTF tyro_heap
  - i386 | NX
  - heap buffer overflow
  - overwrite function pointer
* [x] 2017 0ctf diethard
  - x86-64 | NX
  - custom heap (?)
* [x] 2016 bctf bcloud
  - i386 | NX
  - heap (House of force)
  - leak by got overwritten
* [x] 2017 RCTF aiRcraft
  - amd64 | NX | PIE | Partial Relro
  - Heap Exploit
  - double-free
  - use-after-free
  - overwritten function ptr
* [x] 2017 h3x0r mic for pwn
  - i386 | NX | SSP
  - Format String Bug (FSB)
  - Leak memory by SSP
* [x] 2017 bugsbunny Pwn50
  - Simple Pwnable Challenge
* [x] 2017 bugsbunny Pwn100
  - i386
  - return to shellcode
* [x] 2017 bugsbunny Pwn150
  - x86_64 simple stack bof
  - gdb : set follow-fork-mode [child | parent]
* [x] 2017 bugsbunny Pwn200
  - overwrite got
* [x] 2017 bugsbunny Pwn250
  - 64bit One-shot gadget
  - rdi, rsi, edx
* [ ] 2017 bugsbunny Pwn300
  - tired to make the shellcode.... :(
  - 64bit shellcode
  - Alphanumeric shellcode
* [x] 2017 SHA Megan-35
  - Megan-35 encoder
  - FSB
  - one-shot gadget in 32bit libc
* [x] 2017 SHA Echo Service
  - amd64 | FULL RELRO | NX | SSP | PIE
  - Object-c
  - FSB (but Object-c version)
  - construct fake frame
* [x] 2015 32C3 teufel
  - Virtual Memory Privilege
  - Stack overflow/underflow
* [x] 2015 MMA RPS
  - overwrite random seed
  - Pwntools(ctypes)
* [x] 2017 TWCTF Just Do It
  - 32bit ELF
  - overwrite local variable
* [x] 2017 Asis Mrs. Hudson
  - 64bit ELF
  - 64bit ROP Gadget
* [x] 2017 Asis Greg Lestrade
  - 64bit ELF
  - integer overflow
  - format string

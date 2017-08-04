import z3

s = z3.Solver()

a = []
for i in xrange(20):
	a.append(z3.Int('a[' + str(i) + ']'))
	s.add(a[i] >= 0)
	s.add(a[i] <= 9)

s.add(a[11] == 0)
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



import z3

s = z3.Solver()

a = []
for i in xrange(32):
    a.append(z3.Int('a[' + str(i) + ']'))
    s.add(a[i] >= 0x30)
    s.add(a[i] <= 0x66)

s.add( (a[0] + a[7] + 109) % 126 == 8 )
s.add( (a[1] + a[8] + 8) % 126 == 38 )
s.add( (a[2] + a[9] + 38) % 126 == 21 )
s.add( (a[3] + a[10] + 21) % 126 == 42 )
s.add( (a[4] + a[11] + 42) % 126 == 73 )
s.add( (a[5] + a[12] + 73) % 126 == 54 )
s.add( (a[6] + a[13] + 54) % 126 == 83 )
s.add( (a[7] + a[14] + 83) % 126 == 106 )
s.add( (a[8] + a[15] + 106) % 126 == 55 )
s.add( (a[9] + a[16] + 55) % 126 == 86 )
s.add( (a[10] + a[17] + 86) % 126 == 32 )
s.add( (a[11] + a[18] + 32) % 126 == 16 )
s.add( (a[12] + a[19] + 16) % 126 == 0 )
s.add( (a[13] + a[20] + 0) % 126 == 31 )
s.add( (a[14] + a[21] + 31) % 126 == 6 )
s.add( (a[15] + a[22] + 6) % 126 == 31 )
s.add( (a[16] + a[23] + 31) % 126 == 103 )
s.add( (a[17] + a[24] + 103) % 126 == 4 )
s.add( (a[18] + a[25] + 4) % 126 == 108 )
s.add( (a[19] + a[26] + 108) % 126 == 10 )
s.add( (a[20] + a[27] + 10) % 126 == 85 )
s.add( (a[21] + a[28] + 85) % 126 == 56 )
s.add( (a[22] + a[29] + 56) % 126 == 79 )
s.add( (a[23] + a[30] + 79) % 126 == 105 )
s.add( (a[24] + a[31] + 105) % 126 == 84 )
s.add( (a[25] + a[0] + 84) % 126 == 61 )
s.add( (a[26] + a[1] + 61) % 126 == 91 )
s.add( (a[27] + a[2] + 91) % 126 == 117 )
s.add( (a[28] + a[3] + 117) % 126 == 88 )
s.add( (a[29] + a[4] + 88) % 126 == 38 )
s.add( (a[30] + a[5] + 38) % 126 == 18 )
s.add( (a[31] + a[6] + 18) % 126 == 43 )

if s.check() != z3.sat:
    print "[*] not sat"
    exit()

flag = []
for i in xrange(32):
    flag.append(0)

m = s.model()

print m

for x in m.decls():
    print str(m[x])
    flag[int(str(x)[2:-1])] = str(m[x])

flag = "".join(flag[i] for i in range(0, len(flag)))
print "[*] SAT : " + flag

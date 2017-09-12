c = "7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e".decode("hex")

flag = "TWCTF{"

for _ in range(0x20, 0x7f):
    print "\n*** {} ***\n".format(chr(_))
    key = "ENJ0YHOLIDAY{}".format(chr(_))
    k = "45".decode("hex")

    for i in range(0, len(flag)):
        a = ord(flag[i]) + ord(c[i]) % 128
        b = (128 - a + ord(c[i+1])) % 128

    pt = ""
    for i in range(0, len(c)-1):
        a = ord(key[i % len(key)]) + ord(c[i]) % 128
        b = (128 - a + ord(c[i+1])) % 128
        pt += chr(b)
    print pt

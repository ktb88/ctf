def sxor(a, b):
    ret = ""
    for i in range(0, len(a)):
        ret += chr( ord(a[i]) ^ ord(b[i]))
    return ret

#            %  P   D   F   -   1   .   X   .
predict = "\x25\x50\x44\x46\x2d\x31\x2e\x00\x00\x00\x00\x00\x00\x00\x00\x00"

# p1  = 5c4260, obj = 6f626a : p1 xor obj = 33200a
predict = "\x25\x50\x44\x46\x2d\x31\x2e\x33\x20\x0a\x00\x00\x00\x00\x00\x00"

# p2 = 4200, obj = 7320
predict = "\x25\x50\x44\x46\x2d\x31\x2e\x33\x20\x0a\x31\x20\x00\x00\x00\x00"

# p3 = 5a2a, obj = 6a0a
predict = "\x25\x50\x44\x46\x2d\x31\x2e\x33\x20\x0a\x31\x20\x30\x20\x00\x00"

# p3 = 0e05, obj = 6167
predict = "\x25\x50\x44\x46\x2d\x31\x2e\x33\x20\x0a\x31\x20\x30\x20\x6f\x62"

enc     = "\xD6\xEA\xB9\x75\x30\x19\x6A\x9B\x05\x2A\xEF\x97\xEE\x2C\x00\xDB"
#print sxor("\x0e\x05", "\x61\x67").encode("hex")

key    = sxor(predict, enc)

data = open("flag.pdf.enc", "rb").read()
i = 0
res = ""
while i < len(data)-16:
    res += sxor(data[i*16:i*16+16], key)
    i += 1

fd = open("flag.pdf", "wb")
fd.write(res)
fd.close()


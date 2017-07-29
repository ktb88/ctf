def sxor(c, k):
	res   = ""
	len_c = len(c)
	len_k = len(k)
	min_len = len_c

	if len_c > len_k: 
		min_len = len_k

	for i in xrange(min_len):
		res += chr(ord(c[i]) ^ ord(k[i]))

	res += "_" * (len(c)-len(k))
	return res

def get_char(ct, idx, offset, g_char):
	return chr(ord(ct[idx][offset]) ^ ord(g_char))

def show_res(ct, key):
	print "KEY: {}".format(key + "_" * (len(ct[0]) - len(key)))
	print "%4s 01234567890123456789012345" % (" ")
	for i in range(0, len(ct)):
		print "[%02d] %s" % (i, sxor(ct[i], key))
	print

ct = None
with open("msg") as fd:
	ct = fd.read().split("\n")[:-1]

for i in range(0, len(ct)):
	ct[i] = ct[i].decode("hex")

g_k = "ALEXCTF{"
show_res(ct, g_k)

g_p = "Dear Friend"
print "Plain text : " + g_p
g_k = sxor(ct[0], g_p).split("_")[0]
print "Key        : " + g_k

guess = [
	(1, 11, "y"),
	(6, 12, "e"),
	(6, 13, " "),
	(2, 14, "a"),
	(3, 15, "r"),
	(0, 16, "s"),
	(0, 17, " "),
	(1, 18, "k"),
	(5, 19, "t"),
	(5, 20, "i"),
	(5, 21, "c"),
	(5, 22, "a"),
	(5, 23, "l"),
	(5, 24, "l"),
	(5, 25, "y")
]

for idx, off, ch in guess:
	g_k += get_char(ct, idx, off, ch)
	print "KEY : " + g_k

print
show_res(ct, g_k)


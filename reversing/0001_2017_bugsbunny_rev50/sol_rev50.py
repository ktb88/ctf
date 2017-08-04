from pwn import *

fd = open("rev50_strings","r")
lines = fd.read().splitlines()
fd.close()

target = "./rev50"

for i in range(0, len(lines)):
	print "[%10d] [%s] Try" % (i, lines[i])
	p = process([target, lines[i]])

	if "Good" in p.recv():
		print "[*] found : [{}]".format(lines[i])
		break

	p.close()




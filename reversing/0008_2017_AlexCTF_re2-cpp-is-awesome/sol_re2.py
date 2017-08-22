from pwn import *
from hackability_gdb import Gdb as hgdb

target = "./re2"

d = hgdb(target)
d.bp("*0x400c75")
d.r("A"*0x20, prompt=True)

def get_one():
	temp = d.getReg("al")[2:]
	d.setR2R("dl", "al")
	d.c()
	return temp.decode("hex")

res = ""
for i in range(0, 0x20):
	res += get_one()
	print res

	if res[len(res)-1] == "}":
		break



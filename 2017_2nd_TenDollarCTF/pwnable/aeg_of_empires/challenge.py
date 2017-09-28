#!/usr/bin/python
#-*- coding: utf-8 -*-
import signal, sys, os, random, string

os.environ["TERM"] = "linux"
os.environ["TERMINFO"] = "/usr/share/terminfo"

from pwn import *
context(os='linux', arch='amd64', log_level='error')

PATH = "/home/aeg"

class Timeout(Exception): pass

def clock_is_ticking(signum, frame):
    raise Timeout()

def generate_code( nonce ):

	local_buf_size = random.randrange(64, 256)
	local_buf_size += 8 - (local_buf_size % 8)
	check_size = random.randrange(16, local_buf_size)

	chk_list = []
	for i in range(0, local_buf_size):
		rnd_ch = random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
		chk_list.append((i, rnd_ch))
	random.shuffle(chk_list)

	chk_logic = ''
	for i in range(0, check_size):
		idx, ch = chk_list[i]
		chk_logic += "if (buf[{}] != '{}') exit(-1);\n".format(idx, ch)

	source = '''
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <unistd.h>
	#include <sys/stat.h>
	#include <fcntl.h>

	void exploited() {{
		char buf[64] = {{0,}};
		ssize_t fd = open("/home/aeg/flag", O_RDONLY);
		read(fd, buf, 63);
		printf("%s\\n", buf);
	}}

	int main(int argc, char **argv)
	{{
		char buf[{}] = {{0,}};
		read(0, buf, {});
		{}
		return 0;
	}}
	'''.format(local_buf_size, local_buf_size+0x30, chk_logic)

	#print source

	with open("{}/source/{}.c".format(PATH, nonce), "wb") as fd:
		fd.write(source)

	try:
		os.system('gcc -fno-stack-protector -mpreferred-stack-boundary=4 {}/source/{} -o {}/executable/{}'.format(PATH, str(nonce) + ".c", PATH, str(nonce)))
	except Exception as e:
		print sys.exc_info()
		raise 1

	data = ""
	with open("{}/executable/{}".format(PATH, nonce), "rb") as fd:
		data = fd.read()

	return data.encode("base64"), str(nonce)
		
def main():
	MAGIC = ""
	with open("{}/flag".format(PATH), "r") as fd:
		MAGIC = fd.read()

	signal.signal(signal.SIGALRM, clock_is_ticking)

	try:
		gen_base64, nonce = generate_code(random.randrange(100000000000000))
		sys.stdout.write('Give me the your exploit input as base64 encoded \n')
		sys.stdout.flush()
		sys.stdout.write('Generated the binary (You have 20 sec to solve) \n')
		sys.stdout.flush()
		sys.stdout.write(gen_base64 + "\n")
		sys.stdout.flush()

		signal.alarm(20)
		user_answer = raw_input('')
		signal.alarm(0)

		try:
			user_answer = user_answer.decode("base64")
		except Exception as e:
			sys.stdout.write("Not valid base64 string \n")
			exit(-1)

		user_answer = user_answer.replace("\n","")

		try:
			p = process("{}/executable/{}".format(PATH, nonce))
			p.send(user_answer)
			data = p.recv()
			if MAGIC in data:
				sys.stdout.write("Congratz!! Here is your prize :)\n")
				sys.stdout.write(MAGIC)
			else:
				sys.stdout.write("Wrong :( try harder\n")
			sys.stdout.flush()
		except Exception as e:
			pass
		finally:
			os.system("rm {}/source/{}.c".format(PATH, nonce))
			os.system("rm {}/executable/{}".format(PATH, nonce))
			p.close()	
		
	except Exception as e:
		print str(e)
		print '[*] Sorry, there is an error in the system.'
		print 'If you see this message consistently, plz DM me (kakaotalk ID: hackability)'
		sys.stdout.flush()
		exit(-1)	

if __name__ == "__main__":
	main()

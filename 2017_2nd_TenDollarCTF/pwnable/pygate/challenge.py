#!/usr/bin/python
#-*- coding: utf-8 -*-

import signal
from sys import stdout

__CHALL__ = "pygate"

class Timeout(Exception): pass

def clock_is_ticking(signum, frame):
    raise Timeout()

def main():
    signal.signal(signal.SIGALRM, clock_is_ticking)
    signal.alarm(60)

    welcome = '''
    _______  __   __  _______  _______  _______  _______
    |       ||  | |  ||       ||   _   ||       ||       |
    |    _  ||  |_|  ||    ___||  |_|  ||_     _||    ___|
    |   |_| ||       ||   | __ |       |  |   |  |   |___
    |    ___||_     _||   ||  ||       |  |   |  |    ___|
    |   |      |   |  |   |_| ||   _   |  |   |  |   |___
    |___|      |___|  |_______||__| |__|  |___|  |_______|
    '''
    stdout.write(welcome)
    stdout.flush()

    stdout.write("\n\t[*] 'Q' or 'q' to exit")
    stdout.write("\n\t[*] FLAG is in the /home/{}/flag\n\n".format(__CHALL__))
    stdout.flush()

    while True:
        try:
            stdout.write("$ ")
            stdout.flush()
            data = raw_input()

            if data == 'q' or data == 'Q':
                exit()

            exec data
        except Timeout as e:
            print "See ya :P"
            exit()
        except Exception as e:
            exit()

if __name__ == "__main__":
    main()
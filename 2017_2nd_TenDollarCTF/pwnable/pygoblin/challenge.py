#!/usr/bin/python
#-*- coding: utf-8 -*-

import signal as sczrklckwzlnuzqc
from sys import stdout as ekfhjydedynsmyox

__CHALL__ = "pygoblin"

class Timeout(Exception): pass

def clock_is_ticking(signum, frame):
    raise Timeout()

def main():
    sczrklckwzlnuzqc.signal(sczrklckwzlnuzqc.SIGALRM, clock_is_ticking)
    sczrklckwzlnuzqc.alarm(60)

    welcome = '''
     _______  __   __  _______  _______  _______  ___      ___   __    _
    |       ||  | |  ||       ||       ||  _    ||   |    |   | |  |  | |
    |    _  ||  |_|  ||    ___||   _   || |_|   ||   |    |   | |   |_| |
    |   |_| ||       ||   | __ |  | |  ||       ||   |    |   | |       |
    |    ___||_     _||   ||  ||  |_|  ||  _   | |   |___ |   | |  _    |
    |   |      |   |  |   |_| ||       || |_|   ||       ||   | | | |   |
    |___|      |___|  |_______||_______||_______||_______||___| |_|  |__|
    '''
    ekfhjydedynsmyox.write(welcome)
    ekfhjydedynsmyox.flush()

    ekfhjydedynsmyox.write("\n\t[*] 'Q' or 'q' to exit")
    ekfhjydedynsmyox.write("\n\t[*] FLAG is in the /home/{}/flag\n\n".format(__CHALL__))
    ekfhjydedynsmyox.flush()

    _Exception = Exception

    _raw_input = raw_input
    __builtins__.__dict__.clear()
    __builtins = None

    while 1:
        try:
            ekfhjydedynsmyox.write("$ ")
            ekfhjydedynsmyox.flush()
            data = _raw_input()

            if data == 'q' or data == 'Q':
                return

            exec data
        except Timeout as e:
            print "See ya :P"
            return
        except _Exception as e:
            return

if __name__ == "__main__":
    main()
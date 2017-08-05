# -*- coding: utf-8 -*-
#/usr/bin/env python
import string
# Flag : Piug_Pibbm{Q35oF_3BQ0R3_4F3_B0H_G3QiF3_OH_4ZZ}
def encode(story, shift):
  return ''.join([
            (lambda c, is_upper: c.upper() if is_upper else c)
                (
                  ("abcdefghijklmnopqrstuvwxyz"*2)[ord(char.lower()) - ord('a') + shift % 26],
                  char.isupper()
                )
            if char.isalpha() else char
            for char in story
        ])


def decode(story,key):
    pass


if __name__ == '__main__':
    print ord('n') - ord('b')
    exit()
    key = [_YOUR_KEY_HERE_]
    print decode("Piug_Pibbm{Q35oF_3BQ0R3_4F3_B0H_G3QiF3_OH_4ZZ}",key)
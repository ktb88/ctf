#!/usr/bin/env python

import pyDes
from struct import pack, unpack

def xors(a, b):
    return pack('<Q', unpack('<Q', a)[0] ^ unpack('<Q', b)[0])

# pyDes do not support OFB mode
# so I have to implement myself T_T

class DES_OFB:
    def __init__(self, iv, key):
        self.iv = iv
        self.key = key
    def encrypt(self, data):
        data += '\x00' * (-len(data) % 8)
        ret = ''
        prev = self.iv
        for i in xrange(0, len(data), 8):
            blk = pyDes.des(self.key, pyDes.ECB).encrypt(prev)
            ret += xors(blk, data[i:i+8])
            prev = blk
        return ret

# I want to be sure that my precious file is not corrupted!!

legal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_0123456789'

with open('flag', 'rb') as f:
    flag = f.read()
    for ch in flag:
        assert ch in legal

# iv and key are same as plaintext, but anyway it's secret
# so I think it's absolutely safe :p

k = DES_OFB(flag[:8], flag[:8])

with open('flag.enc', 'wb') as f:
    f.write(k.encrypt(flag))

#!/usr/bin/env python

import pyDes
from struct import pack, unpack

def xors(a, b):
    return pack('<Q', unpack('<Q', a)[0] ^ unpack('<Q', b)[0])

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

            if i == 0:
                if ret[0] != "I" or ret[1] != "N" or ret[2] != "C" or ret[3] != "0":
                    return False
        return ret

'''
7E 1F C5 5B 4B 62 1C A8   54 6E 4B 20 E3 88 03 40
A3 C5 81 78 7F 28 DA D3   A1 05 02 B8 FA 81 A1 5C
32 D7 04 74 43 60 24 91   07 E9 59 46 39 63 E4 FB
'''

legal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_0123456789'

ct = open("flag.enc", "rb").read()

#   = "   I   N   C   0   {"
iv  = "\x49\x4e\x43\x30\x7b"
key = iv

table = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

for i in table:
    print i
    for j in table:
        for k in table:
            tmp = iv + i + j + k
            obj = DES_OFB(tmp, tmp)
            res = obj.encrypt(ct)

            if res == False:
                continue

            try:
                res = res.decode("hex")
            except Exception as e:
                print str(e)
                print repr(res)

            if res[0] == "I" and res[1] == "N" and res[2] == "C" and res[3] == "0":
                print repr(res)
                exit()

# INC0{1t_wAs_jUSt_an_3A5Y_bf___I_was_stupid__T_T}
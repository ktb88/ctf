import hashlib

msg = "5616f5962674d26741d2810600a6c5647620c4e3d2870177f09716b2379012c342d3b584c5672195d653722443f1c39254360007010381b721c741a532b03504d2849382d375c0d6806251a2946335a67365020100f160f17640c6a05583f49645d3b557856221b2"
key = "0826152a4936536a37562010001f061f67046c0a55384f69543d5b755826122b".decode("hex")
enc = 0x6d

''' solver.py
t = "199c6d939d6b9b954b9d486e6e9d6597c61be61cc961959869679c98614c6a97".decode("hex")

x = 0
y = 7
N = 32
for i in range(0, len(t)):
    #print "s.add( (a[{:d}] + a[{:d}] + {:d}) % 126 == {:d} )".format( (x+i)%N, (y+i)%N, enc, ord(key[i]) )
    print "(key[{:d}] + key[{:d}] + 0x{:02x}) % 126 == 0x{:02x} )".format( (x+i)%N, (y+i)%N, enc, ord(key[i]) )
    enc = ord(key[i])

a = []
for i in xrange(32):
    a.append(0)

res = ""
for i in range(0, 32):
    res += chr(a[i])
print res

exit()
'''

''' challenge.php
for($i=0;$i<strlen($message);$i++)
    $encrypted .= chr((ord($message[$i]) + ord($key[$i % strlen($key)]) + ord($encrypted[$i])) % 126);
'''
enc_msg = "65615f6962472d76142d1860006a5c4667024c3e2d7810770f79612b7309213c243d5b485c7612596d352742341f3c29456300701030187b127c145a230b53402d4839283d570c6d0826152a4936536a37562010001f061f67046c0a55384f69543d5b755826122b".decode("hex")
print repr(enc_msg)
key = "6941f4cac9b7784fdd77e11b51cd0d64"
res = ""

enc = ord(enc_msg[0])
for i in range(1, len(enc_msg)):
    o_enc = ord( enc_msg[i] )
    o_key = ord(key[(i-1) % len(key)])

    found = False
    for j in range(0x30, 0x7f):
        if (j + o_key + enc) % 126 == o_enc:
            found = True
            res += chr(j)
            break

    if found == False:
        print "Not found"
        exit()

    enc = ord(enc_msg[i])

print res

# VDCTF{f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b}|806251a2946335a67365020100f160f17640c6a05583f49645d3b557856221b2
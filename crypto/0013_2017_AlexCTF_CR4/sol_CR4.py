from Crypto.PublicKey import RSA

def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return gcd, x, y

key = RSA.importKey(open("pub.key").read())

# n = 965445304326998194798282228842484732438457170595999523426901
n = key.n
# e = 65537
e = key.e

p = 863653476616376575308866344984576466644942572246900013156919
q = 965445304326998194798282228842484732438457170595999523426901
phi = (p-1) * (q-1)
_, d, _ = egcd(e, phi)
d = d % phi

#ct = int(open("flag.b64").read().decode("base64").encode("hex"), 16)
ct = int(open("flag.b64").read().decode("base64").encode("hex"), 16)
pt = pow(ct, d, n)
pt = hex(pt)[2:-1]
if len(pt) % 2 != 0:
    pt = "0" + pt

print pt.decode("hex")
# N: 20473673450356553867543177537
# e: 17

fd = open("Baby_RSA.txt", "r")
data = fd.read()
fd.close()

def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return gcd, x, y

def decrypt(p, q, e, ct):
    n = p * q
    phi = (p - 1) * (q - 1)
    gcd, a, b = egcd(e, phi)
    d = a % phi
    pt = pow(ct, d, n)
    return hex(pt)[2:-1].decode("hex")


p = 2165121523231
q = 9456131321351327
phi = (p-1) * (q-1)
n = p * q
e = 17

res = ""
for l in data.splitlines():
    res += decrypt(p, q, e, int(l))
print res

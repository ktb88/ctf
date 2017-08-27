import requests
import httplib
httplib._MAXHEADERS = 1000

url = "http://defcon.org.in:6060/index.php"

r = requests.get(url)
# requests.exceptions.ConnectionError: ('Connection aborted.', HTTPException('got more than 100 headers',))

print r.headers
data = r.headers['set-cookie'].split(";")

i = 0
res = ""
while i < len(data):
    tmp = data[i]
    if ", " in tmp:
        tmp = tmp.split(", ")[1]

    ch = tmp.split("=")[1]
    if len(ch) != 1:
        ch = ch[1:]
        ch = chr(int(ch, 16))

    res += ch
    i += 3

# ++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>+++++++++++++++++.--.--------------.+++++++++++++.----.-------------.++++++++++++.--------.<------------.<++.>>----.+.<+++++++++++.+++++++++++++.>+++++++++++++++++.---------------.++++.+++++++++++++++.<<.>>-------.<+++++++++++++++.>+++..++++.--------.+++.<+++.<++++++++++++++++++++++++++.<++++++++++++++++++++++.>++++++++++++++..>+.----.>------.+++++++.--------.<+++.>++++++++++++..-------.++./
print res

# username: abERsdhw password: HHealskdwwpr
# d4rk{c00k13s_4r3_fun}c0de

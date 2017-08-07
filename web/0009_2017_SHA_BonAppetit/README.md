# 2017 SHA - [WEB] Bon Appetit

## Key words

- LFI
- PHP wrapper
- .htaccess

## Solution

문제 웹 페이지에 접속하면 유저와 interaction 하는 부분은 찾기가 어렵고 대신에 `page`파라미터를 이용하여 페이지를 호출하는 것을 알 수 있습니다.

따라서, 일반적인 `LFI`라 생각하고 `PHP wrapper`를 이용하여 `index.php` 등등의 페이지를 조사해보았지만 결과가 나오지 않아 `/etc/passwd`를 해보니 정상적으로 불러 오는 것을 알 수 있었습니다.

여러가지 파일들을 게싱하다가 `.htaccess`를 생각했고 이 파일을 열어 보니 다음과 같았습니다.

```
<FilesMatch "\.(htaccess|htpasswd|sqlite|db)$">
 Order Allow,Deny
 Deny from all
</FilesMatch>

<FilesMatch "\.phps$">
 Order Allow,Deny
 Allow from all
</FilesMatch>

<FilesMatch "suP3r_S3kr1t_Fl4G">
  Order Allow,Deny
  Deny from all
</FilesMatch>


# disable directory browsing
Options -Indexes
```

기본적으로 `.htaccess`에 저렇게 되어 있기 때문에 우리가 페이지에서 저 룰로 접속을 하게 되면 `access deny`가 되지만 우리는 `index.php`에 존재하는 `LFI`취약점을 이용하여 해당 파일을 불러 오기 때문에 무시할 수 있습니다.

내용을 보면 `suP3r_S3kr1t_Fl4G` 이 굉장히 의심스럽기 때문에 이 경로를 다시 읽어 보면 다음과 같고 플래그를 얻을 수 있습니다.

```
ZmxhZ3s4MmQ4MTczNDQ1ZWE4NjU5NzRmYzA1NjljNWM3Y2Y3Zn0K
=> flag{82d8173445ea865974fc0569c5c7cf7f}
```

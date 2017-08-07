# 2017 SHA - [NET] Vod Kanockers

## Key Words

- Port knocking

## Solution

문제에 웹 서버를 제공해주는데 내용은 없고 주석에 `88 156 983 1287 8743 5622 9123` 이라는 영문 모를 값만 적혀 있습니다.

이리저리 보던 중, 문제가 `Port knocking`에 관련되었음을 알았습니다.

> https://en.wikipedia.org/wiki/Port_knocking
> http://www.portknocking.org

라업 중에 주최측에서 예전에 썻던 라업 중 포트 노킹에 관련된 라업이 있어서 시도를 해보았지만 포트 노킹 이후에 열리는 포트가 존재 하지 않았습니다.

결국엔 단순히 nc 로 해당 포트를 순서대로 접속하면 마지막에서 플래그를 제공해줍니다.

## Result

```
tbkim@ubuntu:~/ctfing/2017_sha/network$ nc 34.249.81.124 88;  nc 34.249.81.124 156 ; nc 34.249.81.124 983 ; nc 34.249.81.124 1287;  nc 34.249.81.124 8743 ; nc 34.249.81.124 5622 ; nc 34.249.81.124 9123

flag{6283a3856ce4766d88c475668837184b}
```

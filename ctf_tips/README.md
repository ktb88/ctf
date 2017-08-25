# CTF TIPS

## Python

* [x] requests
* [x] PIL (known as Pillow) 

## Pwnable

### 로컬에서 리모트 환경 처럼 설정하기 (xinetd)

로컬에서 문제 서버 처럼 리모트로 돌아 가는 환경을 만들어서 테스트 해야 할 경우, 다음 설정을 이용합니다.

먼저 `xinetd` 설치 합니다.

```
$ sudo apt-get install xinetd
```

`xinetd`는 수퍼 데몬으로 대상 바이너리를 데몬화 하고 네트워크 포트를 통해 IO를 할 수 있도록 해줍니다.

설치가 되면 `/etc/xinetd.d/` 폴더에 관리 데몬에 대한 명세를 할 수 있습니다. 이 위치에 파일을 하나 생성해주고 내용을 넣어 줍니다.

저는 `prob` 라는 파일을 만들었습니다.

```
tbkim@ubuntu:~$ cat /etc/xinetd.d/prob

service babyheap
{
    type = UNLISTED
    socket_type = stream
    protocol = tcp
    user = tbkim
    wait = no
    bind = 0.0.0.0
    port = 31337
    server = /home/tbkim/ctf_old/2017_secuinside/pwn_babyheap/babyheap
}
service childheap
{
    type = UNLISTED
    socket_type = stream
    protocol = tcp
    user = tbkim
    wait = no
    bind = 0.0.0.0
    port = 31338
    env = LD_LIBRARY_PATH=/home/tbkim/ctf/2017_secuinside/pwn_childheap/
    server = /home/tbkim/ctf_old/2017_secuinside/pwn_childheap/childheap
}
```

`type`, `socket_type`, `protocol`, `wait` 은 동일하게 적어 주면 되고 그 다음의 파라미터가 자신의 환경에 맞게끔 맞춰주어야 합니다.

- user: 해당 바이너리가 동작할 리눅스 유저 아이디
- bind: listen IP (로컬 아이피 또는 0.0.0.0 으로 설정 합니다. 0.0.0.0 으로 설정한 경우, 외부에서도 접근이 가능 합니다.)
- port: listen Port
- server: 데몬화 시킬 바이너리 절대 경로
- env: (optional) 필요하다면 환경 변수를 등록할 수 있습니다. 위 예어서는 특정 라이브러리를 사용한다면 `LD_LIBRARY_PATH`, `LD_PRELOAD` 등을 통해 원하는 라이브러리 경로를 지정할 수 있습니다.

생성한 뒤, `xinetd` 서비스를 재시작 해줍니다.

```
$ sudo service xinetd restart
```

그리고 `netstat` 명령을 통해 해당 바이너리가 정상적으로 올라왔는지 확인합니다.

```
tbkim@ubuntu:~$ netstat -naop | grep 31337
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:31337           0.0.0.0:*               LISTEN      -                off (0.00/0/0)
tbkim@ubuntu:~$ netstat -naop | grep 31338
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:31338           0.0.0.0:*               LISTEN      -                off (0.00/0/0)
```

만약 지정된 포트에 리슨을 하고 있지 않다면 몇 가지 이유가 있을 수 있습니다.

- `/etc/xinetd.d/` 에 등록된 내용이 잘못된 경우 (오타, 경로 지정)
- `/etc/xinetd.d/` 에 등록된 `server` (대상 바이너리)의 실행 권한이 없는 경우
- 지정된 포트가 이미 사용중인  경우

이러한 잡다한 이슈가 있을 수 있으니 만약 정상적으로 포트가 올라오지 않는다면 여러가지로 확인을 해보셔야 합니다.

이제 바이너리가 올라 왔으니 `nc` 로 테스트 해보시면 됩니다.

```
tbkim@ubuntu:~$ nc 0.0.0.0 31337
1. Create Team
2. Delete Team
3. Manager Team
4. List Team
5. Exit
>^C
```

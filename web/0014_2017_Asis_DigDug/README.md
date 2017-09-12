# 2017 Asis - [WEB] Dig Dug

## Key words

- dig, nslookup

## Solution

문제에 static 페이지만 달랑 있고 아무것도 제공이 안됩니다.

문제 제목이 Dig 인것으로 보아 Dig를 이용하여 페이지를 확인해봅니다.

```
tbkim@ubuntu:~/ctfing/challenges/easy$ dig digx.asisctf.com

; <<>> DiG 9.10.3-P4-Ubuntu <<>> digx.asisctf.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 63075
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 5, ADDITIONAL: 6

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;digx.asisctf.com.      IN  A

;; ANSWER SECTION:
digx.asisctf.com.   300 IN  A   192.81.223.250

tbkim@ubuntu:~/ctfing/challenges/easy$ nslookup
> 192.81.223.250
Server:     127.0.1.1
Address:    127.0.1.1#53

Non-authoritative answer:
250.223.81.192.in-addr.arpa name = airplane.asisctf.com.
```

`airplane.asisctf.com` 이라는 또다른 페이지가 존재 합니다. 이 페이지를 들어 가면 페이지에 또 아무것도 존재 하지 않아 여기저기 보던 중 콘솔 로그에 `Check out https://github.com/chrisbolin/react-detect-offline (if you're online!)` 라는 메시지를 확인했습니다.

해당 깃허브에 들어 가보니 'offline' 모드로 생성할수 있는 방식이 있는데 처음에 airplane.asisctf.com 에 들어 가면 offline으로 하고 flag를 얻으라고 되어 있었기 때문에 console 명령창에 해당 자바스크립트를 넣어 줍니다.

```
window.dispatchEvent(new Event('offline'))
```

그러면 새로운 페이지가 뜨게 되고 안에 플래그가 있습니다.

```
Do you want to be productive? Just go offline, because to maintain a constant connection to the internet is to maintain a constant connection to interruptions, both external and internal.

The external interruptions are legion and well-documented: you have a new message on Gmail, Slack, Twitter, Facebook, Instagram, Snapchat, LinkedIn. Friends, family, coworkers, and spammers: each have direct access to your precious attention.

Offline-only content would also force creators to think differently. Look at this page: there is not a single link, no footnote offering to distract readers. How many good articles have you left half-read because you chased a shiny underlined link? When you are offline, right here is the only place you can be.

I can already hear the groans: “But I have to be online for my job.” I don’t care. Make time. I bet the thing that makes you valuable is not your ability to Google something, but your ability to synthesize information. Do your research online, but create offline.

Now back to your regularly scheduled internet. Just remember to give yourself an occasional gift of disconnection. ASIS{_just_Go_Offline_When_you_want_to_be_creative_!}

❤️ thanks to Chris
```

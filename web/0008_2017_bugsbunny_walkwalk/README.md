# 2017 BugsBunny - [WEB] Walk walk

## Key words

- Cloud Web Service
- AWS S3 bucket
- robots.txt

## Solution

이 문제는 아마존 웹서버 S3 Bucket 의 동작 형태에 대해서 알고 있는지에 대한 문제 입니다.

문제 서버에 접속해서 이리저리 둘러 보면 딱히 ineraction 할 부분이 보이지 않습니다.

보통 이럴경우 `robots.txt` 를 한번 참고 해봅니다.

```
404 Not Found

Code: NoSuchKey
Message: The specified key does not exist.
Key: robots.txt
RequestId: B0778A843C3D94D1
HostId: wQtljBo/Cos8OqAWu34oTSzy7mNPYQNxp4fHA1AObJ8CGld0b58FOX/7GqxdFoADsg0T5HxfRjM=
An Error Occurred While Attempting to Retrieve a Custom Error Document

Code: NoSuchKey
Message: The specified key does not exist.
Key: error.html
```

서버의 `Response Headers`를 확인해보면 위 메시지가 무엇인지 더욱 확실해 집니다.

```
Content-Length:538
Content-Type:text/html; charset=utf-8
Date:Wed, 02 Aug 2017 23:51:56 GMT
Server:AmazonS3
x-amz-id-2:fYIDnC+fTfY/n3eToWo11oE8PHuGh2mBS3Wu8QGkllB4VRutoNy/9681kbYIbmY3LYtnKwUF81A=
x-amz-request-id:99C4E764F7007423
```

서버가 `Amazon S3 Bucket`을 사용하고 있음을 알 수 있습니다. 동작 과정을 좀더 자세히 살펴 보면 다음과 같습니다.

- `http://www.chouaibhm.me` 요청
- `http://cdn.origin.chouaibhm.me.s3.amazonaws.com` 으로 Redirect

위 경로로 접근 시, 어떠한 인증없이 접근이 가능하여 다음과 같은 출력을 보입니다.

> http://www.chouaibhm.me.s3.amazonaws.com/

```xml
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<Name>www.chouaibhm.me</Name>
<Prefix/>
<Marker/>
<MaxKeys>1000</MaxKeys>
<IsTruncated>false</IsTruncated>
<Contents>
<Key>
QnVnc19CdW5ueXtZMHVfNHJlX0MwMDFfdDBkYXlfRHVkM30/flag.txt
</Key>
<LastModified>2017-07-20T07:33:18.000Z</LastModified>
<ETag>"b440f1e6f9a8c0ece5fcdce05252c818"</ETag>
<Size>69</Size>
<StorageClass>STANDARD</StorageClass>
</Contents>
<Contents>
<Key>css/animate.css</Key>
<LastModified>2017-07-20T07:33:11.000Z</LastModified>
... snip ...
```

`QnVnc19CdW5ueXtZMHVfNHJlX0MwMDFfdDBkYXlfRHVkM30/flag.txt` 경로에 플래그 파일이 존재합니다. 따라서 해당 경로로 접근해봅니다.

> http://www.chouaibhm.me.s3.amazonaws.com/QnVnc19CdW5ueXtZMHVfNHJlX0MwMDFfdDBkYXlfRHVkM30/flag.txt

```
you are so close don't be stupid tho xD

Bugs_Bunny{I_am_JOking_lol}
```

아니...이녀석이...

플래그 경로가 `base64` 형태로 되어 있는데 이것을 복호화 하면 진짜 플래그가 나옵니다.

```
Bugs_Bunny{Y0u_4re_C001_t0day_Dud3}
```

`awscli` 라는 cli 툴을 이용하면 좀 보기 편하게 접근이 가능합니다.
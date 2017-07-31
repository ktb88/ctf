# 2017 h3x0r - [FORENSIC] Android Forensic

## Key words

- Android Forensic
- Keygesture
- mmssms

## Description

```
해커의 휴대폰을 획득한 당신, 당신에게 특별한 미션 2가지가 주어졌다.

Flag 1.
그의 패턴을 숫자로 표현하라!

ex)

1 2 3
4 5 6
7 8 9

예를 들어 좌측상단에서 시작하는 Z 모양의 패턴은
1235789 로 표현할 수 있다. 이와 같은 규칙으로
공격자의 패턴을 숫자로 표현하라.

Flag 2.
수상한 메세지를 추적하라!

피해자에게 수상한 메세지를 보냈다던데...
그 흔적을 쫓으면 Flag2가 나온다!

최종 플래그 : md5(flag1+flag2)
```

## Solution

문제로는 안드로이드 파일 시스템을 제공 받습니다.

먼저, Flag 1인 패턴을 풀어보도록 하겠습니다. 안드로이드에서 패턴이 저장되는 위치는 `/data/system/gesture.key`에 저장되어 있습니다.

해당 파일을 열어 보면 다음과 같이 헥스 값을 갖음을 알 수 있습니다.

```
27 86 70 B9 98 F7 03 35 65 C3 8E C8 49 8C 27 A4 74 AC 86 1B
```

이 값은 사용자가 입력한 패턴의 `SHA1`값 입니다. 사용자 입력 패턴은 다음과 같이 헥스 값으로 저장이 됩니다.

```
1 2 3 => \x00 \x01 \x02
4 5 6 => \x03 \x04 \x05
7 8 9 => \x06 \x07 \x08
```

따라서, `guesture.key`에 존재하는 값을 만드는 조합을 무작위 대입을 통해 구합니다.

```python
import itertools
import hashlib

gesture = "278670B998F7033565C38EC8498C27A474AC861B".lower()       
table = ["\x00", "\x01", "\x02", "\x03", "\x04", "\x05", "\x06", "\x07", "\x08"]

'''
0 1 2      1 2 3
3 4 5  =>  4 5 6
6 7 8      7 8 9

1234576820 -> 245687931
'''

mp = itertools.permutations(table, 9)
for m in mp:
	m = "".join(x for x in m)

	if hashlib.sha1(m).hexdigest() == gesture:
		print m.encode("hex")
		break
```

위 결과, 패턴은 `245687931` 임을 알 수 있습니다.

두 번째로, Flag2의 위치는 수상한 메시지를 추적하는 것이 목적입니다. 메시지라고 햇기 때문에 사용자가 설치한 메시지 앱이나 디폴트앱 등등을 조사하다가 결국엔 `/data/data/com.android.providers.telephony/databases/mmssms.db` 에 메시지 관련 정보가 저장됨을 알수 있었습니다.

이를 `sqlite browser`로 열어 내용을 확인해본 결과

```
Hi! Do you want to decrypt your file? Then, Deposit Here! SV9MMHYzX1J1TTE0XzdpbjZFbA==
```

라는 문자열이 있었고, `SV9MMHYzX1J1TTE0XzdpbjZFbA==`를 `base64` 형식으로 디코드 하면 `I_L0v3_RuM14_7in6El` 값이 나오게 됩니다.

따라서, `md5("245687931" + "I_L0v3_RuM14_7in6El")` 값인 `d4555b9549dcb4915c1464e8d74682f3` 가 정답이 됩니다.

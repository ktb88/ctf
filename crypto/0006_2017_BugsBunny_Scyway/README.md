# 2017 BugsBunny - [CRYPTO] Scy Way

## Key words

- Classic Cipher
- Scytale

## Solution

문제에 다음과 같은 내용을 제공합니다.

```
IHUDERMRCPESOLLANOEIHR
```

문제 제목에 `Scy` 라고 되어 있기 때문에 `Scytale`을 생각해볼 수 있습니다.

![](./Skytable.png)

이 문제를 풀기 위해서는 제공된 문자열을 나눠보면 되는데 문자열의 길이가 22이기 때문에 2또는 11로 밖에 나눠 지지 않습니다. 두 줄로 나눳을 때 플래그를 발견할 수 있었습니다.

```
IHUDERMRCPE
SOLLANOEIHR
```

> ISHOULDLEARNMORECIPHER
> = I SHOULD LEARN MORE CIPHER

# 2017 BugsBunny - [CRYPTO] Crypto-50

## Key words

- Base64

## Solution

문제에 엄청나게 긴 `base64` 문자열을 제공합니다. 이를 계속 디코딩 해도 계속 `base64`가 나오기 때문에 더이상 디코딩이 될 수 없을 때 까지 디코딩을 하면 플래그 나옵니다.

## Solution Code

```python
fd = open("crypto50.txt","r")
data = fd.read()
fd.close()

while True:
    try:
        data = data.decode("base64")
    except Exception as e:
        print data
        break
```

> Bugs_Bunny{N0T_H4Rd_4T_4ll}
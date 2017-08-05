# 2017 BugsBunny - [CRYPTO] Crypto-15

## Key words

- Classic Cipher
- Cesar 
- Rot12, Rot13

## Solution

문제에서 아래 파일을 제공해줍니다.

```
# -*- pbqvat: hgs-8 -*-
#/hfe/ova/rai clguba
vzcbeg fgevat
# Synt : Cvht_Cvooz{D35bS_3OD0E3_4S3_O0U_T3DvS3_BU_4MM}
qrs rapbqr(fgbel, fuvsg):
  erghea ''.wbva([
            (ynzoqn p, vf_hccre: p.hccre() vs vf_hccre ryfr p)
                (
                  ("nopqrstuvwxyzabcdefghijklm"*2)[beq(pune.ybjre()) - beq('n') + fuvsg % 26],
                  pune.vfhccre()
                )
            vs pune.vfnycun() ryfr pune
            sbe pune va fgbel
        ])


qrs qrpbqr(fgbel,xrl):
    cnff


vs __anzr__ == '__znva__':
    xrl = [_LBHE_XRL_URER_]
    cevag qrpbqr("Cvht_Cvooz{D35bS_3OD0E3_4S3_O0U_T3DvS3_BU_4MM}",xrl)
```

형태가 파이썬 같은데 뭔가 문자가 바뀐 것 같습니다.

일단은 간단히 `Rot13` 으로 돌리면 정상적인 파이썬 코드가 나옵니다.

```python
# -*- coding: utf-8 -*-
#/usr/bin/env python
import string
# Flag : Piug_Pibbm{Q35oF_3BQ0R3_4F3_B0H_G3QiF3_OH_4ZZ}
def encode(story, shift):
  return ''.join([
            (lambda c, is_upper: c.upper() if is_upper else c)
                (
                  ("abcdefghijklmnopqrstuvwxyz"*2)[ord(char.lower()) - ord('a') + shift % 26],
                  char.isupper()
                )
            if char.isalpha() else char
            for char in story
        ])


def decode(story,key):
    pass


if __name__ == '__main__':
    print ord('n') - ord('b')
    exit()
    key = [_YOUR_KEY_HERE_]
    print decode("Piug_Pibbm{Q35oF_3BQ0R3_4F3_B0H_G3QiF3_OH_4ZZ}",key)
```

내용을 보면 이것도 `Rot` 연산인데 인코딩된 문자열과 `BugsBunny{`를 고려한 결과 `Rot12`로 되어 있음을 알 수 있습니다. 따라서 `Rot12`로 인코딩된 문자열을 복호화 하면 플래그 나옵니다.

## Solution Code

```python
import string

fd = open("crypto15.txt", "r")
data = fd.read()
fd.close()

rot13 = string.maketrans(
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
print string.translate(data, rot13)

rot12 = string.maketrans(
    "ABCDEFGHIJKLabcdefghijklMNOPQRSTUVWXmnopqrstuvwxYZyz",
    "MNOPQRSTUVWXmnopqrstuvwxYZABCDEFGHIJyzabcdefghijKLkl")
print string.translate("Piug_Pibbm{Q35oF_3BQ0R3_4F3_B0H_G3QiF3_OH_4ZZ}", rot12)

# Piug_Pibbm{Q35oF_3BQ0R3_4F3_B0H_G3QiF3_OH_4ZZ}
# Bugs_Bunny{C35aR_3NC0D3_4R3_N0T_S3CuR3_AT_4LL}
```

# 2017 SHA - [REV] asby

## Key words

- PE Reversing

## Solution

바이너리를 동적으로 분석해보면 내가 입력한 글자가 내부 로직에 의해 다른 글자로 변환되고 해당 글자와 어떤 글자 배열을 비교 합니다.

따라서, 바이너리에서 내 글자를 어떻게 변환시키는지 표를 만들고 바이너리에서 요구되는 글자를 맞추기 위해 내가 어떻게 입력을 해야 하는지 맞추면 내 입력 자체가 플래그라는 것을 알 수 있습니다.

```
abcdefghijklmnopqrstuvwxyz  0   1   2   3   4   5   6   7   8   9 {}
KHINOLMBC@AFGDEZ[XY^_\]RSP\x1a\x1b\x18\x19\x1e\x1f\x1c\x1d\x12\x13QW
```

문제에서 요구되었던 스트링과 위 테이블을 이용하여 찾은 스트링은 다음과 같습니다.

```
Compare String : LFKMQ\x1a\x18\x1eHKK\x12KI\x1a\x19OL\x18\x18LNNO\x1c\x1bI\x1aL\x1b\x1b\x1a\x1c\x13L\x18LW
Input String   : flag{024baa8ac03ef22fdde61c0f11069f2f}
```

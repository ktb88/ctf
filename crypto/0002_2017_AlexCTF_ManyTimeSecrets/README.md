# 2017 AlexCTF - [CRYPTO] ManyTimeSecrets

## Key words

- One-time pad vulnerability
- crib dragging attack
- guessing words

## Solution

문제에 msg 파일이 주어 집니다.

```
0529242a631234122d2b36697f13272c207f2021283a6b0c7908
2f28202a302029142c653f3c7f2a2636273e3f2d653e25217908
322921780c3a235b3c2c3f207f372e21733a3a2b37263b313012
2f6c363b2b312b1e64651b6537222e37377f2020242b6b2c2d5d
283f652c2b31661426292b653a292c372a2f20212a316b283c09
29232178373c270f682c216532263b2d3632353c2c3c2a293504
613c37373531285b3c2a72273a67212a277f373a243c20203d5d
243a202a633d205b3c2d3765342236653a2c7423202f3f652a18
2239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c
263e203d63232f0f20653f207f332065262c3168313722367918
2f2f372133202f142665212637222220733e383f2426386b
```

문제에 `One-time pad`로 되어 있는데, 만약 키를 여러번 사용하게 되면 `xor` 기반이기 때문에 `crib dragging attack`에 취약하게 됩니다.
- http://samwho.co.uk/blog/2015/07/18/toying-with-cryptography-crib-dragging/

```
ct = pt ^ key
pt = ct ^ key
key = ct ^ pt
```

아직 `key`를 모르지만 대회 플래그 포멧이 `ALEXCTF{` 인 것을 감안하여 `xor`을 해보았습니다.

```
KEY: ALEXCTF{__________________
     01234567890123456789012345
[00] Dear Fri__________________
[01] nderstoo__________________
[02] sed One __________________
[03] n scheme__________________
[04] is the o__________________
[05] hod that__________________
[06]  proven __________________
[07] ever if __________________
[08] cure, Le__________________
[09] gree wit__________________
[10] ncryptio________________
```

부분 적이지만 정상적으로 `plain text`가 추출된 것 같습니다. 여기서 부터 한 글자씩 조립해 봅니다.

먼저, 0번 인덱스의 `Dear Fri`를 `Dear Friend`로 변경하여 `key`를 추출해봅니다.

```
key = ct ^ pt

Plain text : Dear Friend
Key        : ALEXCTF{HER
```

원본 텍스트를 이런식으로 계속 유추 하면서 키를 추출합니다.

## Result

```
KEY: ALEXCTF{__________________
     01234567890123456789012345
[00] Dear Fri__________________
[01] nderstoo__________________
[02] sed One __________________
[03] n scheme__________________
[04] is the o__________________
[05] hod that__________________
[06]  proven __________________
[07] ever if __________________
[08] cure, Le__________________
[09] gree wit__________________
[10] ncryptio________________

Plain text : Dear Friend
Key        : ALEXCTF{HER
GUESSING : 'nderstood m_______________' -> 'nderstood my'
KEY IS : 'ALEXCTF{HERE'

GUESSING : ' proven to b______________' -> ' proven to be'
KEY IS : 'ALEXCTF{HERE_'

GUESSING : ' proven to be_____________' -> ' proven to be '
KEY IS : 'ALEXCTF{HERE_G'

GUESSING : 'sed One time p____________' -> 'sed One time pa'
KEY IS : 'ALEXCTF{HERE_GO'

GUESSING : 'n scheme, I hea___________' -> 'n scheme, I hear'
KEY IS : 'ALEXCTF{HERE_GOE'

GUESSING : 'Dear Friend, Thi__________' -> 'Dear Friend, This'
KEY IS : 'ALEXCTF{HERE_GOES'

GUESSING : 'Dear Friend, This_________' -> 'Dear Friend, This '
KEY IS : 'ALEXCTF{HERE_GOES_'

GUESSING : 'nderstood my mista________' -> 'nderstood my mistak'
KEY IS : 'ALEXCTF{HERE_GOES_T'

GUESSING : 'hod that is mathema_______' -> 'hod that is mathemat'
KEY IS : 'ALEXCTF{HERE_GOES_TH'

GUESSING : 'hod that is mathemat______' -> 'hod that is mathemati'
KEY IS : 'ALEXCTF{HERE_GOES_THE'

GUESSING : 'hod that is mathemati_____' -> 'hod that is mathematic'
KEY IS : 'ALEXCTF{HERE_GOES_THE_'

GUESSING : 'hod that is mathematic____' -> 'hod that is mathematica'
KEY IS : 'ALEXCTF{HERE_GOES_THE_K'

GUESSING : 'hod that is mathematica___' -> 'hod that is mathematical'
KEY IS : 'ALEXCTF{HERE_GOES_THE_KE'

GUESSING : 'hod that is mathematical__' -> 'hod that is mathematicall'
KEY IS : 'ALEXCTF{HERE_GOES_THE_KEY'

GUESSING : 'hod that is mathematicall_' -> 'hod that is mathematically'
KEY IS : 'ALEXCTF{HERE_GOES_THE_KEY}'


KEY: ALEXCTF{HERE_GOES_THE_KEY}
     01234567890123456789012345
[00] Dear Friend, This time I u
[01] nderstood my mistake and u
[02] sed One time pad encryptio
[03] n scheme, I heard that it
[04] is the only encryption met
[05] hod that is mathematically
[06]  proven to be not cracked
[07] ever if the key is kept se
[08] cure, Let Me know if you a
[09] gree with me to use this e
[10] ncryption scheme always.
```

## Solution Code

```python
def sxor(c, k):
	res   = ""
	len_c = len(c)
	len_k = len(k)
	min_len = len_c

	if len_c > len_k:
		min_len = len_k

	for i in xrange(min_len):
		res += chr(ord(c[i]) ^ ord(k[i]))

	res += "_" * (len(c)-len(k))
	return res

def get_char(ct, idx, offset, g_char):
	return chr(ord(ct[idx][offset]) ^ ord(g_char))

def show_res(ct, key):
	print "%4s 01234567890123456789012345" % (" ")
	for i in range(0, len(ct)):
		print "[%02d] %s" % (i, sxor(ct[i], key))
	print

ct = None
with open("msg") as fd:
	ct = fd.read().split("\n")[:-1]
print ct

for i in range(0, len(ct)):
	ct[i] = ct[i].decode("hex")

g_k = "ALEXCTF{HER"
show_res(ct, g_k)

g_p = "Dear Friend"
show_res(ct, g_p)

guess = [
	(1, 11, "y"),
	(6, 12, "e"),
	(6, 13, " "),
	(2, 14, "a"),
	(3, 15, "r"),
	(0, 16, "s"),
	(0, 17, " "),
	(1, 18, "k"),
	(5, 19, "t"),
	(5, 20, "i"),
	(5, 21, "c"),
	(5, 22, "a"),
	(5, 23, "l"),
	(5, 24, "l"),
	(5, 25, "y")
]

for idx, off, ch in guess:
	g_k += get_char(ct, idx, off, ch)
	print "KEY : " + g_k

print
show_res(ct, g_k)
```

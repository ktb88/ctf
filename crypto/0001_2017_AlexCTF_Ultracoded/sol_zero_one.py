from binascii import unhexlify

target = "./zero_one"
msg1   = ""
print "[step 1] : read from file"
with open(target) as fd:
	msg1 = fd.read()
print msg1 + "\n"

print "[step 2] reaplce 'ZERO' to '0' and 'ONE' to '1'"
msg2 = ""
for m in msg1.split(" "):
	m = m.replace("\n","")
	if m == "ONE": msg2 += "1"
	elif m == "ZERO": msg2 += "0"
print msg2

print "[step 3] convert binary string to binary and unhex"
msg3 = ""
msg3 = unhexlify('%x' % int(msg2, 2))
print msg3 + "\n"

print "[step 4] decode base64"
msg4 = ""
msg4 = msg3.decode("base64")
print msg4

encode_mc = {
        'A': '.-',              'a': '.-',
        'B': '-...',            'b': '-...',
        'C': '-.-.',            'c': '-.-.',
        'D': '-..',             'd': '-..',
        'E': '.',               'e': '.',
        'F': '..-.',            'f': '..-.',
        'G': '--.',             'g': '--.',
        'H': '....',            'h': '....',
        'I': '..',              'i': '..',
        'J': '.---',            'j': '.---',
        'K': '-.-',             'k': '-.-',
        'L': '.-..',            'l': '.-..',
        'M': '--',              'm': '--',
        'N': '-.',              'n': '-.',
        'O': '---',             'o': '---',
        'P': '.--.',            'p': '.--.',
        'Q': '--.-',            'q': '--.-',
        'R': '.-.',             'r': '.-.',
        'S': '...',             's': '...',
        'T': '-',               't': '-',
        'U': '..-',             'u': '..-',
        'V': '...-',            'v': '...-',
        'W': '.--',             'w': '.--',
        'X': '-..-',            'x': '-..-',
        'Y': '-.--',            'y': '-.--',
        'Z': '--..',            'z': '--..',
        '0': '-----',           ',': '--..--',
        '1': '.----',           '.': '.-.-.-',
        '2': '..---',           '?': '..--..',
        '3': '...--',           ';': '-.-.-.',
        '4': '....-',           ':': '---...',
        '5': '.....',           "'": '.----.',
        '6': '-....',           '-': '-....-',
        '7': '--...',           '/': '-..-.',
        '8': '---..',           '(': '-.--.-',
        '9': '----.',           ')': '-.--.-',
        ' ': ' ',               '_': '..--.-',
}

msg5 = ""
decode_mc = dict((v, k) for (k, v) in encode_mc.items())
msg5 = ''.join(decode_mc[dec] for dec in msg4.split(" "))
print msg5


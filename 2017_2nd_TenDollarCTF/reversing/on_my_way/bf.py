import hashlib

chMoves = ["L", "D", "U", "R", "0", "1"]
xor = "20372966"

for ch in chMoves:
    hexMsg = hashlib.md5(ch + xor).hexdigest()
    print ch + " => " + hexMsg

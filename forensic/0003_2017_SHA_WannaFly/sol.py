fd = open("dump", "r")
data = fd.read()
fd.close()

fd = open("res","wb")
fd.write(data.decode("base64"))
fd.close()
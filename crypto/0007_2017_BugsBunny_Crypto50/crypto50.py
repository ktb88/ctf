fd = open("crypto50.txt","r")
data = fd.read()
fd.close()

while True:
    try:
        data = data.decode("base64")
    except Exception as e:
        print data
        break
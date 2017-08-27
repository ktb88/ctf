data = open("dump.bin", "r").read().decode("base64")

for i in range(0, 50):
    open("dmup_%02d.png"%(i), "wb").write(data)
    data = data.split("IEND")[1][4:].decode("base64")
    idx = data.index("IEND")

    if len(data) >= idx+8:
        continue

    open("dmup_%02d.png"%(i), "wb").write(data)
    break

# d4rk{1mag3_m4n1pul4t10n_F7W}c0d3
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
# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
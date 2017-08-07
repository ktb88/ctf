from Crypto.Cipher import AES
import base64

obj = AES.new('n0t_just_t00ling', AES.MODE_CBC, '7215f7c61c2edd24')
ciphertext = "cnKlXI1pPEbuc1Av3eh9vxEpIzUCvQsQLKxKGrlpa8PvdkhfU5yyt9pJw43X9Mqe"
message = obj.decrypt(base64.b64decode(ciphertext))
print message

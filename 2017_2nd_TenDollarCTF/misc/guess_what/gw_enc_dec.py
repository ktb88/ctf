#coding: utf-8

from PIL import Image

def encrypt_png(png_name, target_name, output_name):
	print "[*][*][*] Encrypt File : {} png에 넣기 : {} [*][*][*]".format(target_name, png_name)
	img = Image.open(png_name, "r").convert("RGBA")
	width, height = img.size
	data = img.load()

	new_img = Image.new("RGBA", (width, height))
	new_img_pixel = new_img.load()

	flag_data = open(target_name, "rb").read()
	flag_len = len(flag_data)

	cnt = 0
	for w in range(0, width):
		for h in range(0, height):
			pixel = data[w, h]
			(r, g, b, a) = pixel

			if cnt < flag_len:
				new_img_pixel[w, h] = (r, g, b, ord(flag_data[cnt]))
				cnt += 1
			else:
				new_img_pixel[w, h] = (r, g, b, a)

	new_img.save(output_name)
	print "[*][*][*] Encrypt 완료 : {} [*][*][*]".format(output_name)

def decrypt_png(png_name, output_name):
	print "[*][*][*] Decrypt할 파일은 : {} [*][*][*]".format(png_name)

	img = Image.open(png_name, "r").convert("RGBA")
	width, height = img.size
	data = img.load()

	output = ""

	for w in range(0, width):
		for h in range(0, height):
			pixel = data[w, h]
			(r, g, b, a) = pixel
			output += chr(a)

	open(output_name, "wb").write(output)
	print "[*][*][*] Decrypt 완료! : {} [*][*][*]".format(output_name)

encrypt_png("TDCTF.png", "ENCTDCTF.zip", "challenge.png")
decrypt_png("challenge.png", "dec_challenge.zip")
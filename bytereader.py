with open("filename.txt", "rb") as f:
	content = f.read()


read_bytes = []
for i in content:
	read_bytes.append(i)


def filler(string):
	return "0"*(8-len(string))+string

amount_keys = read_bytes.pop(0)

keys = {}

for i in range(amount_keys):
	key_char = read_bytes.pop(0)
	key_len = read_bytes.pop(0)
	if key_len > 8:
		repeats = key_len//8
		key_list = []
		for i in range(0,repeats+1):
			key_list.append(read_bytes.pop(0))
		key = filler(bin(key_list.pop(0))[2:])

		for i in key_list:
			key += filler(bin(i)[2:])

	else:
		key = filler(bin(read_bytes.pop(0))[2:])

	key = key[len(key)-key_len:]

	keys.update({key: chr(key_char)})

len_last = read_bytes.pop(0)
last_byte = bin(read_bytes.pop())[2:]
last_byte = filler(last_byte)[8-len_last:]

code = ""

for byte in read_bytes:
	code += filler(bin(byte)[2:])

code += last_byte

text = ""
bfr = ""

for char in code:
	bfr += char
	if bfr in keys:
		text += keys[bfr]
		bfr = ""

print(keys)
with open("result.txt", "w") as f:
	f.write(text)
	f.close()
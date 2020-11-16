import tree_code_generator as huffman

text = huffman.get_data("loremipsum.txt")
tree = huffman.build_tree(text)
codes = huffman.get_codes(tree)
result = "".join([codes[letter] for letter in text])

splitcode = []
for index in range(0, len(result), 8):
    splitcode.append(result[index : index + 8])

class Byte:
	def __init__(self, char, lenght, key):
		self.char = char
		self.lenght = lenght
		self.key = key

key_bytes = []

amount_keys = len(codes)
for key, value in codes.items():
	key_bytes.append(Byte(ord(key), len(value), value))

len_last = len(splitcode[-1])
for byte in key_bytes:
	print(byte.char)
	print(chr(byte.char))
	print(byte.lenght)
	print(byte.key)
	print("--------------")

byte_list = []

byte_list.append(amount_keys)

for byte in key_bytes:
	byte_list.append(byte.char)
	byte_list.append(byte.lenght)
	if byte.lenght > 8:
		split = []
		for index in range(len(byte.key), 0, -8):
			step = 8
			if index - 8 <= 0:
				step = index
			split.append(byte.key[index - step : index])
			split.reverse()
		for i in split:
			byte_list.append(int(i, 2))
	else:
		byte_list.append(int(byte.key, 2))

byte_list.append(len_last)

for code in splitcode:
	code = int(code, 2)
	byte_list.append(code)


with open("filename.txt", "wb") as f:
	newFileByteArray = bytearray(byte_list)
	print(type(newFileByteArray))
	f.write(newFileByteArray)

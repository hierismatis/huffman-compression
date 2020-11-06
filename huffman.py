file = open("loremipsum.txt", "r")
text = file.read()

freq = {}

for letter in text:
	if letter in freq:
		freq[letter] += 1
	else:
		freq.update({letter: 1})


freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1])}

freq_ls = [k for k, v in freq.items()]

branch = {freq[freq_ls[0]]+freq[freq_ls[1]]:[freq_ls[0], freq_ls[1]]}

print(branch)

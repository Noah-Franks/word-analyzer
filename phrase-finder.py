import os



def load_from_file(filepath):   # loads the output of word-analyzer into memory
	data = {}

	with open(filepath, 'r') as source:
		
		for line in source:

			if line.find('\t') >= 0:

				disposition =     line[: line.find(' ')      ]
				frequency   = int(line[  line.find(' ') + 1 :])

				data[word][disposition] = frequency

			else:
				word = line[:line.find('\n')]
				data[word] = {}

	return data


data = load_from_file('word-frequencies.txt')


for word, disposition_dict in data.items():
	print(word)
	for disposition, frequency in disposition_dict.items():
		print("\t" + disposition + " " + str(frequency))
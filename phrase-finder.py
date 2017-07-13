import os



def load_from_file(filepath):   # loads the output of word-analyzer into memory
	data = {}

	with open(filepath, 'r') as source:
		
		for line in source:

			if line.find('\t') >= 0:

				disposition =     line[line.find('\t') + 1 : line.find(' ')      ]
				frequency   = int(line[  line.find(' ') + 1 :])

				data[word][disposition] = frequency

			else:
				word = line[:line.find('\n')]
				data[word] = {}

	return data

def print_data(data):
	for word, disposition_dict in data.items():
		print(word)
		for disposition, frequency in disposition_dict.items():
			print("\t%s %s" % (disposition, frequency))


def prune_data_by_percentage(data, limit_percentage):   # shortens the amount of data to work with by eliminating rare words

	total_words = 0   # The total number of words in the data as the sum of frequencies

	for word, disposition_dict in data.items():
		total_words += disposition_dict['total']
	
	for word, disposition_dict in data.items():
		frequency_percentage = disposition_dict['total'] / total_words
		print(frequency_percentage)


data = load_from_file('word-frequencies.txt')
prune_data_by_percentage(data, 1.0)

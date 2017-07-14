import os



def load_from_file(filepath):   # loads the output of word-analyzer into memory
	data = None

	read_string = ''
	with open(filepath, 'r') as source:
		for line in source:
			read_string += line

	print (read_string)
	data = dict(read_string)
		

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
print(data)
#prune_data_by_percentage(data, 1.0)

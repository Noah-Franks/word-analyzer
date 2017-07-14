import os
import pickle

# words data structure:
#
# words
#     word
#          total frequency              The number of times a word is present in a set of files
#          file frequency               The number of different files a word is present in
#          dispositions                 The outcome of the phone call
#               disposition             The choice selected by an agent
#                    frequency          The number of times a word is in a file with a given disposition
#          ...
#     ...


def load_from_file(filepath):   # loads the output of word-analyzer into memory
	return pickle.load(open("word-frequencies.txt", "rb"))

def print_dictionary(dictionary, tabs=0):
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            print("\t" * tabs + str(key))
            print_dictionary(dictionary[key], tabs + 1)
        else:
            print("\t" * tabs       + str(key))
            print("\t" * (tabs + 1) + str(dictionary[key]))


def prune_data_by_percentage(data, limit_percentage):   # shortens the amount of data to work with by eliminating rare words

	total_words = 0   # The total number of words in the data as the sum of frequencies

	for word, disposition_dict in data.items():
		total_words += disposition_dict['total']
	
	for word, disposition_dict in data.items():
		frequency_percentage = disposition_dict['total'] / total_words
		print(frequency_percentage)


words = load_from_file('word-frequencies.txt')
print(words)
#prune_data_by_percentage(data, 1.0)

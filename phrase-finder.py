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
	return pickle.load(open(filepath, "rb"))

def print_dictionary(dictionary, tabs=0):
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            print("\t" * tabs + str(key))
            print_dictionary(dictionary[key], tabs + 1)
        else:
            print("\t" * tabs       + str(key))
            print("\t" * (tabs + 1) + str(dictionary[key]))

def prune_data_by_percentage(data, meta, limit_percentage):   # shortens the amount of data to work with by eliminating rare words
	
	pruned_data = dict(data)

	for word, root_dict in data.items():
		frequency_percentage = root_dict['file frequency'] / meta['file count'] * 100
		if frequency_percentage > limit_percentage:
			pass
			#print("%s\t%s" % (word, frequency_percentage))
		else:
			del pruned_data[word]

	return data


def find_word_success(data):

	for word, root_dict in data.items():
		for disposition in root_dict['dispositions']:
			print("%s\t%s\t%s" % (word, disposition, root_dict['dispositions'][disposition] / root_dict['total frequency']))


words = load_from_file('word-frequencies.txt')
meta  = load_from_file('meta.txt')
words = prune_data_by_percentage(words, meta, 10.0)   # Remove the lower-frequency words to improve the analysis
words = find_word_success(words)

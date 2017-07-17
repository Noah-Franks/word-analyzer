import os
import pickle
import math
import statistics as stats

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

	return pruned_data


def analyze_word_disposition_percentage_composition(data):

	analysis = {}

	for word, root_dict in data.items():
		for disposition in root_dict['dispositions']:

			percentage = root_dict['dispositions'][disposition] / root_dict['total frequency']
			
			if disposition not in analysis:
				analysis[disposition] = {}
				analysis[disposition]['values'] = []
			analysis[disposition]['values'].append(percentage)

	for disposition in analysis:
		mean = sum(analysis[disposition]['values']) / len(analysis[disposition]['values'])
		standard_deviation = stats.pstdev(analysis[disposition]['values'], mean)

		analysis[disposition]['mean'] = mean
		analysis[disposition]['standard deviation'] = standard_deviation

		print('%s\n\tmu: %s\n\tst: %s' % (disposition, mean * 100, standard_deviation))

		for word in data:
			if disposition in data[word]['dispositions']:
				percentage = data[word]['dispositions'][disposition] / data[word]['total frequency']
				z_score = (percentage - mean) / standard_deviation
				if math.fabs(z_score) > 3.819:
					print('\t%s%sp < %s\tz: %s' % (word, ' ' * (20 - len(word)), 0.0001, z_score))
				elif math.fabs(z_score) > 3.291:
					print('\t%s%sp < %s\tz: %s' % (word, ' ' * (20 - len(word)), 0.001, z_score))
				elif math.fabs(z_score) > 2.576:
					print('\t%s%sp < %s\tz: %s' % (word, ' ' * (20 - len(word)), 0.01, z_score))
				elif math.fabs(z_score) > 1.960:
					print('\t%s%sp < %s\tz: %s' % (word, ' ' * (20 - len(word)), 0.05, z_score))





words = load_from_file('word-frequencies.txt')
meta  = load_from_file('meta.txt')
words = prune_data_by_percentage(words, meta, 0.5)   # Remove the lower-frequency words to improve the analysis
words = analyze_word_disposition_percentage_composition(words)

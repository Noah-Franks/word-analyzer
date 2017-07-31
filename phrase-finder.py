import os
import sys
import pickle
import math
import statistics as stats

# words data structure:
#
# words
#     word
#          total frequency                    The number of times a word is present in a set of files
#          file frequency                     The number of different files a word is present in
#          agents                             The agents associated with a word
#               agent                         The agent
#                    frequency                The number of times a word is in a file with a given agent
#               ...
#          dispositions                       The outcomes associated with a word
#               disposition                   The choice selected by an agent
#                    frequency                The number of times a word is in a file with a given disposition
#               ...
#          phrases                            The phrases the word ends
#               phrase length
#                    phrase root              The previous words in the phrase
#                         total frequency     The number of times a word completes a phrase of a specific length
#                         file frequency      The number of different files a word is present in
#                         dispositions        The outcomes associated with a phrase
#                              disposition    The choice selected by an agent
#                              frequency      The number of times a phrase is in a file with a given disposition
#                         ...
#                    ...
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

def prune_data_by_word_percentage(data, meta, limit_percentage):   # shortens the amount of data to work with by eliminating rare words
	
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
					print('\t%s%s\tp < %s  \t%%: %s\tz: %s' % (word, ' ' * (12 - len(word)), 0.0001, percentage, z_score))
				elif math.fabs(z_score) > 3.291:
					print('\t%s%s\tp < %s   \t%%: %s\tz: %s' % (word, ' ' * (12 - len(word)), 0.001, percentage, z_score))
				elif math.fabs(z_score) > 2.576:
					print('\t%s%s\tp < %s    \t%%: %s\tz: %s' % (word, ' ' * (12 - len(word)), 0.01, percentage, z_score))
				elif math.fabs(z_score) > 1.960:
					print('\t%s%s\tp < %s    \t%%: %s\tz: %s' % (word, ' ' * (12 - len(word)), 0.05, percentage, z_score))

def analyze_word_agent_percentage_composition(data):

	analysis = {}

	for word, root_dict in data.items():
		for agent in root_dict['agents']:

			percentage = root_dict['agents'][agent] / root_dict['total frequency']

			if agent not in analysis:
				analysis[agent] = {}
				analysis[agent]['values'] = []
			analysis[agent]['values'].append(percentage)

	for agent in analysis:
		mean = sum(analysis[agent]['values']) / len(analysis[agent]['values'])
		standard_deviation = stats.pstdev(analysis[agent]['values'], mean)

		analysis[agent]['mean'] = mean
		analysis[agent]['standard deviation'] = standard_deviation

		print('%s\n\tmu: %s\n\tst: %s' % (agent, mean * 100, standard_deviation))

		for word in data:
			if agent in data[word]['agents']:
				percentage = data[word]['agents'][agent] / data[word]['total frequency']
				z_score = (percentage - mean) / standard_deviation
				if math.fabs(z_score) > 3.819:
					print('\t%s%s\tp < %s  \t%%: %s\tz: %s' % (word, ' ' * (12 - len(word)), 0.0001, percentage, z_score))
				elif math.fabs(z_score) > 3.291:
					print('\t%s%s\tp < %s   \t%%: %s\tz: %s' % (word, ' ' * (12 - len(word)), 0.001, percentage, z_score))
				elif math.fabs(z_score) > 2.576:
					print('\t%s%s\tp < %s    \t%%: %s\tz: %s' % (word, ' ' * (12 - len(word)), 0.01, percentage, z_score))
				elif math.fabs(z_score) > 1.960:
					print('\t%s%s\tp < %s    \t%%: %s\tz: %s' % (word, ' ' * (12 - len(word)), 0.05, percentage, z_score))

def analyze_word_phrase_composition(data):

	phrases = {}
	phrases['lengths'] = {}

	for word in data:
		for phrase_length in data[word]['phrases']:

			if phrase_length not in phrases['lengths']:
				phrases['lengths'][phrase_length] = {}
				phrases['lengths'][phrase_length]['phrases'] = {}       # Phrases paired with frequencies
				phrases['lengths'][phrase_length]['frequencies'] = []   # List of frequencies used for statistics

			for root in data[word]['phrases'][phrase_length]:

				frequency = words[word]['phrases'][phrase_length][root]['total frequency']

				phrase = word
				for part in root.split():
					phrase = "%s %s" % (part, phrase)
				#phrase = "%s %s" % (word, phrase)

				phrases['lengths'][phrase_length]['phrases'][phrase] = frequency
				phrases['lengths'][phrase_length]['frequencies'].append(frequency)


	for phrase_length in phrases['lengths']:
		mean = sum(phrases['lengths'][phrase_length]['frequencies']) / len(phrases['lengths'][phrase_length]['frequencies'])
		standard_deviation = stats.pstdev(phrases['lengths'][phrase_length]['frequencies'], mean)

		phrases['lengths'][phrase_length]['common'] = {}   # A phrase list of only the statistically significant

		for phrase in phrases['lengths'][phrase_length]['phrases']:

			frequency = phrases['lengths'][phrase_length]['phrases'][phrase]
			z_score = (frequency - mean) / standard_deviation

			if math.fabs(z_score) > 3.819:
				print('\t%s%s\tp < %s  \tn: %s\tz: %s' % (phrase, ' ' * (6 * phrase_length - len(phrase)), 0.0001, frequency, z_score))
			elif math.fabs(z_score) > 3.291:
				print('\t%s%s\tp < %s   \tn: %s\tz: %s' % (phrase, ' ' * (6 * phrase_length - len(phrase)), 0.001, frequency, z_score))
			elif math.fabs(z_score) > 2.576:
				print('\t%s%s\tp < %s    \tn: %s\tz: %s' % (phrase, ' ' * (6 * phrase_length - len(phrase)), 0.01, frequency, z_score))
			elif math.fabs(z_score) > 1.960:
				print('\t%s%s\tp < %s    \tn: %s\tz: %s' % (phrase, ' ' * (6 * phrase_length - len(phrase)), 0.05, frequency, z_score))
			else:
				continue

			phrases['lengths'][phrase_length]['common'][phrase] = frequency   # Getting here means it's statistically significant
			


words = load_from_file('word-frequencies.txt')
meta  = load_from_file('meta.txt')

for argument in sys.argv[1:]:

	if argument.find('p') != -1:
		pruned = prune_data_by_word_percentage(words, meta, 0.5)
		analyze_word_phrase_composition(pruned)

	if argument.find('a') != -1:
		pruned = prune_data_by_word_percentage(words, meta, 0.5)
		analyze_word_agent_percentage_composition(pruned)

	if argument.find('d') != -1:
		pruned = prune_data_by_word_percentage(words, meta, 0.5)
		analyze_word_disposition_percentage_composition(pruned)

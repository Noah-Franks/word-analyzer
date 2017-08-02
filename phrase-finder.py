import os
import sys
import pickle
import math
import statistics as stats

# dictionary data structures:
#
# words
#     word
#          total frequency                         The number of times a word is present in a set of files
#          file frequency                          The number of different files a word is present in
#          agents                                  The agents associated with a word
#               agent                              The agent
#                    frequency                     The number of times a word is in a file with a given agent
#               ...
#          dispositions                            The outcomes associated with a word
#               disposition                        The choice selected by an agent
#                    frequency                     The number of times a word is in a file with a given disposition
#               ...
#          phrases                                 The phrases the word ends
#               phrase length
#                    phrase root                   The previous words in the phrase
#                         total frequency          The number of times a word completes a phrase of a specific length
#                         file frequency           The number of different files a word is present in
#                         dispositions             The outcomes associated with a phrase
#                              disposition         The choice selected by an agent
#                                   frequency      The number of times a phrase is in a file with a given disposition
#                         ...
#                    ...
#          ...
#     ...
#
# phrases
#     lengths                                      The number of words phrases can have
#          phrase length                           The particular number of words phrases in this dictionary have
#               phrases                            The potential phrases, most of which are random word groupings of rare meaning
#                    phrase
#                         frequency                The number of times a phrase is present in a set of files
#                    ...
#               common                             The phrases statistically likely to mean something
#                    phrase
#                         frequency                The number of times a phrase is present in a set of files
#                    ...
#               ...
#               frequencies                        The list of every phrase frequency for phrases of a particular length
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

	total_words = len(data)   # Used for progress bar
	total_done = 0
	last_progress = -1   # Used to keep from reprinting equivalent progress lines
	
	for word in data:

		progress = int(70.0 * total_done / total_words)
		if progress != last_progress:
			print("\rBuilding potential phrases\t|%s%s|" % (progress * '#', (70 - progress) * ' '), end="")   # A simple loading bar
			last_progress = progress
		total_done += 1

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

				phrases['lengths'][phrase_length]['phrases'][phrase] = frequency
				phrases['lengths'][phrase_length]['frequencies'].append(frequency)


	print()
	total_phrases = 0
	for phrase_length in phrases['lengths']:
		total_phrases += len(phrases['lengths'][phrase_length]['phrases'])   # Used for progress bar
	total_done = 0
	last_progress = -1   # Used to keep from reprinting equivalent progress lines
	

	for phrase_length in phrases['lengths']:

		mean = sum(phrases['lengths'][phrase_length]['frequencies']) / len(phrases['lengths'][phrase_length]['frequencies'])
		standard_deviation = stats.pstdev(phrases['lengths'][phrase_length]['frequencies'], mean)

		phrases['lengths'][phrase_length]['common'] = {}   # A phrase list of only the statistically significant
		phrases['lengths'][phrase_length]['common frequencies'] = []

		for phrase in phrases['lengths'][phrase_length]['phrases']:

			progress = int(70.0 * total_done / total_phrases)   # This block is only used for progress bar
			if progress != last_progress:
				print("\rAnalyzing potential phrases\t|%s%s|" % (progress * '#', (70 - progress) * ' '), end="")   # A simple loading bar
				last_progress = progress
			total_done += 1

			frequency = phrases['lengths'][phrase_length]['phrases'][phrase]
			z_score = (frequency - mean) / standard_deviation

			if math.fabs(z_score) < 1.960:
				continue

			phrases['lengths'][phrase_length]['common'][phrase] = frequency   # Getting here means it's statistically significant
	return phrases

def analyze_phrase_disposition_percentage_composition(data):

	phrases = analyze_word_phrase_composition(data)

	analysis = {}
	analysis['lengths'] = {}

	total_done = 0
	last_progress = -1
	print()

	for word in data:

		progress = int(70.0 * total_done / total_words)
		if progress != last_progress:
			print("\rFinding Sample Statistics\t|%s%s|" % (progress * '#', (70 - progress) * ' '), end="")   # A simple loading bar
			last_progress = progress
		total_done += 1


		for phrase_length in data[word]['phrases']:

			#print(phrases['lengths'][phrase_length]['common'])

			if phrase_length not in analysis['lengths']:
				analysis['lengths'][phrase_length] = {}
				analysis['lengths'][phrase_length]['dispositions'] = {}

			for root in data[word]['phrases'][phrase_length]:

				phrase = word
				for part in root.split():
					phrase = "%s %s" % (part, phrase)

				if phrase not in phrases['lengths'][phrase_length]['common']:   # Filter out the uncommon phrases
					continue

				for disposition in data[word]['phrases'][phrase_length][root]['dispositions']:

					percentage = data[word]['phrases'][phrase_length][root]['dispositions'][disposition] / data[word]['phrases'][phrase_length][root]['total frequency']

					if disposition not in analysis['lengths'][phrase_length]['dispositions']:
						analysis['lengths'][phrase_length]['dispositions'][disposition] = {}
						analysis['lengths'][phrase_length]['dispositions'][disposition]['values'] = []
						#print(disposition)
					analysis['lengths'][phrase_length]['dispositions'][disposition]['values'].append(percentage)

	#print(analysis)

	for phrase_length in analysis['lengths']:
		for disposition in analysis['lengths'][phrase_length]['dispositions']:
			mean = sum(analysis['lengths'][phrase_length]['dispositions'][disposition]['values']) / len(analysis['lengths'][phrase_length]['dispositions'][disposition]['values'])
			standard_deviation = stats.pstdev(analysis['lengths'][phrase_length]['dispositions'][disposition]['values'], mean)

			#analysis['lengths'][phrase_length]['dispositions'][disposition]['mean'] = mean
			#analysis['lengths'][phrase_length]['dispositions'][disposition]['standard deviation'] = standard_deviation

			print('%s\n\tmu: %s\n\tst: %s' % (disposition, mean * 100, standard_deviation))

			for word in data:
				for root in data[word]['phrases'][phrase_length]:

					phrase = word
					for part in root.split():
						phrase = "%s %s" % (part, phrase)

					if phrase not in phrases['lengths'][phrase_length]['common']:   # Filter out the uncommon phrases
						continue

					if disposition not in data[word]['phrases'][phrase_length][root]['dispositions']:   # Excise phrases with zero frequency for the given disposition
						continue

					if data[word]['phrases'][phrase_length][root]['dispositions'][disposition]:
						percentage = data[word]['phrases'][phrase_length][root]['dispositions'][disposition] / data[word]['phrases'][phrase_length][root]['total frequency']
						z_score = (percentage - mean) / standard_deviation
						if math.fabs(z_score) > 3.819:
							print('\t%s%s\tp < %s  \t%%: %s\tz: %s' % (phrase, ' ' * (8 * phrase_length - len(phrase)), 0.0001, round(percentage, 3), round(z_score, 3)))
						elif math.fabs(z_score) > 3.291:
							print('\t%s%s\tp < %s   \t%%: %s\tz: %s' % (phrase, ' ' * (8 * phrase_length - len(phrase)), 0.001, round(percentage, 3), round(z_score, 3)))
						elif math.fabs(z_score) > 2.576:
							print('\t%s%s\tp < %s    \t%%: %s\tz: %s' % (phrase, ' ' * (8 * phrase_length - len(phrase)), 0.01, round(percentage, 3), round(z_score, 3)))
						elif math.fabs(z_score) > 1.960:
							print('\t%s%s\tp < %s    \t%%: %s\tz: %s' % (phrase, ' ' * (8 * phrase_length - len(phrase)), 0.05, round(percentage, 3), round(z_score, 3)))

def analyze_phrase_agent_percentage_composition(data):

	phrases = analyze_word_phrase_composition(data)

	analysis = {}
	analysis['lengths'] = {}

	total_done = 0
	last_progress = -1
	print()

	for word in data:

		progress = int(70.0 * total_done / total_words)
		if progress != last_progress:
			print("\rFinding Sample Statistics\t|%s%s|" % (progress * '#', (70 - progress) * ' '), end="")   # A simple loading bar
			last_progress = progress
		total_done += 1


		for phrase_length in data[word]['phrases']:

			if phrase_length not in analysis['lengths']:
				analysis['lengths'][phrase_length] = {}
				analysis['lengths'][phrase_length]['agent'] = {}

			for root in data[word]['phrases'][phrase_length]:

				phrase = word
				for part in root.split():
					phrase = "%s %s" % (part, phrase)

				if phrase not in phrases['lengths'][phrase_length]['common']:   # Filter out the uncommon phrases
					continue

				for agent in data[word]['phrases'][phrase_length][root]['agents']:

					percentage = data[word]['phrases'][phrase_length][root]['agents'][agent] / data[word]['phrases'][phrase_length][root]['total frequency']

					if agent not in analysis['lengths'][phrase_length]['agents']:
						analysis['lengths'][phrase_length]['agents'][agent] = {}
						analysis['lengths'][phrase_length]['agents'][agent]['values'] = []
					analysis['lengths'][phrase_length]['agents'][agent]['values'].append(percentage)

	for phrase_length in analysis['lengths']:
		for agent in analysis['lengths'][phrase_length]['agents']:
			mean = sum(analysis['lengths'][phrase_length]['agents'][agent]['values']) / len(analysis['lengths'][phrase_length]['agents'][agent]['values'])
			standard_deviation = stats.pstdev(analysis['lengths'][phrase_length]['agents'][agent]['values'], mean)

			print('%s\n\tmu: %s\n\tst: %s' % (agent, mean * 100, standard_deviation))

			for word in data:
				for root in data[word]['phrases'][phrase_length]:

					phrase = word
					for part in root.split():
						phrase = "%s %s" % (part, phrase)

					if phrase not in phrases['lengths'][phrase_length]['common']:   # Filter out the uncommon phrases
						continue

					if agent not in data[word]['phrases'][phrase_length][root]['agents']:   # Excise phrases with zero frequency for the given agent
						continue

					if data[word]['phrases'][phrase_length][root]['agents'][agent]:
						percentage = data[word]['phrases'][phrase_length][root]['agents'][agent] / data[word]['phrases'][phrase_length][root]['total frequency']
						z_score = (percentage - mean) / standard_deviation
						if math.fabs(z_score) > 3.819:
							print('\t%s%s\tp < %s  \t%%: %s\tz: %s' % (phrase, ' ' * (8 * phrase_length - len(phrase)), 0.0001, round(percentage, 3), round(z_score, 3)))
						elif math.fabs(z_score) > 3.291:
							print('\t%s%s\tp < %s   \t%%: %s\tz: %s' % (phrase, ' ' * (8 * phrase_length - len(phrase)), 0.001, round(percentage, 3), round(z_score, 3)))
						elif math.fabs(z_score) > 2.576:
							print('\t%s%s\tp < %s    \t%%: %s\tz: %s' % (phrase, ' ' * (8 * phrase_length - len(phrase)), 0.01, round(percentage, 3), round(z_score, 3)))
						elif math.fabs(z_score) > 1.960:
							print('\t%s%s\tp < %s    \t%%: %s\tz: %s' % (phrase, ' ' * (8 * phrase_length - len(phrase)), 0.05, round(percentage, 3), round(z_score, 3)))


#print("Loading words")
words = load_from_file('word-frequencies.txt')
#print("Loading metadata")
meta  = load_from_file('meta.txt')

for argument in sys.argv[1:]:

	if argument.find('p') != -1:
		print("Pruning words")
		pruned = prune_data_by_word_percentage(words, meta, 0.5)
		print("Finding phrases")
		analyze_word_phrase_composition(pruned)

	if argument.find('a') != -1:
		pruned = prune_data_by_word_percentage(words, meta, 0.5)
		analyze_word_agent_percentage_composition(pruned)

	if argument.find('d') != -1:
		pruned = prune_data_by_word_percentage(words, meta, 0.5)
		analyze_word_disposition_percentage_composition(pruned)

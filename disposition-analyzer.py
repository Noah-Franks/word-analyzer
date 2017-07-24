import os
import sys
import pickle
import math
import statistics as stats

# words data structure:
#
# words
#     word
#          total frequency              The number of times a word is present in a set of files
#          file frequency               The number of different files a word is present in
#          agents                       The agents associated with a word
#               agent                   The agent
#                    frequency          The number of times a word is in a file with a given agent
#          dispositions                 The outcomes associated with a word
#               disposition             The choice selected by an agent
#                    frequency          The number of times a word is in a file with a given disposition
#          ...
#     ...

def load_from_file(filepath):   # loads the output of word-analyzer into memory
	return pickle.load(open(filepath, "rb"))



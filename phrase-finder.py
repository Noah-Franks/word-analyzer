import os

data = {}

with open('word-frequencies.txt', 'r') as source:
	

	for line in source:

		if line.find('\t') >= 0:

			disposition =     line[: line.find(' ')      ]
			frequency   = int(line[  line.find(' ') + 1 :])

			print(disposition + str(frequency))

		else:
			word = line[:line.find('\n')]
			print(word)
			data[line] = {}

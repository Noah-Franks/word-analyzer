import os

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

def print_dictionary(dictionary, tabs=0):
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            print("\t" * tabs + str(key))
            print_dictionary(dictionary[key], tabs + 1)
        else:
            print("\t" * tabs       + str(key))
            print("\t" * (tabs + 1) + str(dictionary[key]))

def write_dictionary(dictionary, tabs=0):
    with open('word-frequencies.txt', 'w') as output:
        for key in dictionary:
            if isinstance(dictionary[key], dict):
                output.write(" " * tabs + str(key) + "\n")
                write_dictionary(dictionary[key], tabs + 1)
            else:
                output.write(" " * tabs       + str(key) + "\n")
                output.write(" " * (tabs + 1) + str(dictionary[key]) + "\n")

def words_from_file(filepath):
    words = {}   # All of the unique words. Has the form {word -> [(disposition, frequency),...]}

    disposition = filepath[filepath.find('_as_') + 4 : filepath.find('.txt')]

    with open(filepath, 'r') as file:
        for line in file:
            for word in line.split():

                if word not in words:
                    words[word] = {}
                    words[word]['dispositions']    = {}
                    words[word]['total frequency'] = 0
                    words[word]['file frequency']  = 1

                if disposition not in words[word]['dispositions']:
                    words[word]['dispositions'][disposition] = 0

                words[word]['dispositions'][disposition] += 1
                words[word]['total frequency']           += 1

    return words

def words_from_directory(directorypath):
    allwords = {}

    for root, dirs, files in os.walk(directorypath):
        for filename in files:
            
            filepath = os.path.join(root, filename)
            print(filename)

            filewords = words_from_file(filepath)
            
            for word, meta_dict in filewords.items():

                if word not in allwords:
                    allwords[word]                    = {}
                    allwords[word]['dispositions']    = {}
                    allwords[word]['total frequency'] = 0
                    allwords[word]['file frequency']  = 0

                allwords[word]['file frequency']  += meta_dict['file frequency']    # This should always be 1
                allwords[word]['total frequency'] += meta_dict['total frequency']   # Adding the frequency of the word in the file

                for disposition, frequency in meta_dict['dispositions'].items():

                    if disposition not in allwords[word]['dispositions']:
                        allwords[word]['dispositions'][disposition] = 0
                
                    allwords[word]['dispositions'][disposition] += frequency


    return allwords


#wordFrequencies = words_from_directory('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/')
wordFrequencies = words_from_directory('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/text-analysis-corpus/')
print_dictionary(wordFrequencies)
write_dictionary(wordFrequencies)
'''
with open('word-frequencies.txt', 'w') as output:
    for word, disposition_dict in wordFrequencies.items():
        output.write(word + "\n")
        for disposition, frequency in disposition_dict.items():
            output.write("\t" + disposition + " " + str(frequency) + "\n")'''

import os

def words_from_file(filepath):
    words = {}   # All of the unique words. Has the form {word -> [(disposition, frequency),...]}

    disposition = filepath[filepath.find('_as_') + 4 : filepath.find('.txt')]

    with open(filepath, 'r') as file:
        for line in file:
            for word in line.split():

                if word not in words:
                    words[word] = {}
                if disposition not in words[word]:
                    words[word][disposition] = 0

                words[word][disposition] += 1
                

    return words

def words_from_directory(directorypath):
    allwords = {}

    for root, dirs, files in os.walk(directorypath):
        for filename in files:
            
            filepath = os.path.join(root, filename)
            print(filename)

            filewords = words_from_file(filepath)
            
            for word, disposition_dict in filewords.items():

                if word not in allwords:
                    allwords[word] = {}
                    allwords[word]['total'] = 0

                for disposition, frequency in disposition_dict.items():

                    if disposition not in allwords[word]:
                        allwords[word][disposition] = 0
                
                    allwords[word][disposition] += 1
                    allwords[word]['total']     += 1


    return allwords


#wordFrequencies = words_from_directory('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/')
wordFrequencies = words_from_directory('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/text-analysis-corpus/')
print(wordFrequencies)

with open('word-frequencies.txt', 'w') as output:
    for word, disposition_dict in wordFrequencies.items():
        output.write(word + "\n")
        for disposition, frequency in disposition_dict.items():
            output.write("\t" + disposition + " " + str(frequency) + "\n")

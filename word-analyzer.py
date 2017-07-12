import os

def words_from_file(filepath):
    words = {}

    with open(filepath, 'r') as file:
        for line in file:
            for word in line.split():
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

    return words

def words_from_directory(directorypath):
    allwords = {}

    for root, dirs, files in os.walk(directorypath):
        for filename in files:
            
            filepath = os.path.join(root, filename)
            print(filepath)

            filewords = words_from_file(filepath)
            
            for key, value in filewords.items():
                if key in allwords:
                    allwords[key] += value
                else:
                    allwords[key] = value

    return allwords


wordFrequencies = words_from_directory('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/')
print(wordFrequencies)

with open('word-frequencies-dictionary.txt', 'w') as output:
    for word, frequency in wordFrequencies.items():
        output.write(word + " " + str(frequency) + "\n")
import os

def words_from_file(filepath, unique):
    words = []

    with open(filepath, 'r') as file:
        for line in file:
            if unique:
                words = list(set(words + line.split()))   # Add only the unique words from each line
            else:
                words = words + line.split()

    return words

def words_from_directory(directorypath, unique):
    allwords = []

    for root, dirs, files in os.walk(directorypath):
        for filename in files:
            
            filepath = os.path.join(root, filename)
            print(filepath)

            filewords = words_from_file(filepath, unique)
            if unique:
                allwords = list(set(allwords + filewords))   # Add only the unique words from each file
            else:
                allwords = allwords + filewords

    return allwords


# A list of every unique word from the directory tree
distinctWords = words_from_directory(
    '../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/', True)

# A list of every word from the directory tree
totalityWords = words_from_directory(
    '../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/', False)


wordFrequencies = []
maxWordLength = len(distinctWords[0])   # The length of the longest word
wordsCounted = 0

for unique in distinctWords:

    frequency = 0
    for word in totalityWords:
        if word == unique:
            frequency += 1

    totalityWords = [w for w in totalityWords if w != unique]
    wordFrequencies.append((unique, frequency))   # The word associated with the number of times it was found

    if len(unique) > maxWordLength:
        maxWordLength = len(unique)
    wordsCounted += 1
    print(unique + (" " * (maxWordLength - len(unique) + 3)) + str(frequency) + (" " * (10 - len(str(frequency)))) + str(wordsCounted) + "/" + str(len(distinctWords)))

with open('word-frequencies.txt', 'w') as output:
    for word, frequency in wordFrequencies:
        output.write(word + (" " * (maxWordLength - len(word) + 1)) + str(frequency) + "\n")
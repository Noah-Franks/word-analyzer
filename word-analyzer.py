import os

def words_from_file(filepath):
    words = []

    with open(filepath, 'r') as file:
        for line in file:
            if unique:
                words = list(set(words + line.split()))   # Add only the unique words from each line
            else:
                words = words + line.split()

    return words

def words_from_directory(directorypath):
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


wordFrequencies = words_from_file('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/', True)

with open('word-frequencies.txt', 'w') as output:
    for word, frequency in wordFrequencies:
        output.write(word + " " + str(frequency) + "\n")
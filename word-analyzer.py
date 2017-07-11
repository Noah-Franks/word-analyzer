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

for unique in distinctWords:
    frequency = 0
    for word in totalityWords:
        if word == unique:
            frequency += 1
    print unique + "\t" + str(frequency)
import os

def words_from_file(filepath):
    words = []

    with open(filepath, 'r') as file:
        for line in file:
            words = list(set(words + line.split()))   # Add only the unique words from each line

    return words

def words_from_directory(directorypath, verbose=False):
    allwords = []

    for root, dirs, files in os.walk(directorypath):
        for filename in files:
            
            filepath = os.path.join(root, filename)

            if verbose:
                print(filepath)

            allwords = list(set(allwords + words_from_file(filepath)))   # Add only the unique words from each file

    return allwords

#print words_from_file('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/p9000/p9000_000.txt')
print words_from_directory('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/', True)

exit(1)

file = open('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/p9000/p9000_000.txt', 'r')
book = file.read()




def tokenize():
    if book is not None:
        words = book.lower().split()
        return words
    else:
        return None
        

def map_book(tokens):
    hash_map = {}

    if tokens is not None:
        for element in tokens:
            # Remove Punctuation
            word = element.replace(",","")
            word = word.replace(".","")

            # Word Exist?
            if word in hash_map:
                hash_map[word] = hash_map[word] + 1
            else:
                hash_map[word] = 1

        return hash_map
    else:
        return None


# Tokenize the Book
words = tokenize()
word_list = ['the','life','situations','since','day']

# Create a Hash Map (Dictionary)
map = map_book(words)

# Show Word Information
for word in word_list:
    print('Word: [' + word + '] Frequency: ' + str(map[word]))
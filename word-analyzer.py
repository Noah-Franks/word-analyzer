
def words_from_file(filepath):

    words = []

    with open(filepath, 'r') as file:
        for line in file:
            for word in line.split():
                words.append(word)

    return list(set(words))

print words_from_file('../../Desktop/YouTube/Source/120mins/uploaded/downloaded/VCTK-8000-Fake/newText/p9000/p9000_000.txt')

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
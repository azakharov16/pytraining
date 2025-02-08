import sys
import os
import json
from collections import Counter
from itertools import repeat
from string import punctuation, digits, ascii_lowercase
from math import floor

script, path, m = sys.argv

try:
    m = int(m)
except ValueError:
    print("You have supplied a wrong argument type. The parameter m will be set to its default value.")
    m = 20

os.chdir(path)


def process_textfile():
    while True:
        filename = input("Enter file name >: ")
        if os.path.exists(filename + '.txt'):
            break
        else:
            print("The file does not exist. Please try again.")

    f = open(filename + '.txt', 'r')
    content = f.read()
    f.close()
    words = []
    nuisance = punctuation + digits
    vowels = 'aeiouy'
    consonants = ''.join(filter(lambda char: char not in vowels, ascii_lowercase))
    vcount = ccount = 0
    letter_count = Counter(dict(zip(ascii_lowercase, repeat(0, len(ascii_lowercase)))))
    begin_count = Counter(dict(zip(ascii_lowercase, repeat(0, len(ascii_lowercase)))))

    for word in content.split(' '):
        word = ''.join(filter(lambda char: char not in nuisance, word.strip()))
        word = word.lower()
        if word:
            vcount += sum(map(lambda char: char in vowels, word))
            ccount += sum(map(lambda char: char in consonants, word))
            letter_count.update(Counter(word))
            begin_count.update(Counter({word[0]: 1}))
            words.append(word)
    words_count = Counter(words)
    with open('word_counts_' + filename + '.json', 'w') as jfile:
        json.dump(dict(words_count), jfile)
        jfile.close()
    with open('letter_counts_' + filename + '.json', 'w') as jfile:
        json.dump(dict(letter_count), jfile)
        jfile.close()
    with open('begin_letter_counts_' + filename + '.json', 'w') as jfile:
        json.dump(dict(begin_count.most_common()), jfile)
        jfile.close()
    print("Letter and word counts have been successfully saved.")
    text_size = len(words)
    print("The text has {} words, {} vowels and {} consonants.".format(text_size, vcount, ccount))
    f = open('emotional_words.txt', 'r')
    emo_words = f.read().split(' ')
    f.close()
    emotionality = sum(map(lambda w: w in emo_words, words)) / text_size
    print("The given text has emotionality score of {}".format(emotionality))
    parasites = filter(lambda w: len(w) >= 2 and words_count[w] > floor(5 * (text_size / m)), words)
    if parasites:
        parasites = list(set(parasites))
        print("The following parasite words were identified: {}".format(*parasites))
    else:
        print("No parasite words found.")


while True:
    process_textfile()
    print("Would you like to analyze another file? (Y/N)")
    response = input(">: ")
    if response == 'Y':
        continue
    elif response == 'N':
        sys.exit(0)
    else:
        print("Wrong input. Program terminated with errors.")
        sys.exit(1)

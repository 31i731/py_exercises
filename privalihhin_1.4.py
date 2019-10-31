# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 20:46:14 2019

@author: Vassili Privalihhin
"""
from os import path
from string import digits
from collections import Counter

def wordCounter(fileName, length, n):
    currentScriptDir = path.dirname(path.abspath(__file__))
    try:
        f = open(currentScriptDir + "\\" + fileName, "r")
    except FileNotFoundError:
        print("Sorry could not find", fileName)
        return

    if f.mode == 'r':
        contents = f.read()
        charactersToRemove = r"!\"#$%&()*+,.-/:;<=>?@[\]^_`{|}~"
        
        # replaces each character above of our text with space (generally removes all these characters from our text)
        contents = contents.translate(str.maketrans(charactersToRemove, ' ' * len(charactersToRemove)))
        
        # every digit in our text becomes none (removes all digits from our text)
        contents = contents.translate(str.maketrans('', '', digits))
        
        # removes '\n' and '\r'. these characters occur due to enters in our text
        contents = contents.replace('\n', ' ').replace('\r', '')
        
        # makes a list with words of given length, which were separated by space
        words = [word for word in contents.split() 
        if len(word) == length]
        
        if len(words) == 0:
            print("No words with {} characters were found".format(length))
            return
                
        # generally, this part of code below finds needed words in words
        # transforms the list to set, so now there are unique words only
        uniqueWords = set(words)
        for word in contents.split():
            for uniqueWord in uniqueWords:
                # checks if there's needed word/s in a word and it's really a part of the word
                if word.count(uniqueWord) > 0 and not len(uniqueWord) == len(word):
                    # then adds this needed word/words to our list of words
                    occurance = 0
                    while occurance < word.count(uniqueWord):
                        words.append(uniqueWord)
                        occurance += 1
                               
        counter = Counter(words) # counts all the same words in the list
        
        # prints 'n' common word
        for most_common_word in counter.most_common(n):
            print('"{}"'.format(most_common_word[0]), ":", most_common_word[1])
        
wordCounter("test1.txt", 2, 4)
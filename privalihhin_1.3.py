# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:10:13 2019

@author: Vassili Privalihhin
"""

grid = [
        
        ["C", "D", "N", "L", "O", "V", "E", "D", "M", "H", "C", "L", "O", "U", "D"],
        ["O", "R", "I", "I", "M", "C", "H", "E", "A", "N", "Y", "T", "D", "D", "S"],
        ["O", "A", "A", "R", "H", "D", "R", "E", "T", "M", "B", "H", "T", "C", "B"],
        ["L", "M", "H", "A", "D", "O", "O", "P", "H", "L", "E", "A", "T", "A", "I"],
        ["M", "A", "C", "H", "I", "N", "E", "L", "E", "A", "R", "N", "I", "N", "G"],
        ["A", "D", "K", "I", "N", "G", "S", "E", "M", "H", "S", "F", "S", "F", "D"],
        ["T", "S", "C", "B", "Y", "T", "E", "A", "A", "A", "E", "H", "T", "A", "A"],
        ["P", "D", "O", "L", "Y", "F", "T", "R", "T", "P", "C", "K", "A", "C", "T"],
        ["L", "Z", "L", "J", "F", "R", "K", "N", "I", "P", "U", "R", "T", "E", "A"],
        ["O", "T", "B", "H", "A", "R", "O", "I", "C", "Y", "R", "E", "I", "B", "W"],
        ["T", "S", "J", "H", "O", "H", "F", "N", "S", "S", "I", "M", "S", "O", "G"],
        ["L", "O", "Z", "W", "T", "S", "H", "G", "H", "G", "T", "S", "T", "O", "Q"],
        ["I", "Q", "T", "Y", "D", "G", "A", "N", "A", "L", "Y", "T", "I", "C", "S"],
        ["B", "E", "P", "A", "N", "D", "A", "S", "K", "K", "T", "L", "C", "Z", "D"],
        ["N", "Z", "R", "B", "L", "O", "C", "K", "C", "H", "A", "I", "S", "M", "F"]

        ]

def findWord(word):
    
    # searches in → direction
    for charList in grid:
        string = ''.join(charList)
        if word in string:
            index = string.find(word)
            return [(index, grid.index(charList)), "→"]
    
    
    # searches in ↓ and ↑ direction
    for col in range(0, len(grid[0])):
        
        string = ''
        for charList in grid:
            string += charList[col]
        
        if word in string:
            return [(col, string.index(word)), "↓"]
        elif word in string[::-1]:
            return [(col, len(grid) - 1 - string[::-1].index(word)), "↑"]

    
    # searches in ↘ (left half) 
    for y in range(0, len(grid)):
        string = ''
        z = 0
        for row in range(y, len(grid)):
            string += grid[row][z]
            if word in string:
                return [(string.find(word), y + string.find(word)), "↘"]
            z += 1
    
    # searches in ↘ (right half)
    for x in range(1, len(grid[0])):
        string = ''
        z = 0
        for row in range(x, len(grid[0])):
            string += grid[z][row]
            if word in string:
                return [(x + string.find(word), string.find(word)), "↘"]
            z += 1
        
    # searches in ↗ (first half)
    for y in range(len(grid) - 1, -1, -1):
        string = ''
        z = 0
        for row in range(y, -1, -1):
            string += grid[row][z]
            if word in string:
                return [(string.find(word), y - string.find(word)), "↗"]
            z += 1

    # searches in ↗ (second half)
    for x in range(1, len(grid[0])):
        string = ''
        z = len(grid) - 1
        for row in range(x, len(grid[0])):
            string += grid[z][row]
            if word in string:
                return [(x + string.find(word), len(grid) - 1 - string.find(word)), "↗"]
            z -= 1
        
    return None

word = input("Enter word to find: ")
result = findWord(word)
if (result is None):
    print("Oops, I could not find {} in the grid.".format(word))
else:
    print("{} found in location {} in {} direction".format(word, result[0], result[1]))
    
    
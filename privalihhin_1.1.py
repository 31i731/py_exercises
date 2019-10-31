# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 15:24:20 2019

@author: Vassili
"""

def isPalindromic(n):
    return n == int(str(n)[::-1]) # checks if a number is the same after the reverse

number = input("Enter a number: ")

if not number.isnumeric() or int(number) <= 1: # if the input is not a number or less than 2 - fail
    print("Only integer numbers greater than 1 are allowed!")
else:
    number = int(number)
    x = range(1, number) # creates a range of numbers
    counter = 0
    for n in x:
        if isPalindromic(n):
            counter += 1

    print("There are", counter, "Palindromic numbers")
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:30:23 2019

@author: Vassili Privalihhin
"""
from re import compile

initial_balance = "322.43" # if initially there's no balance at all in a file
balance = 0
transactions = []
commands = {
        "transaction": r'^-t +[+-]?((\d+)|(\d+\.\d\d?)) +".+"$', 
        "display": r'^-d +\d+$', 
        "quit": r'^-q$'
        }

def initialize():
    global balance, transactions
            
    balanceFile = open("balance.txt", "a+")
    balanceFile.seek(0) # go to the beginning
    balance = balanceFile.readline()
    if len(balance) == 0:
        balanceFile.write(initial_balance)
        balance = initial_balance
    
    balanceFile.close()

    try:
        balance = float(balance)
    except ValueError:
        print("Balance has an inappropriate value")
        return
        
    transactionsFile = open('transactions.txt', 'a+')
    transactionsFile.seek(0) # go to the beginning
    transactions = [transaction.strip() for transaction in transactionsFile.readlines()] # read all transactions of the log file, clean them a bit and put them in a list
    transactionsFile.close()
                                            
    print("Welcome !\nCurrently, your balance is {} Euros.\nThere are {} transactions in your log file.".format(balance, len(transactions)))
        
    start_transactions()

def start_transactions():
    rawCommand = input("✎\t")
    recognised = False
    global balance
    for k,v in commands.items(): # looping through all dictionary's items, knowing their keys and values
        regex = compile(v) # get regular expression
        if not regex.match(rawCommand) is None:
            recognised = True
            if k == "quit":
                print("Bye!")
                return
            elif k == "transaction":
                # get transaction as a list of amount and note
                transaction = [action for action in rawCommand.split(maxsplit=2) if not action == "-t"]
                
                money = float(transaction[0])
                
                # check if the expenses lead us to a negative balance, if that's so - gets out of this part of code and calls this function again  
                if money < 0:
                    if money * -1 > balance:
                        print("sorry, can’t spend more than you have!")
                        break
                
                balance += money
                balance = round(balance, 2)
                print("OK, your balance is now {} Euros".format(balance))
                
                balanceFile = open('balance.txt', 'w')
                balanceFile.write(str(balance))
                balanceFile.close()
                       
                transactionsFile = open('transactions.txt', 'a')
                transactionsFile.write(" ".join(transaction))
                transactionsFile.write("\n")
                transactionsFile.close()
                transactions.append(" ".join(transaction))
            else:
                numberOfTransactions = int(rawCommand.split()[1]) # gets a number in the called command, which means a number of the last transactions
                # gets a list of transactions from the end until 'numberOfTransactions'*-1
                lastTransactions = transactions[:numberOfTransactions*-1-1:-1]
                if len(lastTransactions) == 0:
                    print("There are no transactions in the log file.")
                    break
                for lastTransaction in lastTransactions:
                    print(lastTransaction)

    if not recognised: 
        print("Computer didn't understand this command. Try again.")
        
    start_transactions()

initialize()

from flask import session
from .models import Word
from . import db
from sqlalchemy.sql import func
import random
from random import choice
from datetime import datetime, timedelta

#Generates the inital random word in session, it is ran when the practice page is loaded
def firstRandomWord():
    getNextWord()

    if "random_number" not in session:
        randomNumber()

#Generate 1 or 0 for Mix page to know which leangue to display
def randomNumber():
    random_number = random.randint(0, 1)
    session["random_number"] = random_number

def getNextWord():
    if "recent_word_list" not in session: #New session for recent words
        session["recent_word_list"] = []

    recent_word_list = session["recent_word_list"]

    #Make sure there are words in the database to choose from
    if Word.query.count() == 0:
        session["random_german_word"] = "No words added in last week"
        session["random_english_word"] = "No words added in last week"
        raise Exception("No words available in the database.")

    #Run a loop to get a word
    while True:
        get_random_word = Word.query.order_by(func.random()).first()
        random_english_word = get_random_word.englishWord
            
        if Word.query.count() > 5: #If there are more than 5 words in the database
            if random_english_word not in recent_word_list:
                session["random_german_word"] = get_random_word.germanWord
                session["random_english_word"] = random_english_word
                print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])

                print("0-0-0-0-0-0-0-0-0-0-0-0-0-0-0")
                for word in recent_word_list:
                    print(word)
                print("0-0-0-0-0-0-0-0-0-0-0-0-0-0-0")

                # Update the recent words list
                if len(recent_word_list) >= 5:  #If the list has 5 or more items, remove the first item (oldest)
                    recent_word_list.pop(0)

                recent_word_list.append(random_english_word)
                session["recent_word_list"] = recent_word_list  # Update the session list
                break
        else: #Handle cases where there are 5 or fewer words in the database
            session["random_german_word"] = get_random_word.germanWord
            session["random_english_word"] = random_english_word         
            break

def getNewWord():
    if "recent_word_list" not in session: #New session for recent words
        session["recent_word_list"] = []

    recent_word_list = session["recent_word_list"]
    last_week = datetime.now() - timedelta(days=7)

    #Make sure there are words in the database to choose from
    if Word.query.filter(Word.dateAdded >= last_week).count() == 0:
        session["random_german_word"] = "No words added in last week"
        session["random_english_word"] = "No words added in last week"
        raise Exception("No words available in the database from last week.")

    #Run a loop to get a word
    while True:

        get_random_new_word = Word.query.filter(Word.dateAdded >= last_week).order_by(func.random()).first()
        random_english_word = get_random_new_word.englishWord
            
        if Word.query.filter(Word.dateAdded >= last_week).count() > 5: #If there are more than 5 words in the database
            if random_english_word not in recent_word_list:
                session["random_german_word"] = get_random_new_word.germanWord
                session["random_english_word"] = random_english_word
                print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])

                print("0-0-0-0-0-0-0-0-0-0-0-0-0-0-0")
                for word in recent_word_list:
                    print(word)
                print("0-0-0-0-0-0-0-0-0-0-0-0-0-0-0")

                # Update the recent words list
                if len(recent_word_list) >= 5:  #If the list has 5 or more items, remove the first item (oldest)
                    recent_word_list.pop(0)

                recent_word_list.append(random_english_word)
                session["recent_word_list"] = recent_word_list  # Update the session list
                break
        else: #Handle cases where there are 5 or fewer words in the database
            session["random_german_word"] = get_random_new_word.germanWord
            session["random_english_word"] = random_english_word         
            break


#Check if the user's guess is correct
def check_answer(guess, correct_answers):
    if isinstance(correct_answers, list):
        return guess in correct_answers[:2] if len(correct_answers) > 1 else correct_answers[0] == guess
    return guess == correct_answers
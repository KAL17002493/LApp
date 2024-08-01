from flask import session
from .models import Word
from . import db
from sqlalchemy.sql import func
import random
from random import choice
from datetime import datetime, timedelta

#Generates the inital random word in session, it is ran when the practice page is loaded
def firstRandomWord():
    if "random_german_word" not in session: 
        get_random_word = Word.query.order_by(func.random()).first()
        session["random_german_word"] = get_random_word.germanWord
        session["random_english_word"] = get_random_word.englishWord
        print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])

        randomNumber()
    else:
        subsequentRandomWord()

    print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])

#Generate 1 or 0 for Mix page to know which leangue to display
def randomNumber():
    random_number = random.randint(0, 1)
    session["random_number"] = random_number

#Random new word (From last week for now)
def randomNewWord():
    last_week = datetime.now() - timedelta(days=7) #All items from last week
    ran_new_word = Word.query.filter(Word.dateAdded >= last_week).order_by(func.random()).first()

    if ran_new_word is None:
        session["random_english_word"], session["random_german_word"] = "No new words added in last week"
        print("No new words added in last week")
    else:
        session["random_english_word"] = ran_new_word.englishWord
        session["random_german_word"] = ran_new_word.germanWord

    print("Random new word: " + ran_new_word.englishWord + " Date added: " + str(ran_new_word.dateAdded))

    #get_random_word = Word.query.order_by(func.random()).first()
    #session["random_german_word"] = get_random_word.germanWord
    #session["random_english_word"] = get_random_word.englishWord
    #print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])

#Generates a subsequent random word in session, it is ran when the user submits a guess
def subsequentRandomWord():
    get_random_word = Word.query.order_by(func.random()).first()
    session["random_german_word"] = get_random_word.germanWord
    session["random_english_word"] = get_random_word.englishWord
    print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])

#Makes sure that the same word will not appear for a list the next 5 words
def recentWordsGuessed(word):
    if "recent_word_list" not in session:  # Create new session if one does not exist yet
        session["recent_word_list"] = []

    recent_word_list = session["recent_word_list"]

    if Word.query.count() > 5: # If the database has more than 5 words run the check (without this if database has less than 5 words check will be stuck in an infinite loop)
        if word in recent_word_list:
            return False  # Indicate a duplicate word
        else:
            if len(recent_word_list) >= 5:  # If the list has 5 or more elements, remove the first element
                recent_word_list.pop(0)

            recent_word_list.append(word)
            session["recent_word_list"] = recent_word_list  # Update the session list

    print("0-0-0-0-0-0-0-0-0-0")
    for i in recent_word_list:
        print(i)
    print("0-0-0-0-0-0-0-0-0-0")

    return True  # Indicate no duplicate word

def check_answer(guess, correct_answers):
    if isinstance(correct_answers, list):
        return guess in correct_answers[:2] if len(correct_answers) > 1 else correct_answers[0] == guess
    return guess == correct_answers
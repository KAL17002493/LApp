from flask import session
from .models import Word
from . import db
from sqlalchemy.sql import func

#Generates the inital random word in session, it is ran when the practice page is loaded
def firstRandomWord():
    if "random_german_word" not in session: 
        get_random_word = Word.query.order_by(func.random()).first()
        session["random_german_word"] = get_random_word.germanWord
        session["random_english_word"] = get_random_word.englishWord
        print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])
    else:
        subsequentRandomWord()

    print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])

#Generates a subsequent random word in session, it is ran when the user submits a guess
def subsequentRandomWord():
    get_random_word = Word.query.order_by(func.random()).first()
    session["random_german_word"] = get_random_word.germanWord
    session["random_english_word"] = get_random_word.englishWord
    print("English: " + session["random_english_word"] + "\nGerman: " + session["random_german_word"])

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
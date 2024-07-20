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
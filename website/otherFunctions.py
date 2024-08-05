from flask import session
from .models import Word, UserWordPerformance
from . import db
from sqlalchemy.sql import func
import random
from datetime import datetime, timedelta

#Generates the inital random word in session, it is ran when the practice page is loaded
def first_random_word():
    get_next_word()

    if "random_number" not in session:
        random_number_get()

#Generate 1 or 0 for Mix page to know which leangue to display
def random_number_get():
    random_number = random.randint(0, 1)
    session["random_number"] = random_number

def get_random_word_from_db(word_query, count_threshold=5):
    if "recent_word_list" not in session:
        session["recent_word_list"] = []

    recent_word_list = session["recent_word_list"]

    # Make sure there are words in the database to choose from
    if word_query.count() == 0:
        session["random_german_word"] = "No words available"
        session["random_english_word"] = "No words available"
        print ("No words available in the database.")
        return

    # Run a loop to get a word
    while True:
        get_random_word = word_query.order_by(func.random()).first() #Picks a random word from the quaery send from helper functions
        random_english_word = get_random_word.english_word

        if word_query.count() > count_threshold:  #If there are more than threshold words in the database
            if random_english_word not in recent_word_list:
                session["random_german_word"] = get_random_word.german_word
                session["random_english_word"] = random_english_word

                # Update the recent words list
                if len(recent_word_list) >= count_threshold:
                    recent_word_list.pop(0)

                recent_word_list.append(random_english_word)
                session["recent_word_list"] = recent_word_list
                break
        else:  #Handle cases where there are threshold or fewer words in the database
            session["random_german_word"] = get_random_word.german_word
            session["random_english_word"] = random_english_word
            break

def get_next_word():
    get_random_word_from_db(Word.query, count_threshold=5)

def get_new_word():
    last_week = datetime.now() - timedelta(days=7)
    new_words_query = Word.query.filter(Word.date_added >= last_week)
    get_random_word_from_db(new_words_query, count_threshold=5)

#Check if the user's guess is correct, calls wrong_answer() if the guess is wrong
def check_answer(guess, correct_answers):
    if isinstance(correct_answers, list):
        if guess in correct_answers[:2]:
            wrong_answer(False)
            return True
    elif guess == correct_answers:
        wrong_answer(False)
        return True
    
    wrong_answer(True)
    return False

#Called when user makes wrong guess in check_answer()
#If the user guessed wrong, add 1 to the fail_count, if the user guessed right, subtract 1 from the fail_count
def wrong_answer(is_incorrect):
    word = Word.query.filter_by(english_word=session["random_english_word"]).first() #Finds right word from Word table in database
    user_word_performance = UserWordPerformance.query.filter_by(word_id=word.id).first() #Finds the right word from UserWordPerformance table in database

    if not user_word_performance: #If the word is not in the UserWordPerformance table, add it
        user_word_performance = UserWordPerformance(word_id=word.id, fail_count=0)

    if is_incorrect == True: #If the user guessed wrong, add 1 to the fail_count
        if user_word_performance.fail_count >= 10: #If the fail_count is 10 or more, end the function (So you could not get really bad at a single word)
            return
        else:
            user_word_performance.fail_count += 1
    else: #If the user guessed right, subtract 1 from the fail_count IF the fail_count is not 0
        if user_word_performance.fail_count != 0:
            user_word_performance.fail_count -= 1
        else:
            return

    db.session.add(user_word_performance)
    db.session.commit()
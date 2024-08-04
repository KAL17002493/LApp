from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from .models import Word, UserWordPerformance
from . import db
import json
from sqlalchemy import desc #Importing desc to order the words from newest to oldest
from .otherFunctions import *

views = Blueprint("views", __name__)

#Home page
@views.route("/", methods=["GET", "POST"]) 
def index():
    if request.method == "POST":
        englishWord = request.form.get("englishWord").strip()
        germanWord = request.form.get("germanWord").strip()

        #Check if the word is already in the database and flash an error message if instance of word is found
        if Word.query.filter_by(english_word=englishWord).first():
            flash(f"{englishWord}, already in database", category="error")
        if Word.query.filter_by(german_word=germanWord).first():
            flash(f"{germanWord}, already in database", category="error")
                

        #Check if the word fields are empty
        if not englishWord or not germanWord:
            if not englishWord:
                flash("English word field is empty", category="error")
            if not germanWord:
                flash("German word field is empty", category="error")
        else:
            new_word = Word(english_word=englishWord, german_word=germanWord)
            db.session.add(new_word)
            db.session.commit()
            return redirect(url_for("views.index"))

    #Render the index page with the words in the database, from newest to oldest and total word count
    return render_template("index.html", words = Word.query.order_by(desc(Word.id)).all(), wordCount=Word.query.count())

#Practice page
@views.route("/practice")
def practice():
    firstRandomWord() #Genreates initial random word and stores it in session storage
    return render_template("practice.html")

#Practice english to german page
@views.route("/practice/english", methods=["GET", "POST"])
def english():
    if request.method == "POST":
        guess = request.form.get("guess").strip()
        german_word = session.get("random_german_word")

        if check_answer(guess, german_word):
            flash("Correct!!!", category="success")
        else:
            flash(f"My guess: {guess} || Correct answer: {german_word}", category="wrong")

    getNextWord()

    return render_template("english.html", english_word=session["random_english_word"])

#Practice german to english page
@views.route("/practice/german", methods=["GET", "POST"])
def german():
    if request.method == "POST":
        guess = request.form.get("guess").strip()
        english_word = session.get("random_english_word")
        check_portion = [part.strip() for part in english_word.split("(")[0].split("/")]  # Handle multiple correct answers
        correct = check_answer(guess, check_portion)

        if correct:
            flash(f"{guess} is correct!!!", category="success")
        else:
            flash(f"My guess: {guess} || Correct answer: {english_word}", category="wrong")

        getNextWord()

    return render_template("german.html", german_word=session["random_german_word"])

#Practice mix of german and english
@views.route("/practice/mix", methods=["GET", "POST"])
def mix():
    random_number = session.get("random_number") #This must be here so for the first round of guesses the code would know what random_number is

    if request.method == "POST":
        guess = request.form.get("guess").strip()

        if random_number == 0:  # Display in German, guess in English
            english_word = session.get("random_english_word")
            check_portion = [part.strip() for part in english_word.split("(")[0].split("/")]  # Handle multiple correct answers
            correct = check_answer(guess, check_portion)

            if correct:
                flash(f"{guess} is correct!!!", category="success")
            else:
                flash(f"My guess: {guess} || Correct answer: {english_word}", category="wrong")
        else:  # Display in English, guess in German
            german_word = session.get("random_german_word")

            if check_answer(guess, german_word):
                flash("Correct!!!", category="success")
            else:
                flash(f"My guess: {guess} || Correct answer: {german_word}", category="wrong")

        #Roll the random number again after processing the guess
        randomNumber()
        random_number = session.get("random_number") #This MUST be here, it handes all of the following random_number checks / guesses (I am tired whiles writing this I could be more specific but cannot be botehred)

    getNextWord()

    # Send the correct word to the view
    word_to_display = session.get("random_german_word") if random_number == 0 else session.get("random_english_word")

    return render_template("mix.html", word_to_display=word_to_display)

#Practice new words
@views.route("/practice/new", methods=["GET", "POST"])
def new():
    random_number = session.get("random_number") #This must be here so for the first round of guesses the code would know what random_number is

    if request.method == "POST":
        guess = request.form.get("guess").strip()

        if random_number == 0:  # Display in German, guess in English
            english_word = session.get("random_english_word")
            check_portion = [part.strip() for part in english_word.split("(")[0].split("/")]  # Handle multiple correct answers
            correct = check_answer(guess, check_portion)

            if correct:
                flash(f"{guess} is correct!!!", category="success")
            else:
                flash(f"My guess: {guess} || Correct answer: {english_word}", category="wrong")
        else:  # Display in English, guess in German
            german_word = session.get("random_german_word")

            if check_answer(guess, german_word):
                flash("Correct!!!", category="success")
            else:
                flash(f"My guess: {guess} || Correct answer: {german_word}", category="wrong")

        #Roll the random number again after processing the guess
        randomNumber()
        random_number = session.get("random_number") #This MUST be here, it handes all of the following random_number checks / guesses (I am tired whiles writing this I could be more specific but cannot be botehred)

    getNewWord()

    # Send the correct word to the view
    word_to_display = session.get("random_german_word") if random_number == 0 else session.get("random_english_word")

    return render_template("new.html", word_to_display=word_to_display)

#Practice terrible at
@views.route("/practice/terrible", methods=["GET", "POST"])
def terrible():

    session.clear() #Clear the session storage
    print("Session cleared")

    return render_template("terrible.html")

#Practice terrible at
@views.route("/session-variables", methods=["GET", "POST"])
def sessionVariables():

    print("======== Session variables =========")
    print(session.keys())
    print("====================================")

    return render_template("info.html")

#Info page
@views.route("/info")
def info():

    return render_template("info.html")

#Delete word route
@views.route("/delete-word", methods=["POST"])
def delete_word():
    word = json.loads(request.data)
    wordId = word["wordId"]
    word = Word.query.get(wordId)

    if word:
        db.session.delete(word)
        db.session.commit()

    return jsonify({})

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from .models import Word
from . import db
import json
from sqlalchemy.sql import func
from .otherFunctions import *

views = Blueprint("views", __name__)

#Home page
@views.route("/", methods=["GET", "POST"]) 
def index():
    if request.method == "POST":
        englishWord = request.form.get("englishWord")
        germanWord = request.form.get("germanWord")

        #Check if the word is already in the database
        if Word.query.filter_by(englishWord=englishWord).first():
            flash(f"{englishWord}, already in database", category="error")
        if Word.query.filter_by(germanWord=germanWord).first():
            flash(f"{germanWord}, already in database", category="error")
                

        #Check if the word fields are empty
        if not englishWord or not germanWord:
            if not englishWord:
                flash("English word field is empty", category="error")
            if not germanWord:
                flash("German word field is empty", category="error")
        else:
            new_word = Word(englishWord=englishWord, germanWord=germanWord)
            db.session.add(new_word)
            db.session.commit()
            return redirect(url_for("views.index"))

    return render_template("index.html", words=Word.query.all(), wordCount=Word.query.count())

#Practice page
@views.route("/practice")
def practice():
    firstRandomWord()
    return render_template("practice.html")

#Practice english to german page
@views.route("/practice/english", methods=["GET", "POST"])
def english():
    if request.method == "POST":
        guess = request.form.get("guess")
        german_word = session["random_german_word"]

        if german_word == guess:
            flash(f"Correct!!!", category="success")
        else:
            flash(f"My guess: {guess} || Correct answer: {german_word}", category="wrong")

        subsequentRandomWord()
    return render_template("english.html", english_word=session["random_english_word"])

#Practice german to english page
@views.route("/practice/german", methods=["GET", "POST"])
def german():
        
    if request.method == "POST":
        guess = request.form.get("guess")
        english_word = session["random_english_word"]

        check_portion = english_word.split("(")[0] #Check if the word has a bracket and remove it from the guess portion / check portion
        check_portion = [part.strip() for part in check_portion.split("/")] #Check if the word has a slash turn words on either side into a list item

        correct = False

        if len(check_portion) > 1:  # If check_portion has more than one item run this block
            correct = guess in check_portion[:2]
        else:  # If check_portion has only one item run this block
            correct = check_portion[0] == guess

        if correct:
            flash(f"{guess} is correct!!!" if len(check_portion) > 1 else "Correct!!!", category="success")
        else:
            flash(f"My guess: {guess} || Correct answer: {english_word}", category="wrong")

        subsequentRandomWord()

    return render_template("german.html", german_word=session["random_german_word"])

#Practice mix of german and english
@views.route("/practice/mix")
def mix():
    return render_template("mix.html")

#Practice new words
@views.route("/practice/new")
def new():
    return render_template("new.html")

#Practice terrible at
@views.route("/practice/terrible")
def terrible():
    return render_template("terrible.html")

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

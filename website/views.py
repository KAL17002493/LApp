from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Word
from . import db
import json

views = Blueprint("views", __name__)

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

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/delete-word", methods=["POST"])
def delete_word():
    word = json.loads(request.data)
    wordId = word["wordId"]
    word = Word.query.get(wordId)

    if word:
        db.session.delete(word)
        db.session.commit()

    return jsonify({})

from . import db
from sqlalchemy.sql import func

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_word = db.Column(db.String(150))
    german_word = db.Column(db.String(150))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

class UserWordPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fail_count = db.Column(db.Integer, default=0)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    word = db.relationship('Word', backref=db.backref('performances', lazy=True))
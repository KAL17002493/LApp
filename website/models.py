from . import db
from sqlalchemy.sql import func

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    englishWord = db.Column(db.String(150))
    germanWord = db.Column(db.String(150))
    dateAdded = db.Column(db.DateTime(timezone=True), default=func.now())
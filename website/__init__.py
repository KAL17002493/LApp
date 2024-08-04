from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    
    app.register_blueprint(views, url_prefix='/')

    #This is to create the database if it does not exist (SQLAlchemy will not overwrite the database if it already exists)
    from .models import Word, UserWordPerformance
    with app.app_context():
        db.create_all()

    return app
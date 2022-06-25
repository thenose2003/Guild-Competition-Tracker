from flask import Flask
import sqlite3

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super_secret_key'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app

from os import environ

from patentsearch import db, app
from patentsearch.models import User
from flask_script import Manager, prompt_bool




"""
This script runs the FlaskWebProject4 application using a development server.
"""

from os import environ
from patentsearch import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

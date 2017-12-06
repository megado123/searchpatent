
from os import environ

from patentsearch import db, app
from patentsearch.models import User
from flask_script import Manager, prompt_bool



#def wsgi_app(environ, start_response):
    #status = '200 OK'
    #response_headers = [('Content-type', 'text/plain')]
    #start_response(status, response_headers)
    #response_body = 'Hello World'
    #yield response_body.encode()

#if __name__ == '__main__':
#    from wsgiref.simple_server import make_server

#    httpd = make_server('localhost', 5555, wsgi_app)
#    httpd.serve_forever()


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


from patentsearch import db, app
from patentsearch.models import User
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command



def initdb():
    db.create_all()
    db.session.add(User(username="megan", email="megan@example.com", password="test"))

    db.session.add(User(username="cynthai", email="cynthia@example.com", password="test"))

    db.session.commit()
    print ('Initialized the database')

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data - for sure?"):
        db.drop_all()
        print ('Database has been dropped')


if __name__ == '__main__':
    manager.run()
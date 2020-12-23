1. Required python packages:

sudo pip3 install flask
sudo pip3 install flask_sqlalchemy
sudo pip3 install flask-marshmallow
sudo pip3 install marshmallow-sqlalchemy
sudo pip3 install flask-bcrypt
sudo pip3 install mysqlclient

2. Prepare alembic configuration:
a) execute:

    alembic init alembic

b) edit ~/flask_user_notes/alembic.ini, add:

    sqlalchemy.url = mysql://katya:1@localhost/users_notes


c) edit ~/flask_user_notes/alembic/env.py, add:

    import sys
    sys.path.append('/home/katya/AppliedProg/Applied-programming')

    from app.users_notes import db
    target_metadata = db.Model.metadata

d) start tables creation (initial migation):

    alembic revision --autogenerate -m "Initial tables creation"
    alembic upgrade head

3. Requests examples:

a) register user:
  - correct request:
      curl -d "username=katya&email=katya@ukr.net&passwd=123" -H "Content-Type: application/x-www-form-urlencoded" -X POST  '127.0.0.1:5000/register/user'
  - bad request method:
      curl -d "username=katya&email=katya@ukr.net&passwd=123" -H "Content-Type: application/x-www-form-urlencoded" -X GET  '127.0.0.1:5000/register/user'
  - bad email address:
      curl -d "username=katya&email=katya.ukr.net&passwd=123" -H "Content-Type: application/x-www-form-urlencoded" -X POST  '127.0.0.1:5000/register/user'

b) getting user:
  - correct request:
      curl -X GET '127.0.0.1:5000/user/katya'
  - user doesn't exist:
      curl -X GET '127.0.0.1:5000/user/olya'

c) delete user:
  - correct request:
      curl -X DELETE '127.0.0.1:5000/deluser/katya'
  - user doesn't exist:
      curl -X DELETE '127.0.0.1:5000/deluser/katya'

d) modify user data:
  - correct request:
      curl -d "username=katya&email=katya@ukr.net&passwd=345" -H "Content-Type: application/x-www-form-urlencoded" -X PUT  '127.0.0.1:5000/moduser/katya'

e) add note:
  - correct reuest:
      curl -d "text=my first test message" -H "Content-Type: application/x-www-form-urlencoded" -X POST  '127.0.0.1:5000/add/note/katya'

f) get all notes:
  - correct reuest:
      curl -X GET  '127.0.0.1:5000/notes'
g) get note info by note ID:
  - correct reuest:
      curl -X GET  '127.0.0.1:5000/note/2'

i) get note info by pattern:
  - correct reuest:
      curl -d "text=my" -X GET  '127.0.0.1:5000/text/note'

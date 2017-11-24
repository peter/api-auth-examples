# Flask API Authentation Example App

## Dependencies

* Python 3
* PostgreSQL
* Flask

## Installing and Starting the Server

```
pip install virtualenv
. venv/bin/activate

pip install -r requirements.txt

createdb api-auth-flask-dev

python
from app import db
db.create_all()
```

Start dev server:

```
/bin/start-dev
```

## Example API Requests

For locally running server:

```
export BASE_URL=http://localhost:5000
```

Examples below with [httpie](https://httpie.org):

```
alias uuid="python -c 'import sys,uuid; sys.stdout.write(uuid.uuid4().hex)' | pbcopy && pbpaste && echo"
export EMAIL="admin-$(uuid)@example.com"

# Successful register (=> 201)
echo "{\"user\": {\"email\": \"$EMAIL\", \"password\": \"123\"}}" | http POST $BASE_URL/register

# Successful login (=> 200, returns token)
echo "{\"email\": \"$EMAIL\", \"password\": \"123\"}" | http POST $BASE_URL/login
export TOKEN=<token-in-response-above>

# Failed login attempt (=> 401)
echo "{\"email\": \"$EMAIL\", \"password\": \"122\"}" | http POST $BASE_URL/login

# Successful get user info (=> 200, returns recent_successful_logins)
http $BASE_URL/me Authorization:"Bearer $TOKEN"

# Failed get user info (=> 401)
http $BASE_URL/me
```

## How this App was Created

```
pip install virtualenv
mkdir flask
cd flask

virtualenv venv
. venv/bin/activate

pip install Flask psycopg2 Flask-SQLAlchemy Flask-Migrate Flask-Bcrypt PyJWT WTForms
pip freeze > requirements.txt

createdb api-auth-flask-dev

python
from app import db
db.create_all()
from app import User
from app import bcrypt
# password_digest = bcrypt.generate_password_hash('123')
user = User(email='admin@example.com', password='123')
db.session.add(user)
db.session.commit()

psql api-auth-flask-dev
select * from users;
```

## Deployment

TODO

## TODO

* require_login filter
* Add exp to token
* Handle invalid/expired token
* Double register of user yields 500 (db error)
* login_attempts table
* same endpoints as in Rails app
* tests
* deployment

## Resources

* [Token-Based Authentication With Flask](https://realpython.com/blog/python/token-based-authentication-with-flask)
* [Securing REST APIs: Basic HTTP Authentication with Python / Flask](http://polyglot.ninja/securing-rest-apis-basic-http-authentication-python-flask)

* [Flask by Example - Setting Up Postgres, SQLAlchemy, and Alembic](https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic)

* [Build a CRUD Web App With Python and Flask](https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one)

* [PyJWT](http://pyjwt.readthedocs.io/en/latest)

* [Flask-SQLAlchemy (ORM)](http://flask-sqlalchemy.pocoo.org/2.3)
* [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)
* [Flask-Bcrypt](http://flask-bcrypt.readthedocs.io/en/0.7.1)

* [Flask (Web Framework)](http://flask.pocoo.org)
* [Flask Documentation (PDF)](http://flask.pocoo.org/docs/0.12/.latex/Flask.pdf)
* [Zappa/AWS Lambda (Deployment)](https://github.com/Miserlou/Zappa)

* [Hug (Python API Framework)](http://www.hug.rest)
* [Zappa Hug Example (Hug/Lambda Deployment)](https://github.com/mcrowson/zappa-hug-example)

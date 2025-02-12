python3 -m venv env

source env/bin/activate

# Run if requirements.txt file doesn't work
pip install Flask  flask-cors
pip install psycopg2-binary
pip install flask-sqlalchemy
pip install python-dotenv
pip install Flask-SQLAlchemy Flask-Migrate

# For DB migrations
flask db init
flask db migrate -m "Initial migration after resetting"
flask db upgrade

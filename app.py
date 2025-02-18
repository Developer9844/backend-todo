from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from flask_redis import FlaskRedis
from models import db, TodoItem
from config import Config
import json

# Initialize the Flask app
app = Flask(__name__)

# Load the configuration from config.py
app.config.from_object(Config)
CORS(app)

# Initialize the database with the app
db.init_app(app)

# Initialize Flask-Migrate with the app and db
migrate = Migrate(app, db)

# Initialize Redis
redis_client = FlaskRedis(app)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/todos', methods=['GET'])
def get_todos():
    # Check if data exists in Redis cache
    cached_todos = redis_client.get("todos")
    

    if cached_todos:
        return jsonify(json.loads(cached_todos))  # Return cached data

    # Fetch from database if cache is empty
    todos = TodoItem.query.all()
    todos_list = [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in todos]

    # Store data in Redis cache for 5 minutes
    redis_client.setex("todos", 300, json.dumps(todos_list))

    return jsonify(todos_list)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = TodoItem(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()

    # Clear cache to refresh data
    redis_client.delete("todos")

    return jsonify({'id': new_todo.id, 'task': new_todo.task, 'completed': new_todo.completed}), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = TodoItem.query.get(id)
    if todo:
        data = request.get_json()
        todo.completed = data['completed']
        db.session.commit()

        # Clear cache to refresh data
        redis_client.delete("todos")

        return jsonify({'id': todo.id, 'task': todo.task, 'completed': todo.completed})
    return jsonify({'message': 'Todo not found'}), 404

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = TodoItem.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()

        # Clear cache to refresh data
        redis_client.delete("todos")

        return jsonify({'message': 'Todo deleted'})
    return jsonify({'message': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

import logging
import sqlite3
from flask import Flask, request, jsonify
from pythonjsonlogger import jsonlogger
from prometheus_client import start_http_server, Counter, Summary

app = Flask(__name__)
tasks = []

# Configure logging
logger = logging.getLogger('flask_app')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing requests')
ERROR_COUNT = Counter('error_count', 'Total number of errors', ['method', 'endpoint'])

# SQLite setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    REQUEST_COUNT.labels(method='GET', endpoint='/tasks').inc()
    with REQUEST_TIME.time():
        logger.info('GET /tasks called')
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM tasks')
        tasks = [{'id': row[0], 'task': row[1]} for row in c.fetchall()] # Create a list of task dicts from DB query results
        conn.close()
        return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    REQUEST_COUNT.labels(method='POST', endpoint='/tasks').inc()
    with REQUEST_TIME.time():
        task = request.json.get('task')
        if task:
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()
            c.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            conn.commit()
            conn.close()
            logger.info(f'Task added: {task}')
            return jsonify({"message": "Task added"}), 201
        ERROR_COUNT.labels(method='POST', endpoint='/tasks').inc()
        logger.warning('POST /tasks called with no task')
        return jsonify({"error": "No task provided"}), 400

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    REQUEST_COUNT.labels(method='PUT', endpoint='/tasks/<id>').inc()
    with REQUEST_TIME.time():
        task = request.json.get('task')
        if task:
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()
            c.execute('UPDATE tasks SET task = ? WHERE id = ?', (task, task_id))
            if c.rowcount == 0: # No rows updated means task ID wasn’t found
                conn.close()
                ERROR_COUNT.labels(method='PUT', endpoint='/tasks/<id>').inc()
                logger.warning(f'PUT /tasks/{task_id} failed: task not found')
                return jsonify({"error": "Task not found"}), 404
            conn.commit()
            conn.close()
            logger.info(f'Task {task_id} updated: {task}')
            return jsonify({"message": "Task updated"}), 200
        ERROR_COUNT.labels(method='PUT', endpoint='/tasks/<id>').inc()
        logger.warning(f'PUT /tasks/{task_id} called with no task')
        return jsonify({"error": "No task provided"}), 400

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    REQUEST_COUNT.labels(method='DELETE', endpoint='/tasks/<id>').inc()
    with REQUEST_TIME.time():
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        if c.rowcount == 0:
            conn.close()
            ERROR_COUNT.labels(method='DELETE', endpoint='/tasks/<id>').inc()
            logger.warning(f'DELETE /tasks/{task_id} failed: task not found')
            return jsonify({"error": "Task not found"}), 404
        conn.commit()
        conn.close()
        logger.info(f'Task {task_id} deleted')
        return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    init_db()
    start_http_server(8000)  # Expose metrics on port 8000
    app.run(host='0.0.0.0', port=5000)
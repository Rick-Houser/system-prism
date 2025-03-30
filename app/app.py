import os
import logging
import psycopg2
import time
import threading
import psutil
from flask import Flask, request, jsonify
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Summary, Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Configure logging
logger = logging.getLogger('flask_app')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/flask_app.log')
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing requests')
ERROR_COUNT = Counter('error_count', 'Total number of errors', ['method', 'endpoint'])
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')

def update_resources():
    while True:
        CPU_USAGE.set(psutil.cpu_percent(interval=1))
        MEMORY_USAGE.set(psutil.virtual_memory().used)
        time.sleep(5)

# Start resource monitoring thread
threading.Thread(target=update_resources, daemon=True).start()

db_initialized = False

def init_db():
    global db_initialized
    if not db_initialized:
        retries = 0
        max_retries = 12  # 1 minute
        while retries < max_retries:
            try:
                conn = psycopg2.connect(os.getenv('DB_URL'))
                logger.info(f"Connected to DB: {os.getenv('DB_URL')}")
                c = conn.cursor()
                c.execute('CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, task TEXT NOT NULL)')
                conn.commit()
                conn.close()
                logger.info("Table created")
                db_initialized = True
                return
            except psycopg2.OperationalError as e:
                retries += 1
                logger.warning(f"DB connection failed (attempt {retries}/{max_retries}): {e}")
                if retries == max_retries:
                    logger.error("Max retries reached—aborting")
                    raise
                time.sleep(5)

init_db()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    REQUEST_COUNT.labels(method='GET', endpoint='/tasks').inc()
    with REQUEST_TIME.time():
        logger.info('GET /tasks called')
        conn = psycopg2.connect(os.getenv('DB_URL'))
        c = conn.cursor()
        c.execute('SELECT * FROM tasks')
        tasks = [{'id': row[0], 'task': row[1]} for row in c.fetchall()]
        conn.close()
        return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    REQUEST_COUNT.labels(method='POST', endpoint='/tasks').inc()
    with REQUEST_TIME.time():
        task = request.json.get('task')
        if task:
            conn = psycopg2.connect(os.getenv('DB_URL'))
            c = conn.cursor()
            c.execute('INSERT INTO tasks (task) VALUES (%s) RETURNING id', (task,))
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
            conn = psycopg2.connect(os.getenv('DB_URL'))
            c = conn.cursor()
            c.execute('UPDATE tasks SET task = %s WHERE id = %s', (task, task_id))
            if c.rowcount == 0:
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
        conn = psycopg2.connect(os.getenv('DB_URL'))
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
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
    app.run(host='0.0.0.0', port=5000)
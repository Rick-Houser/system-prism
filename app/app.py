import logging
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

@app.route('/tasks', methods=['GET'])
def get_tasks():
    REQUEST_COUNT.labels(method='GET', endpoint='/tasks').inc()
    with REQUEST_TIME.time():
        logger.info('GET /tasks called')
        return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    REQUEST_COUNT.labels(method='POST', endpoint='/tasks').inc()
    with REQUEST_TIME.time():
        task = request.json.get('task')
        if task:
            tasks.append(task)
            logger.info(f'Task added: {task}')
            return jsonify({"message": "Task added"}), 201
        logger.warning('POST /tasks called with no task')
        return jsonify({"error": "No task provided"}), 400

if __name__ == '__main__':
    start_http_server(8000)  # Expose metrics on port 8000
    app.run(host='0.0.0.0', port=5000)
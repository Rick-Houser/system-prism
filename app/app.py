import logging
from flask import Flask, request, jsonify
from pythonjsonlogger import jsonlogger

app = Flask(__name__)
tasks = []

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    logger.info('GET /tasks called')
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        tasks.append(task)
        logger.info(f'Task added: {task}')
        return jsonify({"message": "Task added"}), 201
    logger.warning('POST /tasks called with no task')
    return jsonify({"error": "No task provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
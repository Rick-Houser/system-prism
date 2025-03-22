import unittest
import logging
import io
from app.app import app, tasks

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        tasks.clear()
        # capture logs
        self.log_output = io.StringIO()
        handler = logging.StreamHandler(self.log_output)
        formatter = logging.Formatter('%(levelname)s %(message)s')  # Simplified for testing
        handler.setFormatter(formatter)
        logger = logging.getLogger('flask_app')
        logger.handlers = [handler]  # Replace handlers to avoid duplicates        

    def test_get_tasks_empty(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
        log_content = self.log_output.getvalue()
        self.assertIn('INFO GET /tasks called', log_content)

    def test_add_task_success(self):
        response = self.client.post('/tasks', json={"task": "Buy milk"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Task added"})
        log_content = self.log_output.getvalue()
        self.assertIn('INFO Task added: Buy milk', log_content)
        # Verify task was added
        response = self.client.get('/tasks')
        self.assertEqual(response.json, ["Buy milk"])

    def test_add_task_no_data(self):
        response = self.client.post('/tasks', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "No task provided"})
        log_content = self.log_output.getvalue()
        self.assertIn('WARNING POST /tasks called with no task', log_content)

if __name__ == '__main__':
    unittest.main()
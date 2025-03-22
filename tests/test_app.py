import unittest
from app.app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Reset tasks list before each test
        global tasks
        tasks.clear()

    def test_get_tasks_empty(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_add_task_success(self):
        response = self.client.post('/tasks', json={"task": "Buy milk"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Task added"})
        # Verify task was added
        response = self.client.get('/tasks')
        self.assertEqual(response.json, ["Buy milk"])

    def test_add_task_no_data(self):
        response = self.client.post('/tasks', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "No task provided"})

if __name__ == '__main__':
    unittest.main()
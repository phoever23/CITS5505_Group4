import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>', response.data)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_signup_page(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

    def test_dashboard_requires_login(self):
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_upload_requires_login(self):
        response = self.app.get('/upload', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_share_page(self):
        response = self.app.get('/share')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Share', response.data)

    def test_upload_invalid_content_type(self):
        response = self.app.post('/upload', headers={
            'Content-Type': 'text/plain'
        }, follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_api_expenses_requires_login(self):
        response = self.app.get('/api/expenses', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_search_users_requires_login(self):
        response = self.app.get('/api/search-users?term=test', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_share_data_requires_login(self):
        response = self.app.post('/api/share-data', json={}, follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_get_shared_expenses_requires_login(self):
        response = self.app.get('/api/shared-expenses', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_get_my_shared_expenses_requires_login(self):
        response = self.app.get('/api/my-shared-expenses', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_debug_users_requires_login(self):
        response = self.app.get('/debug/users', follow_redirects=True)
        self.assertIn(b'Login', response.data)

# --- Custom Test Runner Section ---
import sys
from unittest.runner import TextTestRunner, TextTestResult

class CustomTestResult(TextTestResult):
    def printErrors(self):
        super().printErrors()
        if not self.failures and not self.errors:
            self.stream.writeln("Passed all tests for key Flask routes")

class CustomTestRunner(TextTestRunner):
    resultclass = CustomTestResult

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner(), verbosity=2)

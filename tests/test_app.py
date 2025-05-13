import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        Creates a test client and enables testing mode for better error messages.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """
        Test that the home page ("/") loads successfully.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>', response.data)  # Confirms HTML is returned

    def test_login_page(self):
        """
        Test that the login page ("/login") loads and contains the word 'Login'.
        """
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_signup_page(self):
        """
        Test that the signup page ("/signup") loads and contains 'Sign Up'.
        """
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)  # Ensure 'Sign Up' matches your HTML

    def test_dashboard_requires_login(self):
        """
        Test that the dashboard route ("/dashboard") redirects unauthenticated users to login.
        """
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_upload_requires_login(self):
        """
        Test that the upload route ("/upload") also redirects unauthenticated users to login.
        """
        response = self.app.get('/upload', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_share_page(self):
        """
        Test that the share page ("/share") loads successfully and contains 'Share'.
        """
        response = self.app.get('/share')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Share', response.data)

    def test_upload_invalid_content_type(self):
        """
        Test POSTing to the upload endpoint with invalid content type while not logged in.
        Should redirect to login page.
        """
        response = self.app.post('/upload', headers={
            'Content-Type': 'text/plain'
        }, follow_redirects=True)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()

import unittest
from app import app
from flask import session

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test the home page is accessible."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>', response.data)  # Basic check for HTML content

    def test_login_page(self):
        """Test the login page loads correctly."""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_signup_page(self):
        """Test the signup page loads correctly."""
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

    def test_dashboard_redirects_when_not_logged_in(self):
        """Dashboard should redirect to login if user is not authenticated."""
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_upload_redirects_when_not_logged_in(self):
        """Upload should redirect to login if user is not authenticated."""
        response = self.app.get('/upload', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_share_page_accessible(self):
        """Share page should load for anonymous users (no login required)."""
        response = self.app.get('/share')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Share', response.data)

    def test_upload_invalid_content_type(self):
        """Upload should return an error for unsupported content types."""
        response = self.app.post('/upload', headers={
            'Content-Type': 'text/plain'
        }, follow_redirects=True)
        # Redirects to login if not authenticated
        self.assertIn(b'Login', response.data)

    def test_api_expenses_requires_login(self):
        """API route for expenses must redirect when unauthenticated."""
        response = self.app.get('/api/expenses', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_api_search_users_requires_login(self):
        """Search user API requires login."""
        response = self.app.get('/api/search-users?term=test', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_api_share_data_requires_login(self):
        """Share data API should require authentication."""
        response = self.app.post('/api/share-data', json={'shareWith': 'dummy'}, follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_api_get_shared_expenses_requires_login(self):
        """Shared expenses API must be protected."""
        response = self.app.get('/api/shared-expenses', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_api_my_shared_expenses_requires_login(self):
        """My shared expenses API must be protected."""
        response = self.app.get('/api/my-shared-expenses', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_debug_users_requires_login(self):
        """Debug user route must be protected."""
        response = self.app.get('/debug/users', follow_redirects=True)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()

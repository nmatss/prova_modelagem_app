import unittest
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, init_db
from db import get_db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for easier testing
        app.config['DATABASE'] = ':memory:' # Use in-memory database
        
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Initialize database
        init_db()
        
        # Create a test user
        from auth import generate_password_hash
        db = get_db()
        db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                   ('testuser', generate_password_hash('testpassword')))
        db.commit()

    def tearDown(self):
        self.app_context.pop()

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_success(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data) # Assuming dashboard has "Dashboard" text

    def test_login_failure(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout(self):
        # Login first
        self.client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        
        # Then logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page_loads(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registrar', response.data)

    def test_register_success(self):
        response = self.client.post('/register', data=dict(
            username='newuser',
            password='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)
        
        # Verify user is in DB
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', ('newuser',)).fetchone()
        self.assertIsNotNone(user)

if __name__ == '__main__':
    unittest.main()

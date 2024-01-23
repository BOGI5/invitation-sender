import os
import sys
import unittest
from flask import Flask, request
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from app.model import User
from app.controller import create_user, validate_user, add_event


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        user_data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@email.com',
            'password': 'testPassword123'
        }
        with app.test_request_context('/'):
            request.form = user_data
            create_user(request)

        with app.app_context():
            user = User.query.filter_by(email=user_data['email']).first()
            self.assertIsNotNone(user)
            self.assertEqual(user.first_name, 'test_first_name')

        with app.test_request_context('/'):
            request.form = user_data
            response = self.app.post('/sign_up', data=user_data)
            self.assertEqual(response.status_code, 200)

    def test_validate_user(self):
        user_data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@email.com',
            'password': 'testPassword123'
        }
        with app.test_request_context('/'):
            request.form = user_data
            create_user(request)

        with app.test_request_context('/'):
            response = self.app.post('/login', data={'email': 'test@email.com', 'password': 'testPassword123'})
            self.assertEqual(response.status_code, 302)

        response = self.app.post('/login', data={'email': 'incorrect@email.com', 'password': 'incorrectPassword'})
        self.assertEqual(response.status_code, 200)

    def test_add_event(self):
        user_data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@email.com',
            'password': 'testPassword123'
        }
        with app.test_request_context('/'):
            request.form = user_data
            create_user(request)

        with app.test_request_context('/'):
            user = User.query.filter_by(email=user_data['email']).first()
            self.assertIsNotNone(user)

        event_data = {
            'name': 'Birthday Party',
            'date': '2024-01-23',
            'address': '123 Bulgaria blvd.',
            'user_id': user.id
        }
        with app.test_request_context('/'):
            request.form = event_data
            response = self.app.post(f'/create_event/{user.id}', data=event_data)
            self.assertEqual(response.status_code, 302)

        invalid_event_data = {
            'name': '',
            'date': 'invalid-date',
            'address': '123 Bulgaria blvd.',
            'user_id': user.id
        }
        with app.test_request_context('/'):
            request.form = invalid_event_data
            response = self.app.post(f'/create_event/{user.id}', data=invalid_event_data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

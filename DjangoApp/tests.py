from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json

class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = 'http://127.0.0.1:8000/user/signup'
        self.login_url = 'http://127.0.0.1:8000/user/signin'
        self.user_data = {
    "fullname": "Salah",
    "email": "salah@gmail.com",
    "address": "123 Street",
    "zip": 12345,
    "city": "City",
    "phone": "1234567890",
    "role": "botaniste",
    "password":"salah"
}

    def test_user_registration(self):
        response = self.client.post(self.register_url, data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):

        self.client.post(self.register_url, data=json.dumps(self.user_data), content_type='application/json')
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }
        response = self.client.post(self.login_url, data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

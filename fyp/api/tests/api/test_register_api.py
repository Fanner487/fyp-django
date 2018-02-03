from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class RegisterTest(APITestCase):
    """
    Tests all register API calls with parameters
    """

    def setUp(self):

        self.client = APIClient()
        self.url = "/api/register"

        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

    def test_create_user(self):

        data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password': 'somepassword',
            'password_confirm': 'somepassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        # We want to make sure we have two users in the database
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if uesr details are the same
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])

    def test_create_user_with_short_password(self):

        data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password': 'test',
            'password_confirm': 'test',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        # asserts status_code, only one
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):

        data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password': '',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        # asserts status_code, only one
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_existing_username(self):
        data = {
            'username': 'testuser',
            'email': 'testuser4@example.com',
            'password': 'somepassword',
            'password_confirm': 'somepassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_existing_email(self):
        data = {
            'username': 'testuser5',
            'email': 'testuser@example.com',
            'password': 'somepassword',
            'password_confirm': 'somepassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_unmatching_passwords(self):
        data = {
            'username': 'testuser6',
            'email': 'testuser6@example.com',
            'password': 'somepassword',
            'password_confirm': 'somepasswordNOT',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        print(response.content)
        self.assertEqual(len(response.data['non_field_errors']), 1)

    def test_create_user_with_no_first_name(self):

        data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password': 'test',
            'password_confirm': 'test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        # asserts status_code, only one
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['first_name']), 1)

    def test_create_user_with_no_last_name(self):

        data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password': 'test',
            'password_confirm': 'test',
            'first_name': "User"
        }

        response = self.client.post(self.url, data=data, format='json')

        # asserts status_code, only one
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['last_name']), 1)



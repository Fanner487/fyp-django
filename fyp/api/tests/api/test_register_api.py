from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse


class RegisterTest(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = "/api/register"
        # self.create_url = reverse("/api/register")

        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

    def test_create_user(self):

        data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password': 'somepassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])

    def test_create_user_with_short_password(self):

        data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password': '',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_existing_username(self):
        data = {
            'username': 'testuser',
            'email': 'testuser4@example.com',
            'password': 'somepassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)




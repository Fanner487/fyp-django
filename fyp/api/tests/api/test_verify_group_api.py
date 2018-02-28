from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class VerifyGroupApiTest(APITestCase):
    """
    Tests all group verify API POSTS with parameters
    """

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/verify_group"
        self.token_url = "/api/api-token-auth/"

        User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

        User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        User.objects.create_user(
            username='testuser3',
            email='testuser3@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        User.objects.create_user(
            username='testuser4',
            email='testuser4@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

        login_data = {
            'username': 'testuser1',
            'password': 'testpassword'
        }

        token_response = self.client.post(self.token_url, data=login_data, format='json')
        self.token = token_response.data.get('token')
        print("\n\ntoken")
        print(self.token)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_verify_group_success(self):
        data = {
            'usernames': ['testuser1', 'testuser2', 'testuser3']
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_group_empty(self):
        data = {
            'usernames': []
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']), 1)

    def test_verify_group_non_existing_user(self):
        data = {
            'usernames': ['testuser1', 'testuser2', 'NOTAUSER']
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']), 1)

    def test_verify_group_none(self):
        data = None

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['usernames']), 1)

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class LoginTest(APITestCase):
    """
    Tests all group verify API POSTS with parameters
    """

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/verify_group"

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

    def test_verify_group_success(self):
        data = {
            'username': ['testuser1', 'testuser2', 'testuser3']
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_login_incorrect_password(self):
    #     data = {
    #         'username': 'testuser',
    #         'password': 'nottherealpassword'
    #     }
    #
    #     response = self.client.post(self.url, data=data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_login_incorrect_username(self):
    #     data = {
    #         'username': 'notauser',
    #         'password': 'testpassword'
    #     }
    #
    #     response = self.client.post(self.url, data=data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_login_null_username(self):
    #     data = {
    #
    #         'password': 'testpassword'
    #     }
    #
    #     response = self.client.post(self.url, data=data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_login_null_password(self):
    #     data = {
    #         'username': 'testuser'
    #     }
    #
    #     response = self.client.post(self.url, data=data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

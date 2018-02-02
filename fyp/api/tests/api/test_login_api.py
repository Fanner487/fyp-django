from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class LoginTest(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = "/api/login"
        # self.create_url = reverse("/api/register")

        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
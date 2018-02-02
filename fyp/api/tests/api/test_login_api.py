from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class LoginTest(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = "/api/register"
        # self.create_url = reverse("/api/register")

        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )



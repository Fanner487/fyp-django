from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status


# User login test
class LoginTestCase(TestCase):
    def setUp(self):
        username = "eamontang1"
        email = "eamontang1@gmail.com"
        password = "orangemonkeyeagle1"
        User.objects.create_user(username, email, password)
        client = APIClient()

    def test_login_success(self):
        data = {'username': 'eamontang1', 'password': 'orangemonkeyeagle1'}
        response = self.client.post("/api/login/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_password_fail(self):
        data = {'username': 'eamontang1', 'password': 'notmypassword'}
        response = self.client.post("/api/login/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_username_fail(self):
        data = {'username': 'eamontangnotreal1', 'password': 'orangemonkeyeagle1'}
        response = self.client.post("/api/login/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterTestCase(TestCase):
    def setUp(self):
        client = APIClient()

    def test_register_success(self):
        data = {
            'username': "billybob1",
            'password': "orangemonkeyeagle1",
            'email': "billybob1@gmail.com",
            'firstname': 'Billy',
            'surname': 'Bob',
        }

        response = self.client.post("/api/register/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Created account')

    def test_register_duplicate_email(self):
        print("test_register_duplicate_email")

        data = {
            'username': "janedoe1",
            'password': "orangemonkeyeagle1",
            'email': "janedoe1@gmail.com",
            'firstname': 'Jane',
            'surname': 'Doe',
        }

        response = self.client.post("/api/register/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print("second user")

        data_new = {
            'username': "testuser1",
            'password': "orangemonkeyeagle1",
            'email': "janedoe1@gmail.com",
            'firstname': 'Jane',
            'surname': 'Doe',
        }
        response_new = self.client.post("/api/register/", data=data_new, format='json')
        self.assertEqual(response_new.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_duplicate_username(self):
        data = {
            'username': "janedoe1",
            'password': "orangemonkeyeagle1",
            'email': "janedoe1@gmail.com",
            'firstname': 'Jane',
            'surname': 'Doe',
        }

        response = self.client.post("/api/register/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print("second user")

        data_new = {
            'username': "janedoe1",
            'password': "orangemonkeyeagle1",
            'email': "testemail@gmail.com",
            'firstname': 'Jane',
            'surname': 'Doe',
        }
        response_new = self.client.post("/api/register/", data=data_new, format='json')
        self.assertEqual(response_new.status_code, status.HTTP_401_UNAUTHORIZED)

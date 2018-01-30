# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status

# Create your tests here.
# User login test
class ExampleTestCase(TestCase):
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

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

    def test_login(self):
        data = {'username': 'eamontang1', 'password': 'orangemonkeyeagle1'}
        response = self.client.post("/api/login/", data=data, format='json')
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
        data = {'username': 'eamontang1', 'password': 'notmypassword'}
        response = self.client.post("/api/login/", data=data, format='json')
        print(response.status_code)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

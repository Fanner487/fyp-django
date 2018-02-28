# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Event
from rest_framework import status
import json

"""
Tests all API calls for CRUD operations of the Event model.
All potential invalid and non-nullable fields are tested
"""


class ApiTokenAuthApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/api-token-auth/"

        self.username = "test1"
        self.email = "test@example.com"
        self.password = "mypassword"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.login_data = {
            'username': self.username,
            'password': self.password
        }

    def test_token_obtain_success(self):

        token_response = self.client.post(self.url, data=self.login_data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(token_response.data)
        print(token_response.data)
        # self.assertTrue(token_response.data.contains("token"))
        self.assertIsNotNone(token_response.json().get('token'))

    def test_token_obtain_wrong_username(self):
        self.login_data = {
            'username': "NOT",
            'password': self.password
        }

        token_response = self.client.post(self.url, data=self.login_data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(token_response.data)



    def test_token_obtain_wrong_password(self):

        self.login_data = {
            'username': self.username,
            'password': "NOT"
        }

        token_response = self.client.post(self.url, data=self.login_data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(token_response.data)

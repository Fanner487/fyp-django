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


class ApiTokenVerifyTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/api-token-verify/"

        self.username = "test1"
        self.email = "test@example.com"
        self.password = "mypassword"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.login_data = {
            'username': self.username,
            'password': self.password
        }

        self.token_url = "/api/api-token-auth/"

        token_response = self.client.post(self.token_url, data=self.login_data, format='json')
        self.token = token_response.data.get('token')

    def test_token_verify_success(self):

        data = {
            'token': self.token
        }

        token_response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)

    def test_token_verify_fail(self):
        data = {
            'token': "sdfsdfsdfs"
        }

        token_response = self.client.post(self.url, data=data, format='json')

        print(token_response.data)
        self.assertNotEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertEqual(token_response.status_code, status.HTTP_400_BAD_REQUEST)

    #
    # def test_token_obtain_wrong_username(self):
    #     self.login_data = {
    #         'username': "NOT",
    #         'password': self.password
    #     }
    #
    #     token_response = self.client.post(self.url, data=self.login_data, format='json')
    #
    #     self.assertEqual(token_response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIsNotNone(token_response.data)
    #     self.assertIsNone(token_response.json().get('token'))
    #     self.assertIsNotNone(token_response.json().get('non_field_errors'))
    #
    # def test_token_obtain_wrong_password(self):
    #
    #     self.login_data = {
    #         'username': self.username,
    #         'password': "NOT"
    #     }
    #
    #     token_response = self.client.post(self.url, data=self.login_data, format='json')
    #
    #     self.assertEqual(token_response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIsNotNone(token_response.data)
    #     self.assertIsNone(token_response.json().get('token'))
    #     self.assertIsNotNone(token_response.json().get('non_field_errors'))
    #
    # def test_token_obtain_blank_username(self):
    #
    #     self.login_data = {
    #         'password': "NOT"
    #     }
    #
    #     token_response = self.client.post(self.url, data=self.login_data, format='json')
    #
    #     self.assertEqual(token_response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIsNotNone(token_response.data)
    #     self.assertIsNone(token_response.json().get('token'))
    #     self.assertIsNotNone(token_response.json().get('username'))
    #
    # def test_token_obtain_blank_password(self):
    #
    #     self.login_data = {
    #         'username': self.username
    #     }
    #
    #     token_response = self.client.post(self.url, data=self.login_data, format='json')
    #
    #     self.assertEqual(token_response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIsNotNone(token_response.data)
    #     self.assertIsNone(token_response.json().get('token'))
    #     self.assertIsNotNone(token_response.json().get('password'))

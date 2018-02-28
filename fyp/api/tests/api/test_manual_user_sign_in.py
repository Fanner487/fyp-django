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


class ManualUserSignInTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/manual_sign_in"

        self.username = "test1"
        self.email = "test@example.com"
        self.password = "mypassword"
        self.user1 = User.objects.create_user(self.username, self.email, self.password)

        self.username2 = "test2"
        self.email2 = "test2@example.com"
        self.password2 = "mypassword"
        self.user2 = User.objects.create_user(self.username2, self.email2, self.password2)

        login_data = {
            'username': 'test1',
            'password': 'mypassword'
        }

        self.token_url = "/api/api-token-auth/"

        token_response = self.client.post(self.token_url, data=login_data, format='json')
        self.token = token_response.data.get('token')
        print("\n\ntoken")
        print(self.token)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        self.event = Event.objects.create(
            organiser="test1",
            event_name="test",
            location="test",
            start_time='2050-01-29T12:00:00',
            finish_time='2050-01-29T12:30:00',
            sign_in_time='2050-01-29T12:00:00',
            attendees=['test2']
        )

    def test_manual_sign_in_success(self):
        # print(str(serializer.validated_data['event_id']))
        # print(str(serializer.validated_data['user']))

        data = {
            'event_id': self.event.id,
            'user': self.user2.username
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_manual_sign_in_wrong_event_id(self):

        data = {
            'event_id': 999999,
            'user': self.user2.username
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.data.get('non_field_errors'))

    def test_manual_sign_in_wrong_user(self):

        data = {
            'event_id': self.event.id,
            'user': "NOT"
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data)
        # print()
        self.assertIsNone(response.data.get('non_field_errors'))

    def test_manual_sign_in_already_signed_in(self):
        data = {
            'event_id': self.event.id,
            'user': self.user2.username
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        response = self.client.post(self.url, data=data, format='json')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.data.get('non_field_errors'))

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

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


class EventCreateTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = ""

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

        self.event2 = Event.objects.create(
            organiser="test2",
            event_name="test",
            location="test",
            start_time='2050-01-29T12:00:00',
            finish_time='2050-01-29T12:30:00',
            sign_in_time='2050-01-29T12:00:00',
            attendees=['test2']
        )

    def test_get_events_for_user_success(self):

        self.url = "/api/" + self.user1.username + "/events"

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_get_events_wrong_user(self):
        self.url = "/api/sdfsdfsdfdfs/events"

        response = self.client.get(self.url)

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(response.data)

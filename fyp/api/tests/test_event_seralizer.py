# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status
from api.models import Event
from api import serializers
import datetime


class UserIsAttendeeTestCase(TestCase):

    def setUp(self):
        client = APIClient()

    # def create_test_event_now(self):
    #
    #     event_start_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
    #     # event_start_time = datetime.datetime.now()
    #     event_sign_in_time = datetime.datetime.now()
    #     event_finish_time = datetime.datetime(
    #         year=event_start_time.year,
    #         month=event_start_time.month,
    #         day=event_start_time.day,
    #         hour=23,
    #         minute=59,
    #         second=59)
    #
    #     print("Now: " + str(datetime.datetime.now()))
    #     print("Start: " + str(event_start_time))
    #     print("Sign in: " + str(event_sign_in_time))
    #     print("Finish: " + str(event_finish_time))
    #     print("\n\n")
    #
    #     data = {
    #         'organiser': "user1",
    #         'event_name': "test1",
    #         'location': "nowhere",
    #         'start_time': event_start_time,
    #         'finish_time': event_finish_time,
    #         'sign_in_time': event_sign_in_time,
    #         'attendees': ['user2', 'user3', 'user4']
    #     }
    #
    #     return self.create_event(data)

    def create_event(self):

        return Event.objects.create(
            organiser="user1",
            event_name="test",
            location="test",
            start_time='2050-01-29T12:00:00',
            finish_time='2050-01-29T12:30:00',
            sign_in_time='2050-01-29T12:00:00',
            attendees=['user1', 'user3', 'user4']
        )

    def test_event_exists_success(self):

        event_id = self.create_event()

        print(event_id)

        result = serializers.event_exists(event_id)

        self.assertTrue(result)

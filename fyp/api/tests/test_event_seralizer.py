# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Event
from django.contrib.auth.models import User
from api import serializers
import datetime


class EventExistsTestCase(TestCase):

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

        event = self.create_event()

        print("Event ID: " + str(event.id))
        self.assertEquals(event.organiser, "user1")
        self.assertEquals(event.event_name, "test")
        self.assertEquals(event.location, "test")
        self.assertEquals(event.start_time, '2050-01-29T12:00:00')
        self.assertEquals(event.finish_time, '2050-01-29T12:30:00')
        self.assertEquals(event.sign_in_time, '2050-01-29T12:00:00')
        self.assertEquals(event.attendees, ['user1', 'user3', 'user4'])

        result = serializers.event_exists(event.id)

        self.assertTrue(result)

    def test_event_exists_wrong_id(self):

        result = serializers.event_exists(9999)

        self.assertFalse(result)


class AttendeeIsUserTestCase(TestCase):

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

    def test_user_exists_success(self):
        user1 = User.objects.create_user("user1", "test@gmail.com", "mypassword")
        user2 = User.objects.create_user("user2", "test@gmail.com", "mypassword")
        user3 = User.objects.create_user("user3", "test@gmail.com", "mypassword")
        user4 = User.objects.create_user("user4", "test@gmail.com", "mypassword")
        event = self.create_event()

        print(event.id)
        print(user2.username)
        print(event.attendees)
        result = serializers.user_is_attendee(user2.username, event.id)

        self.assertTrue(result)
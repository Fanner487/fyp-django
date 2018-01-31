# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Event
from django.contrib.auth.models import User
from api import serializers
import datetime


def create_event():
    return Event.objects.create(
        organiser="user1",
        event_name="test",
        location="test",
        start_time='2050-01-29T12:00:00',
        finish_time='2050-01-29T12:30:00',
        sign_in_time='2050-01-29T12:00:00',
        attendees=['user2', 'user3', 'user4']
    )


def create_users():
    return User.objects.create_user("user1", "test@gmail.com", "mypassword"),\
           User.objects.create_user("user2", "test@gmail.com", "mypassword"),\
           User.objects.create_user("user3", "test@gmail.com", "mypassword"),\
           User.objects.create_user("user4", "test@gmail.com", "mypassword")


class EventSerializerTestCase(TestCase):


class EventExistsTestCase(TestCase):

    def test_event_exists_success(self):

        event = create_event()

        print("Event ID: " + str(event.id))
        self.assertEquals(event.organiser, "user1")
        self.assertEquals(event.event_name, "test")
        self.assertEquals(event.location, "test")
        self.assertEquals(event.start_time, '2050-01-29T12:00:00')
        self.assertEquals(event.finish_time, '2050-01-29T12:30:00')
        self.assertEquals(event.sign_in_time, '2050-01-29T12:00:00')
        self.assertEquals(event.attendees, ['user2', 'user3', 'user4'])

        result = serializers.event_exists(event.id)

        self.assertTrue(result)

    def test_event_exists_wrong_id(self):

        result = serializers.event_exists(9999)

        self.assertFalse(result)


class AttendeeIsUserTestCase(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user("user1", "test@gmail.com", "mypassword")
        self.user2 = User.objects.create_user("user2", "test@gmail.com", "mypassword")
        self.user3 = User.objects.create_user("user3", "test@gmail.com", "mypassword")
        self.user4 = User.objects.create_user("user4", "test@gmail.com", "mypassword")

        self.event = create_event()

    def test_user_exists_success(self):

        result = serializers.attendee_is_user(self.user2.username, self.event.id)
        self.assertTrue(result)

    def test_user_exists_fail_wrong_user(self):

        result = serializers.attendee_is_user("notAUser", self.event.id)
        self.assertFalse(result)

    def test_user_exists_fail_wrong_event(self):

        result = serializers.attendee_is_user(self.user2.username, 99999)
        self.assertFalse(result)

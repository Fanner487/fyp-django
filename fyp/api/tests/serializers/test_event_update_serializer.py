# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from api.models import Event
from django.contrib.auth.models import User
from api import serializers


"""
Tests all parameters and fields of EventUpdateSerializer
"""


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


class EventUpdateSerializerTestCase(TestCase):

    def setUp(self):

        (self.user1, self.user2, self.user3, self.user4) = create_users()

        self.serializer_data = {
            'organiser': self.user1.username,
            'event_name': 'test',
            'location': 'test',
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': [self.user2.username, self.user4.username, self.user4.username],
            'attending': [self.user2.username, self.user4.username]
        }

    def test_serializer_valid(self):

        serializer = serializers.EventSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_null_organiser(self):

        new_serializer_data = self.serializer_data
        new_serializer_data['organiser'] = None
        serializer = serializers.EventSerializer(data=new_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['organiser']))

    def test_serializer_null_event_name(self):
        new_serializer_data = self.serializer_data
        new_serializer_data['event_name'] = None
        serializer = serializers.EventSerializer(data=new_serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['event_name']))

    def test_serializer_null_location(self):
        new_serializer_data = self.serializer_data
        new_serializer_data['location'] = None
        serializer = serializers.EventSerializer(data=new_serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['location']))

    def test_serializer_null_start_time(self):
        new_serializer_data = self.serializer_data
        new_serializer_data['start_time'] = None
        serializer = serializers.EventSerializer(data=new_serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['start_time']))

    def test_serializer_null_finish_time(self):
        new_serializer_data = self.serializer_data
        new_serializer_data['finish_time'] = None
        serializer = serializers.EventSerializer(data=new_serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['finish_time']))

    def test_serializer_null_sign_in_time(self):
        new_serializer_data = self.serializer_data
        new_serializer_data['sign_in_time'] = None
        serializer = serializers.EventSerializer(data=new_serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['sign_in_time']))

    def test_serializer_null_attendees(self):

        new_serializer_data = self.serializer_data
        new_serializer_data['attendees'] = None
        serializer = serializers.EventSerializer(data=new_serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['attendees']))
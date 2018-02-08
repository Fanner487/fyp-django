# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from api.models import Event, Attempt
from django.contrib.auth.models import User
from api import serializers
import datetime

"""
Tests all parameters and fields of AttemptSerializer
"""


def create_event():
    return Event.objects.create(
        organiser="user1",
        event_name="test",
        location="test",
        start_time='2001-01-29T12:00:00+00:00',
        finish_time='2050-01-29T12:30:00+00:00',
        sign_in_time='2001-01-29T12:00:00+00:00',
        attendees=['user2', 'user3', 'user4']
    )


def create_users():
    return User.objects.create_user("user1", "test@gmail.com", "mypassword"), \
           User.objects.create_user("user2", "test@gmail.com", "mypassword"), \
           User.objects.create_user("user3", "test@gmail.com", "mypassword"), \
           User.objects.create_user("user4", "test@gmail.com", "mypassword")


class AttemptSerializerTestCase(TestCase):
    # Does not test the verify scan. Tests for that are down below

    # Check if user set created

    def setUp(self):
        (self.user1, self.user2, self.user3, self.user4) = create_users()

        self.event_serializer_data = {
            'organiser': self.user1.username,
            'event_name': 'test',
            'location': 'test',
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': [self.user2.username, self.user4.username, self.user4.username]
        }

        self.event = create_event()

        self.attempt_serializer_data = {
            'username': self.user2.username,
            'event_id': self.event.id,
            'time_on_screen': '12:30:00',
            'date_on_screen': '2050-01-29'
        }

    def test_serializer_valid(self):
        serializer = serializers.AttemptSerializer(data=self.attempt_serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_null_username(self):
        new_serializer_data = self.attempt_serializer_data
        new_serializer_data['username'] = None
        serializer = serializers.AttemptSerializer(data=new_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['username']))

    def test_serializer_null_event_id(self):
        new_serializer_data = self.attempt_serializer_data
        new_serializer_data['event_id'] = None
        serializer = serializers.AttemptSerializer(data=new_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['event_id']))

    def test_serializer_null_time_on_screen(self):
        new_serializer_data = self.attempt_serializer_data
        new_serializer_data['time_on_screen'] = None
        serializer = serializers.AttemptSerializer(data=new_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['time_on_screen']))

    def test_serializer_null_date_on_screen(self):
        new_serializer_data = self.attempt_serializer_data
        new_serializer_data['date_on_screen'] = None
        serializer = serializers.AttemptSerializer(data=new_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['date_on_screen']))

    def test_serializer_multiple_fields_null(self):
        new_serializer_data = self.attempt_serializer_data
        new_serializer_data['date_on_screen'] = None
        new_serializer_data['username'] = None
        serializer = serializers.AttemptSerializer(data=new_serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), set(['date_on_screen', 'username']))

    def test_serializer_created_auto_set_in_serializer(self):
        new_serializer_data = self.attempt_serializer_data
        new_created = datetime.datetime.now()
        serializer = serializers.AttemptSerializer(data=new_serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertNotEquals(new_created, serializer.validated_data.get('created'))


# TODO: not reading the right data from the database. This test is unusable. API test already tests this
# class VerifyScanExistsTestCase(TestCase):
#
#     def setUp(self):
#         (self.user1, self.user2, self.user3, self.user4) = create_users()
#         self.event = create_event()
#
#     def test_add_to_attending(self):
#
#         attempt1_data = {
#             'username': self.user2.username,
#             'event_id': self.event.id,
#             'time_on_screen': datetime.datetime.now().strftime("%H:%M:%S"),
#             'date_on_screen': datetime.datetime.now().strftime("%Y-%m-%d")
#         }
#
#         attempt1_serializer = serializers.AttemptSerializer(data=attempt1_data)
#
#         sleep(1)
#         attempt2_data = {
#             'username': self.user2.username,
#             'event_id': self.event.id,
#             'time_on_screen': datetime.datetime.now().strftime("%H:%M:%S"),
#             'date_on_screen': datetime.datetime.now().strftime("%Y-%m-%d")
#         }
#
#         attempt2_serializer = serializers.AttemptSerializer(data=attempt2_data)
#
#         attempt1_serializer.is_valid()
#         attempt2_serializer.is_valid()
#
#         attempt1_serializer.save()
#         attempt2_serializer.save()
#
#         attempt1_object = Attempt.objects.filter(username=attempt1_serializer.validated_data.get('username'))\
#             .filter(event_id=attempt1_serializer.validated_data.get('event_id'))\
#             .filter(created=attempt1_serializer.validated_data.get('created'))
#
#         attempt2_object = Attempt.objects.filter(username=attempt2_serializer.validated_data.get('username')) \
#             .filter(event_id=attempt2_serializer.validated_data.get('event_id')) \
#             .filter(created=attempt2_serializer.validated_data.get('created'))
#
#         print(self.event.attending)
#
#         for attempt in attempt1_object:
#             print("----\n\n")
#             print(attempt.id)
#             print(attempt.username)
#             print(attempt.event_id)
#             print(attempt.created)
#             print(attempt.time_on_screen)
#             print(attempt.date_on_screen)
#
#         for attempt in attempt2_object:
#             print("----\n\n")
#             print(attempt.id)
#             print(attempt.username)
#             print(attempt.event_id)
#             print(attempt.created)
#             print(attempt.time_on_screen)
#             print(attempt.date_on_screen)
#
#         print("----\n\n")
#
#         appended_event = Event.objects.get(id=attempt2_serializer.validated_data.get('event_id'))
#
#         print(appended_event.id)
#         print(appended_event.organiser)
#         print(appended_event.attendees)
#         print(appended_event.attending)
#
#         # print(attempt1_object.id)
#         # print(attempt1_object.username)
#         # print(attempt1_object.created)
#         # print(attempt1_object.time_on_screen)
#         # print(attempt1_object.date_on_screen)
#
#         # serializer
#         # serializer = serializers.AttemptSerializer(data=self.attempt_serializer_data)


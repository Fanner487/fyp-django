# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Event, Attempt
from django.contrib.auth.models import User
from api import serializers
import datetime


def create_event():
    return Event.objects.create(
        organiser="user1",
        event_name="test",
        location="test",
        start_time='2050-01-29T12:00:00+00:00',
        finish_time='2050-01-29T12:30:00+00:00',
        sign_in_time='2050-01-29T12:00:00+00:00',
        attendees=['user2', 'user3', 'user4']
    )


def create_users():
    return User.objects.create_user("user1", "test@gmail.com", "mypassword"), \
           User.objects.create_user("user2", "test@gmail.com", "mypassword"), \
           User.objects.create_user("user3", "test@gmail.com", "mypassword"), \
           User.objects.create_user("user4", "test@gmail.com", "mypassword")


# def create_attempt():


class AttemptSerializerTestCase(TestCase):
    # Does not test the verify scan. Tests for that are down below

    # username = models.CharField("username", max_length=50)
    # event_id = models.IntegerField("event_id")
    # created = models.DateTimeField(null=True, blank=True)
    # time_on_screen = models.TimeField()
    # date_on_screen = models.DateField()

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
        new_serializer_data['created'] = new_created
        serializer = serializers.AttemptSerializer(data=new_serializer_data)

        self.assertTrue(serializer.is_valid())
        print(serializer.validated_data.get('id'))
        self.assertNotEquals(new_created, serializer.validated_data.get('created'))

#
# class VerifyScanExistsTestCase(TestCase):
#
#     def setUp(self):
#
#         self.event = create_event()
#
#     def test_add_to_attending(self):
#
#         # serializer
#         # serializer = serializers.AttemptSerializer(data=self.attempt_serializer_data)
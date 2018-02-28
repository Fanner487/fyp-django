# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from api.models import Event
from django.contrib.auth.models import User
from api import serializers


"""
Tests all parameters and fields of ManualSignInSerializer
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


class ManualSignInSerializerTestCase(TestCase):

    def setUp(self):

        (self.user1, self.user2, self.user3, self.user4) = create_users()

        self.event = Event.objects.create(
            organiser=self.user1.username,
            event_name="test",
            location="test",
            start_time='2050-01-29T12:00:00',
            finish_time='2050-01-29T12:30:00',
            sign_in_time='2050-01-29T12:00:00',
            attendees=[self.user2.username, self.user3.username, self.user4.username]
        )

        self.serializer_data = {
            'event_id': self.event.id,
            'user': self.user2.username
        }

    def test_manual_sign_in_success(self):
        serializer = serializers.ManualSignInSerializer(data=self.serializer_data)
        serializer.is_valid()
        print(serializer.errors)
        self.assertTrue(serializer.is_valid())

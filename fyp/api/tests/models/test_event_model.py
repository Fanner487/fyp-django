# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from pprint import pprint
from api.models import Event


class EventModelTestCase(TestCase):

    def test_event_create(self):
        event = Event.objects.create(
            organiser="user1",
            event_name="test",
            location="test",
            start_time='2050-01-29T12:00:00',
            finish_time='2050-01-29T12:30:00',
            sign_in_time='2050-01-29T12:00:00',
            attendees=['user2', 'user3', 'user4']
        )

        self.assertEqual(event.organiser, "user1")
        self.assertEqual(event.event_name, "test")
        self.assertEqual(event.location, "test")
        self.assertEqual(event.start_time, '2050-01-29T12:00:00')
        self.assertEqual(event.finish_time, '2050-01-29T12:30:00')
        self.assertEqual(event.sign_in_time, '2050-01-29T12:00:00')
        self.assertEqual(event.attendees, ['user2', 'user3', 'user4'])
        self.assertIsNone(event.attending)
        self.assertEqual(event.attendance_required, False)

    def test_event_create_wrong_values_compare(self):

        event = Event.objects.create(
            organiser="user1",
            event_name="test",
            location="test",
            start_time='2050-01-29T12:00:00',
            finish_time='2050-01-29T12:30:00',
            sign_in_time='2050-01-29T12:00:00',
            attendees=['user2', 'user3', 'user4']
        )

        self.assertNotEqual(event.organiser, "user1NOT")
        self.assertNotEqual(event.event_name, "testNOT")
        self.assertNotEqual(event.location, "testNOT")
        self.assertNotEqual(event.start_time, '2060-01-29T12:00:00')
        self.assertNotEqual(event.finish_time, '2060-01-29T12:30:00')
        self.assertNotEqual(event.sign_in_time, '2060-01-29T12:00:00')
        self.assertNotEqual(event.attendees, ['user2', 'user3'])
        # self.assertIsNone(event.attending)
        self.assertNotEqual(event.attendance_required, True)

    def test_event_create_user_update(self):
        event = Event.objects.create(
            organiser="user1",
            event_name="test",
            location="test",
            start_time='2050-01-29T12:00:00',
            finish_time='2050-01-29T12:30:00',
            sign_in_time='2050-01-29T12:00:00',
            attendees=['user2', 'user3', 'user4']
        )

        self.assertEqual(event.organiser, "user1")
        self.assertEqual(event.event_name, "test")
        self.assertEqual(event.location, "test")
        self.assertEqual(event.start_time, '2050-01-29T12:00:00')
        self.assertEqual(event.finish_time, '2050-01-29T12:30:00')
        self.assertEqual(event.sign_in_time, '2050-01-29T12:00:00')
        self.assertEqual(event.attendees, ['user2', 'user3', 'user4'])
        self.assertIsNone(event.attending)
        self.assertEqual(event.attendance_required, False)

        event.location = "new_location"
        event.save()

        updated_event = User.objects.get(id=event.id)
        self.assertEqual(updated_event.location, "new_location")
    #
    # def test_event_create_user_destroy(self):
    #     user = User.objects.create_user(username="testuser3", email="test3@example.com", password="mypassword",
    #                                     first_name="Test", last_name="User")
    #
    #     self.assertEqual(user.username, "testuser3")
    #     self.assertEqual(user.email, "test3@example.com")
    #     self.assertEqual(user.first_name, "Test")
    #     self.assertEqual(user.last_name, "User")
    #
    #     user_id = user.id
    #
    #     deleted_user = User.objects.get(pk=user_id).delete()
    #     pprint(deleted_user)
    #
    #     # Asserts how many users deleted
    #     self.assertEqual(deleted_user[0], 1)

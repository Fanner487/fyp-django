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
        self.assertEqual(event.attendance_required, False)
    #
    # def test_event_create_wrong_values_compare(self):
    #     user = User.objects.create_user(username="testuser1", email="test1@example.com", password="mypassword",
    #                                     first_name="Test", last_name="User")
    #
    #     self.assertNotEqual(user.username, "NOTtestuser")
    #     self.assertNotEqual(user.email, "testNOT@example.com")
    #     self.assertNotEqual(user.first_name, "NOTTest")
    #     self.assertNotEqual(user.last_name, "NOtUser")
    #
    # def test_event_create_user_update(self):
    #     user = User.objects.create_user(username="testuser2", email="test2@example.com", password="mypassword",
    #                                     first_name="Test", last_name="User")
    #
    #     self.assertEqual(user.username, "testuser2")
    #     self.assertEqual(user.email, "test2@example.com")
    #     self.assertEqual(user.first_name, "Test")
    #     self.assertEqual(user.last_name, "User")
    #
    #     user.username = "newtestuser2"
    #     user.save()
    #
    #     updated_user = User.objects.get(id=user.id)
    #     self.assertEqual(updated_user.username, "newtestuser2")
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

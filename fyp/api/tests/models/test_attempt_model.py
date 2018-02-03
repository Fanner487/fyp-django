# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pprint import pprint
from api.models import Attempt
from django.utils import timezone


class AttemptModelTestCase(TestCase):
    def test_attempt_create(self):
        attempt = Attempt.objects.create(
            username="user1",
            event_id=1,
            time_on_screen=timezone.now().strftime("%H:%M:%S"),
            date_on_screen=timezone.now().strftime("%Y-%m-%d")
        )

        self.assertEqual(attempt.username, "user1")
        self.assertEqual(attempt.event_id, 1)
        self.assertGreaterEqual(timezone.now().strftime("%Y-%m-%d"), attempt.date_on_screen)
        self.assertGreaterEqual(timezone.now().strftime("%H:%M:%S"), attempt.time_on_screen)
    #
    # def test_attempt_create_wrong_values_compare(self):
    #     attempt = Attempt.objects.create(
    #         organiser="user1",
    #         attempt_name="test",
    #         location="test",
    #         start_time='2050-01-29T12:00:00',
    #         finish_time='2050-01-29T12:30:00',
    #         sign_in_time='2050-01-29T12:00:00',
    #         attendees=['user2', 'user3', 'user4']
    #     )
    #
    #     self.assertNotEqual(attempt.organiser, "user1NOT")
    #     self.assertNotEqual(attempt.attempt_name, "testNOT")
    #     self.assertNotEqual(attempt.location, "testNOT")
    #     self.assertNotEqual(attempt.start_time, '2060-01-29T12:00:00')
    #     self.assertNotEqual(attempt.finish_time, '2060-01-29T12:30:00')
    #     self.assertNotEqual(attempt.sign_in_time, '2060-01-29T12:00:00')
    #     self.assertNotEqual(attempt.attendees, ['user2', 'user3'])
    #     # self.assertIsNone(attempt.attending)
    #     self.assertNotEqual(attempt.attendance_required, True)
    #
    # def test_attempt_create_user_update(self):
    #     attempt = Attempt.objects.create(
    #         organiser="user1",
    #         attempt_name="test",
    #         location="test",
    #         start_time='2050-01-29T12:00:00',
    #         finish_time='2050-01-29T12:30:00',
    #         sign_in_time='2050-01-29T12:00:00',
    #         attendees=['user2', 'user3', 'user4']
    #     )
    #
    #     self.assertEqual(attempt.organiser, "user1")
    #     self.assertEqual(attempt.attempt_name, "test")
    #     self.assertEqual(attempt.location, "test")
    #     self.assertEqual(attempt.start_time, '2050-01-29T12:00:00')
    #     self.assertEqual(attempt.finish_time, '2050-01-29T12:30:00')
    #     self.assertEqual(attempt.sign_in_time, '2050-01-29T12:00:00')
    #     self.assertEqual(attempt.attendees, ['user2', 'user3', 'user4'])
    #     self.assertIsNone(attempt.attending)
    #     self.assertEqual(attempt.attendance_required, False)
    #
    #     attempt.location = "new_location"
    #     attempt.save()
    #
    #     updated_attempt = Attempt.objects.get(id=attempt.id)
    #     self.assertEqual(updated_attempt.location, "new_location")
    #
    # def test_attempt_destroy(self):
    #     attempt = Attempt.objects.create(
    #         organiser="user1",
    #         attempt_name="test",
    #         location="test",
    #         start_time='2050-01-29T12:00:00',
    #         finish_time='2050-01-29T12:30:00',
    #         sign_in_time='2050-01-29T12:00:00',
    #         attendees=['user2', 'user3', 'user4']
    #     )
    #
    #     self.assertEqual(attempt.organiser, "user1")
    #     self.assertEqual(attempt.attempt_name, "test")
    #     self.assertEqual(attempt.location, "test")
    #     self.assertEqual(attempt.start_time, '2050-01-29T12:00:00')
    #     self.assertEqual(attempt.finish_time, '2050-01-29T12:30:00')
    #     self.assertEqual(attempt.sign_in_time, '2050-01-29T12:00:00')
    #     self.assertEqual(attempt.attendees, ['user2', 'user3', 'user4'])
    #     self.assertIsNone(attempt.attending)
    #     self.assertEqual(attempt.attendance_required, False)
    #
    #     attempt_id = attempt.id
    #
    #     deleted_attempt = Attempt.objects.get(id=attempt_id).delete()
    #     pprint(deleted_attempt)
    #
    #     # Asserts how many users deleted
    #     self.assertEqual(deleted_attempt[0], 1)

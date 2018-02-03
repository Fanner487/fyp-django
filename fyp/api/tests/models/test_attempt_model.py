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

    def test_attempt_create_wrong_values_compare(self):
        attempt = Attempt.objects.create(
            username="user1",
            event_id=1,
            time_on_screen=timezone.now().strftime("%H:%M:%S"),
            date_on_screen=timezone.now().strftime("%Y-%m-%d")
        )

        self.assertNotEqual(attempt.username, "user1NOT")
        self.assertNotEqual(attempt.event_id, 9999999)
        self.assertGreaterEqual(timezone.now().strftime("%Y-%m-%d"), attempt.date_on_screen)
        self.assertGreaterEqual(timezone.now().strftime("%H:%M:%S"), attempt.time_on_screen)

    def test_attempt_create_user_update(self):
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

        attempt.username = "new_user"
        attempt.save()

        updated_attempt = Attempt.objects.get(id=attempt.id)
        self.assertEqual(updated_attempt.username, "new_user")

    def test_attempt_destroy(self):
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

        attempt_id = attempt.id

        deleted_attempt = Attempt.objects.get(id=attempt_id).delete()
        pprint(deleted_attempt)

        # Asserts how many users deleted
        self.assertEqual(deleted_attempt[0], 1)

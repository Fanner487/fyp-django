# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pprint import pprint
from api.models import Event


class EventModelTestCase(TestCase):
    """
    Tests Event model for creation, comparison, update and delete
    """

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

        updated_event = Event.objects.get(id=event.id)
        self.assertEqual(updated_event.location, "new_location")

    def test_event_destroy(self):
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

        event_id = event.id

        deleted_event = Event.objects.get(id=event_id).delete()
        pprint(deleted_event)

        # Asserts how many users deleted
        self.assertEqual(deleted_event[0], 1)

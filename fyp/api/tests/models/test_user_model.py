# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User


class UserModelTestCase(TestCase):

    def test_user_create(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="mypassword",
                                        first_name="Test", last_name="User")

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

    def test_user_create_wrong_values(self):
        user = User.objects.create_user(username="testuser1", email="test1@example.com", password="mypassword",
                                        first_name="Test", last_name="User")

        self.assertNotEqual(user.username, "NOTtestuser")
        self.assertNotEqual(user.email, "testNOT@example.com")
        self.assertNotEqual(user.first_name, "NOTTest")
        self.assertNotEqual(user.last_name, "NOtUser")

    def test_user_create_user_update(self):
        user = User.objects.create_user(username="testtuser2", email="test2@example.com", password="mypassword",
                                        first_name="Test", last_name="User")

        self.assertEqual(user.username, "testuser2")

        user.username = "newtestuser2"
        user.save()

        updated_user = User.objects.get(id=user.id)
        self.assertEqual(updated_user, "newtestuser2")
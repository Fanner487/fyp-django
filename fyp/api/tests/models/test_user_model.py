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
        
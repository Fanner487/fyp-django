# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from api import serializers


class LoginSerializerTest(TestCase):
    """
    Tests all parameters of LoginSerializer
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="mypassword",
                                             first_name="Test", last_name="User")

    def test_register_success(self):

        data = {
            'username': 'testuser1',
            'email': "test1@example.com",
            'password': 'mypassword',
            'password_confirm': 'mypassword',
            'first_name': "Test",
            'last_name': "User"
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_register_existing_username(self):
        data = {
            'username': 'testuser',
            'email': "test2@example.com",
            'password': 'mypassword',
            'password_confirm': 'mypassword',
            'first_name': "Test",
            'last_name': "User"
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_register_existing_email(self):
        data = {
            'username': 'testuser3',
            'email': "test@example.com",
            'password': 'mypassword',
            'password_confirm': 'mypassword',
            'first_name': "Test",
            'last_name': "User"
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_register_null_username(self):

        data = {
            'email': "test4@example.com",
            'password': 'mypassword',
            'password_confirm': 'mypassword',
            'first_name': "Test",
            'last_name': "User"
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors['username']), 1)

    def test_register_null_email(self):

        data = {
            'username': 'testuser5',
            'password': 'mypassword',
            'password_confirm': 'mypassword',
            'first_name': "Test",
            'last_name': "User"
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors['email']), 1)

    def test_register_null_password(self):

        data = {
            'username': 'testuser6',
            'email': "test6@example.com",
            'password_confirm': 'mypassword',
            'first_name': "Test",
            'last_name': "User"
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors['password']), 1)

    def test_register_null_confirm_password(self):

        data = {
            'username': 'testuser7',
            'email': "test7@example.com",
            'password': 'mypassword',
            'first_name': "Test",
            'last_name': "User"
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors['password_confirm']), 1)

    def test_register_null_first_name(self):

        data = {
            'username': 'testuser8',
            'email': "test8@example.com",
            'password': 'mypassword',
            'password_confirm': 'mypassword',
            'last_name': "User"
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors['first_name']), 1)

    def test_register_null_last_name(self):

        data = {
            'username': 'testuser9',
            'email': "test9@example.com",
            'password': 'mypassword',
            'password_confirm': 'mypassword',
            'first_name': "Test",
        }

        serializer = serializers.RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors['last_name']), 1)

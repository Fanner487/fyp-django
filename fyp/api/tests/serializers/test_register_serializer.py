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

        serializer = serializers.LoginSerializer(data=data)
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

    # def test_login_null_username(self):
    #     data = {
    #         'password': 'mypassword'
    #     }
    #
    #     serializer = serializers.RegisterSerializer(data=data)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertEqual(len(serializer.errors['username']), 1)
    #
    # def test_login_null_password(self):
    #     data = {
    #         'username': 'testuser'
    #     }
    #
    #     serializer = serializers.LoginSerializer(data=data)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertEqual(len(serializer.errors['password']), 1)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from api import serializers


class LoginSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="mypassword")

    def test_login_success(self):

        data = {
            'username': 'testuser',
            'password': 'mypassword'
        }

        serializer = serializers.LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_login_wrong_username(self):
        data = {
            'username': 'NOTtestuser',
            'password': 'mypassword'
        }

        serializer = serializers.LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_login_wrong_password(self):
        data = {
            'username': 'testuser',
            'password': 'NOTmypassword'
        }

        serializer = serializers.LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_login_null_username(self):
        data = {
            'password': 'mypassword'
        }

        serializer = serializers.LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        print(serializer.errors)

    def test_login_null_password(self):
        data = {
            'username': 'testuser'
        }

        serializer = serializers.LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

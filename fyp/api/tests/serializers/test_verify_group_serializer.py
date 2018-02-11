# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from api import serializers


class VerifyGroupSerializerTest(TestCase):

    """
        Tests all parameters of LoginSerializer
        """
    def setUp(self):
        User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

        User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        User.objects.create_user(
            username='testuser3',
            email='testuser3@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        User.objects.create_user(
            username='testuser4',
            email='testuser4@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

    def test_verify_group_success(self):

        data = {
            'usernames': ['testuser1', 'testuser2', 'testuser3', 'testuser4']
        }

        serializer = serializers.VerifyGroupSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_verify_group_non_existing_username(self):
        data = {
            'usernames': ['testuser1', 'testuser2', 'testuser3', 'NOT A USER']
        }

        serializer = serializers.VerifyGroupSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_verify_group_list_none(self):
        data = None
        serializer = serializers.VerifyGroupSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_verify_group_list_empty(self):
        data = []
        serializer = serializers.VerifyGroupSerializer(data=data)
        self.assertFalse(serializer.is_valid())

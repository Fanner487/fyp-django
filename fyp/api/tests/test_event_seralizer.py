# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status
from api.models import Event
import ...api.serializers


class UserIsAttendeeTestCase(TestCase):

    def test_something(self):

        result = serializers.event_exists(1)

        assertFalse(result)

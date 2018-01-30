# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status

# Create your tests here.
# User login test
class ExampleTestCase(TestCase):

    def test_something(self):

        
        self.assertEqual(1, 2)

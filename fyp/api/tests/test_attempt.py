# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status

import datetime
from time import sleep

# Create your tests here.
# User login test
class AttemptTestCase(TestCase):

    def create_user(self, username, email, password):
        user = User.objects.create_user(username, email, password)
        user.save()

    def create_event(self, data):
        return self.client.post("/api/events/", data=data, format='json')

    def create_attempt(self, data):
        return self.client.post("/api/attempts/", data=data, format='json')

    def setUp(self):
        client = APIClient()

        self.create_user("user1" , "test1@gmail.com", "orangemonkeyeagle1")
        self.create_user("user2" , "test2@gmail.com", "orangemonkeyeagle1")
        self.create_user("user3" , "test3@gmail.com", "orangemonkeyeagle1")
        self.create_user("user4" , "test4@gmail.com", "orangemonkeyeagle1")

    def create_test_attempt_now(self, username, event_id):
        time_on_screen = (datetime.datetime.now() - datetime.timedelta(seconds=3)).strftime("%H:%M:%S")
        date_on_screen = datetime.datetime.now().strftime("%Y-%m-%d")

        data = {
            'username' : username,
            'event_id' : event_id,
            'time_on_screen' : time_on_screen,
            'date_on_screen' : date_on_screen,
        }

        return self.create_attempt(data)


    def create_test_event_now(self):

        event_start_time = datetime.datetime.now() + datetime.timedelta(seconds=2)
        event_sign_in_time = event_start_time
        event_finish_time = datetime.datetime(
        	year=event_start_time.year,
        	month=event_start_time.month,
        	day=event_start_time.day,
        	hour=23,
        	minute=59,
        	second=59)

        print("Now: " + str(datetime.datetime.now()))
        print("Start: " + str(event_start_time))
        print("Sign in: " + str(event_sign_in_time))
        print("Finish: " + str(event_finish_time))
        print("\n\n")

        data = {
            'organiser' :"user1",
            'event_name' : "test1",
            'location' : "nowhere",
            'start_time' : event_start_time,
            'finish_time' : event_finish_time,
            'sign_in_time' : event_sign_in_time,
            'attendees' : ['user2', 'user3', 'user4']
        }

        return self.create_event(data)


    def test_attempt_success(self):

        event_response = self.create_test_event_now()
        self.assertEquals(event_response.status_code, status.HTTP_201_CREATED)

        event_id = event_response.json().get('id')

        sleep(6)

        response = create_test_event_now()
        print(response.json())

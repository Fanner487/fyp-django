 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Event
import json
import datetime
from time import sleep


# Create your tests here.
class AttemptTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.create_user("user1", "test1@gmail.com", "orangemonkeyeagle1")
        self.create_user("user2", "test2@gmail.com", "orangemonkeyeagle1")
        self.create_user("user3", "test3@gmail.com", "orangemonkeyeagle1")
        self.create_user("user4", "test4@gmail.com", "orangemonkeyeagle1")

    def create_user(self, username, email, password):
        user = User.objects.create_user(username, email, password)

    def create_event(self, data):
        return self.client.post("/api/events/", data=data, format='json')

    def create_attempt(self, data):
        return self.client.post("/api/attempts/", data=data, format='json')

    def create_test_attempt_now(self, username, event_id):
        time_on_screen = (datetime.datetime.now() - datetime.timedelta(seconds=1)).strftime("%H:%M:%S")
        date_on_screen = datetime.datetime.now().strftime("%Y-%m-%d")

        data = {
            'username': username,
            'event_id': event_id,
            'time_on_screen': time_on_screen,
            'date_on_screen': date_on_screen,
        }

        return self.create_attempt(data)

    def create_test_event_now(self):
        event_start_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
        # event_start_time = datetime.datetime.now()
        event_sign_in_time = datetime.datetime.now()
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
            'organiser': "user1",
            'event_name': "test1",
            'location': "nowhere",
            'start_time': event_start_time,
            'finish_time': event_finish_time,
            'sign_in_time': event_sign_in_time,
            'attendees': ['user2', 'user3', 'user4']
        }

        return self.create_event(data)

    def test_attempt_success(self):
        event_response = self.create_test_event_now()
        self.assertEquals(event_response.status_code, status.HTTP_201_CREATED)

        event_id = event_response.json().get('id')

        sleep(2)

        response1 = self.create_test_attempt_now("user2", event_id)
        print(response1.status_code)
        print(response1.json())

        sleep(1)

        response2 = self.create_test_attempt_now("user2", event_id)
        print(response1.status_code)
        print(response1.json())

        self.assertEquals(response1.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response2.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=event_id)
        # self.assertIsNone(event.attending)
        self.assertTrue("user2" in event.attending)

    def test_attempt_out_of_time_delta_screen(self):
        event_response = self.create_test_event_now()
        self.assertEquals(event_response.status_code, status.HTTP_201_CREATED)

        event_id = event_response.json().get('id')

        sleep(2)

        response1 = self.create_test_attempt_now("user2", event_id)
        print(response1.status_code)
        print(response1.json())

        sleep(10)

        response2 = self.create_test_attempt_now("user2", event_id)
        print(response1.status_code)
        print(response1.json())

        self.assertEquals(response1.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response2.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=event_id)
        # self.assertIsNone(event.attending)
        self.assertTrue("user2" not in event.attending)


class AttemptUpdateDeleteTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.create_user("user1", "test1@gmail.com", "orangemonkeyeagle1")
        self.create_user("user2", "test2@gmail.com", "orangemonkeyeagle1")
        self.create_user("user3", "test3@gmail.com", "orangemonkeyeagle1")
        self.create_user("user4", "test4@gmail.com", "orangemonkeyeagle1")

    def create_user(self, username, email, password):
        User.objects.create_user(username, email, password)

    def create_event(self, data):
        return self.client.post("/api/events/", data=data, format='json')

    def create_attempt(self, data):
        return self.client.post("/api/attempts/", data=data, format='json')

    def create_test_attempt_now(self, username, event_id):
        time_on_screen = (datetime.datetime.now() - datetime.timedelta(seconds=1)).strftime("%H:%M:%S")
        date_on_screen = datetime.datetime.now().strftime("%Y-%m-%d")

        data = {
            'username': username,
            'event_id': event_id,
            'time_on_screen': time_on_screen,
            'date_on_screen': date_on_screen,
        }

        return self.create_attempt(data)

    def create_test_event_now(self):
        event_start_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
        # event_start_time = datetime.datetime.now()
        event_sign_in_time = datetime.datetime.now()
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
            'organiser': "user1",
            'event_name': "test1",
            'location': "nowhere",
            'start_time': event_start_time,
            'finish_time': event_finish_time,
            'sign_in_time': event_sign_in_time,
            'attendees': ['user2', 'user3', 'user4']
        }

        return self.create_event(data)

    def test_attempt_update_rejection(self):
        event_response = self.create_test_event_now()
        self.assertEquals(event_response.status_code, status.HTTP_201_CREATED)

        event_id = event_response.json().get('id')

        sleep(2)

        response = self.create_test_attempt_now("user2", event_id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        time_on_screen = (datetime.datetime.now() - datetime.timedelta(seconds=1)).strftime("%H:%M:%S")
        date_on_screen = datetime.datetime.now().strftime("%Y-%m-%d")

        data = json.dumps({
            'username': 'user2',
            'event_id': event_id,
            'time_on_screen': time_on_screen,
            'date_on_screen': date_on_screen,
        })

        response_update = self.client.patch("/api/attempts/" + str(event_id) + "/", data=data,
                                            content_type='application/json')

        self.assertEqual(response_update.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_attempt_out_of_time_delta_screen(self):
    #     event_response = self.create_test_event_now()
    #     self.assertEquals(event_response.status_code, status.HTTP_201_CREATED)
    #
    #     event_id = event_response.json().get('id')
    #
    #     sleep(2)
    #
    #     response1 = self.create_test_attempt_now("user2", event_id)
    #     print(response1.status_code)
    #     print(response1.json())
    #
    #     sleep(10)
    #
    #     response2 = self.create_test_attempt_now("user2", event_id)
    #     print(response1.status_code)
    #     print(response1.json())
    #
    #     self.assertEquals(response1.status_code, status.HTTP_201_CREATED)
    #     self.assertEquals(response2.status_code, status.HTTP_201_CREATED)
    #
    #     event = Event.objects.get(id=event_id)
    #     # self.assertIsNone(event.attending)
    #     self.assertTrue("user2" not in event.attending)


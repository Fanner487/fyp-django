# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status

# Create your tests here.s
class EventTestCase(TestCase):

    def create_user(self, username, email, password):
        user = User.objects.create_user(username, email, password)
        user.save()

    def create_event(self, data):
        return self.client.post("/api/events/", data=data, format='json')

    def setUp(self):
        client = APIClient()

        self.create_user("user1" , "test1@gmail.com", "orangemonkeyeagle1")
        self.create_user("user2" , "test2@gmail.com", "orangemonkeyeagle1")
        self.create_user("user3" , "test3@gmail.com", "orangemonkeyeagle1")
        self.create_user("user4" , "test4@gmail.com", "orangemonkeyeagle1")


    # def test_event_create_success(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.json().get('organiser'), "user1")
    #     self.assertEqual(response.json().get('event_name'), "Test1")
    #     self.assertEqual(response.json().get('location'), "nowhere")
    #     self.assertEqual(response.json().get('start_time'), "2050-01-29T12:00:00Z")
    #     self.assertEqual(response.json().get('finish_time'), "2050-01-29T12:30:00Z")
    #     self.assertEqual(response.json().get('sign_in_time'), "2050-01-29T12:00:00Z")
    #     self.assertEqual(response.json().get('attendees'), ['user2', 'user3', 'user4'])
    #
    #
    # def test_event_create_organiser_fail(self):
    #
    #     data = {
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('organiser'), ['This field is required.'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_event_name_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('event_name'), ['This field is required.'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_location_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('location'), ['This field is required.'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_start_time_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('start_time'), ['This field is required.'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_finish_time_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('finish_time'), ['This field is required.'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_sign_in_time_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('sign_in_time'), ['This field is required.'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_attendees_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('non_field_errors'), ['Attendees cannot be null'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #
    # def test_event_create_organiser_exists_fail(self):
    #
    #     data = {
    #         'organiser' :"user1234",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('non_field_errors'), ['User does not exist'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_organiser_start_gt_finish_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:31:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:31:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('non_field_errors'), ['Invalid time entry'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_future_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2001-01-29T12:31:00',
    #         'finish_time' : '2001-01-29T12:59:00',
    #         'sign_in_time' : '2001-01-29T12:31:00',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('non_field_errors'), ['Time must be in future'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_sign_in_time_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:01',
    #         'attendees' : ['user2', 'user3', 'user4']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('non_field_errors'), ['Sign in time must be in before or equal start time'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #
    # def test_event_create_attendee_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('non_field_errors'), ['user does not exist'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_event_create_attending_fail(self):
    #
    #     data = {
    #         'organiser' :"user1",
    #         'event_name' : "Test1",
    #         'location' : "nowhere",
    #         'start_time' : '2050-01-29T12:00:00',
    #         'finish_time' : '2050-01-29T12:30:00',
    #         'sign_in_time' : '2050-01-29T12:00:00',
    #         'attendees' : ['user2', 'user3', 'user4'],
    #         'attending' : ['user2']
    #     }
    #
    #     response = self.create_event(data)
    #
    #     self.assertEqual(response.json().get('non_field_errors'), ['Attending must be empty'])
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_event_update(self):
        data = {
            'organiser' :"user1",
            'event_name' : "Test1",
            'location' : "nowhere",
            'start_time' : '2050-01-29T12:00:00',
            'finish_time' : '2050-01-29T12:30:00',
            'sign_in_time' : '2050-01-29T12:00:00',
            'attendees' : ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        data = {
            'organiser' :"user1",
            'event_name' : "update",
            'location' : "update",
            'start_time' : '2050-01-29T12:00:00',
            'finish_time' : '2050-01-29T12:30:00',
            'sign_in_time' : '2050-01-29T12:00:00',
            'attendees' : ['user2', 'user3']
        }

        # user 4
        event_id = response.get('id')
        update_response = self.client.patch("/api/events/" + str(event_id), data=data, format='json')

        print(update_response.status_code)
        print(update_response.json())

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Event
from rest_framework import status
import json


# Create your tests here.s


class EventTestCase(TestCase):

    def create_user(self, username, email, password):
        user = User.objects.create_user(username, email, password)
        user.save()

    def create_event(self, data):
        return self.client.post("/api/events/", data=data, format='json')

    def setUp(self):
        client = APIClient()

        self.create_user("user1", "test1@gmail.com", "orangemonkeyeagle1")
        self.create_user("user2", "test2@gmail.com", "orangemonkeyeagle1")
        self.create_user("user3", "test3@gmail.com", "orangemonkeyeagle1")
        self.create_user("user4", "test4@gmail.com", "orangemonkeyeagle1")

    def test_event_create_success(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('organiser'), "user1")
        self.assertEqual(response.json().get('event_name'), "Test1")
        self.assertEqual(response.json().get('location'), "nowhere")
        self.assertEqual(response.json().get('start_time'), "2050-01-29T12:00:00Z")
        self.assertEqual(response.json().get('finish_time'), "2050-01-29T12:30:00Z")
        self.assertEqual(response.json().get('sign_in_time'), "2050-01-29T12:00:00Z")
        self.assertEqual(response.json().get('attendees'), ['user2', 'user3', 'user4'])

    def test_event_create_organiser_fail(self):
        data = {
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('organiser'), ['This field is required.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_event_name_fail(self):
        data = {
            'organiser': "user1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('event_name'), ['This field is required.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_location_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('location'), ['This field is required.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_start_time_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('start_time'), ['This field is required.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_finish_time_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('finish_time'), ['This field is required.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_sign_in_time_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('sign_in_time'), ['This field is required.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_attendees_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('non_field_errors'), ['Attendees cannot be null'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_organiser_exists_fail(self):
        data = {
            'organiser': "user1234",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('non_field_errors'), ['User does not exist'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_organiser_start_gt_finish_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:31:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:31:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('non_field_errors'), ['Invalid time entry'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_future_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2001-01-29T12:31:00',
            'finish_time': '2001-01-29T12:59:00',
            'sign_in_time': '2001-01-29T12:31:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('non_field_errors'), ['Time must be in future'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_sign_in_time_required(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:01',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('non_field_errors'),
                         ['Sign in time must be in before or equal start time'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_attendee_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('non_field_errors'), ['user does not exist'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_create_attending_fail(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4'],
            'attending': ['user2']
        }

        response = self.create_event(data)

        self.assertEqual(response.json().get('non_field_errors'), ['Attending must be empty'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_update(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        data_update = json.dumps({
            'organiser': "user1",
            'event_name': "update",
            'location': "update",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3']
        })

        # user 4
        update_response = self.client.patch("/api/events/" + str(response.json().get('id')) + "/", data_update,
                                            content_type='application/json')
        self.assertEquals(update_response.status_code, status.HTTP_200_OK)
        self.assertEquals(update_response.json().get('event_name'), "update")
        self.assertEquals(update_response.json().get('location'), "update")
        self.assertEquals(update_response.json().get('attendees'), ['user2', 'user3'])

    def test_event_delete(self):
        data = {
            'organiser': "user1",
            'event_name': "Test1",
            'location': "nowhere",
            'start_time': '2050-01-29T12:00:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2050-01-29T12:00:00',
            'attendees': ['user2', 'user3', 'user4']
        }

        response = self.create_event(data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        delete_response = self.client.delete("/api/events/" + str(response.json().get('id')) + "/",
                                             content_type='application/json')

        get_response = self.client.delete("/api/events/" + str(response.json().get('id')) + "/",
                                          content_type='application/json')

        self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(get_response.status_code, status.HTTP_404_NOT_FOUND)


class EventUpdateTest(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = "/api/events/"

        self.test_event = Event.objects.create(
            organiser="user1",
            event_name="test",
            location="test",
            start_time='2001-01-29T12:00:00',
            finish_time='2050-01-29T12:30:00',
            sign_in_time='2001-01-29T12:00:00',
            attendees=['user2', 'user3', 'user4']
        )

    def test_event_update(self):

        new_data = json.dumps({
            'organiser': 'user1',
            'event_name': 'new_test',
            'location': 'new_test',
            'start_time': '2001-01-29T12:30:00',
            'finish_time': '2050-01-29T12:30:00',
            'sign_in_time': '2001-01-29T12:30:00',
            'attendees': ['user2', 'user3']
        })

        response = self.client.patch(self.url + str(self.test_event.id), data=new_data, content_type='application/json')
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('event_name'), 'new_test')
        self.assertEqual(response.json().get('location'), 'new_test')
        self.assertEqual(response.json().get('start_time'), '2001-01-29T12:30:00')
        self.assertEqual(response.json().get('finish_time'), '2050-01-29T12:30:00')
        self.assertEqual(response.json().get('sign_in_time'), '2001-01-29T12:30:00')
        self.assertEqual(response.json().get('attendees'), ['user2', 'user3'])

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import EventSerializer, AttemptSerializer, UserSerializer, LoginSerializer, RegisterSerializer, \
    VerifyGroupSerializer, EventUpdateSerializer, ManualSignInSerializer, ManualRemoveUserFromAttendingSerializer
from .models import Event, Attempt
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from pprint import pprint

"""
This is the API access points for users, events and attempts
"""


class EventViewSet(ModelViewSet):
    # authentication_classes = ()
    # permission_classes = ()
    """
    ModelViewSet for Event.
    GET, POST, PATCH operations and handling are generated from the parent class
    Only the serializer and relevant object class are needed
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def update(self, request, *args, **kwargs):
        """
        Update override of the ModelViewSet so EventUpdateSerializer
        can be used to validate data
        """
        print(request.data)

        partial = kwargs.pop('partial', False)

        instance = self.get_object()

        serializer = EventUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        print("Update serializer is valid, updating now")
        self.perform_update(serializer)

        return Response(serializer.data)


class AttemptViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    Generic for Attempt.
    Only list and create methods are permitted from the mixins in the declaration above
    It forbids end users to update, or delete attempts using the API (DELETE, PATCH)
    """

    authentication_classes = ()
    permission_classes = ()

    serializer_class = AttemptSerializer
    queryset = Attempt.objects.all()

    def create(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)

        # instance = self.get_object()
        serializer = AttemptSerializer(data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):

            verify_scan(serializer.validated_data)
            self.perform_create(serializer)

            print("Serializer valid. Verifying last scan now")

            return Response({"Success": "Attempt created"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"Error": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


# class UserViewSet(ModelViewSet):
#     """
#     ModelViewSet for User.
#     GET, POST, PATCH, DELETE operations and handling are generated from the parent class
#     Only the serializer and relevant object class are needed
#     """
#     authentication_classes = ()
#     permission_classes = ()
#
#     serializer_class = UserSerializer
#     queryset = User.objects.all()


@api_view(["POST"])
@authentication_classes(())
@permission_classes(())
def login(request):
    """
    Login API view.
    Returns appropriate authentication messages
    """

    serializer = LoginSerializer(data=request.data)

    # if not user:
    if not serializer.is_valid():
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:

        user = User.objects.get(username=serializer.validated_data.get('username'))
        print("USER")
        print(user)
        user_serializer = UserSerializer(user)
        # user_serializer.is_valid(raise_exception=True)
        print(user_serializer.data)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes((JSONWebTokenAuthentication,))
def manually_sign_in_user(request):

    serializer = ManualSignInSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    print("\n\nManual sign in validated")
    print(str(serializer.validated_data['event_id']))
    print(str(serializer.validated_data['user']))

    event = Event.objects.get(id=serializer.validated_data['event_id'])

    if event.attending is None:
        event.attending = []

    event.attending.append(serializer.validated_data['user'])
    event.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes((JSONWebTokenAuthentication,))
def remove_user_from_attending(request):

    serializer = ManualRemoveUserFromAttendingSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    event = Event.objects.get(id=serializer.validated_data['event_id'])

    if serializer.validated_data['user'] in event.attending:
        event.attending.remove(serializer.validated_data['user'])

    event.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_group(request):
    """
    Verifies that all users that are in a group are in the database
    """

    serializer = VerifyGroupSerializer(data=request.data)

    if serializer.is_valid():
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes(())
@permission_classes(())
def register(request):
    """
    Register API view.
    Returns appropriate validation messages from the serializer
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_events_for_user(request, username):
    """
    Gets all events for user
    """

    username = username.strip().lower()

    events_organised = Event.objects.filter(organiser__iexact=username) \
        .order_by('-start_time')

    events_attending = Event.objects.filter(attendees__icontains=username) \
        .order_by('-start_time')

    events_attending_filtered = []

    # "attendees__icontains" will do 'LIKE' searching, not exact for arrays. Is not suitable for arrays
    # QuerySet data needs to be accessed individually to filter out
    for event in events_attending:

        if username in event.attendees:
            events_attending_filtered.append(event)

    # Only returns distinct events. Filters out duplicates
    events_combined = set(list(events_organised) + events_attending_filtered)
    serialized = EventSerializer(events_combined, many=True)

    if serialized.data:
        return Response(serialized.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def verify_scan(data):
    """
    Algorithm
    1. Verify if current attempt is valid
        - valid in event
        - data scanned from camera is valid within timestamp and the information scanned on the screen of the phone
    2. Retrieve and verify the last attempt with the same username and event_id
        - validate attempt as per step 1
    3. If the two attempts or scans are within the time delta(5 seconds), the user is added to the event attending list
    """

    username = data.get('username')
    event_id = data.get('event_id')
    time_on_screen = data.get('time_on_screen')
    date_on_screen = data.get('date_on_screen')
    current_created = data.get('created')

    verified = True

    # Verifies current attempt
    if valid_attempt_in_event(username, event_id, time_on_screen, date_on_screen, current_created):

        print("Current attempt is valid")

        # Gets last attempt
        last_attempt = Attempt.objects.filter(username=username).filter(event_id=event_id).order_by("-created").first()

        if last_attempt:

            # Verifies second attempt for event
            if valid_attempt_in_event(last_attempt.username, last_attempt.event_id, last_attempt.time_on_screen,
                                      last_attempt.date_on_screen, last_attempt.created):

                print("Previous attempt valid")

                # Check if time within 5 seconds of last
                time_stamp_seconds_difference = (current_created - last_attempt.created).total_seconds()
                delta = 5

                current_time_on_screen = time_on_screen
                current_date_on_screen = date_on_screen

                current_time_on_screen = datetime.combine(current_date_on_screen, current_time_on_screen)
                last_attempt_screen_time_formatted = datetime.combine(last_attempt.date_on_screen,
                                                                      last_attempt.time_on_screen)

                screen_seconds_difference = (current_time_on_screen
                                             - last_attempt_screen_time_formatted).total_seconds()

                print("\n\nSCREEN TIME")
                print("screen: " + str(screen_seconds_difference))
                print("timestamp: " + str(time_stamp_seconds_difference))
                print("\n\n")

                # Makes sure that the current time after last attempt time and within delta
                if 0 < time_stamp_seconds_difference < delta:

                    if 1 <= screen_seconds_difference < delta:

                        add_to_attending(username, event_id)
                else:
                    verified = False
            else:

                print("Previous attempt not valid")
                verified = False
        else:

            print("No last attempt")
            verified = False

    else:

        print("Current attempt not valid")
        verified = False

    return verified


# Adds a user to the attending list of an event if they're not already in there
def add_to_attending(username, event_id):

    event = Event.objects.get(id=event_id)

    print("organiser: " + str(event.organiser))
    print("location: " + str(event.location))
    print("Username to append:" + username)
    print("Event_id to append: " + str(event_id))
    print("Attending: " + str(event.attendees))

    if username not in event.attending:

        print("Appending user")
        event.attending.append(username.strip().lower())
        event.save()

        return True
    else:

        print("Not Appending user")
        return False


def valid_attempt_in_event(username, event_id, time_on_screen, date_on_screen, timestamp):
    """
    Checks if time scanned on screen AND the creation time stamp is within the event sign_in_time an finish_time
    Verifies if the user is part of the event specified
    Checks if the creation timestamp and time/date scanned from the phone screen is within a certain delta
    """

    print("\n Validating attempt")

    event = Event.objects.get(id=event_id)

    # parsing date and time on screen into new datetime variable for comparison

    utc = pytz.UTC
    combined_time = datetime(year=date_on_screen.year, month=date_on_screen.month, day=date_on_screen.day,
                             hour=time_on_screen.hour, minute=time_on_screen.minute, second=time_on_screen.second)\
        .replace(tzinfo=utc)

    print("Combined time: " + str(combined_time))
    print("Event sign in: " + str(event.sign_in_time))
    print("Event finish: " + str(event.finish_time))

    verified = True

    # Checks combined times
    if event.sign_in_time <= combined_time <= event.finish_time:
        print("Within the time")
    else:
        verified = False

    print(event.sign_in_time)
    print(event.finish_time)
    print(timestamp)
    # Check through timestamp
    if event.sign_in_time <= timestamp <= event.finish_time:

        print("Within timezone")
    else:
        verified = False

    # Check screen time within timestamp delta
    time_difference = (timestamp - combined_time).total_seconds()
    print("Time difference: " + str(time_difference))

    if time_difference < 10:
        print("Screen time within delta")
    else:
        verified = False

    return verified

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import EventSerializer, AttemptSerializer, UserSerializer, LoginSerializer, RegisterSerializer, VerifyGroupSerializer
from .models import Event, Attempt
from rest_framework import mixins
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from pprint import pprint

"""
This is the API access points for users, events and attempts
"""


class EventViewSet(ModelViewSet):
    """
    ModelViewSet for Event.
    GET, POST, PATCH operations and handling are generated from the parent class
    Only the serializer and relevant object class are needed
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all()


class AttemptViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    Generic for Event.
    Only list and create methods are permitted from the mixins in the declaration above
    It forbids end users to update, or delete attempts using the API (DELETE, PATCH)
    """

    serializer_class = AttemptSerializer
    queryset = Attempt.objects.all()


class UserViewSet(ModelViewSet):
    """
    ModelViewSet for User.
    GET, POST, PATCH, DELETE operations and handling are generated from the parent class
    Only the serializer and relevant object class are needed
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(["POST"])
@authentication_classes(JSONWebTokenAuthentication)
def jwt_login(request):
    """
    Login API view.
    Returns appropriate authentication messages
    """

    return Response({"message": "something happened"}, status=status.HTTP_200_OK)

    # serializer = LoginSerializer(data=request.data)
    #
    # # if not user:
    # if not serializer.is_valid():
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    # else:
    #     return Response({"message": "Login successful"}, status=status.HTTP_200_OK)



@api_view(["POST"])
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
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


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
def delete_table(request, table):
    """
    Delete table API view.
    Deletes specified tables.
    This is scrictly for debugging purposes
    """

    if table == "event":
        Event.objects.all().delete()

    if table == "attempt":
        Attempt.objects.all().delete()

    if table == "all":
        Event.objects.all().delete()
        Attempt.objects.all().delete()

    return Response(status=status.HTTP_200_OK)


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
    # if events_combined:
    #
    #     serialized = EventSerializer(data=events_combined, many=True)
    #
    #     if serialized.is_valid():
    #         return Response(serialized.data)
    #     else:
    #         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_events(request, username, event_type, time):
    """
    Get events for user according to organising/attending, and time tense.
    """

    username = username.strip().lower()
    event_type = event_type.strip().lower()

    if event_type == "organising":

        organised_events = Event.objects.filter(organiser__iexact=username) \
            .order_by('-start_time')

        time_filtered_events = filter_events_by_time(organised_events, time)

        serialized = EventSerializer(time_filtered_events, many=True)

        return Response(serialized.data)

    elif event_type == "attending":

        attending_events = Event.objects.filter(attendees__icontains=username) \
            .order_by('-start_time')

        attending_events_filtered = []

        # filters for exact matches instead of (LIKE %username%) in contains
        # statement in query
        for event in attending_events:

            if username in event.attendees:
                attending_events_filtered.append(event)

        time_filtered_events = filter_events_by_time(attending_events_filtered, time)

        serialized = EventSerializer(time_filtered_events, many=True)

        return Response(serialized.data)

    else:

        return Response(status=status.HTTP_400_BAD_REQUEST)


def filter_events_by_time(events, event_time):
    """Filters events by all, past, ongoing or future."""

    utc = pytz.UTC  # using timezones for time checking
    time_now = datetime.now().replace(tzinfo=utc)

    filtered_set = []

    if event_time == "all":

        filtered_set = events

    elif event_time == "past":

        for event in events:

            if event.finish_time < time_now:
                filtered_set.append(event)

    elif event_time == "ongoing":

        for event in events:

            if event.start_time <= time_now <= event.finish_time:
                filtered_set.append(event)

    elif event_time == "upcoming":

        for event in events:

            if event.start_time > time_now:
                filtered_set.append(event)
    else:
        filtered_set = []

    return filtered_set


# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .serializers import EventSerializer, AttemptSerializer, UserSerializer
from .models import Event, Attempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from datetime import datetime
import pytz
# Create your views here.

class EventViewSet(ModelViewSet):
    """ModelViewSet for Event."""

    serializer_class = EventSerializer
    queryset = Event.objects.all()


class AttemptViewSet(ModelViewSet):
    """ModelViewSet for Attempt."""

    serializer_class = AttemptSerializer
    queryset = Attempt.objects.all()


class UserViewSet(ModelViewSet):
    """ModelViewSet for User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


def filter_events_by_time(events, event_time):
    """Filters events by all, past, ongoing or future."""
    utc = pytz.UTC  # using timezomes for time checking
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


@api_view(["GET"])
def get_events(request, username, event_type, time):
    """Get events for user according to organising, and time tense."""
    username = username.strip().lower()
    event_type = event_type.strip().lower()

    if event_type == "organising":

        organised_events = Event.objects.filter(organiser__iexact=username) \
            .order_by('-start_time')

        time_filtered_events = filter_events_by_time(organised_events, time)

        serialized = EventSerializer(time_filtered_events, many=True)

        return Response(serialized.data)

    elif event_type == "attending":

        attending_events = Event.objects.filter(attendees__icontains=username)\
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


@api_view(["POST"])
def login(request):
    """Login."""
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def register(request):
    """Register users with unique email and username."""
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    first_name = request.data.get("firstname")
    surname = request.data.get("surname")

    unique = verify_unique_username_email(username, email)

    print(unique)
    if unique:
        print("\n\nEmail is unique\n\n")

        print(username)
        print(password)
        print(email)
        print(first_name)
        print(surname)

        new_user = User.objects.create_user(username, email, password)

        new_user.is_active = True
        new_user.first_name = first_name
        new_user.last_name = surname
        new_user.save()

        return Response({"message": "Created account"}, status.HTTP_200_OK)
    else:
        return Response({"message": "Username or email already exists"}, status.HTTP_401_UNAUTHORIZED)


def verify_unique_username_email(username, email):
    """Verify users with unique email and username input."""
    usernames = User.objects.filter(username=username)
    emails = User.objects.filter(email=email)

    if not emails.exists() and not usernames.exists():
        return True
    else:
        return False
        # if emails.exists():
        #     return False
        #
        # elif usernames.exists():
        #     return False
        # else:
        #     return False, "null"


@api_view(["GET"])
def delete_table(request, table):

    if table == "event":

        Event.objects.all().delete()

    if table == "attempt":

        Attempt.objects.all().delete()

    if table == "all":

        Event.objects.all().delete()
        Attempt.objects.all().delete()

    return Response(status=status.HTTP_200_OK)

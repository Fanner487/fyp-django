from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Event, Attempt
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate
import pytz


"""
Serializers declared
Serializers are the middleware between models and the API views.
Data can be validated here before the object gets created in the DB
Data can be de/serialized to/from JSON into a format the ORM understands
"""


class LoginSerializer(serializers.Serializer):
    """
    Authenticates username and password against the DB
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):

        if not authenticate(username=data.get('username'), password=data.get('password')):
            raise serializers.ValidationError("Login denied")

        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for User registration. Verifies unique usernames, emails
    and validates other fields required for registration
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8)

    password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8)

    first_name = serializers.CharField(
        required=True)

    last_name = serializers.CharField(
        required=True)

    def create(self, validated_data):

        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name']
                                        )

        return user

    def validate(self, data):

        # Validates if user input the same password to be valid
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Incorrect passwords")

        return data

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     username
#     current_password
#     new_password


class VerifyGroupSerializer(serializers.Serializer):

    usernames = serializers.ListField(child=serializers.CharField())

    def validate(self, data):

        users = data.get('usernames')
        print("In validate")
        print(users)

        if users is not None or not users:

            for user in data.get('usernames'):
                print(user)
                if not user_exists(user):
                    print(user + " does not exist")
                    raise serializers.ValidationError(user + " does not exist")
                else:
                    print(user + "exists")
        else:
            raise serializers.ValidationError("Empty list")
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User display
    """

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ('password',)


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event CRUD operations.
    Verifies if users exists in attendees and organisers
    """

    def validate(self, data):

        utc = pytz.UTC  # using timezones for time checking

        username = data.get('organiser').strip()
        start_time = data.get('start_time').replace(tzinfo=utc)
        finish_time = data.get('finish_time').replace(tzinfo=utc)
        sign_in_time = data.get('sign_in_time').replace(tzinfo=utc)
        attendees = data.get('attendees')
        time_now = datetime.now().replace(tzinfo=utc)

        print("Start time: " + str(start_time))
        print("End time: " + str(finish_time))
        print("Attendees: " + str(data.get('attendees')))
        print("Attending: " + str(data.get('attending')))

        # Checks if user exists
        if not user_exists(username.strip()):
            raise serializers.ValidationError("User does not exist")

        if not attendees:
            raise serializers.ValidationError("Attendees cannot be null")

        # Throw if start time after finish_time
        if start_time >= finish_time:
            raise serializers.ValidationError("Invalid time entry")

        if start_time < time_now or finish_time < time_now:
            raise serializers.ValidationError("Time must be in future")

        if sign_in_time > start_time:
            raise serializers.ValidationError("Sign in time must be in before or equal start time")

        # Checks every username in attendee list
        for attendee in attendees:

            if not user_exists(attendee.strip()):
                raise serializers.ValidationError(attendee + " does not exist")

        # Attending must be empty
        if data.get('attending'):
            raise serializers.ValidationError("Attending must be empty")

        return data

    def create(self, validated_data):

        # Makes sure attending does not get instantiated with NoneType during creation
        validated_data['attending'] = []
        event = Event.objects.create(**validated_data)
        return event

    class Meta:
        model = Event
        fields = "__all__"
        # exclude = ('created',)


class AttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for Attempt.
    Verifies username, event existing and if user is specified attendee in the event or
    is already in the attending list

    This is the main validation for event sign-in
    The method verify_scan() is as follows
    1. Verify if current attempt is valid
        - valid in event
        - data scanned from camera is valid within timestamp and the information scanned on the screen of the phone
    2. Retrieve and verify the last attempt with the same username and event_id
        - validate attempt as per step 1
    3. If the two attempts or scans are within the time delta(10 seconds), the user is added to the event attending list
    """

    def validate(self, data):

        now = timezone.now()

        username = data.get('username').strip()
        event_id = data.get('event_id')

        # Setting created_time to now
        data['created'] = now

        created = data.get('created')
        print("\n\n\n----------NEW ATTEMPT---------\n" )

        print("\nCreated: " + str(created))

        # Checks if user exists
        if not user_exists(username.strip()):
            raise serializers.ValidationError("User does not exist")

        # Checks if event exists
        if not event_exists(event_id):
            raise serializers.ValidationError("Event does not exist")

        # Check if user exists in attendee list and not already in attending
        if not attendee_is_user(username, event_id):
            raise serializers.ValidationError("User is not in attendees or already in list")

        print("Serializer valid. Verifying last scan now")

        # If user is attendee, add to list with verification
        # Doesn't need to raise Validation error, needs to check for duplicates
        verify_scan(data)

        return data

    class Meta:
        model = Attempt
        fields = "__all__"
        read_only_fields = ('created',)


def verify_scan(data):
    """
    Algorithm
    1. Verify if current attempt is valid
        - valid in event
        - data scanned from camera is valid within timestamp and the information scanned on the screen of the phone
    2. Retrieve and verify the last attempt with the same username and event_id
        - validate attempt as per step 1
    3. If the two attempts or scans are within the time delta(10 seconds), the user is added to the event attending list
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
                # Check if time within 10 seconds of last
                seconds_difference = (current_created - last_attempt.created).total_seconds()
                delta = 10

                # Makes sure that the current time after alst attempt time and within delta
                if 0 < seconds_difference < delta:

                    print("Two attempts within delta")
                    add_to_attending(username, event_id)
                else:
                    verified = False
                    print("Two attempts not within delta")
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

    # Check through timestamp
    if event.sign_in_time <= timestamp <= event.finish_time:

        print("Within timezone")
    else:
        verified = False

    # Check screen time within timestamp delta
    time_difference = (timestamp - combined_time).total_seconds()
    print("Time difference: " + str(time_difference))

    if time_difference < 10:
        print("Screen time withing delta")
    else:
        verified = False

    return verified


# Checks if user exists with only one entry
def user_exists(username):

    user_count = User.objects.filter(username__iexact=username.strip()).count()

    if user_count == 1:
        return True
    else:
        return False


def event_exists(event_id):

    event_count = Event.objects.filter(id=event_id).count()

    if event_count == 1:
        return True
    else:
        return False


# Checks to see if attendee of an event is part of the event
def attendee_is_user(username, event_id):

    if user_exists(username) and event_exists(event_id):

        # Checks if user in attendee and not already in attending
        event = Event.objects.filter(id=event_id) \
            .filter(attendees__icontains=username.strip().lower()) \
            .exclude(attending__icontains=username.strip().lower())

        # If there's only one entry of event and is exists
        if event.exists() and event.count() == 1:
            print(username + " exists in " + str(event_id))
            return True
        else:
            print(username + " does not exist in " + str(event_id) + " or is already in there")
            return False

    else:
        return False


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

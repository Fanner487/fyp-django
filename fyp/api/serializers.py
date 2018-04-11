from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Event, Attempt
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate
import pytz


"""
Serializers are the middleware between models and the API views.
Data can be validated here before the object gets before DB operations
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


class VerifyGroupSerializer(serializers.Serializer):
    """
    Serializer for verifying users. Verifies unique usernames, emails
    and validates other fields required for registration
    """

    usernames = serializers.ListField(child=serializers.CharField())

    def validate(self, data):

        users = data.get('usernames')

        if users is None or len(users) == 0:
            raise serializers.ValidationError("Empty list")
        else:

            for user in data.get('usernames'):
                print(user)
                if not user_exists(user):
                    print(user + " does not exist")
                    raise serializers.ValidationError(user + " does not exist")
                else:
                    print(user + "exists")

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


class EventUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Event Update endpoint.
    Verifies if users exists in attendees and organisers
    Similar to EventSerializer but without checking if the event create time
    is after current time
    Performs updates on attendees/attending
    """

    def validate(self, data):

        utc = pytz.UTC  # using timezones for time checking

        username = data.get('organiser').strip()
        start_time = data.get('start_time').replace(tzinfo=utc)
        finish_time = data.get('finish_time').replace(tzinfo=utc)
        sign_in_time = data.get('sign_in_time').replace(tzinfo=utc)
        attendees = data.get('attendees')

        print("Update Serializer data")
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

        if sign_in_time > start_time:
            raise serializers.ValidationError("Sign in time must be in before or equal start time")

        # Checks every username in attendee list
        for attendee in attendees:

            if not user_exists(attendee.strip()):
                raise serializers.ValidationError(attendee + " does not exist")

        # Attending must be empty
        # if data.get('attending'):
        #     raise serializers.ValidationError("Attending must be empty")

        if data.get('attending') is None:

            print("Attending is none, assigning new data")
            data['attending'] = []

            print("New data")
            print(data.get('attending'))
        else:
            data['attending'] = update_attendees(data.get('attendees'), data.get('attending'))

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


def update_attendees(attendees, attending):

    print("in update attendees")
    print("old attending")
    print(attending)
    new_attending = []

    for user in attending:

        if user in attendees:

            new_attending.append(user)

    print("new attending")
    print(new_attending)

    return new_attending


class ManualSignInSerializer(serializers.Serializer):

    event_id = serializers.IntegerField()
    user = serializers.CharField()

    def validate(self, data):

        user = data.get('user')
        event_id = data.get('event_id')

        if not event_exists(event_id):
            raise serializers.ValidationError("Event does not exist")

        if not user_exists(user):
            raise serializers.ValidationError("User does not exist")

        if not attendee_is_user(user.strip().lower(), event_id):
            raise serializers.ValidationError("User is not attendee to event")

        if attendee_is_in_attending(user, event_id):
            raise serializers.ValidationError("User is already signed in")

        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def __reduce_ex__(self, protocol: int) -> tuple:
        return super().__reduce_ex__(protocol)


class ManualRemoveUserFromAttendingSerializer(serializers.Serializer):

    event_id = serializers.IntegerField()
    user = serializers.CharField()

    def validate(self, data):

        print("In ManualRemoveUserFromAttendingSerializer")

        user = data.get('user')
        event_id = data.get('event_id')

        if not event_exists(event_id):
            raise serializers.ValidationError("Event does not exist")

        if not user_exists(user):
            raise serializers.ValidationError("User does not exist")

        # if not attendee_is_user(user.strip().lower(), event_id):
        #     raise serializers.ValidationError("User is not attendee to event")

        event = Event.objects.get(id=event_id)

        print("\nEvent")
        print(event)

        if user not in event.attending:
            raise serializers.ValidationError("User is not in attending")

        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def __reduce_ex__(self, protocol: int) -> tuple:
        return super().__reduce_ex__(protocol)


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

    """

    def validate(self, data):

        utc = pytz.UTC
        now = timezone.now()
        new_now = now.replace(tzinfo=utc)

        username = data.get('username').strip()
        event_id = data.get('event_id')

        # Setting created_time to now
        data['created'] = new_now

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
            raise serializers.ValidationError(username + " is not in attendee")

        if attendee_is_in_attending(username, event_id):
            raise serializers.ValidationError(username + " signed in")

        return data

    class Meta:
        model = Attempt
        fields = "__all__"
        read_only_fields = ('created',)


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
            .filter(attendees__icontains=username.strip().lower())

        # If there's only one entry of event and is exists
        if event.exists() and event.count() == 1:
            print(username + " exists in " + str(event_id))
            return True
        else:
            print(username + " does not exist in " + str(event_id) + " or is already in there")
            return False

    else:
        return False


def attendee_is_in_attending(username, event_id):

    if user_exists(username) and event_exists(event_id):

        # Checks if user in attendee and not already in attending
        event = Event.objects.filter(id=event_id) \
            .filter(attending__icontains=username.strip().lower())

        # If there's only one entry of event and is exists
        if event.exists() and event.count() == 1:
            print(username + " is in attending")
            return True
        else:
            print(username + " is not in attending")
            return False

    else:
        return False

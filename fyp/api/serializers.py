from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta
from django.utils import timezone 
import pytz


class EventSerializer(serializers.ModelSerializer):

	def validate(self, data):

		utc = pytz.UTC # using timezomes for time checking

		username= data.get('organiser').strip()
		start_time = data.get('start_time').replace(tzinfo=utc)
		finish_time = data.get('finish_time').replace(tzinfo=utc)
		sign_in_time = data.get('sign_in_time').replace(tzinfo=utc)
		attendees = data.get('attendees')
		time_now = datetime.now().replace(tzinfo=utc)

		print("Start time: " + str(start_time))
		print("End time: " + str(finish_time))
		print("Attending: " + str(data.get('attending')))

		# Checks if user exists
		if not user_exists(username.strip()):
			raise serializers.ValidationError("User does not exist")

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


	class Meta:
		model = Event
		fields = "__all__"
		# exclude = ('created',)


def event_exists(event_id):

	event_count = Event.objects.filter(id=event_id).count()
	
	event = Event.objects.filter(id=event_id)

	if event_count == 1:
		return True
	else:
		return False
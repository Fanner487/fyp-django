# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime 
from django.utils import timezone

# Create your models here.
class Event(models.Model):
	organiser = models.CharField("organiser", max_length=50)
	event_name = models.CharField("event_name", max_length=50)
	location = models.CharField("location", max_length=50)
	start_time = models.DateTimeField()
	finish_time = models.DateTimeField()
	sign_in_time = models.DateTimeField()
	attendees = ArrayField(models.CharField(max_length=50))
	attending = ArrayField(models.CharField(max_length=50), blank=True, null=True)
	attendance_required = models.BooleanField(default=False)



class Attempt(models.Model):
	username = models.CharField("username", max_length=50)
	event_id = models.IntegerField("event_id")
	created = models.DateTimeField(null=True, blank=True)
	time_on_screen = models.TimeField()
	date_on_screen = models.DateField()


	# def save(self, *args, **kwargs):

	# 	# Create timestamp
	# 	if not self.id: 
	# 		self.time_created = timezone.now()

	# 	super(Attempt, self).save(*args, **kwargs)



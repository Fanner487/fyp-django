# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
	list_display = ('id', 'organiser', 'event_name', 'location', 'start_time', 'sign_in_time', 'finish_time')
	# readonly_fields = ('time_created',)



admin.site.register(Event, EventAdmin)
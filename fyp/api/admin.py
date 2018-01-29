# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Event, Attempt

# Register your models here.
class EventAdmin(admin.ModelAdmin):
	list_display = ('id', 'organiser', 'event_name', 'location', 'start_time', 'sign_in_time', 'finish_time')
	# readonly_fields = ('time_created',)

class AttemptAdmin(admin.ModelAdmin):
	list_display = ('username', 'event_id', 'time_on_screen', 'date_on_screen')
	readonly_fields = ('created',)



admin.site.register(Event, EventAdmin)
admin.site.register(Attempt, AttemptAdmin)
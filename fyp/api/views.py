# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.viewsets import ModelViewSet
from .serializers import EventSerializer
from .models import Event
from rest_framework.generics import ListCreateAPIView

from django.contrib.auth import authenticate

from django.shortcuts import render

from django.contrib.auth.models import User

from datetime import datetime
import pytz



class EventViewSet(ModelViewSet):

	serializer_class = EventSerializer
	queryset = Event.objects.all()
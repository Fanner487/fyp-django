from django.conf.urls import url
from rest_framework.routers import SimpleRouter

# from .views import SubscriberView
from .views import EventViewSet, AttemptViewSet, UserViewSet
from .views import login, register, get_events, delete_table, verify_group

"""
URLs and patterns specified for the REST API views
"""

# ViewSets group the API views together and generates the HTTP URLS, actions and patterns
# needed for them to according to general API standards (GET, POST, PATCH)
router = SimpleRouter()
router.register("events", EventViewSet)
router.register("attempts", AttemptViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    url(r'^login', login, name="login"),
    url(r'^register', register, name="register"),
    url(r'^profile/(?P<username>[\w.@+-]+)/(?P<event_type>[-\w]+)/(?P<time>[-\w]+)/$', get_events, name="get_events"),
    url(r'^deletetable/(?P<table>[\w.@+-]+)/$', delete_table, name="delete_table"),
    url(r'^verify_group', verify_group, name="verify_group"),
]

urlpatterns += router.urls

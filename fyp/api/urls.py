from django.conf.urls import url
from rest_framework.routers import SimpleRouter

# from .views import SubscriberView
from .views import EventViewSet, AttemptViewSet, UserViewSet
from .views import login, register, get_events, delete_table, verify_group, get_events_for_user, jwt_login, manually_sign_in_user
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

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
    url(r'^jwt_login', jwt_login, name="jwt_login"),
    url(r'^register', register, name="register"),
    url(r'^profile/(?P<username>[\w.@+-]+)/(?P<event_type>[-\w]+)/(?P<time>[-\w]+)/$', get_events, name="get_events"),
    url(r'^deletetable/(?P<table>[\w.@+-]+)/$', delete_table, name="delete_table"),
    url(r'^verify_group', verify_group, name="verify_group"),
    url(r'^manual_sign_in', manually_sign_in_user, name="manually_sign_in_user"),
    url(r'^(?P<username>[\w.@+-]+)/events', get_events_for_user, name="get_events_for_user"),
    url(r'^(?P<username>[\w.@+-]+)/events', get_events_for_user, name="get_events_for_user"),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]

urlpatterns += router.urls

from django.conf.urls import url
from rest_framework.routers import SimpleRouter

# from .views import SubscriberView
from .views import EventViewSet, AttemptViewSet, UserViewSet
from .views import login, register, get_events, delete_table


router = SimpleRouter()
router.register("events", EventViewSet)
router.register("attempts", AttemptViewSet)
router.register("users", UserViewSet)



urlpatterns = [
    url(r'^login', login, name="login"),
    url(r'^register', register, name="register"),
    url(r'^profile/(?P<username>[\w.@+-]+)/(?P<event_type>[-\w]+)/(?P<time>[-\w]+)/$', get_events, name="get_events"),
    url(r'^deletetable/(?P<table>[\w.@+-]+)/$', delete_table, name="delete_table"),
    # url(r'^profile/(?P<username>[\w.@+-]+)/$', view_subscribers, name="view_subscribers"),
    # url(r'^attempts', AttemptView.as_view(), name="attempt")
    # url(r'^register', register, name="register")
    # url(r'^hello', SubscriberView.as_view(), name="subsriber")
    # url(r'^hello', hello_world, name="hello_world")
]

urlpatterns += router.urls

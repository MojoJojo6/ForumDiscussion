from django.conf.urls import url

from .consumers import ForumConsumer

websocket_urlpatterns = [
    url(r'^ws/forum/(?P<course_room_id>\d+)/$', ForumConsumer),
]
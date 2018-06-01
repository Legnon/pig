from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name="main"),
    url(r'^feed/$', views.feed, name="feed"),
    url(r'^meat/$', views.meat, name="meat"),
    url(r'^feed_1/$', views.feed_1, name="feed_1"),
    url(r'^feed_2/$', views.feed_2, name="feed_2"),
    url(r'^feed_3/$', views.feed_3, name="feed_3"),
]

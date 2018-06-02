from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name="main"),
    url(r'^feed/$', views.feed, name="feed"),
    url(r'^meat/$', views.meat, name="meat"),
    url(r'^feed_1/$', views.feed_1, name="feed_1"),
    url(r'^feed_2/$', views.feed_2, name="feed_2"),
    url(r'^feed_3/$', views.feed_3, name="feed_3"),
    url(r'^meat_1/$', views.meat_1, name="meat_1"),
    url(r'^meat_2/$', views.meat_2, name="meat_2"),
    url(r'^meat_3/$', views.meat_3, name="meat_3"),
    url(r'^result/$', views.result, name="result"),
]

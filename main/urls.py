from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name="main"),
    url(r'^feed/$', views.feed, name="feed"),
    url(r'^meat/$', views.meat, name="meat"),
]

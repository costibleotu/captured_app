from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from django.contrib import admin
from api import views


urlpatterns = [
    url( r'^winners/$', views.winners_list ),
]

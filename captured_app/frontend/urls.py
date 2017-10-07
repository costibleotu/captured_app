from django.conf.urls import include, url
from django.contrib import admin
from frontend import views



urlpatterns = [
    url(r'', views.index),
]

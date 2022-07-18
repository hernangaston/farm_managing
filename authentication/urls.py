#! /usr/bin/env python3
from django.contrib import admin
from django.urls import include, path


from .views import *


urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro' ),
    path('login/', loginView, name='login' ),
    path('', close_session, name='close-session' )
]

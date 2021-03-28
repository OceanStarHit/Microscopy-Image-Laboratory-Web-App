"""
Script file: urls.py
Created on: Feb 25, 2021
Last modified on: Mar 28, 2021

Comments:
    URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from . import apis


urlpatterns = [
    path('set-image', apis.set_image),
    path('set-metadata', apis.set_metadata),
    path('change-image', apis.change_image),
    path('change-parameter', apis.change_parameter),
    path('adjust-image', apis.adjust_image),
    path('color-channel', apis.color_channel),
    path('gray', apis.gray),
    path('hist', apis.equalize),
]

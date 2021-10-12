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
from django.contrib.auth.models import User


# Routers provide an easy way of automatically determining the URL conf.

from apis.tile_viewset import TileViewSet
from rest_framework import routers, serializers, viewsets
router = routers.DefaultRouter()
router.register(r'tiles', TileViewSet, basename='tile')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('set-image', apis.set_image),
    path('set-metadata', apis.set_metadata),
    path('change-image', apis.change_image),
    path('change-parameter', apis.change_parameter),
    path('adjust-image', apis.adjust_image),
    path('color-channel', apis.color_channel),
    path('gray', apis.gray),
    path('hist', apis.equalize),
]

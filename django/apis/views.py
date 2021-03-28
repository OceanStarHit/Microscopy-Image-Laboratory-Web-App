"""
Script file: views.py
Created on: Feb 25, 2021
Last modified on: Mar 28, 2021

Comments:
    Rendering page
"""

from django.shortcuts import render


def index(request):
    """
    Create your views here
    :param request: API request
    :return: rendered HTML page
    """
    return render(request,'index.html')

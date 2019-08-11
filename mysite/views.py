from urllib import request

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


def redirect_view(request):
    response = redirect('/polls/')
    return response

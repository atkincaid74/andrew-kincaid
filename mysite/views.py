from urllib import request

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


def redirect_view(request):
    response = redirect('/polls/')
    return response


class CreateNewUserView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        data = request.data
        user = User.objects.create_user(data['username'], data['email'],
                                        data['password'])
        user.first_name = data['firstName']
        user.last_name = data['lastName']

        user.save()
        return HttpResponse('Success')

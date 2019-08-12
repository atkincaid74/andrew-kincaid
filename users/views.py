from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from .models import ValidEmails


class CreateNewUserView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        data = request.data
        username = data['username']
        email = data['email']

        if User.objects.filter(email=email).exists():
            return HttpResponse('Email already used')

        elif User.objects.filter(username=username).exists():
            return HttpResponse('Username already taken')

        else:
            if ValidEmails.objects.filter(email=email).exists():
                user = User.objects.create_user(username, email,
                                                data['password'])
                user.first_name = data['firstName']
                user.last_name = data['lastName']

                user.save()
                return HttpResponse('Success')

            else:
                return HttpResponse("Email hasn't been approved")

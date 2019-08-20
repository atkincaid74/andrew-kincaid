from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ValidEmails
from rest_framework_jwt.views import (ObtainJSONWebToken, RefreshJSONWebToken,
                                      VerifyJSONWebToken)


class CreateNewUserView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        data = request.data
        username = data['username'].lower()
        email = data['email'].lower()

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


class GetUserInfo(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        user = request.data['username']

        user_record = User.objects.filter(username=user).first()

        first_name = user_record.first_name
        last_name = user_record.last_name
        email = user_record.email

        email_record = ValidEmails.objects.filter(email=email).first()
        paid = email_record.paid

        output = dict(
            firstName=first_name,
            lastName=last_name,
            email=email,
            paid=paid,
        )

        return Response(output)


class AllowedObtainJSONWebToken(ObtainJSONWebToken):
    permission_classes = (AllowAny, )


class AllowedRefreshJSONWebToken(RefreshJSONWebToken):
    permission_classes = (AllowAny, )


class AllowedVerifyJSONWebToken(VerifyJSONWebToken):
    permission_classes = (AllowAny, )



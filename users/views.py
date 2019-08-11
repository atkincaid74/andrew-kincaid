from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


class CreateNewUserView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        data = request.data
        username = data['username']
        email = data['email']

        user = User.objects.create_user(username, email, data['password'])
        user.first_name = data['firstName']
        user.last_name = data['lastName']

        user.save()
        return HttpResponse('Success')

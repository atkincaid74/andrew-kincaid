from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import Game


# Create your views here.
class GetGamesView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request):
        # TODO come back and add the logic to pick correct week

        return Response(list(Game.objects.filter(week=1).all()))

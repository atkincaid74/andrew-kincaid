from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import Game, SeasonPickem
from .serializers import SeasonPickemSerializer, GameSerializer
import pandas as pd


# Create your views here.
class GetGamesView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        week = request.week

        return Response(JSONRenderer().render(
            GameSerializer(
                Game.objects.filter(week=week).all(), many=True
            ).data
        ))


class GetPicksView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request):


        return Response(JSONRenderer().render(
            SeasonPickemSerializer(SeasonPickem.objects.all(), many=True).data
        ))

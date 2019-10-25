from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import Game, SeasonPickem
from .serializers import SeasonPickemSerializer, GameSerializer
from .helpers import update_winners, get_game_results, get_summary
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

    def post(self, request):
        return Response(get_game_results().to_json(orient='records'))


class UpdateWinnersView(APIView):
    def post(self, request):
        update_winners()

        return Response('success')


class GetPickSummaryView(APIView):
    renderer_classes = (JSONRenderer, )

    @staticmethod
    def get():
        df = get_summary()

        return Response(df.to_json(orient='records'))

from .models import GolfPicks
from rest_framework.serializers import ModelSerializer


class GolfPicksSerializer(ModelSerializer):
    class Meta:
        model = GolfPicks
        fields = ['name', 'player1', 'player2', 'player3', 'player4', 'player5', 'player6', 'winning_score']

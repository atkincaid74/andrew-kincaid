from .models import SeasonPickem, Game, Team
from rest_framework.serializers import ModelSerializer, StringRelatedField


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class GameSerializer(ModelSerializer):
    home_team = StringRelatedField()
    away_team = StringRelatedField()

    class Meta:
        model = Game
        fields = '__all__'


class SeasonPickemSerializer(ModelSerializer):
    game = GameSerializer()
    andrew_pick = TeamSerializer()
    steve_pick = TeamSerializer()

    class Meta:
        model = SeasonPickem
        fields = '__all__'

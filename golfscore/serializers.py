from .models import GolfPicks
from rest_framework.serializers import ModelSerializer


class GolfPicksSerializer(ModelSerializer):
    class Meta:
        model = GolfPicks
        fields = '__all__'

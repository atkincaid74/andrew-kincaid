from .models import *
from rest_framework.serializers import ModelSerializer


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TeeSerializer(ModelSerializer):
    class Meta:
        model = Tee
        fields = '__all__'


class ScorecardSerializer(ModelSerializer):
    class Meta:
        model = Scorecard
        fields = '__all__'


class RoundSerializer(ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'

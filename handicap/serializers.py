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
        exclude = ['par_out', 'par_in', 'par']

    def validate(self, attrs):
        instance = Scorecard(**attrs)
        instance.clean()

        return instance.to_dict()


class RoundSerializer(ModelSerializer):
    class Meta:
        model = Round
        exclude = ['course_handicap', 'score_out', 'score_in', 'gross',
                   'differential', 'nh_already_used', 'nine_holes_combined']

    def validate(self, attrs):
        instance = Round(**attrs)
        instance.clean()

        return instance.to_dict()

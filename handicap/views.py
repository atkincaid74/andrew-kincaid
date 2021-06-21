import datetime
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .serializers import *
from .models import *


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)  # TODO remove
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class TeeViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)  # TODO remove
    serializer_class = TeeSerializer
    queryset = Tee.objects.all()


class ScorecardViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)  # TODO remove
    serializer_class = ScorecardSerializer
    queryset = Scorecard.objects.all()


class RoundViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)  # TODO remove
    serializer_class = RoundSerializer
    queryset = Round.objects.all()


class HandicapView(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)  # TODO remove

    @staticmethod
    def get(request):
        handicap_records = HandicapHistory.objects.filter(
            user=request.user)

        if not handicap_records:
            return Response(status=204)

        else:
            current = handicap_records.order_by('-date').first().handicap
            low = handicap_records.filter(
                date__gte=datetime.datetime.now() -
                datetime.timedelta(days=365)).order_by(
                'handicap').first().handicap

            return Response({'current': current, 'low': low})

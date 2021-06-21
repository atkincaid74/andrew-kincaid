from django_pandas.io import read_frame
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
        rounds = read_frame(Round.objects.filter(user__email=request.user))

        return Response('hello')

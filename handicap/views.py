import re
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.fields import (IntegerField, CharField, ChoiceField,
                                   FloatField, DateField, empty, BooleanField)
from rest_framework.serializers import PrimaryKeyRelatedField
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

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)


class SerializerToForm(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)  # TODO remove

    @staticmethod
    def get(request, serializer_name):
        serializer_dict = {
            'course': CourseSerializer,
            'tee': TeeSerializer,
            'scorecard': ScorecardSerializer,
            'round': RoundSerializer,
        }

        serializer = serializer_dict.get(serializer_name)
        if serializer is None:
            return Response('Serializer not found', status=204)

        serializer = serializer()

        out_dict = {}
        for field_name, field in serializer.fields.items():
            if field.read_only:  # No need to provide input for read-only
                continue

            if field_name == 'user':  # User is filled out automatically
                continue

            component_dict = {'label': field_name.title(), 'value': None}
            if isinstance(field, (IntegerField, FloatField)):
                component_dict['component'] = 'v-text-field'
                component_dict['type'] = 'number'

                if re.match(r'^par\d{1,2}$', field_name):
                    # default par of 4 for easy input
                    component_dict['value'] = 4

            elif isinstance(field, CharField):
                component_dict['component'] = 'v-text-field'
                rules = {}

                if field.required is not empty and field.required:
                    rules['required'] = True
                if field.max_length is not empty:
                    rules['max_length'] = field.max_length

                component_dict['rules'] = rules

                if field.default is not empty:
                    component_dict['value'] = field.default

            elif isinstance(field, ChoiceField):
                component_dict['component'] = 'v-select'
                component_dict['items'] = [
                    {'text': v, 'value': k, 'disabled': False}
                    for k, v in field.choices.items()]

                if field.required is not empty:
                    component_dict['clearable'] = True

            elif isinstance(field, PrimaryKeyRelatedField):
                component_dict['component'] = 'v-select'
                component_dict['items'] = [
                    {'text': str(q), 'value': q.id, 'disabled': False}
                    for q in field.queryset.all()
                ]

                if field.required is not empty:
                    component_dict['clearable'] = True

            elif isinstance(field, DateField):
                component_dict['component'] = 'DateField'

            elif isinstance(field, BooleanField):
                component_dict['component'] = 'v-checkbox'

            out_dict[field_name] = component_dict

        return Response(out_dict)


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

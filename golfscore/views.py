import re

import pandas as pd
from django_pandas.io import read_frame
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser
from .serializers import GolfPicksSerializer
from .models import GolfPicks
from .pull_pga import get_player_data, get_status, get_soup, get_projected_cut
from mysite import is_numeric


class PicksView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @staticmethod
    def get(request):
        return Response(JSONRenderer().render(
            GolfPicksSerializer(GolfPicks.objects.all(), many=True).data
        ))

    @staticmethod
    def post(request):
        data = JSONParser().parse(request)
        serializer = GolfPicksSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(JSONRenderer().render(serializer.data), status=201)
        return Response(JSONRenderer().render(serializer.errors), status=400)

    @staticmethod
    def put(request):
        data = JSONParser().parse(request)
        old_record = GolfPicks.objects.get(name=data['name'])
        serializer = GolfPicksSerializer(old_record, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(JSONRenderer().render(serializer.data), status=200)
        return Response(JSONRenderer().render(serializer.errors), status=400)

    @staticmethod
    def delete(request):
        data = JSONParser().parse(request)
        GolfPicks.objects.get(name=data['name']).delete()
        return Response(status=204)


class PicksWithScoresView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        score_df = get_player_data()

        picks_df = read_frame(
            GolfPicks.objects.all(), [f'player{i}' for i in range(1, 7)],
            'name').rename(columns=lambda c: c.replace('player', 'Tier '))

        out_dict = {}
        for name in picks_df.index:
            df = picks_df.loc[[name]].T.merge(score_df, how='left',
                                              left_on=name, right_index=True)
            df.rename(columns={name: 'Picks'}, inplace=True)
            cols = ['TO PAR', 'TODAY', 'R1', 'R2', 'R3', 'R4', 'TOTAL']
            df.loc[
                'Total', [col for col in cols if col in df.columns]
            ] = df[[col for col in cols if col in df.columns]].apply(
                lambda x: sum([int(float(s)) for s in x if is_numeric(s)]))

            out_dict[name] = df.to_json(orient='index')

        return Response(out_dict)


class LeaderboardView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        score_df = get_player_data()

        picks_df = read_frame(
            GolfPicks.objects.all(), [f'player{i}' for i in range(1, 7)],
            'name'
        ).rename(columns=lambda c: c.replace('player', 'Tier '))
        if 'TO PAR' not in score_df.columns:
            return Response(picks_df.reset_index().to_json(orient='index'))

        def to_par_or_tee_time(x):
            if re.match(r'^\d{1,2}$|^\a+$', score_df.loc[x, 'THRU']):
                return score_df.loc[x, 'TO PAR']
            else:
                return score_df.loc[x, 'THRU']

        picks_df = picks_df.applymap(to_par_or_tee_time)

        picks_df['TOTAL'] = picks_df.apply(
            lambda x: sum([int(float(s)) for s in x if is_numeric(s)]), axis=1)
        picks_df.sort_values('TOTAL', inplace=True)
        picks_df['RANK'] = picks_df['TOTAL'].rank(method='min').astype(int)

        picks_df = picks_df.reset_index()[
            ['RANK', 'name', 'TOTAL', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5', 'Tier 6']]

        return Response(picks_df.to_json(orient='index'))


class StatusView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        status = get_status()
        return Response(status if status != 'Tournament Field' else 'Contest not started')


class ProjectedCutView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        return Response(get_projected_cut())

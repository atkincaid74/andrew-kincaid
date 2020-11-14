import pandas as pd
from django_pandas.io import read_frame
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import GolfPicksSerializer
from .models import GolfPicks
from .pull_pga import get_player_data, get_status, get_soup, get_projected_cut


class PicksView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        return Response(JSONRenderer().render(
            GolfPicksSerializer(GolfPicks.objects.all()).data
        ))


class PicksWithScoresView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        score_df = get_player_data()

        picks_df = read_frame(
            GolfPicks.objects.all(), [f'player{i}' for i in range(1, 5)],
            'name').rename(columns=lambda c: c.replace('player', 'Tier '))

        out_dict = {}
        for name in picks_df.index:
            df = picks_df.loc[[name]].T.merge(score_df, how='left',
                                              left_on=name, right_index=True)
            df.rename(columns={name: 'Picks'}, inplace=True)
            df.loc[
                'Total', ['TO PAR', 'TODAY', 'R1', 'R2', 'R3', 'R4', 'TOTAL']
            ] = df[['TO PAR', 'TODAY', 'R1', 'R2', 'R3', 'R4', 'TOTAL']].sum()

            out_dict[name] = df.to_json(orient='index')

        return Response(out_dict)


class LeaderboardView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        score_df = get_player_data()

        picks_df = read_frame(
            GolfPicks.objects.all(), [f'player{i}' for i in range(1, 5)],
            'name'
        ).rename(columns=lambda c: c.replace('player', 'Tier '))
        picks_df = picks_df.applymap(lambda x: score_df.loc[x, 'TO PAR'])

        picks_df['TOTAL'] = picks_df.sum(axis=1)
        picks_df.sort_values('TOTAL', inplace=True)
        picks_df['RANK'] = picks_df['TOTAL'].rank(method='min').astype(int)

        picks_df = picks_df.reset_index()[
            ['RANK', 'name', 'TOTAL', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4']]

        return Response(picks_df.to_json(orient='index'))


class StatusView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        return Response(get_status())


class ProjectedCutView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        return Response(get_projected_cut())

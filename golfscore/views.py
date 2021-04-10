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
from .pull_pga import get_player_data, get_status, get_soup, get_cut
from mysite import is_numeric, TIME_REGEX


def clean_up_scores(s_or_t):
    if re.match(TIME_REGEX, str(s_or_t)) or not is_numeric(s_or_t):
        return s_or_t
    elif int(float(s_or_t)) > 0:
        return f'+{s_or_t}'
    elif int(float(s_or_t)) == 0:
        return 'E'
    else:
        return s_or_t


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

            df[['TO PAR', 'TODAY']] = df[['TO PAR', 'TODAY']].applymap(clean_up_scores)

            out_dict[name] = df.to_json(orient='index')

        return Response(out_dict)


class LeaderboardView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        soup = get_soup()
        score_df = get_player_data(soup)

        picks_df = read_frame(
            GolfPicks.objects.all(), [f'player{i}' for i in range(1, 7)],
            'name'
        ).rename(columns=lambda c: c.replace('player', 'Tier '))
        if 'TO PAR' not in score_df.columns:
            return Response(picks_df.reset_index().to_json(orient='index'))

        def to_par_or_tee_time(x):
            thru = score_df.loc[x, 'THRU']
            cut_ = score_df.loc[x, 'POSITION'] in ('WD', 'DQ', 'CUT')
            if re.match(TIME_REGEX, thru) and not is_numeric(score_df.loc[x, 'R1']):
                return thru
            else:
                if not cut_:
                    return score_df.loc[x, 'TO PAR']
                else:
                    return f"CUT:{score_df.loc[x, 'TO PAR']}"

        picks_df = picks_df.applymap(to_par_or_tee_time)

        picks_df['TOTAL'] = picks_df.apply(
            lambda x: sum([int(float(s)) for s in x if is_numeric(s)]), axis=1)
        picks_df.sort_values('TOTAL', inplace=True)
        picks_df['RANK'] = picks_df['TOTAL'].rank(method='min').astype(int)
        picks_df.loc[picks_df['RANK'].duplicated(keep=False), 'RANK'] = \
            picks_df.loc[picks_df['RANK'].duplicated(keep=False), 'RANK'].apply(lambda x: f'T{x}')

        projected, cut = get_cut(soup)
        cut_col = '# Projected to Make Cut' if projected else "# Made the Cut"
        if cut is not None and projected:
            cut = 0 if cut == 'E' else int(cut)
            picks_df[cut_col] = picks_df.apply(
                lambda x: (x.replace('E', 0).loc[x.index.str.match(r'Tier\s\d')] <= cut).sum(), axis=1)
        elif cut is not None:
            picks_df[cut_col] = picks_df.apply(
                lambda x: 6 - (x.loc[x.index.str.match(r'Tier\s\d')].astype(str).str.startswith('CUT:')).sum(), axis=1)
            picks_df = picks_df.applymap(lambda x: x if not isinstance(x, str) else x.replace('CUT:', ''))

        picks_df.loc[:, ~picks_df.columns.isin(['RANK', 'name', cut_col])] = \
            picks_df.loc[:, ~picks_df.columns.isin(['RANK', 'name', cut_col])].applymap(clean_up_scores)

        col_order = ['RANK', 'name', 'TOTAL']
        col_order.extend(picks_df.loc[:, picks_df.columns.str.match(r'Tier\s\d')].columns)
        col_order.extend([col for col in picks_df.columns if col not in col_order])

        picks_df = picks_df.reset_index()[col_order]

        return Response(picks_df.to_json(orient='index'))


class StatusView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        status = get_status()
        return Response(status if status != 'Tournament Field'
                        else 'Contest not started')


class ProjectedCutView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    @staticmethod
    def get(request):
        return Response(get_cut())

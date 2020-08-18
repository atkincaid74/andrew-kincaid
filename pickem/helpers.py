import pandas as pd
from .models import SeasonPickem, Team, Winner
from nflgame import games
from nflgame.sched import current_year_and_week


def get_game_results():
    pickem = SeasonPickem.objects.select_related().all()

    data = []
    for p in pickem:
        week = p.game.week
        home_team = p.game.home_team
        away_team = p.game.away_team
        andrew_pick = p.andrew_pick.city
        steve_pick = p.steve_pick.city
        winner = Winner.objects.filter(game=p.game).first()
        if winner is not None:
            data.append(
                {
                    'Week': week,
                    'Home Team': str(home_team),
                    'Away Team': str(away_team),
                    'Andrew\'s Pick': andrew_pick,
                    'Steve\'s Pick': steve_pick,
                    'Winner': winner.winner.city,
                }
            )

    df = pd.DataFrame.from_records(data)

    return df


def update_winners(week=None):
    # get current year and week
    year, week_ = current_year_and_week()

    week = week if week is not None else week_

    # get all games in week
    pickem = SeasonPickem.objects.select_related()\
        .filter(game__week=week).all()

    # get results for week
    game_list = games(year, week=week)
    game_dict = {(g.away, g.home): g for g in game_list}

    for p in pickem:
        game = p.game
        winner = Winner.objects.filter(game=game).first()
        if winner is None:
            game_results = game_dict.get(
                (game.away_team.abbr, game.home_team.abbr)
            )
            if game_results is not None:
                winner_abbr = game_results.winner
                if winner_abbr is not None:
                    if len(winner_abbr) > 3:
                        winner_abbr = 'TIE'
                    winner = Team.objects.filter(abbr=winner_abbr).first()
                    new_winner = Winner(game=game, winner=winner)
                    new_winner.save()


def get_summary():
    season = SeasonPickem.objects.all()
    season = [s.to_dict() for s in season]

    winners = Winner.objects.all()
    winners = [w.to_dict() for w in winners]

    df = pd.merge(pd.DataFrame.from_records(season),
                  pd.DataFrame.from_records(winners),
                  on='game', how='inner')

    df['andrew_win'] = df['andrew_pick'] == df['winner']
    df['steve_win'] = df['steve_pick'] == df['winner']

    df1 = df[['week', 'andrew_win', 'steve_win']].melt(
        'week', var_name='player')
    df1 = df1.groupby(['week', 'player', 'value']).size().unstack(fill_value=0)
    df1 = df1.append(pd.concat(
        [df1.groupby('player').sum()], keys=['Total'], names=['week']
    ))
    df1['record'] = df1.apply(lambda x: f'{x[True]} - {x[False]}', axis=1)

    df2 = df1.reset_index().pivot(index='week', columns='player',
                                  values='record')

    return df2

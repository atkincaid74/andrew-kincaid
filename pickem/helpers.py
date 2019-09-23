import pandas as pd
from .models import SeasonPickem, Team, Winner
from nflgame import games
from nflgame.live import current_year_and_week


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
                if len(winner_abbr) > 3:
                    winner_abbr = 'TIE'
                winner = Team.objects.filter(abbr=winner_abbr).first()
                new_winner = Winner(game=game, winner=winner)
                new_winner.save()

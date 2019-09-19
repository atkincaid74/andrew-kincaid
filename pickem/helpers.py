import pandas as pd
from .models import SeasonPickem
from nflgame import games


def get_pickem_results():
    pickem = SeasonPickem.objects.select_related().all()

    # do the nflgame stuff here

    data = []
    for p in pickem:
        week = p.game.week
        home_team = str(p.game.home_team)
        away_team = str(p.game.away_team)
        andrew_pick = p.andrew_pick.city
        steve_pick = p.steve_pick.city
        winner = 0

        data.append(
            {
                'week': week,
                'home_team': home_team,
                'away_team': away_team,
                'andrew_pick': andrew_pick,
                'steve_pick': steve_pick,
                'winner': winner,
            }
        )

    df = pd.DataFrame.from_records(data)

    return df

from django.db import models
from itertools import chain


class Team(models.Model):
    city = models.TextField(max_length=64)
    nickname = models.TextField(max_length=64)
    abbr = models.TextField(max_length=4)

    def __str__(self):
        return f"{self.city} {self.nickname}"


class Game(models.Model):
    week = models.IntegerField(null=True)
    date = models.DateTimeField(null=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE,
                                  related_name='game_home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE,
                                  related_name='game_away_team')

    def __str__(self):
        return f"Week {self.week} - {self.away_team} @ {self.home_team}"


class SeasonPickem(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    andrew_pick = models.ForeignKey(Team, on_delete=models.CASCADE,
                                    related_name='andrew_team')
    steve_pick = models.ForeignKey(Team, on_delete=models.CASCADE,
                                   related_name='steve_team')

    def __str__(self):
        return f"{self.game}, Andrew-{self.andrew_pick}, " \
               f"Steve-{self.steve_pick}"

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(self)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(self)]
        data['week'] = self.game.week
        return data


class Winner(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.game}, Winner - {self.winner}"

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(self)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(self)]
        return data

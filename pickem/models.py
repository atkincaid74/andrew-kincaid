from django.db import models


class Team(models.Model):
    city = models.TextField(max_length=64)
    nickname = models.TextField(max_length=64)

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

from django.db import models


class GolfPicks(models.Model):
    name = models.TextField(max_length=64, unique=True)
    player1 = models.TextField(max_length=64)
    player2 = models.TextField(max_length=64)
    player3 = models.TextField(max_length=64)
    player4 = models.TextField(max_length=64)
    player5 = models.TextField(max_length=64)
    player6 = models.TextField(max_length=64)
    winning_score = models.TextField(max_length=8)

    def __str__(self):
        return f"{self.name}'s Picks"

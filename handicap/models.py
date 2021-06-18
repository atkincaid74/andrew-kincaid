from django.db import models
from django.contrib.auth.models import User
from .references import state_abbr, states


class Course(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, null=True,
                             choices=list(zip(state_abbr, states)))
    country = models.CharField(max_length=255, default='USA')

    class Meta:
        unique_together = ('name', 'city', 'country',)


class Tee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    color = models.CharField(max_length=255)
    rating = models.FloatField()
    slope = models.IntegerField()

    class Meta:
        unique_together = ('course', 'color',)


class Scorecard(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=1, choices=[('M', 'Men'), ('W', 'Women'), ('B', 'Both')])

    par1 = models.IntegerField()
    si1 = models.IntegerField()
    par2 = models.IntegerField()
    si2 = models.IntegerField()
    par3 = models.IntegerField()
    si3 = models.IntegerField()
    par4 = models.IntegerField()
    si4 = models.IntegerField()
    par5 = models.IntegerField()
    si5 = models.IntegerField()
    par6 = models.IntegerField()
    si6 = models.IntegerField()
    par7 = models.IntegerField()
    si7 = models.IntegerField()
    par8 = models.IntegerField()
    si8 = models.IntegerField()
    par9 = models.IntegerField()
    si9 = models.IntegerField()
    par10 = models.IntegerField()
    si10 = models.IntegerField()
    par11 = models.IntegerField()
    si11 = models.IntegerField()
    par12 = models.IntegerField()
    si12 = models.IntegerField()
    par13 = models.IntegerField()
    si13 = models.IntegerField()
    par14 = models.IntegerField()
    si14 = models.IntegerField()
    par15 = models.IntegerField()
    si15 = models.IntegerField()
    par16 = models.IntegerField()
    si16 = models.IntegerField()
    par17 = models.IntegerField()
    si17 = models.IntegerField()
    par18 = models.IntegerField()
    si18 = models.IntegerField()


class Round(models.Model):
    tee = models.ForeignKey(Tee, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    score1 = models.IntegerField()
    score2 = models.IntegerField()
    score3 = models.IntegerField()
    score4 = models.IntegerField()
    score5 = models.IntegerField()
    score6 = models.IntegerField()
    score7 = models.IntegerField()
    score8 = models.IntegerField()
    score9 = models.IntegerField()
    score10 = models.IntegerField()
    score11 = models.IntegerField()
    score12 = models.IntegerField()
    score13 = models.IntegerField()
    score14 = models.IntegerField()
    score15 = models.IntegerField()
    score16 = models.IntegerField()
    score17 = models.IntegerField()
    score18 = models.IntegerField()

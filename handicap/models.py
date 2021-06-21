from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .references import state_abbr, states, initial_handicap_adjustments


class Course(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, null=True,
                             choices=list(zip(state_abbr, states)))
    country = models.CharField(max_length=255, default='USA')

    class Meta:
        unique_together = ('name', 'city', 'country',)

    def __str__(self):
        return f'{self.name} ({self.city}, {self.state})'


class Scorecard(models.Model):
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
    par_out = models.IntegerField(blank=True)

    @property
    def get_par_out(self):
        return sum([getattr(self, f'par{i}') for i in range(1, 10)])

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
    par_in = models.IntegerField(blank=True)

    @property
    def get_par_in(self):
        return sum([getattr(self, f'par{i}') for i in range(10, 19)])

    par = models.IntegerField(blank=True)

    @property
    def get_par(self):
        return self.get_par_out + self.get_par_in

    def __str__(self):
        return f'Par {self.get_par} ({self.id})'

    def clean(self):
        self.par_out = self.get_par_out
        self.par_in = self.get_par_in
        self.par = self.get_par


class Tee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=1, choices=[('M', 'Men'), ('W', 'Women'), ('B', 'Both')])

    color = models.CharField(max_length=255)
    rating = models.FloatField()
    slope = models.IntegerField()
    scorecard = models.ForeignKey(Scorecard, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('course', 'color',)

    def __str__(self):
        return f'{self.course.name} - {self.color}'


class Round(models.Model):
    tee = models.ForeignKey(Tee, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    course_handicap = models.IntegerField(null=True, blank=True)

    @property
    def get_course_handicap(self):
        handicap_set = HandicapHistory.objects.filter(
            user=self.user, date__lte=self.date)
        if not handicap_set:
            return None
        else:
            current_handicap = handicap_set.order_by('-date').first().handicap
            return (current_handicap * (self.tee.slope / 113) +
                    (self.tee.rating - self.tee.scorecard.par))

    score1 = models.IntegerField()
    score2 = models.IntegerField()
    score3 = models.IntegerField()
    score4 = models.IntegerField()
    score5 = models.IntegerField()
    score6 = models.IntegerField()
    score7 = models.IntegerField()
    score8 = models.IntegerField()
    score9 = models.IntegerField()
    score_out = models.IntegerField(blank=True)

    @property
    def get_score_out(self):
        return sum([getattr(self, f'score{i}') for i in range(1, 10)])

    score10 = models.IntegerField()
    score11 = models.IntegerField()
    score12 = models.IntegerField()
    score13 = models.IntegerField()
    score14 = models.IntegerField()
    score15 = models.IntegerField()
    score16 = models.IntegerField()
    score17 = models.IntegerField()
    score18 = models.IntegerField()
    score_in = models.IntegerField(blank=True)

    @property
    def get_score_in(self):
        return sum([getattr(self, f'score{i}') for i in range(10, 19)])

    gross = models.IntegerField(blank=True)

    @property
    def get_gross(self):
        return self.get_score_out + self.get_score_in

    differential = models.FloatField(blank=True)

    @property
    def get_differential(self):
        return (113 / self.tee.slope) * (self.get_gross - self.tee.rating)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - ' \
               f'{self.tee.course.name} - {self.date}'

    def clean(self):
        self.course_handicap = self.get_course_handicap
        self.score_out = self.get_score_out
        self.score_in = self.get_score_in
        self.gross = self.get_gross
        self.differential = self.get_differential


class HandicapHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    handicap = models.FloatField()
    trigger_round = models.ForeignKey(Round, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.date}'


@receiver(post_save, sender=Round, dispatch_uid="update_handicap")
def update_handicap(sender, instance, created, **kwargs):
    if created:
        rounds = Round.objects.filter(user=instance.user)
        num_rounds = len(rounds)
        if num_rounds < 3:  # Cannot create handicap before 3 rounds entered
            return
        elif num_rounds < 20:  # Use modified calc until 20 rounds entered
            round_count = initial_handicap_adjustments[num_rounds]['count']
            adjustment = initial_handicap_adjustments[num_rounds]['adjustment']
        else:  # Standard calc uses 8 of last 20, no adjustment
            rounds = rounds.order_by('-date')[:20]
            round_count = 8
            adjustment = 0

        counted_rounds = rounds.order_by('differential')[:round_count]
        handicap = (sum([r.differential for r in counted_rounds]) /
                    round_count + adjustment)

        new_handicap = HandicapHistory(
            user=instance.user, date=instance.date, handicap=handicap,
            trigger_round=instance)
        new_handicap.save()

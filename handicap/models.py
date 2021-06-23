import datetime
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from .references import state_abbr, states, initial_handicap_adjustments


class Course(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, null=True, blank=True,
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
        tees = [f'{tee.course.name} - {tee.get_gender_display()}'
                for tee in self.tee_set.all()]
        return f"Par {self.get_par} ({', '.join(set(tees))})"

    def clean(self):
        self.par_out = self.get_par_out
        self.par_in = self.get_par_in
        self.par = self.get_par

    def to_dict(self):
        return {
            'par1': self.par1,
            'si1': self.si1,
            'par2': self.par2,
            'si2': self.si2,
            'par3': self.par3,
            'si3': self.si3,
            'par4': self.par4,
            'si4': self.si4,
            'par5': self.par5,
            'si5': self.si5,
            'par6': self.par6,
            'si6': self.si6,
            'par7': self.par7,
            'si7': self.si7,
            'par8': self.par8,
            'si8': self.si8,
            'par9': self.par9,
            'si9': self.si9,
            'par_out': self.par_out,
            'par10': self.par10,
            'si10': self.si10,
            'par11': self.par11,
            'si11': self.si11,
            'par12': self.par12,
            'si12': self.si12,
            'par13': self.par13,
            'si13': self.si13,
            'par14': self.par14,
            'si14': self.si14,
            'par15': self.par15,
            'si15': self.si15,
            'par16': self.par16,
            'si16': self.si16,
            'par17': self.par17,
            'si17': self.si17,
            'par18': self.par18,
            'si18': self.si18,
            'par_in': self.par_in,
            'par': self.par
        }


class Tee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=1, choices=[('M', 'Men'), ('W', 'Women'), ('B', 'Both')])
    holes = models.CharField(
        max_length=1, choices=[('T', '18'), ('F', 'Front 9'), ('B', 'Back 9')])

    color = models.CharField(max_length=255)
    rating = models.FloatField()
    slope = models.IntegerField(validators=[MinValueValidator(55),
                                            MaxValueValidator(155)])
    scorecard = models.ForeignKey(Scorecard, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('course', 'gender', 'holes', 'color',)

    def __str__(self):
        return (f'{self.course.name} - {self.color} - '
                f'{self.get_holes_display()}')


class Round(models.Model):
    tee = models.ForeignKey(Tee, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    @property
    def nine_holes(self):
        return self.tee.holes != 'T'

    nh_already_used = models.BooleanField(default=False)
    nine_holes_combined = models.BooleanField(default=False)

    course_handicap = models.IntegerField(null=True, blank=True)

    @property
    def current_handicap(self):
        handicap_set = HandicapHistory.objects.filter(
            user=self.user, date__lte=self.date)
        if not handicap_set:
            return None
        else:
            return handicap_set.order_by('-date').first().handicap

    @property
    def get_course_handicap(self):
        if self.current_handicap is None:
            return None
        else:
            return (self.current_handicap * (self.tee.slope / 113) +
                    (self.tee.rating - self.tee.scorecard.par))

    score1 = models.IntegerField(null=True, blank=True)
    score2 = models.IntegerField(null=True, blank=True)
    score3 = models.IntegerField(null=True, blank=True)
    score4 = models.IntegerField(null=True, blank=True)
    score5 = models.IntegerField(null=True, blank=True)
    score6 = models.IntegerField(null=True, blank=True)
    score7 = models.IntegerField(null=True, blank=True)
    score8 = models.IntegerField(null=True, blank=True)
    score9 = models.IntegerField(null=True, blank=True)
    score_out = models.IntegerField(blank=True)

    @property
    def get_score_out(self):
        scores = [getattr(self, f'score{i}') for i in range(1, 10)]
        if any([s is None for s in scores]):
            return 0
        return sum(scores)

    score10 = models.IntegerField(null=True, blank=True)
    score11 = models.IntegerField(null=True, blank=True)
    score12 = models.IntegerField(null=True, blank=True)
    score13 = models.IntegerField(null=True, blank=True)
    score14 = models.IntegerField(null=True, blank=True)
    score15 = models.IntegerField(null=True, blank=True)
    score16 = models.IntegerField(null=True, blank=True)
    score17 = models.IntegerField(null=True, blank=True)
    score18 = models.IntegerField(null=True, blank=True)
    score_in = models.IntegerField(blank=True)

    @property
    def get_score_in(self):
        scores = [getattr(self, f'score{i}') for i in range(10, 19)]
        if any([s is None for s in scores]):
            return 0
        return sum(scores)

    gross = models.IntegerField(blank=True)

    @property
    def get_gross(self):
        return self.score_out + self.score_in

    differential = models.FloatField(blank=True, null=True)

    @property
    def get_differential(self):
        if self.differential is not None:
            return self.differential
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

    def to_dict(self):
        return {
            'tee': self.tee,
            'user': self.user,
            'date': self.date,
            'course_handicap': self.course_handicap,
            'score1': self.score1,
            'score2': self.score2,
            'score3': self.score3,
            'score4': self.score4,
            'score5': self.score5,
            'score6': self.score6,
            'score7': self.score7,
            'score8': self.score8,
            'score9': self.score9,
            'score_out': self.score_out,
            'score10': self.score10,
            'score11': self.score11,
            'score12': self.score12,
            'score13': self.score13,
            'score14': self.score14,
            'score15': self.score15,
            'score16': self.score16,
            'score17': self.score17,
            'score18': self.score18,
            'score_in': self.score_in,
            'gross': self.gross,
            'differential': self.differential,
        }


class HandicapHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    handicap = models.FloatField()
    trigger_round = models.ForeignKey(Round, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.date}'


@receiver(post_save, sender=Round, dispatch_uid="update_handicap")
def update_handicap(sender, instance, created, **kwargs):
    if not created:
        return

    # First combine any nine hole rounds if possible
    if instance.nine_holes:
        nine_hole_round = Round.objects.filter(
            ~models.Q(id=instance.id),
            tee__holes__in=['F', 'B'], nh_already_used=False)
        # If there's no other nine-hole rounds, we can't update handicap
        if not nine_hole_round:
            return

        other_nine_holes = nine_hole_round.order_by('-date').first()
        tee = Tee.objects.get(course__name='Nine-Hole Combined')

        new_attrs = {
            'tee': tee, 'nine_holes_combined': True, 'date': instance.date,
            'user': instance.user, 'differential':
                instance.differential + other_nine_holes.differential}
        if instance.tee.holes == 'F':
            new_attrs.update({f'score{i + 9}': getattr(instance, f'score{i}')
                              for i in range(1, 10)})
            new_attrs['score_in'] = instance.score_out
        else:
            new_attrs.update({f'score{i}': getattr(instance, f'score{i}')
                              for i in range(10, 19)})
            new_attrs['score_in'] = instance.score_in
        if other_nine_holes.tee.holes == 'F':
            new_attrs.update({
                f'score{i}': getattr(other_nine_holes, f'score{i}')
                for i in range(1, 10)})
            new_attrs['score_out'] = other_nine_holes.score_out
        else:
            new_attrs.update({
                f'score{i - 9}': getattr(other_nine_holes, f'score{i}')
                for i in range(10, 19)})
            new_attrs['score_out'] = other_nine_holes.score_in

        new_attrs['gross'] = new_attrs['score_out'] + new_attrs['score_in']
        new_round = Round(**new_attrs)
        new_round.save()

        instance.nh_already_used = True
        other_nine_holes.nh_already_used = True
        instance.save()
        other_nine_holes.save()

    rounds = Round.objects.filter(user=instance.user, tee__holes='T')

    # Check if an exceptional score adjustment is needed - section 5.9
    if instance.current_handicap is not None:
        if instance.current_handicap - instance.differential > 7:
            exceptional_adjustment = (
                -2 if instance.current_handicap - instance.differential > 10
                else -1)
            for round_ in rounds.order_by('-date')[:20]:
                round_.differential += exceptional_adjustment
                round_.save()
            rounds = Round.objects.filter(user=instance.user, tee__holes='T')

    num_rounds = len(rounds)
    if num_rounds < 3:  # Cannot create handicap before 3 rounds entered
        return
    elif num_rounds < 20:  # Use modified calc until 20 rounds entered
        round_count = initial_handicap_adjustments[num_rounds]['count']
        adjustment = initial_handicap_adjustments[num_rounds]['adjustment']
        low = None
    else:  # Standard calc uses 8 of last 20, no adjustment
        rounds = rounds.order_by('-date')[:20]
        round_count = 8
        adjustment = 0
        low = HandicapHistory.objects.filter(
            user=instance.user,
            date__gte=datetime.datetime.now() - datetime.timedelta(days=365)
        ).order_by('handicap').first().handicap

    counted_rounds = rounds.order_by('differential')[:round_count]
    handicap = (sum([r.differential for r in counted_rounds]) /
                round_count + adjustment)
    handicap = min(handicap, 54.0)

    if low is not None:
        # Apply soft and hard caps - section 5.8
        diff = handicap - low
        if diff > 5:
            handicap = low + 5
        elif diff > 3:
            handicap = low + 3 + (diff - 3) / 2

    new_handicap = HandicapHistory(
        user=instance.user, date=instance.date, handicap=handicap,
        trigger_round=instance)
    new_handicap.save()

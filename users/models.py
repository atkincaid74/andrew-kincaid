import datetime

from django.utils import timezone
from django.db import models


class ValidEmail(models.Model):
    email = models.EmailField()
    paid = models.BooleanField()
    date_added = models.DateTimeField()
    date_paid = models.DateTimeField(null=True)

    def add_email(self, email, paid: bool = False):
        self.email = email.lower()
        self.paid = paid
        self.date_added = timezone.now()
        self.date_paid = timezone.now() if paid else None

        self.save()

    def __str__(self):
        return self.email

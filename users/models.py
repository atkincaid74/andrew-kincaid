import datetime

from django.utils import timezone
from django.db import models


class ValidEmails(models.Model):
    email = models.EmailField()
    paid = models.BooleanField()
    date_added = models.DateTimeField()
    date_paid = models.DateTimeField()

    def __str__(self):
        return self.email

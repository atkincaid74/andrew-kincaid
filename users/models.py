from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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


class PrivilegeLookup(models.Model):
    privilege = models.TextField(max_length=32)

    def add_privilege(self, privilege):
        self.privilege = privilege

        self.save()

    def __str__(self):
        return self.privilege


class UserPrivilege(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    privilege = models.ForeignKey(PrivilegeLookup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.privilege.privilege}"


class EmailPrivilege(models.Model):
    email = models.ForeignKey(ValidEmail, on_delete=models.CASCADE)
    privilege = models.ForeignKey(PrivilegeLookup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email} - {self.privilege.privilege}"

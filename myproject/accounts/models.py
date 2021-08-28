from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.dispatch import receiver

from myproject.core.models import TimeStampedModel

from .signals import user_login_password_failed

# https://stackoverflow.com/a/37620866/802542


class AuditEntry(TimeStampedModel):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return f'{self.action}-{self.username}-{self.ip}'

    def __str__(self):
        return f'{self.action}-{self.username}-{self.ip}'


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(
        action='user_logged_in',
        ip=ip, username=user.username
    )


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(
        action='user_logged_out',
        ip=ip, username=user.username
    )


@receiver(user_login_password_failed)
def user_login_failed_callback(sender, **kwargs):
    user = kwargs['user']
    AuditEntry.objects.create(
        action='user_login_password_failed',
        username=user.username
    )

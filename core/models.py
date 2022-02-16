import logging
import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


notification_logger = logging.getLogger('notification_logger')


class User(AbstractUser):
    language = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES, default='en')
    timezone = models.CharField(
        _("timezone"), max_length=100, choices=[(i, i) for i in pytz.common_timezones], default="UTC"
    )

    def save(self, **kwargs):
        is_new = not self.pk
        super().save(**kwargs)
        if is_new:
            __ = Token.objects.get_or_create(user=self)

from django.conf import settings
from django.db import models
# Create your models here.


class Resume(models.Model):
    card = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='resume_set')

    def __str__(self):
        return self.card

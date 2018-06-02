from django.db import models


class Feed(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):
    card = models.CharField(max_length=20)
    element = models.CharField(max_length=20)
    amount = models.CharField(max_length=20)

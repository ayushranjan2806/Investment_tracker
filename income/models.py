from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Income(models.Model):
    amount = models.FloatField()
    date =models.DateField(default=())
    description = models.TextField(blank=True)
    owner =models.ForeignKey(to= User, on_delete=models.CASCADE)
    source =models.CharField(max_length=250)
    def __str__(self):
        return self.source


class Source(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-name']


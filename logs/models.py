from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    name = models.CharField(max_length=30)
    reps = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    @classmethod
    def create(cls, name, reps):
        workout = cls(name=name, reps=reps)
        return workout


class Log(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=30)
    workouts = models.ManyToManyField(Workout)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    name = models.CharField(max_length=30)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    last_date_added = models.DateField(auto_now=True, editable=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def create(cls, name, sets, reps):
        workout = cls(name=name, sets=sets, reps=reps)
        return workout


class Log(models.Model):
    date = models.DateField(default=datetime.now, blank=True)
    name = models.CharField(max_length=30)
    workouts = models.ManyToManyField(Workout)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    logs = models.ManyToManyField(Log, related_name="profile", blank=True)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.user.username

from django.db import models


class Workout(models.Model):
    name_of_workout = models.CharField(max_length=30)
    reps = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name_of_workout

    @classmethod
    def create(cls, name_of_workout, reps):
        workout = cls(name_of_workout=name_of_workout, reps=reps)
        return workout


class Log(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=30)
    workouts = models.ManyToManyField(Workout)

    @classmethod
    def create(cls):
        log = cls()
        return log

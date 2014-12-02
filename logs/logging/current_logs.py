from django.http import HttpResponseRedirect
from django.shortcuts import render

from logs.models import Log, Workout


class CurrentLogs(object):

    def add_to_existing_log(self, request):
        workout = Workout.create(request['workout'], request['reps'])
        workout.save()
        if request.get('log_dropdown'):
            log = Log.objects.get(name=request['log_dropdown'])
            log.workouts.add(workout)
        else:
            log = Log.objects.get(pk=request['log'])
            log.workouts.add(workout)
            return log

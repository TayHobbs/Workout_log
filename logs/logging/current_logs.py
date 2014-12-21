from logs.models import Log, Workout


class CurrentLogs(object):

    def add_to_existing_log(self, request):
        workout = Workout.create(name=request['workout'], sets=request["sets"], reps=request['reps'])
        workout.save()
        if request.get('log_dropdown'):
            log = Log.objects.get(name=request['log_dropdown'])
            log.workouts.add(workout)
        else:
            log = Log.objects.get(pk=request['log'])
            log.workouts.add(workout)
        return log

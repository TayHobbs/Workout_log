from logs.models import UserProfile
from logs.serializers import WorkoutSerializer


class PreviousWorkouts(object):

    def show_recently_used_workouts(self, user):
        profile = UserProfile.objects.get(user=user)
        logs = profile.logs.all().order_by("-date")
        workouts = []
        for log in logs:
            for workout in log.workouts.all().order_by("-last_date_added"):
                workout = WorkoutSerializer(workout)
                workouts.append(workout.data)
        return workouts[:20]

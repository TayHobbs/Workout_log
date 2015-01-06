from django.contrib.auth.models import User

from rest_framework import serializers

from logs.models import Log, Workout, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "logs",
            "profile_picture",
            "twitter",
            "facebook",
            "website"
        )


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ("id", "name", "date", "workouts")


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ("id", "name", "sets", "reps")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "userprofile", "email")

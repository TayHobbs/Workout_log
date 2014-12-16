from django.contrib import admin
from logs.models import Workout, Log, UserProfile

admin.site.register(Workout)
admin.site.register(Log)
admin.site.register(UserProfile)

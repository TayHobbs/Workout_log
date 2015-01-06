from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from rest_framework import viewsets, generics, filters

from logs.forms import UserForm
from logs.models import Workout, Log, UserProfile
from logs.serializers import (
    LogSerializer, UserProfileSerializer, WorkoutSerializer)
from logs.logging.current_logs import CurrentLogs
from logs.logging.search import Search
from logs.logging.profile import ProfileNotFound, ProfileManager


class Logs(View):

    def get(self, request):
        if request.user.is_authenticated():
            logs = UserProfile.objects.get(
                user=request.user).logs.all().order_by("-date")
            return render(request, "logs/logs.html", {"logs": logs})
        else:
            return HttpResponse("You are not signed in")


class Signup(View):

    def post(self, request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                new_user.set_password(new_user.password)
                new_user.save()
                UserProfile.objects.create(user=new_user)
                new_user = authenticate(username=form.cleaned_data["username"],
                                        password=form.cleaned_data["password"])
                login(request, new_user)
                return HttpResponseRedirect(reverse("logs"))
            else:
                return self.get(request, form)
        return self.get(request)

    def get(self, request, form=UserForm()):
        return render_to_response(
            "logs/signup.html", {"user_form": form}
        )


class UserLogin(View):

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("logs"))
            else:
                error = "Your account is disabled"
                return render(request, "logs/login.html", {"error": error})
        else:
                error = "Invalid login details"
                return render(request, "logs/login.html", {"error": error})

    def get(self, request):
        return render(request, "logs/login.html")


class Detail(View):

    def get(self, request, log_id):
        if request.user.is_authenticated():
            try:
                log = Log.objects.get(pk=log_id)
                return render(request, "logs/detail.html", {"log": log})
            except:
                return render(request, "errors/404.html")
        else:
            return HttpResponseRedirect(reverse("index"))


class AddToLog(View):

    def post(self, request):
        log = CurrentLogs().add_to_existing_log(request.POST)
        return HttpResponseRedirect(reverse("detail", args=(log.id,)))


class CreateNewLog(View):

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        workout = Workout.create(
            request.POST["workout"],
            request.POST["sets"],
            request.POST["reps"]
        )
        workout.save()
        log = Log.objects.create(name=request.POST["log"])
        log.workouts.add(workout)
        profile.logs.add(log)
        return HttpResponseRedirect(reverse("logs"))


class Account(View):

    def __init__(self):
        self.account_manager = ProfileManager()

    def get(self, request):
        account = UserProfile.objects.get(user=request.user)
        return render(request, "logs/account.html", {"account": account})

    def post(self, request):
        account = UserProfile.objects.get(user=request.user)
        if request.FILES:
            self.account_manager.change_profile_pic(
                account,
                request.FILES["image"]
            )
        return render(request, "logs/account.html", {"account": account})


class Profile(View):

    def get(self, request, username):
        try:
            profile = UserProfile.objects.get(user__username=username)
            return render(request, "logs/profile.html", {"profile": profile})
        except ProfileNotFound:
            return render(request, "errors/404.html")


class SearchLogs(View):

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        context = RequestContext(request)
        search = request.GET["suggestion"]
        logs = Search().search_logs(profile, 8, search)
        return render_to_response(
            "logs/_log_list.html", {"logs": logs}, context
        )


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    return render(request, "logs/index.html")


class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class WorkoutAPIView(generics.ListAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'sets')

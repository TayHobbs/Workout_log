from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import viewsets

from logs.forms import UserForm
from logs.models import Workout, Log, UserProfile
from logs.serializers import LogSerializer, UserSerializer, UserProfileSerializer, WorkoutSerializer
from logs.logging.current_logs import CurrentLogs


def index(request):
    return render(request, "logs/index.html")


def logs(request):
    if request.user.is_authenticated():
        logs = UserProfile.objects.get(user=request.user).logs.all().order_by("-date")
        return render(request, "logs/logs.html", {"logs": logs})
    else:
        return HttpResponse("You are not signed in")


def signup(request):
    context = RequestContext(request)
    registered = False
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
        form = UserForm()
    return render_to_response(
        "logs/signup.html",
        {"user_form": form, "registered": registered},
        context
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("logs"))
            else:
                return HttpResponse("Your account is disabled")
        else:
            return render(request, "logs/login.html")
    else:
        return render(request, "logs/login.html")


def detail(request, log_id):
    if request.user.is_authenticated():
        try:
            log = Log.objects.get(pk=log_id)
            return render(request, "logs/detail.html", {"log": log})
        except:
            return render(request, "errors/404.html")
    else:
        return HttpResponseRedirect(reverse("index"))


def add_to_log(request):
    log = CurrentLogs().add_to_existing_log(request.POST)
    return HttpResponseRedirect(reverse("detail", args=(log.id,)))


def create_new_log(request):
    profile = UserProfile.objects.get(user=request.user)
    workout = Workout.create(request.POST["workout"], request.POST["sets"], request.POST["reps"])
    workout.save()
    log = Log.objects.create(name=request.POST["log"])
    log.workouts.add(workout)
    profile.logs.add(log)
    return HttpResponseRedirect(reverse("logs"))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        return render(request, "logs/profile.html", {"profile": profile})
    except:
        return render("errors/404.html")


class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class WorkoutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

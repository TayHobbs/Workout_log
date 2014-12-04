from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from logs.forms import UserForm
from logs.models import Workout, Log
from logs.logging.current_logs import CurrentLogs


def index(request):
    return render(request, 'logs/index.html')


def logs(request):
    if request.user.is_authenticated():
        logs = Log.objects.filter(user=request.user)
        return render(request, 'logs/logs.html', {'logs': logs})
    else:
        return HttpResponse("You are not signed in")


def signup(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(new_user.password)
            new_user.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
            return HttpResponseRedirect("/logs/")
    else:
        form = UserForm()
    return render_to_response(
        'logs/signup.html',
        {'user_form': form, 'registered': registered},
        context
    )


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/logs')
            else:
                return HttpResponse("Your account is disabled")
        else:
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'logs/login.html')


def detail(request, log_id):
    if request.user.is_authenticated():
        log = Log.objects.get(pk=log_id)
        return render(request, 'logs/detail.html', {'log': log})
    else:
        return HttpResponseRedirect('/')


def add_to_log(request):
    log = CurrentLogs().add_to_existing_log(request.POST)
    return HttpResponseRedirect(reverse('detail', args=(log.id,)))


def create_new_log(request):
    workout = Workout.create(request.POST['workout'], request.POST['reps'])
    workout.save()
    log = Log.objects.create(user=request.user, name=request.POST['log'])
    log.workouts.add(workout)
    return HttpResponseRedirect(reverse('logs'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

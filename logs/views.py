from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from logs.forms import UserForm
from logs.models import Workout, Log


def index(request):
    return render(request, 'logs/index.html')


def logs(request):
    logs = Log.objects.all()
    return render(request, 'logs/logs.html', {'logs': logs})


def signup(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render_to_response(
        'logs/signup.html',
        {'user_form': user_form, 'registered': registered},
        context
    )

    return render(request, 'logs/signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid login details: {}, {}".format(username, password)
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'logs/login.html')


def detail(request, log_id):
    log = Log.objects.get(pk=log_id)
    return render(request, 'logs/detail.html', {'log': log})


def create(request, log_id):
    workout = Workout.create(request.POST['workout'], request.POST['reps'])
    workout.save()
    log = Log.objects.create()
    log.workouts.add(workout)
    return HttpResponseRedirect(reverse('logs'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

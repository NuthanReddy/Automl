from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf

from mlearn.backend import UserAuth
from .forms import SubmitModel, RegistrationForm, EditProfileForm
from .models import *

ACCEPTED_FILE_TYPES = ['csv']


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        competitions = Competition.objects.all()
        query = request.GET.get("q")
        if query:
            competitions = competitions.filter(Q(comp_name__icontains=query) | Q(comp_desc__icontains=query)).distinct()
            return render(request, 'mlearn/index.html', {
                'competitions': competitions,
            })
        else:
            return render(request, 'mlearn/index.html', {'competitions': competitions})


def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'mlearn/login.html', c)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = UserAuth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                UserAuth.login(user)
                return render(request, 'mlearn/index.html')
            else:
                return render(request, 'mlearn/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'mlearn/login.html', {'error_message': 'Invalid login'})
    return render(request, 'mlearn/login.html')


def logout_user(request):
    logout(request)
    form = RegistrationForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'mlearn/login.html', context)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/mlearn')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'mlearn/register.html', args)


def detail(request, competition_id):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        competition = get_object_or_404(Competition, pk=competition_id)
        return render(request, 'mlearn/detail.html', {'competition': competition, })


def data(request, competition_id):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        competition = get_object_or_404(Competition, pk=competition_id)
        return render(request, 'mlearn/data.html', {'competition': competition, })


def score(request, competition_id):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        competition = get_object_or_404(Competition, pk=competition_id)
        return render(request, 'mlearn/score.html', {'competition': competition, })


def submit(request, competition_id):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        competition = get_object_or_404(Competition, pk=competition_id)
        return render(request, 'mlearn/submit.html', {'competition': competition, })


def model_upload(request):
    if request.method == 'POST':
        form = SubmitModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            competition = get_object_or_404(Competition, pk=id)
            return render(request, 'mlearn/submit.html', {'competition': competition,})
    else:
        form = SubmitModel()
    return render(request, 'mlearn/submit.html', {
        'form': form
    })


@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'mlearn/view_profile.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('mlearn:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'mlearn/edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('mlearn:view_profile'))
        else:
            message = {'message': "Password is invalid"}
            return redirect(reverse('mlearn:change_password'), message)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'mlearn/change_password.html', args)

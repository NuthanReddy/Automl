from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from comp.models import Registration, Competition, Submission
from .forms import SubmitModel

ACCEPTED_FILE_TYPES = ['csv']


@login_required
def index(request):
    competitions = Competition.objects.all()
    registrations = Registration.objects.all()
    return render(request, 'comp/index.html', {'competitions': competitions, 'registrations': registrations,})


@login_required
def detail(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    try:
        registered = Registration.objects.get(comp=competition, user=request.user)
    except Registration.DoesNotExist:
        registered = False
    return render(request, 'comp/detail.html', {'competition': competition, 'registered': registered,})


@login_required
def data(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'comp/data.html', {'competition': competition,})


@login_required
def score(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    subs = Submission.objects.filter(comp=competition).order_by('score').reverse()
    user = request.user
    if request.method == 'GET':
        try:
            registered = Registration.objects.get(comp=competition, user=user)
        except Registration.DoesNotExist:
            registered = False
        args = {'competition': competition, 'registered': registered, 'user': user, 'submissions': subs}
        return render(request, 'comp/score.html', args)
    elif request.method == 'POST':
        return render(request, 'comp/submit.html', {'competition': competition, 'user': user,})


@login_required
def register(request, competition_id):
    comp = get_object_or_404(Competition, pk=competition_id)
    regn = Registration.objects.get_or_create(comp=comp, user=request.user)
    return render(request, 'comp/detail.html', {'competition': comp, 'registered': regn})


@login_required
def submit(request, competition_id):
    user = request.user
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'comp/submit.html', {'competition': competition, 'user': user,})


@login_required
def model_upload(request):
    if request.method == 'POST':
        form = SubmitModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            competition = get_object_or_404(Competition, pk=id)
            return render(request, 'comp/submit.html', {'competition': competition,})
    else:
        form = SubmitModel()
    return render(request, 'comp/submit.html', {'form': form})

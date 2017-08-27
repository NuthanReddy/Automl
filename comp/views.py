from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .forms import SubmitModel
from .models import *

ACCEPTED_FILE_TYPES = ['csv']


@login_required
def index(request):
    competitions = Competition.objects.all()
    query = request.GET.get("q")
    if query:
        competitions = competitions.filter(Q(comp_name__icontains=query) | Q(comp_desc__icontains=query)).distinct()
        return render(request, 'comp/index.html', {
            'competitions': competitions,
        })
    else:
        return render(request, 'comp/index.html', {'competitions': competitions})


@login_required
def detail(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'comp/detail.html', {'competition': competition,})


@login_required
def data(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'comp/data.html', {'competition': competition,})


@login_required
def score(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'comp/score.html', {'competition': competition,})


@login_required
def submit(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'comp/submit.html', {'competition': competition,})


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

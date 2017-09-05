from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from comp.forms import SubmitForm
from comp.models import Registration, Competition, Submission

# from pyspark.sql import SparkSession

ACCEPTED_FILE_TYPES = ['csv']


# spark = SparkSession \
#    .builder \
#    .appName("Data Crunch") \
#    .config("spark.some.config.option", "some-value") \
#    .getOrCreate()

# df = spark.read.csv.options(header='true', inferSchema='true').load("examples/src/main/resources/people.json")


def index(request):
    competitions = Competition.objects.all()
    return render(request, 'comp/index.html', {'competitions': competitions})


def detail(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'comp/detail.html', {'competition': competition})


def data(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'comp/data.html', {'competition': competition})


def score(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    subs = Submission.objects.filter(comp=competition).order_by('score').reverse()
    if request.method == 'GET':
        args = {'competition': competition, 'submissions': subs}
        return render(request, 'comp/score.html', args)
    elif request.method == 'POST':
        return render(request, 'comp/submit.html', {'competition': competition})


@login_required
def register(request, competition_id):
    comp = get_object_or_404(Competition, pk=competition_id)
    regn = Registration.objects.get_or_create(comp=comp, user=request.user)
    return render(request, 'comp/detail.html', {'competition': comp, 'registered': regn})


@login_required
def submit(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    if request.method == 'GET':
        form = SubmitForm()
        args = {'form': form, 'competition': competition}
        return render(request, 'comp/submit.html', args)
    elif request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            newsub = form.save(commit=False)
            file_type = newsub.file_submission.url.split('.')[-1].lower()
            if file_type not in ACCEPTED_FILE_TYPES:
                args = {
                    'form': form,
                    'competition': competition,
                    'error_message': 'File must be in CSV format',
                }
                return render(request, 'comp/submit.html', args)
            newsub.file_submission = request.FILES['file_submission']
            newsub.user = request.user
            newsub.comp = competition
            newsub.language = form.cleaned_data['language']
            newsub.algo = form.cleaned_data['algo']
            newsub.score = 0.5
            newsub.save()
            # need to change
            subs = Submission.objects.filter(comp=newsub.comp).order_by('score').reverse()
            return render(request, 'comp/score.html', {'competition': competition, 'submissions': subs})
        else:
            args = {'form': form}
            return render(request, 'comp/submit.html', args)


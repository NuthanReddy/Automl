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
        return render(request, 'comp/submit.html', {'competition': competition})


@login_required
def register(request, competition_id):
    comp = get_object_or_404(Competition, pk=competition_id)
    regn = Registration.objects.get_or_create(comp=comp, user=request.user)
    return render(request, 'comp/detail.html', {'competition': comp, 'registered': regn})


@login_required
def submit(request, competition_id):
    if request.method == 'GET':
        form = SubmitForm()
        args = {'form': form}
        return render(request, 'comp/submit.html', args)
    elif request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            newsub = form.save(commit=False)
            file_type = newsub.file_submission.url.split('.')[-1].lower()
            if file_type not in ACCEPTED_FILE_TYPES:
                args = {
                    'form': form,
                    'error_message': 'File must be in CSV format',
                }
                return render(request, 'comp/submit.html', args)
            newsub.file_submission = request.FILES['file_submission']
            newsub.user = request.user
            newsub.comp = get_object_or_404(Competition, pk=competition_id)
            newsub.language = form.cleaned_data['language']
            newsub.algo = form.cleaned_data['algo']
            newsub.score = 0.5
            newsub.save()
            # need to change
            subs = Submission.objects.filter(comp=newsub.comp).order_by('score').reverse()
            try:
                registered = Registration.objects.get(comp=newsub.comp, user=request.user)
            except Registration.DoesNotExist:
                registered = False
            return render(request, 'comp/score.html', {'competition': newsub.comp, 'user': request.user,
                                                       'registered': registered, 'submissions': subs})
        else:
            args = {'form': form,}
            return render(request, 'comp/submit.html', args)


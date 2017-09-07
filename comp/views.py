from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from comp.forms import SubmitForm
from comp.models import Registration, Competition, Submission
from pandas import read_table
from sklearn.metrics import mean_squared_error

ACCEPTED_FILE_TYPES = ['csv']


# from pyspark.sql import SparkSession
# spark = SparkSession \
#    .builder \
#    .appName("Data Crunch") \
#    .config("spark.some.config.option", "some-value") \
#    .getOrCreate()

# spark = SparkSession.builder.master("local").appName("Data Crunch").\
#    config("spark.sql.warehouse.dir", "hdfs://localhost:8020/user/spark/warehouse").getOrCreate()

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
    global scr
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
                    'form': form, 'competition': competition,
                    'error_message': 'File must be in CSV format'}
                return render(request, 'comp/submit.html', args)
            newsub.file_submission = request.FILES['file_submission']
            newsub.user = request.user
            newsub.comp = competition
            newsub.language = form.cleaned_data['language']
            newsub.algo = form.cleaned_data['algo']
            # score calculation
            header = 0
            sep = ','
            index_col = None
            scoring_formula = "RMSE"
            predict_path = newsub.file_submission
            p_table = read_table(predict_path, header=header, index_col=index_col, sep=sep, skiprows=0,
                                 nrows=None, skip_blank_lines=True)
            pcols = p_table.columns
            if scoring_formula == "RMSE":
                valid_path = competition.valid
                v_table = read_table(valid_path, header=header, index_col=index_col, sep=sep, skiprows=0,
                                     nrows=None, skip_blank_lines=True)
                vcols = v_table.columns
                if pcols.all() == vcols.all():
                    newsub.score = round(1 / mean_squared_error(v_table, p_table, multioutput='raw_values')[-1], 2)
                else:
                    args = {'form': form, 'competition': competition,
                            'error_message': 'Header Columns does not match in uploaded submission'}
                    return render(request, 'comp/submit.html', args)
            newsub.save()
            subs = Submission.objects.filter(comp=newsub.comp).order_by('score').reverse()
            return render(request, 'comp/score.html', {'competition': competition, 'submissions': subs})
        else:
            args = {'form': form}
            return render(request, 'comp/submit.html', args)


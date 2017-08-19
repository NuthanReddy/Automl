from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .forms import UserForm, DatasetForm
from .models import *
from pandas import read_csv
from django.contrib.auth.models import User

ACCEPTED_FILE_TYPES = ['csv']


def create_dataset(request):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        form = DatasetForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.user = request.user
            file_type = dataset.data_file.url.split('.')[-1].lower()
            if file_type not in ACCEPTED_FILE_TYPES:
                context = {
                    'dataset': dataset,
                    'form': form,
                    'error_message': 'File must be CSV or TXT format',
                }
                return render(request, 'mlearn/create_dataset.html', context)
            dataset.data_file = request.FILES['data_file']
            dataset.file_path = dataset.data_file.url
            dataset.file_name = dataset.file_path.split('/')[-1].split('.')[0]
            dataset.file_type = file_type
            dataset.save()
            name = dataset.file_name
            url = 'http://127.0.0.1:8000' + dataset.file_path
            dframe = read_csv(url, header=0, parse_dates=True) \
                .to_html(bold_rows=True, classes=["table table-striped", "table table-bordered", "table table-hover"])
            return render(request, 'mlearn/show_dataset.html', {'dframe': dframe, 'name': name})
        context = {
            "form": form,
        }
        return render(request, 'mlearn/create_dataset.html', context)


def delete_dataset(request, dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)
    dataset.delete()
    datasets = Dataset.objects.filter(user=request.user)
    return render(request, 'mlearn/index.html', {'datasets': datasets})


def show_dataset(request, dataset_id):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        dataset = Dataset.objects.get(pk=dataset_id)
        name = dataset.file_name
        url = 'http://127.0.0.1:8000' + dataset.file_path
        dframe = read_csv(url, header=0, parse_dates=True)\
            .to_html(bold_rows=True, classes=["table table-striped", "table table-bordered", "table table-hover"])
        return render(request, 'mlearn/show_dataset.html', {'dframe': dframe, 'name': name})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        users = User.objects.all()
        competitions = Competition.objects.all()
        # albums = Album.objects.all()
        #song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            competitions = competitions.filter(
                Q(comp_name__icontains=query) |
                Q(comp_desc__icontains=query)
            ).distinct()
            return render(request, 'mlearn/index.html', {
                'competitions': competitions,
            })
        else:
            return render(request, 'mlearn/index.html', {'competitions': competitions})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                datasets = Dataset.objects.filter(user=request.user)
                return render(request, 'mlearn/index.html', {'datasets': datasets})
            else:
                return render(request, 'mlearn/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'mlearn/login.html', {'error_message': 'Invalid login'})
    return render(request, 'mlearn/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'mlearn/login.html', context)


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                datasets = Dataset.objects.filter(user=request.user)
                return render(request, 'mlearn/index.html', {'datasets': datasets})
    context = {
        "form": form,
    }
    return render(request, 'mlearn/register.html', context)


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

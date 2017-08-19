from django.contrib.auth.models import Permission, User
from django.db import models

COMP_STATUS = (('A', 'Active'), ('C', 'Closed'))
CRITERIA = (('D', 'Desc'), ('A', 'Asc'))
LANG = (('Python', 'Python'), ('C', 'C'), ('C++', 'C++'), ('R', 'R'), ('Python3', 'Python3'), ('Scala', 'Scala'))
ALGO = (('Reg', 'Regression'), ('LogReg', 'Logistic Regression'), ('RandF', 'Random Forest'),
        ('KNN', 'K - Nearest Neighbour'), ('NN', 'Neural Networks'), ('ACO', 'Ant Colony Optimization'),
        ('SVM', 'Support Vector Machines'), ('PSA', 'Particle Swarm Algorithm'))


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    mail_id = models.EmailField(max_length=100)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    rank = models.IntegerField()
    points = models.DecimalField(max_digits=100, decimal_places=2)


class Team(models.Model):
    user = models.ForeignKey(User)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Competition(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000)
    logo = models.FileField(default='')
    team_size = models.IntegerField(default=1)
    status = models.CharField(default="Active", max_length=1, choices=COMP_STATUS)
    start = models.DateTimeField()
    end = models.DateTimeField()
    sample = models.FileField()
    train = models.FileField(default='')
    test = models.FileField(default='')
    train2 = models.FileField(default='')
    test2 = models.FileField(default='')
    valid = models.FileField(default='')
    scoring_formula = models.CharField(max_length=1000)
    criteria = models.CharField(default="Desc", max_length=1, choices=CRITERIA)
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()
    prize4 = models.IntegerField()
    prize5 = models.IntegerField()
    prize6 = models.IntegerField()
    prize7 = models.IntegerField()
    prize8 = models.IntegerField()
    prize9 = models.IntegerField()
    prize10 = models.IntegerField()


class Submission(models.Model):
    team = models.ForeignKey(Team)
    comp = models.ForeignKey(Competition)
    id = models.IntegerField()
    time = models.DateTimeField()
    score = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    rank = models.IntegerField(default=9999)
    language = models.CharField(default="Python", max_length=1, choices=LANG)
    algo = models.CharField(default="Reg", max_length=100, choices=ALGO)


class Dataset(models.Model):
    user = models.ForeignKey(User)
    data_id = models.IntegerField()
    data_file = models.FileField(default='')
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=250)
    file_type = models.CharField(max_length=50)

    def __str__(self):
        return self.file_name

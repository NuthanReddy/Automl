from django.contrib.auth.models import User, AbstractBaseUser
from django.db import models
from django.utils import timezone

COMP_STATUS = (('A', 'Active'), ('C', 'Closed'))
CRITERIA = (('D', 'Desc'), ('A', 'Asc'))
LANG = (('Python', 'Python'), ('C', 'C'), ('C++', 'C++'), ('R', 'R'), ('Python3', 'Python3'), ('Scala', 'Scala'))
ALGO = (('Reg', 'Regression'), ('LogReg', 'Logistic Regression'), ('RandF', 'Random Forest'),
        ('KNN', 'K - Nearest Neighbour'), ('NN', 'Neural Networks'), ('ACO', 'Ant Colony Optimization'),
        ('SVM', 'Support Vector Machines'), ('PSA', 'Particle Swarm Algorithm'), ('Oth', 'Other'))


class Team(models.Model):
    user = models.ManyToManyField(User)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(default='', max_length=50)
    lead = models.CharField(max_length=50)
    member = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000)
    logo = models.FileField(default='')
    team_size = models.IntegerField(default=1)
    status = models.CharField(default="Active", max_length=1, choices=COMP_STATUS)
    start = models.DateTimeField(default=timezone.now, blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    sample = models.FileField(default='', blank=True, null=True)
    train = models.FileField(default='')
    test = models.FileField(default='')
    train2 = models.FileField(default='', blank=True, null=True)
    test2 = models.FileField(default='', blank=True, null=True)
    valid = models.FileField(default='', blank=True, null=True)
    scoring_formula = models.Expression()
    gold = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)
    bronze = models.IntegerField(default=0)
    prize4 = models.IntegerField(default=0)
    prize5 = models.IntegerField(default=0)
    prize6 = models.IntegerField(default=0)
    prize7 = models.IntegerField(default=0)
    prize8 = models.IntegerField(default=0)
    prize9 = models.IntegerField(default=0)
    prize10 = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Submission(models.Model):
    file_submission = models.FileField(default='', blank=False, null=False)
    team = models.ForeignKey(Team)
    comp = models.ForeignKey(Competition)
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    score = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    language = models.CharField(default="Python", max_length=100, choices=LANG)
    algo = models.CharField(default="Reg", max_length=100, choices=ALGO)

    def __str__(self):
        return self.team.name + ' ' + self.comp.name


class Registration(models.Model):
    user = models.ForeignKey(User)
    comp = models.ForeignKey(Competition)

    def __str__(self):
        return self.user.username + ' ' + self.comp.name

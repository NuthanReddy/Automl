from django.contrib.auth.models import Permission, User
from django.db import models


class Dataset(models.Model):
    user = models.ForeignKey(User)
    data_id = models.IntegerField(max_length=10)
    data_file = models.FileField(default='')
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=250)
    file_type = models.CharField(max_length=50)

    def __str__(self):
        return self.file_name


class Competition(models.Model):
    comp_id = models.CharField(max_length=10)
    comp_name = models.CharField(max_length=50)
    comp_desc = models.CharField(max_length=1000)
    comp_logo = models.FileField(default='')
    comp_train = models.FileField(default='')
    comp_test = models.FileField(default='')


class Leaderboard(models.Model):
    comp_id = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    rank = models.IntegerField(max_length=10)
    score = models.FloatField(max_length=10)
    entries = models.IntegerField(max_length=3)


class Team(models.Model):
    team_id = models.CharField(max_length=10)
    team_name = models.CharField(max_length=50)
    team_lead = models.ForeignKey(User)


class User(models.Model):
    user_id = models.CharField(max_length=10)
    mail_id = models.EmailField(max_length=100)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    rank = models.IntegerField(max_length=10)

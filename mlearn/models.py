from django.contrib.auth.models import Permission, User
from django.db import models


class Dataset(models.Model):
    user = models.ForeignKey(User, default=1)
    data_file = models.FileField(default='')
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=250)
    file_type = models.CharField(max_length=50)

    def __str__(self):
        return self.file_name


class Competition(models.Model):
    Comp_id = models.CharField(max_length=10)
    comp_name = models.CharField(max_length=50)
    comp_desc = models.CharField(max_length=1000)
    comp_logo = models.FileField(default='')
    comp_train = models.FileField(default='')
    comp_test = models.FileField(default='')


class Leaderboard(models.Model):
    user = models.ForeignKey(User, default=1)
    score = models.FloatField()
    entries_count = models.IntegerField(max_length=3)
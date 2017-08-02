from django.contrib import admin
from .models import Dataset
from .models import Competition
from .models import Leaderboard

admin.site.register(Dataset)
admin.site.register(Competition)
admin.site.register(Leaderboard)

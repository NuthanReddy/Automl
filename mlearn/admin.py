from django.contrib import admin

from .models import *

admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(Submission)
admin.site.register(Dataset)
admin.site.register(Registration)

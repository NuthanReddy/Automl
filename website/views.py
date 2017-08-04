from django.shortcuts import render, HttpResponseRedirect, redirect
from . import settings
import os


def getfile(request, file_name):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        url = os.path.join(settings.MEDIA_ROOT, file_name)
        print(url)
        return redirect(url)

import os

from django.shortcuts import render, redirect

from . import settings


def getfile(request, file_name):
    if not request.user.is_authenticated():
        return render(request, 'mlearn/login.html')
    else:
        url = os.path.join(settings.MEDIA_ROOT, file_name)
        print(url)
        return redirect(url)

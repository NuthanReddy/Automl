from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from accounts.forms import (
    RegistrationForm,
    EditProfileForm
)
from comp.models import Registration, Submission


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login'))
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
        regs = Registration.objects.all().filter(user=user)
        subs = Submission.objects.all().filter(user=user)
    else:
        user = request.user
        regs = Registration.objects.all().filter(user=user)
        subs = Submission.objects.all().filter(user=user)
    args = {'user': user, 'registrations': regs, 'submissions': subs,}
    return render(request, 'accounts/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

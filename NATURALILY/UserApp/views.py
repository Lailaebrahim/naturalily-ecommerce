from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, UpdateForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def signUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def logOutView(request):
    logout(request)
    return redirect('home')


@login_required
def userProfileView(request, pk):
    if request.method == 'POST':
        if request.user.pk != pk:
            raise PermissionDenied("You are not authorized to do this action.")
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('profile', pk=user.pk)
    else:
        form = UpdateForm(instance=request.user)
        form.fields['phone'].initial = request.user.shopUser.phone
    return render(request, 'UserApp/profile.html', {'form': form})


@login_required
def deleteProfile(request, pk):
    if request.user.pk != pk:
        raise PermissionDenied("You are not authorized to do this action.")
    request.user.shopUser.delete()
    request.user.delete()
    return redirect('home')

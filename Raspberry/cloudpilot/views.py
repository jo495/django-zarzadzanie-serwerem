import re
import subprocess
from django.shortcuts import render, get_object_or_404
from .models import Button
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users

@login_required(login_url='/login')
@allowed_users(allowed_roles=['IntUsers', 'ExtUsers'])
def button_list(request):
    buttons = Button.objects.all()
    return render(request, 'cloudpilot/button/list.html', {'buttons': buttons, 'userAccessLevel': request.user.customer.userAccessLevel })

@login_required(login_url='/login')
@allowed_users(allowed_roles=['IntUsers', 'ExtUsers'])
def turn_on(request, id):
    pushed_button = Button.objects.get(pk=id)

    if request.user.customer.userAccessLevel >= pushed_button.accessLevel:
        response = subprocess.Popen(pushed_button.command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        print(response)
        new_button = Button(pk=id, title=pushed_button.title, isOn=True, command=pushed_button.command, accessLevel=pushed_button.accessLevel)
        new_button.save()

    return HttpResponseRedirect('/')

@unauthenticated_user
def registerPage(request):
    #czyli jak ta funkcja dostanie żądanie get, to wyśle templata, a jak post, to stworzy użytkownika
    form = CreateUserForm()

    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Zarejestrowano pomyślnie")
            return HttpResponseRedirect('/login')

    context = {'form': form}
    return render(request, 'cloudpilot/accounts/register.html', context )

@unauthenticated_user
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # messages.success(request, "Witaj " + username)
            return HttpResponseRedirect('/')
        else:
            messages.info(request, 'Nazwa użytkownika lub hasło są nieprawidłowe')
            return HttpResponseRedirect('/login')

    context = {}
    return render(request, 'cloudpilot/accounts/login.html')


@login_required(login_url='/login')
def logoutPage(request):
    logout(request)
    return HttpResponseRedirect('/login')
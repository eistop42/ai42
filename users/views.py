from django.shortcuts import render, redirect
from django.contrib.auth import login as login_func, logout as logout_func

from .forms import LoginForm


def logout(request):

    logout_func(request)

    return redirect('/')

def login(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login_func(request, user)

            return redirect('/')

    context = {'form': form}

    return render(request, 'users/login.html', context)

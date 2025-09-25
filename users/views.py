from django.shortcuts import render

from .forms import LoginForm

def login(reqeust):

    form = LoginForm()
    context = {'form': form}

    return render(reqeust, 'users/login.html', context)

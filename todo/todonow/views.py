from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Todo
from django.contrib.auth.models import User


@login_required
def index(request):
    todo = Todo.objects.filter(user=request.user)
    print("hello")
    return render(request, 'home.html', context={'todo_entries': todo})

@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'home.html', context={'user': args})

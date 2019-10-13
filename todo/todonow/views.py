from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Todo


@login_required
def index(request):
    todo = Todo.objects.filter(user=request.user)
    return render(request, 'home.html', context={'todo_entries': todo})

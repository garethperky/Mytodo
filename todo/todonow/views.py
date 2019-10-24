from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Todo
from django.contrib.auth.models import User
import math
from .forms import TodoForm
from django.views.generic import UpdateView, ListView

def sum_total_values(user):
    values = Todo.objects.filter(
        user=user
    ).filter(completed = True)
    total_values = sum([entry.value for entry in values]) / 100
    return total_values

@login_required
def index(request):
    todo = Todo.objects.filter(user=request.user)
    net_value = sum_total_values(request.user)
    percentage = round(net_value * 100)
    if percentage > 100:
        percentage = 100
    return render(request, 'home.html', context={'todo_entries': todo, "percentage": percentage})

@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'home.html', context={'user': args})


@login_required
def todo_create_view(request):
    users = User.objects.filter(groups__name='Kids')
    form = TodoForm(request.POST)
    if form.is_valid():
        form.save()

    return render(request, 'create_todo.html', context={'form': form, 'users': users})

@login_required
def detail_view(UpdateView):
    model = Todo
    fields = ["user", 'title', 'description', 'value']

@login_required
def todo_group_view(request):
    users = User.objects.filter(groups__name='Kids')
    return render(request, 'overall.html', context = {'users': users})

@login_required
def todo_individual_view(request):
    users = User.objects.filter(groups__name='Kids')
    todo = Todo.objects.filter(pk=request.pk)
    return render(request, 'overall.html', context = {'users': users, 'todo': todo})

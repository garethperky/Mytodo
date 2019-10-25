from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Todo
from django.contrib.auth.models import User
import math
from .forms import TodoForm
from django.views.generic import UpdateView, ListView
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect

def sum_total_values(user):
    values = Todo.objects.filter(
        user=user
    ).filter(completed = True)
    total_values = sum([entry.value for entry in values]) / 100
    return total_values

@login_required
def index(request):
    if request.user.is_superuser:
        return redirect("/admin_homepage/")
    else:
        todo = Todo.objects.filter(user=request.user)
        net_value = sum_total_values(request.user)
        percentage = round(net_value * 100)
        users = User.objects.filter(groups__name='Kids')
        if percentage > 100:
            percentage = 100
    return render(request, 'home.html', context={'todos': todo, "percentage": percentage, 'users': users})

@staff_member_required(login_url='index')
def admin_view(request):
    todo = Todo.objects.filter(user=request.user)
    net_value = sum_total_values(request.user)
    percentage = round(net_value * 100)
    users = User.objects.filter(groups__name='Kids')
    if percentage > 100:
        percentage = 100
    return render(request, 'admin_homepage.html', context={'todos': todo, "percentage": percentage, 'users': users})

@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'home.html', context={'user': args})

@staff_member_required(login_url='index')
def todo_create_view(request):
    users = User.objects.filter(groups__name='Kids')
    form = TodoForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect('todo_detail', pk=post.pk)
    else:
        form = TodoForm()

    return render(request, 'create_todo.html', context={'form': form, 'users': users})

@login_required
def detail_view(UpdateView):
    model = Todo
    fields = ["user", 'title', 'description', 'value']

def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todo_detail.html', {'todo': todo})

@staff_member_required(login_url='index')
def user_todos(request, pk):
    todo = Todo.objects.filter(user=pk)
    net_value = sum_total_values(user=pk)
    percentage = round(net_value * 100)
    return render(request, 'user_todos.html', {'todo': todo, 'percentage': percentage})

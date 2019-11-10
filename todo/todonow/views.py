from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Todo, UserProfile
from django.contrib.auth.models import User
import math
from .forms import TodoForm, ImageUploadForm
from django.views.generic import UpdateView, ListView
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.conf import settings
import requests


@receiver(post_init, sender= UserProfile)
def backup_image_path(sender, instance, **kwargs):
    instance._current_imagen_file = instance.image


@receiver(post_save, sender= UserProfile)
def delete_old_image(sender, instance, **kwargs):
    if hasattr(instance, '_current_imagen_file'):
        if instance._current_imagen_file != instance.image:
            instance._current_imagen_file.delete(save=False)

def sum_total_values(user):
    completed_values = Todo.objects.filter(
        user=user
    ).filter(completed=True).count()
    total_values = Todo.objects.filter(
        user=user
    )
    no_values = 0
    if completed_values:
        divided_values = completed_values / total_values.count()
        return divided_values
    else:
        return no_values

def pushover_handler(user, todo):
    myMessage= user +' has completed the task ' + todo
    url = "https://api.pushover.net/1/messages.json"
    querystring = {"token":settings.PUSH_OVER_APP_TOKEN,"user":settings.PUSH_OVER_USER_TOKEN,"message":myMessage}
    response = requests.request("POST", url, params=querystring)

@login_required
def index(request):
    if request.user.is_superuser:
        return redirect("/admin_homepage/")
    else:
        todo = Todo.objects.filter(user=request.user)
        net_value = sum_total_values(request.user)
        percentage = round(net_value * 100)
        if percentage > 100:
            percentage = 100
    return render(request, 'app/home.html', context={'todos': todo, "percentage": percentage})

@staff_member_required(login_url='index')
def admin_view(request):
    todo = Todo.objects.filter(user=request.user)
    net_value = sum_total_values(request.user)
    percentage = round(net_value * 100)
    users = User.objects.filter(groups__name='Kids')
    if percentage > 100:
        percentage = 100
    return render(request, 'app/admin_homepage.html', context={'todos': todo, "percentage": percentage, 'users': users})

@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'app/home.html', context={'user': args})

@staff_member_required(login_url='index')
def todo_create_view(request):
    users = User.objects.filter(groups__name='Kids')
    form = TodoForm(request.POST)
    if form.is_valid():
        post = form.cleaned_data
        post = form.save(commit=False)
        post.save()
        messages.info(request, "Todo added successfully")
        return redirect('user_todos', pk=post.user.id)
    else:
        form = TodoForm()

    return render(request, 'app/create_todo.html', context={'form': form, 'users': users})

class update_todo_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'app/todo_form.html'
    model = Todo
    fields = ["user", 'title', 'description', 'value']

    def form_isvalid(self, form):
        form.instance.pk = self.request.user
        return super().form_isvalid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.is_staff:
            return True
        return False

def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.user:
        return render(request, 'app/todo_detail.html', {'todo': todo})
    else: raise Http404("Entry not found")

@staff_member_required(login_url='index')
def user_todos(request, pk):
    form = TodoForm(request.POST)
    todo = Todo.objects.filter(user=pk)
    net_value = sum_total_values(user=pk)
    percentage = round(net_value * 100)
    user = User.objects.get(pk=pk)
    if form.is_valid():
        post = form.cleaned_data
        post = form.save(commit=False)
        post.save()
        messages.info(request, "Todo added successfully")
        return redirect('user_todos', pk=post.user.id)
    else:
        form = TodoForm()
    return render(request, 'app/user_todos.html', {'form': form, 'user': user, 'todos': todo, 'percentage': percentage})

@login_required
def profile_page(request):
    form_class = ImageUploadForm
    form = form_class(request.POST or None)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture uploaded successfully')
            return redirect('index')
    return render(request, 'app/profile.html', context={'form': form})

def delete_todo(request, pk):
    instance = get_object_or_404(Todo, pk=pk)
    next = request.POST.get('next', '/')
    instance.delete()
    messages.info(request, "Todo deleted successfully")
    return redirect('user_todos', pk=instance.user.id)

def update_completed_status(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    user = request.user
    if request.method == 'POST':
        todo.completed = not todo.completed
        if todo.completed == True and user.groups.filter(name = "Kids").exists():
            pushover_handler(user.first_name, todo.title)
        next = request.POST.get('next', '/')
        todo.save()
        return redirect(next)

def approve_completed(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    user = request.user
    if request.method == 'POST':
        todo.confirm_complete = not todo.confirm_complete
        if todo.completed == True and user.groups.filter(name = "Kids").exists():
            pushover_handler(user.first_name, todo.title)
        next = request.POST.get('next', '/')
        todo.save()
        return redirect(next)

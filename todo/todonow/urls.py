from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create/', views.todo_create_view, name="create"),
    path('<int:pk>/', views.UpdateView.as_view(), name="update"),
    path('list/', views.ListView.as_view(), name="List"),
    path('details/<int:pk>/', views.todo_detail, name='todo_detail'),
    path('usertodos/<int:pk>/', views.user_todos, name='user_todos'),
    path('admin_homepage/', views.admin_view, name='admin_homepage'),
    path('profile/', views.profile_page, name='profile'),
    path('delete/<int:pk>/', views.delete_todo, name='delete')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
